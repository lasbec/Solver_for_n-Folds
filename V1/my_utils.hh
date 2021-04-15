#include "typedefs.hh"
#include "NFILP.hh"
#include "NodeSet.hh"

// for debugging purpose
std::string putVec(Vec v){
    std::string ret = "";
    for(int i=0; i<v.size(); i++){
        ret = ret + std::to_string(v(i)) + " ";
    }
    return ret;
}

std::vector<Integer> vecVec(Vec v){
    std::vector<Integer> ret(v.size());
    for(int i=0; i<v.size(); i++){
        ret[i] = v(i);
    }
    return ret;
}


Vec mulVec(Mat m, Vec v){
    return m*v;
}

std::string putMulVec(NFILP* ilp, Vec v){
    return putVec((ilp->get_hole_matrix())*v);
}

std::vector<Integer> vecMulVec(NFILP* ilp, Vec v){
    return vecVec((ilp->get_hole_matrix())*v);
}

std::vector<Vec> getKeys(NodeSet s){
    std::vector<Vec> ret(s.size());
    int i =0;
    for (Node node : s) {
        ret[i] = node.value;
        i++;
    }
    return ret;
}

std::vector<Vec> getKeys(NodeSet s, int m){
    int si = s.size();
    int t = std::min(si,m);
    std::vector<Vec> ret(t);
    int i =0;
    for (Node node : s) {
        ret[i] = node.value;
        if( i >= m) break;
        i++;
    }
    return ret;
}

std::vector<std::pair<Vec, Integer>> getVals(NodeSet s){
    int si = s.size();
    std::vector<std::pair<Vec, Integer>> ret(si);
    int i =0;
    for (Node node : s) {
        ret[i] = std::pair<Vec, Integer>(node.path, node.costs);
        i++;
    }
    return ret;
}

std::vector<std::pair<Vec, Integer>> getVals(NodeSet s, int m){
    int si = s.size();
    int t = std::min(si,m);
    std::vector<std::pair<Vec, Integer>> ret(t);
    int i =0;
    for (Node node : s) {
        ret[i] = std::pair<Vec, Integer>(node.path, node.costs);
        if( i >= m) break;
        i++;
    }
    return ret;
}



Vec myVec(0);
Vec myVec0(1);
Vec myVec00(2);
Vec myVec000(3);
Vec myVec0001(4);
Vec myVec00010(5);
Vec myVec000100(6);
Vec myVec0001000(7);
Vec myVec00010000(8);
Vec myVec000100000(9);
Vec myVec000100000m1(10);
Vec myVec000100000m1m1(11);
Vec myVec000100000m1m1m1(12);
Vec myVec000100000m1m1m12(13);
Vec myVec000100000m1m1m120(14);
Vec myVec000100000m1m1m1200(15);
Vec myVec000100000m1m1m12000(16);
Vec myVec000100000m1m1m120000(17);
Vec myVec000100000m1m1m1200000(18);

Vec myVec00000(5);
Vec myVec11111(5);
Vec myVec_1_1_1_1_1(5);
Vec myVec_2_2_2_2_2(5);
void init_myVecs(){
    myVec00000 << 0, 0, 0, 0, 0;
    myVec11111 << 1, 1, 1, 1, 1;
    myVec_1_1_1_1_1 << -1, -1, -1, -1, -1;
    myVec_2_2_2_2_2 << -2, -2, -2, -2, -2;

    myVec0 << 0;
    myVec00 << 0, 0;
    myVec000 << 0, 0, 0;
    myVec0001 << 0, 0, 0, 1;
    myVec00010 << 0, 0, 0, 1, 0;
    myVec000100 << 0, 0, 0, 1, 0, 0;
    myVec0001000 << 0, 0, 0, 1, 0, 0, 0;
    myVec00010000 << 0, 0, 0, 1, 0, 0, 0, 0;
    myVec000100000 << 0, 0, 0, 1, 0, 0, 0, 0, 0;
    myVec000100000m1 << 0, 0, 0, 1, 0, 0, 0, 0, 0, -1;
    myVec000100000m1m1 << 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, -1;
    myVec000100000m1m1m1 << 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, -1, -1;
    myVec000100000m1m1m12 << 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, -1, -1, 2;
    myVec000100000m1m1m120 << 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, -1, -1, 2, 0;
    myVec000100000m1m1m1200 << 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, -1, -1, 2, 0, 0;
    myVec000100000m1m1m12000 << 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, -1, -1, 2, 0, 0, 0;
    myVec000100000m1m1m120000 << 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, -1, -1, 2, 0, 0, 0, 0;
    myVec000100000m1m1m1200000 << 0, 0, 0, 1, 0, 0, 0, 0, 0, -1, -1, -1, 2, 0, 0, 0, 0, 0;
}

// Vec getKeysByVal(NodeSet s, Vec v, int index){
//     int i = 0;
//     for (Node node : s){
//         if (index < i) break;
//         if (node.path == v){
//             return node.value;
//         }
//         i++;
//     }
//     return myVec;
// }

Vec getKey(NodeSet s, int i){
    return getKeys(s)[i];
}

std::pair<Vec,Integer> getVal(NodeSet s, int i){
    return getVals(s)[i];
}

std::string putKey(NodeSet s, int i){
    return putVec(getKeys(s)[i]);
}

std::string putValV(NodeSet s, Vec v){
    return putVec(s.getPathTo(v));
}


std::string putVal(NodeSet s, int i){
    return putVec(getVals(s)[i].first);
}
