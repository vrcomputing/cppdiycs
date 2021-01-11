#include "transform_to_string.h"
#include "transform_to_string.hpp"
#include <iostream>

using namespace std;
using namespace generated::string_util;

int main()
{
	const Vector3D v{1,2,3};
	cout << v << endl;
	cout << to_string(v) << endl;
    return 0;
}