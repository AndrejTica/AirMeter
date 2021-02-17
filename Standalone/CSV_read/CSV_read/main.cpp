#include "CSV_read.h";

int main() {

	CSVRead quelle("airMeter_20210202.csv");

	string datum;
	datum = quelle.getDate();
	cout << "this is the date: " << datum << endl;

	vector<string> names = quelle.getNames();
	int counter = 0;
	for (auto tokens : names) {
		counter++;
		cout << "Columns are: " << counter << " -> " << tokens << endl;

	}

	vector<string> x_axis = quelle.getX_Axis();
	cout << "The x-Axis vector:" << endl;
	for (auto tokens : x_axis) {
		cout << tokens << endl;
	}

	vector<string> column = quelle.getColumn(4);
	for (auto tokens : column) {
		cout << tokens << endl;
	}
}