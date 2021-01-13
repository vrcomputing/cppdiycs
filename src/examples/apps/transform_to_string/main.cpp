#include "transform_to_string.h"
#include "transform_to_string.hpp"
#include <iostream>
#include <cassert>
#include <sstream>

using namespace std;
using namespace generated::string_util;

int main()
{
    const Vector3D v{ 1, 2, 3 };

    std::stringstream ss;
    ss << v;
    cout << v << endl;
    assert(ss.str() == "1,2,3");
    
    cout << to_string(v) << endl;
    assert(to_string(v) == "1,2,3");
    return 0;
}