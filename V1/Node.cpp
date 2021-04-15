#include "Node.hh"

Node::Node() : value(0), path(0), costs(0) {}

Node::Node(NodePair np) {
	value = np.first;
	path = np.second.first;
	costs = np.second.second;

}

NodePair Node::get_node_pair() {
		const Vec  const_val = value;
		return {const_val, {path, costs}};
	}
