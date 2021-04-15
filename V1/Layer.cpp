#include "Layer.hh"

#include "NFILP.hh"

Layer::Layer(NFILP& ilp, Vec feasable, Integer lambda) : ilp(ilp), feasable(feasable), lambda(lambda), path_len(0) {
	// initialize layer 0
	nodes.update_node(Vec::Zero(ilp.A_height + ilp.B_height), Vec::Zero(0), 0);
}


// calculate current special lower and upper bounds
void Layer::update_star() {
	Integer ceiled = ceil((ilp.u(path_len) - feasable(path_len)) / lambda);
	if(  ilp.graver_bound  < 2147483647 && ilp.graver_bound > 0 
	  && ceiled > ilp.graver_bound ){
		std::cerr << "FATAL: interfering augumenting ilp bounds and graver element bounds" << std::endl;
	}
	// no exact calculation because of usual overflow on graver_bound
	// actual code would be:
	// u_star = std::min(ceiled, ilp.graver_bound);
	u_star = ceiled;

	Integer floored = floor((ilp.l(path_len) - feasable(path_len)) / lambda);
	if(  ilp.graver_bound <  2147483647 && ilp.graver_bound > 0 
	  && floored          > ilp.graver_bound ){
		std::cerr << "FATAL: interfering augumenting ilp bounds and graver element bounds" << std::endl;
	}
	// no exact calculation because of usual overflow on graver_bound
	// actual code would be:
	// l_star = std::max(floored -ilp.graver_bound);
	l_star = floored;

	
}


Node Layer::get_max_node() {
	Node max_node;
	bool node_init(false);
	for (Node node : nodes) {
		if (node_init) {
			if (max_node.costs < node.costs) {
				max_node = node;
			}
		}
		else {
			max_node = node;
			node_init = true;
		}
	}

	return max_node;
}


bool Layer::is_empty() {
	return (nodes.size() == 0);
}


NodeSet Layer::get_chlidren(Node parent) {
	NodeSet child_set;
	Vec c_value;
	Vec c_path(path_len + 1);
	Integer c_costs;


	for (Integer y = l_star; y <= u_star; y++) {
		c_value = parent.value + (ilp.ABs[path_len] * y);
		c_path << parent.path, y;
		c_costs = parent.costs + (y * ilp.c(path_len));

		// improvement on memory usage? Tradeof (time vs. memory)?
		if (c_path.lpNorm<1>() <= ilp.graver_bound || ilp.graver_bound < 0) { // graver_bound < 0 => overflow
			// Last change
			if ((path_len+1) == ilp.total_width){
				// child needs to be zero
				if (c_value.isZero(ilp.B_height+ ilp.A_height)) {
					child_set.update_node(c_value, c_path, c_costs);
				}
			// Block change (mind the case wher t = 1)
			} else if ((path_len+1) % ilp.A_width == 0) {
				// the lower part of the child needs to be zero
				if (c_value.tail(ilp.B_height).isZero(ilp.B_height)) {
					child_set.update_node(c_value, c_path, c_costs);
				}
			}
			// Inside Block
			else {
				child_set.update_node(c_value, c_path, c_costs);
			}
		}
	}

	return child_set;
}


void Layer::increment() {
	NodeSet new_nodes;
	NodeSet children;

	update_star();

	for (const Node& node : this->nodes) {
		children = get_chlidren(node);
		new_nodes.update(children);

	}

	nodes = new_nodes;

	path_len++;
}
