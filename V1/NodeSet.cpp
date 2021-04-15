#include "NodeSet.hh"


void NodeSet::update_node(const Vec value, Vec path, Integer costs) {
	if (has_key(value)) {
		if ((*this)[value].second < costs){
			(*this)[value] = { path, costs };
		}
	}
	else {
		(*this)[value] = { path, costs };
	}
}

void NodeSet::update_node(Node node) {
	if (has_node(node)) {
		if ((*this)[node.value].second < node.costs){
			(*this)[node.value] = {node.path, node.costs };
		}
	}
	else {
		this->insert(node.get_node_pair());
	}
}

bool NodeSet::has_node(Node node) {
	return this->find(node.value) != this->end();
}

bool NodeSet::has_key(Vec v) {
	return this->find(v) != this->end();
}

void NodeSet::update(NodeSet set) {
	for (Node node : set) {
		update_node(node);
	}
}

Vec NodeSet::getPathTo(Vec v){
	const Vec cv = v;
	return (*this)[cv].first;
}

