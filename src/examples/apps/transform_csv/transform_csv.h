#pragma once

#include <string>

namespace example_namespace
{
struct ExampleA
{
    char c;
    short s;
    int i;
    float f;
    double d;
    std::string name = "empty";
};

struct ExampleB
{
    char c;
    short s;
    int i;
    float f;
    double d;
    std::string name = "empty";
};

struct ExampleD
{
    char c;
    short s;
    int i;
    float f;
    double d;
    std::string name = "empty";
};

struct ExampleC
{
    ExampleA a;
    ExampleB b;
    ExampleD d;
};
} // namespace example_namespace
