#include <iostream>
#include <fstream>


#include "typedefs.hh"
#include "Layer.hh"

#include "NFILP.hh"


NFILP::NFILP(const std::string& path) {
	//	Redirecting standart Input
	std::ifstream in(path);
	std::streambuf* cinbuf = std::cin.rdbuf(); //save old buf
	std::cin.rdbuf(in.rdbuf()); //redirect std::cin to in.txt!

	std::cin >> n;
	block_num = n;

	std::cin >> r;
	A_height = r;

	std::cin >> s;
	B_height = s;

	std::cin >> t;
	A_width = t;
	B_width = t;

	total_height = n * s + r;
	total_width = n * t;

	l = read_vector(total_width);
	u = read_vector(total_width);
	b = read_vector(total_height);
	c = read_vector(total_width);

	As = MatArr(n);
	for (int i = 0; i < n; i++) {
		As[i] = read_matrix(r, t);
	}


	Bs = MatArr(n);
	for (int i = 0; i < n; i++) {
		Bs[i] = read_matrix(s, t);
	}

	ABs = VecArr(total_width);
	Vec AB_col(r + s);
	for (int block=0; block <n; block++){
		for (int i=0; i<B_width; i++){
			AB_col << As[block].col(i), Bs[block].col(i);
			ABs[block * B_width + i] = AB_col;
		}
	}

	delta = get_hole_matrix().lpNorm<Eigen::Infinity>();

	Integer lb = pow((2 * s * delta) + 1, s);
	graver_bound = lb * pow(2 * r * delta * lb + 1, r);
	if(graver_bound < 2147483647 && graver_bound > 0){
		std::cerr << "WARING: small bound on graver basis elements" << std::endl;
	}
	if(graver_bound < 0){
		std::cerr << "INFO: Overflow on bound on graver basis elements" << std::endl;
	}
}


NFILP::NFILP(int n, int r, int s, int t,
	Vec l, Vec u, Vec b, Vec c,
	MatArr& As, MatArr& Bs) :
	n(n), r(r), s(s), t(t),
	block_num(n), A_height(r), B_height(s), A_width(t), B_width(t), // aliasing
	l(l), u(u), b(b), c(c),
	As(As), Bs(Bs),
	total_height(r + n * s), total_width(n* t) {

	ABs = VecArr(total_width);
	Vec AB_col(r + s);
	for (int block=0; block <n; block++){
		for (int i=0; i<B_width; i++){
			AB_col << As[block].col(i), Bs[block].col(i);
			ABs[block * B_width + i] = AB_col;
		}
	}

	delta = get_hole_matrix().lpNorm<Eigen::Infinity>();

	Integer lb = pow((2 * s * delta) + 1, s);
	graver_bound = lb * pow(2 * r * delta * lb + 1, r);
	if(graver_bound < 2147483647 && graver_bound > 0){
		std::cerr << "WARING: small bound on graver basis elements" << std::endl;
	}
	if(graver_bound < 0){
		std::cerr << "INFO: Overflow on bound on graver basis elements" << std::endl;
	}
}


Vec NFILP::read_vector(int height) {
	Vec vector(height);
	for (int i = 0; i < height; i++)
		std::cin >> vector(i);
	return vector;
};

Mat NFILP::read_matrix(int height, int width) {
	Mat matrix(height, width);
	for (int y = 0; y < height; y++) {
		for (int x = 0; x < width; x++)
		{
			std::cin >> matrix(y, x);
		}
	}
	return matrix;
};

int NFILP::trans_block_num() {
	return block_num;
}

int NFILP::trans_total_width() {
	return (block_num * trans_A_width());
}

int NFILP::trans_A_width() {
	return (A_width + A_height + B_height);
}

int NFILP::trans_B_width() {
	return (B_width + A_height + B_height);
}

int NFILP::trans_B_height() {
	return B_height;
}

