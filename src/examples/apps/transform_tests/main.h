#pragma once

class Calculator
{
  public:
    double add(double x, double y) const
    {
        return x + y;
    }

    double sub(double x, double y) const
    {
        return x - y;
    }

    double mul(double x, double y) const
    {
        return x * y;
    }

    double div(double x, double y) const
    {
        return x / y;
    }
};