#pragma once

#include "typedefs.hh"

typedef  std::pair<const Vec, std::pair<Vec, Integer> > NodePair;

class Node {

public:
	Vec value;
	Vec path;
	Integer costs;

public:
	Node();

	Node(NodePair np);

	NodePair get_node_pair();
};
