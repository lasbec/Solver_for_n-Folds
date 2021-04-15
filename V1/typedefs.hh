#pragma once

#include <vector>
#include <unordered_map>

#include "Eigen/Dense"


typedef long long int Integer;
typedef Eigen::Matrix<Integer, Eigen::Dynamic, 1             > Vec;
typedef Eigen::Matrix<Integer, Eigen::Dynamic, Eigen::Dynamic> Mat;
typedef Eigen::Matrix<Integer, 1, Eigen::Dynamic             > Row;
typedef Eigen::Matrix<Integer, Eigen::Dynamic, 1             > Col;
typedef std::vector<Mat> MatArr;
typedef std::vector<Vec> VecArr;

