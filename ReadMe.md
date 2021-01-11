# cppdiycs - C/C++ Do It Yourself Code Synthesis

The purpose of this project is to enable developers to create their own code synthesis' in an uncomplicated and adaptable manor.
It is __not__ the goal of this project to provide the most sophisticated generated code. Instead the project can be seen as a library of distinct examples on how to implement an individual code synthesis for specific use cases.

The core functionality is based on the AST XML output of the [CastXML](https://github.com/CastXML/CastXML) compiler. It provides the *C/C++ Abstract Snytax Tree* of the compilation including type names, alignments, function names, parameter types and many more. In many use cases these "top-level" information are sufficient for the code synthesis e.g.:

```cpp
// input 
struct Vector3D 
{ 
    double x;
    double y;
    double z;
};

// generated output A
std::string to_string(const Vector3D& v) 
{
    std::stringstream ss;
    ss << "(" << v.x << "," << v.y << "," << v.z << ")";
    return ss.str();
}

// generated output B
ostream& operator<<(ostream& os, const Vector3D& v)
{
    os << "(" << v.x << "," << v.y << "," << v.z << ")";
    return os;
}
```

For this use case mostly the names of the struct and fields (types) are relevant. Consider the two generated outputs A and B which are two of many possible ways to realize code generation of the "to_string" use case. The structure of the generated output can be adapted individually, since different code bases need different code synthesis.

## Focus

- usability
- adaptability
- integratability

## Design Descisions

- __Python__ is an established programming language with a variety of utility modules, as well as many business toolchains relying on it. Furthermore it is easy to learn and due to its runtime interpretation ideal for code synthesis that needs highly individual adaptations.

## Dependencies

- [CastXML](https://github.com/CastXML/CastXML) Version 0.3.6
- Python version depends on your scripts (Version 3.9 tested)