#pragma once
#include <iostream>
#include <fstream>


#include "typedefs.hh"
#include "Layer.hh"


class NFILP {
// Members
public:
	int n, r, s, t;
	int block_num, A_height, B_height, A_width, B_width; // aliasing
	Vec l, u, b, c;
	MatArr As, Bs;
	VecArr ABs;
	int total_height, total_width;
	Integer delta, graver_bound;

//	Constructors 
public:
	NFILP(const std::string& path);

	NFILP(int n, int r, int s, int t,
		Vec l, Vec u, Vec b, Vec c,
		MatArr& As, MatArr& Bs);
private:
	//	No default Konstruktor
	NFILP() = delete;

// Methods
private:
	Vec read_vector(int height);

	Mat read_matrix(int height, int width);

	int trans_block_num();
	
	int trans_total_width();

	int trans_A_width();

	int trans_B_width();

	int trans_B_height();

	int trans_A_height();

	MatArr trans_As();

	MatArr trans_Bs();

	Vec trans_b();

	Vec trans_pattern(Vec& on_original, Vec& on_zero, Vec& on_identity_then, Vec& on_identity_else);

	Vec trans_l();

	Vec trans_u();

	Vec trans_c();

public:
	NFILP transformed();

	Vec trans_feasable();

	Vec transform_back(Vec sol);

	void maximize_solution(Vec& feasable);

	Vec solve_aug(Vec feasable, Integer lambda);

	void log();

	Mat get_hole_matrix();
};
