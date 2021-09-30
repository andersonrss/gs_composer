
#ifndef SUBLICKS_H
#define SUBLICKS_H

#include <string>

using namespace std;


extern int sublicks(int n_bend, double r_bend, 
			 int n_bn, double r_bn, 
			 int n_slide, double r_slide, 
			 int n_tri, double r_tri, 
			 int n_tri_bend, double r_tri_bend, 
			 int n_tri_bn, double r_tri_bn, 
			 int n_tri_rest, 
			 int n_rest, 
			 int n_dStop, 
			 int n_note, double r_note, 
			 int nSubs, 
			 string sl_type);


#endif

