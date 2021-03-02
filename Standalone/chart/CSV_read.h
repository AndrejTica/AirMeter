#pragma once

#include<string>
#include<cstring>
#include<vector>
#include<iostream>
#include<cstdlib> 
#include<fstream>
#include <sstream>

using namespace std;
class CSVRead {

private:
	const char* csvDateiname;

public:
	
	CSVRead(const char* s);

	string getDate();
	vector<string> getNames();
    const vector<string> getX_Axis();
	vector<string> getColumn(int x);



};
