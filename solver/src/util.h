#ifndef UTIL_H
#define UTIL_H

#include <string>

using namespace std;


extern vector <int> static_indexes(vector <int> &variables, string indexes_file);

extern void qtity_notes_mapping(vector <int> &values, string data);

extern void duration_sublicks_mapping(vector <double> &values, string data);

extern double** cost_matrix(int nFiles, string data);

extern int check_variable(vector <int> variables, int id);

extern vector <int> random_indexes(vector <int> &variables, string indexes_file, double rate);


#endif
