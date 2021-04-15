#pragma once

#include "typedefs.hh"
#include "Node.hh"
#include "NodeSet.hh"
class NFILP;

class Layer {
// Members
private:
	NFILP& ilp;
	Vec feasable;
	Integer lambda;

	int path_len;
	NodeSet nodes;
	Integer u_star;
	Integer l_star;


// Constructor
public:
	Layer();
	Layer(NFILP& ilp, Vec feasable, Integer lambda);


// Methods 
private:
	void update_star();
public:
	Node get_max_node();
	bool is_empty();
	NodeSet get_chlidren(Node node, Vec skiped_vec, Integer skiped_costs);
	void increment();
};