int NFILP::trans_A_height() {
	return A_height;
}

MatArr NFILP::trans_As() {
	MatArr new_As(block_num);
	Mat block(A_height, trans_A_width());

	block << As[0], Mat::Identity(A_height, A_height), Mat::Zero(A_height, B_height);
	new_As[0] = block;

	for (int i = 1; i < block_num; i++) {
		block << As[i], Mat::Zero(A_height, A_height + B_height);
		new_As[i] = block;
	}

	return new_As;
}

MatArr NFILP::trans_Bs() {
	MatArr new_Bs(block_num);
	Mat block(B_height, trans_B_width());

	for (int i = 0; i < block_num; i++) {
		block << Bs[i], Mat::Zero(B_height, A_height), Mat::Identity(B_height, B_height);
		new_Bs[i] = block;
	}

	return new_Bs;
}


Vec NFILP::trans_b() {
	Vec new_b(total_height);
	new_b << (b - (get_hole_matrix() * l));
	return new_b;
}


// Length on_original  = this->total_width 
// Length on_Identity_than = this->total_height
// Length on_Identity_else = this->total_height
// Lenght on_zero = (block_num -1) * A_height
Vec NFILP::trans_pattern(Vec& on_original, Vec& on_zero, Vec& on_identity_then, Vec& on_identity_else) {
	Vec ret(trans_total_width());
	static Vec t_b = trans_b();

	//	on original index count
	int ooic = 0;
	//	on zero index count
	int ozic = 0;
	//	on Identity index count
	int oiic = 0;
	//	current handled index 
	int index;


	for (int n = 0; n < trans_block_num(); n++) {
		for (int i = 0; i < trans_A_width(); i++) {
			index = n * trans_A_width() + i;
			//	Column is not new
			if (i < A_width) {
				ret(index) = on_original(ooic);
				ooic++;
			}
			// Column is an artificial added zero column
			else if (n > 0 && i < A_width + A_height) {
				ret(index) = on_zero(ozic);
				ozic++;
			}
			// Column contains an artifical added Identitymarix row
			else {
				ret(index) = t_b(oiic) >= 0 ? on_identity_then(oiic) : on_identity_else(oiic);
				oiic++;
			}

		}
	}
	return ret;
}


Vec NFILP::trans_l() {
	Vec on_original = Vec::Zero(total_width);
	Vec on_zero = Vec::Zero((block_num -1) * A_height);
	Vec on_identity_then = Vec::Zero(total_height);
	Vec on_identity_else = trans_b();
	return trans_pattern(on_original, on_zero, on_identity_then, on_identity_else);
}


Vec NFILP::trans_u() {
	Vec on_original = u - l;
	Vec on_zero = Vec::Zero((block_num -1) * A_height);
	Vec on_identity_then = trans_b();
	Vec on_identity_else = Vec::Zero(total_height);
	return trans_pattern(on_original, on_zero, on_identity_then, on_identity_else);
}


Vec NFILP::trans_c() {
	Vec on_original = Vec::Zero(total_width);
	Vec on_zero = Vec::Zero((block_num -1) * A_height);
	Vec on_identity_then = Vec::Constant(total_height, -1);
	Vec on_identity_else = Vec::Constant(total_height, 1);
	return trans_pattern(on_original, on_zero, on_identity_then, on_identity_else);
}


NFILP NFILP::transformed() {
	int _block_num = trans_block_num();
	int _A_height = trans_A_height();
	int _B_height = trans_B_height();
	int _A_width = trans_A_width();
	Vec _lower = trans_l();
	Vec _upper = trans_u();
	Vec _right_hand = trans_b();
	Vec _cost_vec = trans_c();
	MatArr _As = trans_As();
	MatArr _Bs = trans_Bs();
	return NFILP(_block_num, _A_height, _B_height, _A_width,
			_lower, _upper, _right_hand, _cost_vec,
			_As, _Bs);
}


