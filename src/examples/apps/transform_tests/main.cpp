#include <cassert>
#include <cmath>

#include "main.h"
#include "transform_tests.hpp"

int main()
{
    assert(test_suite_Calculator::test_case_all());
    return 0;
}

// must be created manually (or via IDE functions preferably)

test_suite_Calculator::test_case_add_args test_suite_Calculator::test_case_add_get_args()
{
    return { 4, 5, 9 };
}

test_suite_Calculator::test_case_sub_args test_suite_Calculator::test_case_sub_get_args()
{
    return { 4, 5, -1 };
}

test_suite_Calculator::test_case_mul_args test_suite_Calculator::test_case_mul_get_args()
{
    return { 4, 5, 20 };
}

test_suite_Calculator::test_case_div_args test_suite_Calculator::test_case_div_get_args()
{
    return { 4, 5, 0.8 };
}