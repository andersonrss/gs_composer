
#include <ilcplex/ilocplex.h>
#include <cstdio>
#include <iostream>
#include <vector>
#include <time.h>
#include <string>

#include "util.h"

using namespace std;


// Read some types of indexes that are fixed, like rests or dStops 
vector <int> static_indexes(vector <int> &variables, string indexes_file)
{
	ifstream iFile(indexes_file);
	
	if (!iFile){
		cout << "Failed to open file in '" << indexes_file << "'\n";
		cout << "Aborting...\n";
		exit(0);
	}

	vector <int> type_indexes;

	int index = 0;
	int contains = 0;
	int n_indexes = 0;
	while (iFile >> index ){
		for (int i = 0 ; i < variables.size() ; i++){	
			if (index == variables[i]){
				contains = 1;
				break;
			}
		}

		if (contains == 1)
			contains = 0;
		else {
			variables.push_back(index);
			type_indexes.push_back(index);
			n_indexes++;
		}
	}

	return type_indexes;
}


// Read the number of musical notes each sublick has
void qtity_notes_mapping(vector <int> &values, string data)
{
	ifstream data_file(data);
	
	if (!data_file){
		cout << "Failed to open file in '" << data << "'\n";
		cout << "Aborting...\n";
		exit(0);
	}
	
	int index = 0;
	while(data_file >> index)
		values.push_back(index);
}


// Read the total duration of each sublick
void duration_sublicks_mapping(vector <double> &values, string data)
{
	ifstream data_file(data);
	
	if (!data_file){
		cout << "Failed to open file in '" << data << "'\n";
		cout << "Aborting...\n";
		exit(0);
	}
	
	double index = 0;
	while(data_file >> index)
		values.push_back(index);
}


// Read the cost matrix
double** cost_matrix(int nFiles, string data)
{
	double ** costMatrix = new double *[nFiles];
	
	for (int i = 0 ; i < nFiles ; i++)
		costMatrix[i] = new double[nFiles];
	
	string value;
	vector <string> aux;
	ifstream data_file(data);
	
	if (!data_file){
		cout << "Failed to open file in '" << data << "'\n";
		cout << "Aborting...\n";
		exit(0);
	} else
		while(getline(data_file, value, ' '))
			aux.push_back(value);

	int id = 0;
	for (int i = 0 ; i < nFiles ; i++){
		for (int j = 0 ; j < nFiles ; j++){
			costMatrix[i][j] = atoi(aux[id].c_str());
			id++;
		}
	}
	
	return costMatrix;
}


// Checks whether a variable belongs to the subset of variables of the model
int check_variable(vector <int> variables, int id)
{
	for (int i = 0 ; i < variables.size() ; i++)
		if (variables[i] == id)
			return 1;
	
	return 0;
}


// Randomly chooses a subset of variables (sublicks) to be used in lick generation
vector <int> random_indexes(vector <int> &variables, string indexes_file, double rate)
{

	ifstream iFile(indexes_file);

	if (!iFile){
		cout << "Failed to open file in '" << indexes_file << "'\n";
		cout << "Aborting...\n";
		exit(0);
	}
	
	vector <int> indexes;
	vector <int> type_indexes;

	int index = 0;
	while (iFile >> index )
		indexes.push_back(index);

	int bound;
	bound = indexes.size() * rate;

	int contains = 0;
	int random = 0;
	int attempts = 0;
	index = 0;
	while (index < bound){
		//if (attempts == 500){
		//	bound -= 1;
		//	attempts = 0;
		//}
		
		random = rand() % indexes.size();
		for (int i = 0 ; i < variables.size() ; i++){
			if (indexes[random] == variables[i]){
				contains = 1;
				break;
			}
		}

		if (contains == 1){
			contains = 0;
			continue;
			//attempts += 1;
		}
		else {
			variables.push_back(indexes[random]);
			type_indexes.push_back(indexes[random]);
			index++;
		}
	}

	return type_indexes;
}	



