#include "transform_csv.h"
#include "transform_csv.hpp"
#include <iostream>

using namespace std;

int main()
{
	const example_namespace::ExampleA a{ 'A', 1, 2, 3.0f, 4.0 };
	csv::header::operator<<(cout, a) << endl;
	csv::data::operator<<(cout, a) << endl;

	cout << endl;
	
	const example_namespace::ExampleB b{ 'B', 5, 6, 7.0f, 8.0 };
	csv::header::operator<<(cout, b) << endl;
	csv::data::operator<<(cout, b) << endl;

	cout << endl;
	
	const example_namespace::ExampleC c{ a, b };
	csv::header::operator<<(cout, c) << endl;
	csv::data::operator<<(cout, c) << endl;
	
    return 0;
}