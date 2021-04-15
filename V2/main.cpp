#include <iostream>

#include "typedefs.hh"

#include "NFILP.hh"
#include "Layer.hh"

// #define MY_DEBUG
#ifdef MY_DEBUG
#define LOG(y,x) std::cout <<  y << std::endl; std::cout << x << std::endl << std::endl
#include "my_utils.hh" 
#else
#define LOG(y,x)
#endif

int main(int argc, char** argv) {

	NFILP ilp(argv[1]);

	// ilp.log(); // Debug

	NFILP t_ilp = ilp.transformed();
	Vec   t_feasable = ilp.trans_feasable();

	// t_ilp.log();                        				  // Debug

	LOG( "t_feasable" , t_feasable);                      // Debug
	LOG("t*feas", t_ilp.get_hole_matrix() * t_feasable);  // Debug

	t_ilp.maximize_solution(t_feasable);
	Vec t_optimal = t_feasable;

	LOG("t_optimal", t_feasable);    					 // Debug
	LOG("t_obj", t_feasable.dot(t_ilp.c));               // Debug
	LOG("t*opt", t_ilp.get_hole_matrix() * t_feasable);  // Debug

	if (t_ilp.c.dot(t_optimal) == 0) {
		Vec feasable = ilp.transform_back(t_optimal);

		LOG( "feasable" , feasable);                        // Debug
		LOG("ilp*feas", ilp.get_hole_matrix() * feasable);  // Debug

		ilp.maximize_solution(feasable);
		Vec solution = feasable;
		
		LOG("optimal", solution);    					   // Debug
		LOG("obj", solution.dot(ilp.c));      			   // Debug
		LOG("ilp*opt", ilp.get_hole_matrix() * feasable);  // Debug

		std::cout << "solution:\n"  << solution << std::endl;
		std::cout << "maximum: " << ilp.c.dot(solution) << std::endl;
	}
	else {
		std::cout << "No solution" << std::endl;
	}
	return 0;
}


