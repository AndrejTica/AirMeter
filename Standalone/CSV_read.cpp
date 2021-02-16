#include<string>
#include<cstring>
#include<vector>
#include<iostream>
#include<cstdlib> 
#include<fstream>
#include<iostream>
#include <sstream>

using namespace std;

vector<string> getX_Axis(ifstream& source) //right now it saves everything into one vector :(
{
	string s;
	vector<string> tokens;

	while (source >> s) { //every line gets pushed into the string

		string token;
		istringstream tokenStream(s);
		int y = 0;
		while (getline(tokenStream, token, ';')) {	//parses the line string into tokens and pushes it into the vector. Returns a boolean
			y++;
			if (y>1 && y<3) {
				tokens.push_back(token);
			}
		}
		for (static bool first = true; first; first = false) //only runs once to delete the column name
		{
			tokens.erase(tokens.begin());
		}
	}
	return tokens;
}

vector<string> getColumn(ifstream& source, int x) //right now it saves everything into one vector :(
{
	string s;
	vector<string> tokens;

	while (source >> s) { //every line gets pushed into the string

		string token;
		istringstream tokenStream(s);
		int counter = 0;
		switch(x){
		case 1:
			
			while (getline(tokenStream, token, ';')) {	//parses the line string into tokens and pushes it into the vector. Returns a boolean
				counter++;
				if (counter > 2 && counter < 4) { //2,4 -> 3. column -> 1 for user
					tokens.push_back(token);
				}
			}
			for (static bool first = true; first; first = false){ //only runs once to delete the column name
			
				tokens.erase(tokens.begin());
			}
			break;
		case 2:
			
			while (getline(tokenStream, token, ';')) {	//parses the line string into tokens and pushes it into the vector. Returns a boolean
				counter++;
				if (counter > 3 && counter < 5) { //3,4 -> 4. column -> 2 for user
					tokens.push_back(token);
				}
			}
			for (static bool first = true; first; first = false) { //only runs once to delete the column name

				tokens.erase(tokens.begin());
			}
			break;
		case 3:
			
			while (getline(tokenStream, token, ';')) {	//parses the line string into tokens and pushes it into the vector. Returns a boolean
				counter++;
				if (counter > 4 && counter < 6) { //4,6 -> 4. column -> 3 for user
					tokens.push_back(token);
				}
			}
			for (static bool first = true; first; first = false) { //only runs once to delete the column name

				tokens.erase(tokens.begin());
			}
			break;
		case 4:
			
			while (getline(tokenStream, token, ';')) {	//parses the line string into tokens and pushes it into the vector. Returns a boolean
				counter++;
				if (counter > 5 && counter < 7) { //5,7 -> 5. column -> 4 for user
					tokens.push_back(token);
				}
			}
			for (static bool first = true; first; first = false) { //only runs once to delete the column name

				tokens.erase(tokens.begin());
			}
			break;
		}
	}
	return tokens;
}

string getDate(ifstream& quelle) 
{
	
	string s;
	vector<string> tokens;

		while (quelle >> s) { //jede zeile wird durchnommen
		
				string token;
				istringstream tokenStream(s);
				getline(tokenStream, token, ';');	//fuer jede zeile das erste element ins tokens pushen. While noetig wenn wir alle zeilen elemente wollen, returnt ein boolean
				tokens.push_back(token);
				
		}
	
		tokens.erase(tokens.begin(),tokens.end()-1); //aus der ersten spalte wird alles auser letzer element erased
		string ret = tokens[0];
		return ret;
	
}

vector<string> getNames(ifstream& source) //right now it saves everything into one vector :(
{
	string s;
	vector<string> tokens;

		while (source >> s) { //every line gets pushed into the string
			for (static bool first = true; first; first = false) { //only runs once to get only the first line
				string token;
				istringstream tokenStream(s);
				int counter = 0;
			
					while (getline(tokenStream, token, ';')) { //parses the line string into tokens and pushes it into the vector. Returns a boolean
						counter++;
						if (counter > 2) {
						tokens.push_back(token);
						}

					
					}
					return tokens;
			}
		}
		
	
}

int main() {
	
	const char* csvDateiname = "airMeter_20210202.csv";
	
	ifstream quelle1(csvDateiname); 
	ifstream quelle2(csvDateiname);
	ifstream quelle3(csvDateiname);
	ifstream quelle4(csvDateiname);
	//if (!quelle) { // Fehlerabfrage
	//	cerr << csvDateiname << " kann nicht geoffnet werden!\n";
	//	return 0;
	//}
	
	vector<string> names = getNames(quelle1);
	int counter = 0;
	for (auto tokens : names) {
		counter++;
		cout << "Columns are: " << counter << " -> " << tokens << endl;
	}


	vector<string> column = getColumn(quelle2, 3);
	for (auto tokens : column) {
	cout << tokens << endl;
	}


	vector<string> x_axis = getX_Axis(quelle3);
	for (auto tokens : x_axis) {
		cout << tokens << endl;
	}
	
	string datum; 
	datum = getDate(quelle4);
	cout << "this is the date: " << datum << endl;
	
}
