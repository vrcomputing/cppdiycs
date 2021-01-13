#include "transform_csv.h"
#include "transform_csv.hpp"
#include <iostream>
#include <cassert>
#include <sstream>

using namespace std;
using namespace example_namespace;

int main()
{
    const ExampleA a{ 'A', 1, 2, 3.0f, 4.0, "Alex" };
    const ExampleB b{ 'B', 5, 6, 7.0f, 8.0, "Bob" };
    const ExampleC c{ a, b, { 'C', 9, 8, 7, 5, "Carl" } };

    // ExampleA
    {
        // header
        {
            std::stringstream ss;
            generated::csv::header::operator<<(cout, a) << endl;
            generated::csv::header::operator<<(ss, a);
            const string debug = ss.str();
            assert(ss.str() == "c,s,i,f,d,name");
        }

        // data
        {
            std::stringstream ss;
            generated::csv::data::operator<<(cout, a) << endl;
            generated::csv::data::operator<<(ss, a);
            const string debug = ss.str();
            assert(ss.str() == "A,1,2,3,4,Alex");
        }
    }
    cout << endl;

    // ExampleB
    {
        // header
        {
            std::stringstream ss;
            generated::csv::header::operator<<(cout, b) << endl;
            generated::csv::header::operator<<(ss, b);
            const string debug = ss.str();
            assert(ss.str() == "c,s,i,f,d,name");
        }

        // data
        {
            std::stringstream ss;
            generated::csv::data::operator<<(cout, b) << endl;
            generated::csv::data::operator<<(ss, b);
            const string debug = ss.str();
            assert(ss.str() == "B,5,6,7,8,Bob");
        }
    }
    cout << endl;

    // ExampleC
    {
        // header
        {
            std::stringstream ss;
            generated::csv::header::operator<<(cout, c) << endl;
            generated::csv::header::operator<<(ss, c);
            const string debug = ss.str();
            assert(ss.str() == "a,b,d");
        }

        // data
        {
            std::stringstream ss;
            generated::csv::data::operator<<(cout, c) << endl;
            generated::csv::data::operator<<(ss, c);
            const string debug = ss.str();
            assert(ss.str() == "A,1,2,3,4,Alex,B,5,6,7,8,Bob,C,9,8,7,5,Carl");
        }
    }
    cout << endl;

    return EXIT_SUCCESS;
}