Vec NFILP::trans_feasable() {
	Vec on_original = Vec::Zero(this->total_width);
	Vec on_zero = Vec::Zero((block_num -1) * A_height);
	Vec on_identity_then = this->trans_b();
	Vec on_identity_else = this->trans_b();
	return trans_pattern(on_original, on_zero, on_identity_then, on_identity_else);
}


Vec NFILP::transform_back(Vec sol) {
	Vec back(this->total_width);
	int back_index;
	int sol_index;

	for (int n = 0; n < this->trans_block_num(); n++) {
		for (int i = 0; i < this->trans_A_width(); i++) {
			//			Column is not new
			if (i < this->A_width) {
				back_index = n * this->A_width + i;
				sol_index = n * this->trans_A_width() + i;
				back(back_index) = sol(sol_index);
			}
		}
	}
	// shift back
	return back + l;
}


// Lemma 5
void NFILP::maximize_solution(Vec& feasable) {
	Vec     canidate;
	Vec     best_canidate = feasable;
	Integer best_costs = c.dot(feasable);
	Integer canidate_costs;
	Integer lambda;

	Integer roh = (u - l).lpNorm<Eigen::Infinity>(); // roh = max_i (u(i) - l(i))
//	TODO m in die whileschleife bringen f�r lokale verbesserung?
	Integer m = roh == 1 ? // M = ceil(log_2(roh)) + 1
	        1 :
			sizeof(Integer) * __CHAR_BIT__ - __builtin_clzll(roh -1) +1;  


	bool improved = true;
	// improve feasable solution as long as possible
	while (improved) {
		improved = false;
		
		// bruteforce for the best lambda
		for (int k = 0; k <= m; k++) {
			lambda = pow(2, k);
			canidate = solve_aug(feasable, lambda);
			canidate_costs = c.dot(canidate);

			if (canidate_costs > best_costs) {
				best_costs = canidate_costs;
				best_canidate= canidate;
				improved = true; // improvement found
			}
		}
		feasable = best_canidate;
	}
}


// Lemma 4
Vec NFILP::solve_aug(Vec feasable, Integer lambda) {
	Vec ret = feasable;
	Layer layer( *this , ret, lambda);

	for (int i = 0; i < total_width; i++) {
		layer.increment();
	}
	if (layer.is_empty()) {
		return ret;
	}
	else {
		return ret + lambda * layer.get_max_node().path;
	}
}


void NFILP::log() {
	std::cout << get_hole_matrix() << std::endl;
	std::cout << "Lower:" << std::endl;
	std::cout << l << std::endl;
	std::cout << "Upper:" << std::endl;
	std::cout << u << std::endl;
	std::cout << "Costs:" << std::endl;
	std::cout << c << std::endl;
	std::cout << "Right hand:" << std::endl;
	std::cout << b << std::endl;
}


Mat NFILP::get_hole_matrix() {
	Mat hole(total_height, total_width);
	int block_h;
	int block_w;
	int inside_block_h;
	int inside_block_w;
	bool inside_A_block;
	bool inside_B_block;
	for (int w = 0; w < total_width; w++) {
		for (int h = 0; h < total_height; h++) {
			inside_A_block = h < A_height;
			inside_block_w = w % A_width;
			if (inside_A_block) {
				block_h = 0;
				inside_block_h = h;
			}
			else {
				block_h = 1 + ((h - A_height) / B_height);
				inside_block_h = (h - A_height) % B_height;
			}
			block_w = w / A_width;
			inside_B_block = block_w == (block_h - 1);
			if (inside_A_block) {
				hole(h, w) = As[block_w](inside_block_h, inside_block_w);
			}
			else {
				if (inside_B_block) {
					hole(h, w) = Bs[block_w](inside_block_h, inside_block_w);
				}
				else {
					hole(h, w) = 0;
				}
			}
		}
	}
	return hole;
}

