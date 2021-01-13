#pragma once

#include <string>

enum Gender
{
    MALE,
    FEMALE
};

struct Address
{
    std::string streetname;
    unsigned int housenumber;
    unsigned int zipcode;
    std::string city;
};

struct Date
{
    unsigned int day;
    unsigned int month;
    unsigned int year;
};

struct Person
{
    std::string firstname;
    std::string lastname;
    Date birthday;
    Address address;
    double size;
    Gender gender;
};