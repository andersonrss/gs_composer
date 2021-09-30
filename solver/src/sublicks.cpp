
#include <ilcplex/ilocplex.h>
#include <cstdio>
#include <iostream>
#include <vector>
#include <string.h>
#include <stdlib.h>
#include <string>

#include "util.h"
#include "sublicks.h"

using namespace std;


// Implements the mathematical model
int sublicks(int n_bend, double r_bend, 
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
			 string sl_type)
{


// PREPROCESSING
	
	srand(time(NULL));
	
	char arr[100];
	string lp_path = sl_type + "_licks/sublicks.lp";

	// All variables of the problem
	vector <int> variables;

	// Vectors that store specific sublick types
	vector <int> var_bend, 
				 var_bn, 
				 var_slide, 
				 var_tri, 
				 var_tri_bend, 
				 var_tri_bn, 
				 var_tri_rest, 
				 var_note, 
				 var_rest, 
				 var_dStop;
	
	// Vectors for duration/#notes mapping
	vector <int> qNotes;
	vector <double> tSubls;

	var_bend = random_indexes(variables, sl_type + "_licks/indexes/BEND", r_bend);
	
	var_bn = random_indexes(variables, 
	sl_type + "_licks/indexes/BLUE_NOTE", r_bn);
	
	var_slide = random_indexes(variables, 
	sl_type + "_licks/indexes/SLIDE", r_slide);

	var_tri = random_indexes(variables, 
	sl_type + "_licks/indexes/TRIPLET", r_tri);

	var_tri_bend = random_indexes(variables, 
	sl_type + "_licks/indexes/TRIPLET_BEND", r_tri_bend);

	var_tri_bn = random_indexes(variables, 
	sl_type + "_licks/indexes/TRIPLET_BLUE_NOTE", r_tri_bn);

	var_tri_rest = static_indexes(variables, sl_type + "_licks/indexes/TRIPLET_REST");
	
	var_note = random_indexes(variables, 
	sl_type + "_licks/indexes/NORMAL_NOTE", r_note);

	var_rest = static_indexes(variables, sl_type + "_licks/indexes/REST");
	
	var_dStop = static_indexes(variables, sl_type + "_licks/indexes/DOUBLE_STOP");

	qtity_notes_mapping(qNotes, sl_type + "_licks/files/nNotes_sublicks");
	duration_sublicks_mapping(tSubls, sl_type + "_licks/files/tSub");

	// Cost matrix declaration
	double **costMatrix = new double *[nSubs];
	
	for (int i = 0 ; i < nSubs ; i++)
		costMatrix[i] = new double[nSubs];

	costMatrix = cost_matrix(nSubs, sl_type + "_licks/files/matrix");
	

// MATHEMATICAL MODEL


	typedef IloArray <IloNumVarArray> NumVarMatrix;
	
	int i, j, k;
	IloEnv env;
	IloModel model(env);
	char varName[100];
	char cName[100];
	
	// 'x' variables
	NumVarMatrix x(env, nSubs);
	for (i = 0 ; i < nSubs ; i++){
		x[i] = IloNumVarArray(env, nSubs);
		for (j = 0 ; j < nSubs ; j++){
			x[i][j] = IloNumVar(env, 0.0, 1.0, ILOINT);
		} 
	}
	
	// Adding 'x' to the model
	for (i = 0 ; i < nSubs ; i++){
		if (check_variable(variables, i) == 1){
			for (j = 0 ; j < nSubs ; j++){
				if (i == j)
					continue;
				if (check_variable(variables, j) == 1){
					sprintf(varName, "x_%d_%d", i, j);
					x[i][j].setName(varName);
					model.add(x[i][j]);
				}
			}
		}
	}

	// 'y' variables
	IloBoolVarArray y(env, nSubs);
	
	// Adding 'y' to the model
	for (i = 0 ; i < nSubs ; i++){
		if (check_variable(variables, i) == 1){
			sprintf(varName, "y_%d", i);
			y[i].setName(varName);
			model.add(y[i]);
		}
	}

	// Objective function
	IloExpr fo(env);
	for (i = 0 ; i < nSubs ; i++){
		if (check_variable(variables, i) == 1){
			for (j = 0 ; j < nSubs ; j++){
				if (i == j)
					continue;
				if (check_variable(variables, j) == 1){
					fo += costMatrix[i][j] * x[i][j];
				}
			}
		}
	}
	model.add(IloMinimize(env, fo));

	// Constraint: exactly one arc must leave the sublick that has been selected 
	for (i = 0 ; i < nSubs ; i++){
		if (check_variable(variables, i) == 1){
			IloExpr inFlow(env);
			for (j = 0 ; j < nSubs ; j++){
				if (i == j)
					continue;
				if (check_variable(variables, j) == 1){	
					inFlow += x[i][j];
				}
			}
			IloConstraint const_in = (inFlow == y[i]);
			sprintf(cName, "in_%d", i);
			const_in.setName(cName);
			model.add(const_in);
		}
	}
	
	// Constraint: exactly one arc must arrive at the sublick that has been selected
	for (j = 0 ; j < nSubs ; j++){
		if (check_variable(variables, j) == 1){	
			IloExpr outFlow(env);
			for (i = 0 ; i < nSubs ; i++){
				if (j == i)
					continue;
				if (check_variable(variables, i) == 1){
					outFlow += x[i][j];
				}
			}
			IloConstraint const_out = (outFlow == y[j]);
			sprintf(cName, "out_%d", j);
			const_out.setName(cName);
			model.add(const_out);
		}
	}	
	
	// Constraint: imposes that the total duration of the lick must be equal to 'ts'
	IloExpr times(env);
	int ts;
	if (sl_type == "default")
		ts = 64;
	if (sl_type == "repetition")
		ts = 16;
	if (sl_type == "turnaround")
		ts = 32;

	for (i = 0 ; i < nSubs ; i++){
		if (check_variable(variables, i) == 1){
			times += tSubls[i] * y[i];
		}
	}
	IloConstraint const_time = (times == ts);
	const_time.setName("c_time");
	model.add(const_time);
	
	// Constraint: guarantees that the final lick has exactly 'n_bend' bend techniques
	IloExpr bend(env);
	for (i = 0 ; i < var_bend.size() ; i++){
		if (check_variable(variables, var_bend[i]) == 1){
			bend += y[var_bend[i]];
		}
	}
	IloConstraint const_bend = (bend == n_bend);
	const_bend.setName("c_bend");
	model.add(const_bend);

	// Constraint: guarantees that the final lick has exactly 'n_bn' blue notes
	IloExpr blueNote(env);
	for (i = 0 ; i < var_bn.size() ; i++){
		if (check_variable(variables, var_bn[i]) == 1){
			blueNote += y[var_bn[i]];
		}
	}
	IloConstraint const_blueNote = (blueNote == n_bn);
	const_blueNote.setName("c_blueNote");
	model.add(const_blueNote);

	// Constraint: guarantees that the final lick has exactly 'n_slide' slide techniques
	IloExpr slide(env);
	for (i = 0 ; i < var_slide.size() ; i++){
		if (check_variable(variables, var_slide[i]) == 1){
			slide += y[var_slide[i]];
		}
	}
	IloConstraint const_slide = (slide == n_slide);
	const_slide.setName("c_slide");
	model.add(const_slide);
	
	// Constraint: guarantees that the final lick has exactly 'n_tri' triplet notes
	IloExpr triplet(env);
	for (i = 0 ; i < var_tri.size() ; i++){
		if (check_variable(variables, var_tri[i]) == 1){
			triplet += y[var_tri[i]];
		}
	}
	IloConstraint const_triplet = (triplet == n_tri);
	const_triplet.setName("c_triplet");
	model.add(const_triplet);

	// Constraint: guarantees that the final lick has exactly 'n_tri_bend' triplet notes with bend technique
	IloExpr triplet_bend(env);
	for (i = 0 ; i < var_tri_bend.size() ; i++){
		if (check_variable(variables, var_tri_bend[i]) == 1){
			triplet_bend += y[var_tri_bend[i]];
		}
	}
	IloConstraint const_triplet_bend = (triplet_bend == n_tri_bend);
	const_triplet_bend.setName("c_triplet_bend");
	model.add(const_triplet_bend);

	// Constraint: guarantees that the final lick has exactly 'n_tri_bn' triplet blue notes
	IloExpr triplet_blueNote(env);
	for (i = 0 ; i < var_tri_bn.size() ; i++){
		if (check_variable(variables, var_tri_bn[i]) == 1){
			triplet_blueNote += y[var_tri_bn[i]];
		}
	}
	IloConstraint const_triplet_blueNote = (triplet_blueNote == n_tri_bn);
	const_triplet_blueNote.setName("c_triplet_blueNote");
	model.add(const_triplet_blueNote);
	
	// Constraint: guarantees that the final lick has exactly 'n_tri_rest' triplet rests
	IloExpr triplet_rest(env);
	for (i = 0 ; i < var_tri_rest.size() ; i++){
		if (check_variable(variables, var_tri_rest[i]) == 1){
			triplet_rest += y[var_tri_rest[i]];
		}
	}
	IloConstraint const_triplet_rest = (triplet_rest == n_tri_rest);
	const_triplet_rest.setName("c_triplet_rest");
	model.add(const_triplet_rest);


	// Constraint: guarantees that the final lick has exactly 'n_rest' rests
	IloExpr rests(env);
	for (i = 0 ; i < var_rest.size() ; i++){
		if (check_variable(variables, var_rest[i]) == 1){
			rests += y[var_rest[i]];
		}
	}
	IloConstraint const_rest = (rests == n_rest);
	const_rest.setName("c_rest");
	model.add(const_rest);
	
	// Constraint: guarantees that the final lick has exactly 'n_dStop' double stops
	IloExpr doubleStops(env);
	for (i = 0 ; i < var_dStop.size() ; i++){
		if (check_variable(variables, var_dStop[i]) == 1){
			doubleStops += y[var_dStop[i]];
		}
	}
	IloConstraint const_doubleStop = (doubleStops == n_dStop);
	const_doubleStop.setName("c_doubleStop");
	model.add(const_doubleStop);

	// Constraint: guaranteest that the final lick has at most 'n_note' notes
	IloExpr notes(env);	
	for (i = 0 ; i < nSubs ; i++){
		if (check_variable(variables, i) == 1){
			notes += qNotes[i] * y[i];
		}
	}
	IloConstraint const_notes = (notes <= n_note);
	const_notes.setName("c_note");
	model.add(const_notes);
	
	// Last constraints: subtour elimination constraints 
	for (i = 0 ; i < nSubs ; i++){
		if (check_variable(variables, i) == 1){
			for (j = 0 ; j < nSubs ; j++){
				if (check_variable(variables, j) == 1){	
					if (i < j){
						IloConstraint const_sub = (x[i][j] + x[j][i] <= 1);
						sprintf(cName, "self_%d_%d", i, j);
						const_sub.setName(cName);
						model.add(const_sub);
					}
				}
			}
		}
	}
	
	IloArray <IloBoolVarArray> z(env, nSubs);
    for (i = 0 ; i < nSubs ; i++){
    	IloBoolVarArray array(env, nSubs);
    	z[i] = array;
    }
    
	for (i = 0 ; i < nSubs ; i++){
		if (check_variable(variables, i) == 1){
			for (j = 0 ; j < nSubs ; j++){
		    	if (check_variable(variables, j) == 1){
					if (i < j){
				    	sprintf(varName, "Z(%d,%d)", i, j);
				    	z[i][j].setName(varName);
				    	model.add(z[i][j]);
				    }
				}
		    }
		}
    }
    
    for (i = 0 ; i < nSubs ; i++){
		if (check_variable(variables, i) == 1){
			for (j = 0 ; j < nSubs ; j++){
		    	if (check_variable(variables, j) == 1){
					if (i < j){
				    	IloConstraint constr = (x[i][j] + x[j][i] - z[i][j] == 0);
				    	sprintf(cName,"c7_%d_%d", i, j);
				    	constr.setName(cName);
				    	model.add(constr);
				  	}
				}
			}
		}
    }
	
	IloCplex cplex(env);
    //cplex.setOut(env.getNullStream());
    cplex.extract(model);
    strcpy(arr, lp_path.c_str());
    cplex.exportModel(arr);

    return 0;
}



