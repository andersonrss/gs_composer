#ifndef UTIL_H
#define UTIL_H

#include <string>

using namespace std;


extern double** cost_matrix(int nFiles, string data);

extern int check_variable(vector <int> variables, int id);

extern vector <int> static_indexes(vector <int> &variables, string indexes_file);

extern vector <int> random_indexes(vector <int> &variables, string indexes_file, double rate);


#endif
