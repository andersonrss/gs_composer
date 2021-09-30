
#include <ilcplex/ilocplex.h>
#include <cstdio>
#include <iostream>
#include <vector>
#include <string.h>
#include <stdlib.h>
#include <string>

#include "util.h"
#include "licks.h"

using namespace std;


// Implements the mathematical model
int licks(int nLicks, double normal_rate, double rest_rate, double repetition_rate, double turnaround_rate, double bn_rate)
{
	

// PREPROCESSING

	
	srand(time(NULL));

	char arr[100];
	string lp_path = "gs_optimizer/solver/licks.lp";

	vector <int> variables;

	vector <int> var_normal, 
				 var_rest, 
				 var_repetition, 
				 var_turnaround, 
				 var_bn, 
				 var_dummy;

	var_dummy = static_indexes(variables, "gs_optimizer/solver/indexes/DUMMY");
	var_normal = random_indexes(variables, "gs_optimizer/solver/indexes/NORMAL", normal_rate);	
	var_rest = random_indexes(variables, "gs_optimizer/solver/indexes/REST", rest_rate);
	var_repetition = random_indexes(variables, "gs_optimizer/solver/indexes/REPETITION", repetition_rate);
	var_turnaround = random_indexes(variables, "gs_optimizer/solver/indexes/TURNAROUND", turnaround_rate);
	var_bn = random_indexes(variables, "gs_optimizer/solver/indexes/BLUE_NOTE", bn_rate);
	
	cout << "Type and quantity of licks used: " << var_rest.size() + var_repetition.size() + var_turnaround.size() + var_normal.size() + var_bn.size();
	cout << "\n\tRest licks: " << var_rest.size();
	cout << "\n\tRepetition licks: " << var_repetition.size();
	cout << "\n\tTurnaround licks: " << var_turnaround.size();
	cout << "\n\tNormal licks: " << var_normal.size();
	cout << "\n\tBlue note licks: " << var_bn.size();
	cout << '\n';
	
	// Cost matrix declaration
	double **costMatrix = new double *[nLicks];
	
	for (int i = 0 ; i < nLicks ; i++)
		costMatrix[i] = new double[nLicks];

	costMatrix = cost_matrix(nLicks, "gs_optimizer/solver/files/matrix");


// MATHEMATICAL MODEL
	
	
	typedef IloArray <IloNumVarArray> NumVarMatrix;
	
	int i, j, k;
	IloEnv env;
	IloModel model(env);
	char varName[100];
	char cName[100];
	
	// 'x' variables
	NumVarMatrix x(env, nLicks);
	for (i = 0 ; i < nLicks ; i++){
		x[i] = IloNumVarArray(env, nLicks);
		for (j = 0 ; j < nLicks ; j++){
			x[i][j] = IloNumVar(env, 0.0, 1.0, ILOINT);
		} 
	}
	
	// Adding 'x' to the model
	for (i = 0 ; i < nLicks ; i++){
		if (check_variable(variables, i) == 1){
			for (j = 0 ; j < nLicks ; j++){
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
	IloBoolVarArray y(env, nLicks);
	
	// Adding 'y' to the model
	for (i = 0 ; i < nLicks ; i++){
		if (check_variable(variables, i) == 1){
			sprintf(varName, "y_%d", i);
			y[i].setName(varName);
			model.add(y[i]);
		}
	}

	// Objective function
	IloExpr fo(env);
	for (i = 0 ; i < nLicks ; i++){
		if (check_variable(variables, i) == 1){
			for (j = 0 ; j < nLicks ; j++){
				if (i == j)
					continue;
				if (check_variable(variables, j) == 1){
					fo += costMatrix[i][j] * x[i][j];
				}
			}
		}
	}
	model.add(IloMinimize(env, fo));

	// Constraint: exactly one arc must leave the lick that has been selected 
	for (i = 0 ; i < nLicks ; i++){
		if (check_variable(variables, i) == 1){
			IloExpr inFlow(env);
			for (j = 0 ; j < nLicks ; j++){
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
	
	// Constraint: exactly one arc must arrive at the lick that has been selected
	for (j = 0 ; j < nLicks ; j++){
		if (check_variable(variables, j) == 1){
			IloExpr outFlow(env);
			for (i = 0 ; i < nLicks ; i++){
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
	
	// Constraint: imposes that the total of measures in the final progession must be equal to 12
	IloExpr times(env);
	for (i = 0 ; i < nLicks ; i++){
		if (check_variable(variables, i) == 1){
			times += y[i];
		}
	}
	IloConstraint const_time = (times == 12);
	const_time.setName("c_time");
	model.add(const_time);
	
	// Constraint: guarantees that the final progression has exactly 2 rest licks
	IloExpr rest(env);
	for (i = 0 ; i < var_rest.size() ; i++){
		if (check_variable(variables, var_rest[i]) == 1){
			rest += y[var_rest[i]];
		}
	}
	IloConstraint const_rest = (rest == 2);
	const_rest.setName("c_rest");
	model.add(const_rest);
	
	// Constraint: guarantees that the final progression has exactly 2 blue note licks
	IloExpr bn(env);
	for (i = 0 ; i < var_bn.size() ; i++){
		if (check_variable(variables, var_bn[i]) == 1){
			bn += y[var_bn[i]];
		}
	}
	IloConstraint const_bn = (bn == 2);
	const_bn.setName("c_bn");
	model.add(const_bn);
	
	// Constraint: guarantees that the final progression has exactly 1 repetition lick
	IloExpr repetition(env);
	for (i = 0 ; i < var_repetition.size() ; i++){
		if (check_variable(variables, var_repetition[i]) == 1){
			repetition += y[var_repetition[i]];
		}
	}
	IloConstraint const_repetition = (repetition == 1);
	const_repetition.setName("c_repetition");
	model.add(const_repetition);
	
	// Constraint: guarantees that the final progression has exactly 1 turnaround lick
	IloExpr turnaround(env);
	for (i = 0 ; i < var_turnaround.size() ; i++){
		if (check_variable(variables, var_turnaround[i]) == 1){
			//turnaround += y[var_turnaround[i]];
			turnaround += x[var_turnaround[i]][0];
		}
	}
	IloConstraint const_turnaround = (turnaround == 1);
	const_turnaround.setName("c_turnaround");
	model.add(const_turnaround);
	
	//restrição 7: lick dummy
	IloExpr tDummy(env);
	for (i = 0 ; i < var_turnaround.size() ; i++){
		if (check_variable(variables, var_turnaround[i]) == 1){
			tDummy += y[var_turnaround[i]];
		}
	}
	IloConstraint const_tDummy = (tDummy == 1);
	const_tDummy.setName("c_tDummy");
	model.add(const_tDummy);
	
	// Last constraints: subtour elimination constraints 
	for (i = 0 ; i < nLicks ; i++){
		if (check_variable(variables, i) == 1){
			for (j = 0 ; j < nLicks ; j++){
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

	IloArray <IloBoolVarArray> z(env, nLicks);
    for (i = 0 ; i < nLicks ; i++){
    	IloBoolVarArray array(env, nLicks);
    	z[i] = array;
    }
    
    for (i = 0 ; i < nLicks ; i++){
    	if (check_variable(variables, i) == 1){
			for (j = 0 ; j < nLicks ; j++){
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
    
    for (i = 0 ; i < nLicks ; i++){
    	if (check_variable(variables, i) == 1){
			for (j = 0 ; j < nLicks ; j++){
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
