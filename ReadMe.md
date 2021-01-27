# cppdiycs - C/C++ DIY Code Synthesis

The purpose of this project is to enable developers to create their own code syntheses in an uncomplicated and adaptable manor.
It is __not__ the goal of this project to provide the most sophisticated generated code. Instead the project can be seen as a library of distinct examples on how to implement an individual code synthesis for specific use cases.

The core functionality of this project is based on the AST XML output of the [CastXML](https://github.com/CastXML/CastXML) compiler. It provides the [*C/C++ Abstract Syntax Tree*](https://en.wikipedia.org/wiki/Abstract_syntax_tree) of the compilation comprising type names, alignments, function names, parameter names and types and many more. In many use cases these "top-level" information are sufficient for the code synthesis.

# Use Cases

- Input Reader/Output Writer
- Encoding/Decoding e.g. [CSV](src/examples/apps/transform_csv/ReadMe.md), [XML](src/examples/apps/transform_xml/ReadMe.md), JSON, ...
- Serialization/Deserialization e.g. binary or string representation
- Schema synthesis e.g. [XSD](src/examples/apps/transform_xml/ReadMe.md), JSON, ...
- Test suite/case synthesis e.g. for googletest, Catch2, ...
- PIMPL/D-Pointer synthesis for implementation hiding
- REST API synthesis for methods and functions
- Custom reflection synthesis
- C-bindings for C++ classes/structs
- RPC synthesis for functions/methods
- ...

## Example Use Case

Generate a *__to_string__* function for the struct __Vector3D__, and/or an *__ostream& operator<<(ostream&, const T&)__*

## Example Input

```cpp 
struct Vector3D 
{ 
    double x;
    double y;
    double z;
};
```

## Example Generated Output A

```cpp 
std::string to_string(const Vector3D& v) // generated 
{
    std::stringstream ss;
    ss << v.x << "," << v.y << "," << v.z;
    return ss.str();
}
```

## Example Generated Output B

```cpp 
ostream& operator<<(ostream& os, const Vector3D& v) // generated
{
    os << v.x << "," << v.y << "," << v.z;
    return os;
}
```

For this use case mostly the names of the struct and fields (types) are relevant. Consider the two generated outputs A and B which are two of many possible ways to realize code generation of the "to_string" use case. The structure of the generated output can be adapted individually, since different code bases need different code synthesis.

## Intermediate CastXML Representation

```xml
<!-- hint: shortened for readability -->
<?xml version="1.0"?>
<CastXML format="1.1.6">
  <!-- ... -->
  <Struct id="_1" name="Vector3D" context="_2" location="f1:3" file="f1" line="3" members="_3 _4 _5 _6 _7 _8 _9" size="192" align="64"/>
  <Field id="_3" name="x" type="_10" context="_1" access="public" location="f1:5" file="f1" line="5" offset="0"/>
  <Field id="_4" name="y" type="_10" context="_1" access="public" location="f1:6" file="f1" line="6" offset="64"/>
  <Field id="_5" name="z" type="_10" context="_1" access="public" location="f1:7" file="f1" line="7" offset="128"/>
  <!-- ... -->
  <Namespace id="_2" name="::"/>
  <!-- ... -->
  <File id="f1" name="transform_to_string.h"/>  
</CastXML>
```

### Explanation

- __Struct__ This is the struct's element comprising its name
- __Field__ These are the struct's field elements with among others its name, referencing the struct via the __context__ attribute
- __File__ This is the source file of the compilation referenced by via the struct element's __file__ attribute

## Installation

1. Download and build and install the [castxmlcmake](https://github.com/vrcomputing/castxmlcmake) CMake project. 
    - The installation folder will then define __*castxml_DIR*__
2. Download and build and install the [cppdiycs](https://github.com/vrcomputing/cppdiycs) CMake project.
    - The installation folder will then define __*cppdiycs_DIR*__
3. Integrate both installations into your project using the following CMake find_package(...) calls

```cmake
find_package(castxml PATHS ${castxml_DIR} NO_DEFAULT_PATH REQUIRED)
find_package(cppdiycs PATHS ${cppdiycs_DIR} NO_DEFAULT_PATH REQUIRED)
```

## Usage 

1. use the CMake function *castxml_compile* to compiler your sources and get the *xml file
2. use the CMake function *python_transform* to tranform your *.xml file as desired
    - write your own *.py script beforehand to parse the *.xml file

### Example 

```cmake
castxml_compile(XML ${OUTPUT_XML} 
                SOURCES ${INPUT_HPP}
                INCLUDE_DIRS ${CMAKE_CURRENT_LIST_DIR} 
                TYPES Calculator Vector3D)
```

#### Explanation

- __XML__ (*required*) defines the output intermediate XML file
- __SOURCES__ (*required*) defines the input C/C++ source file to be compiled
- __INCLUDE_DIRS__ (*optional*) defines the input C/C++ source file to be compiled
- __TYPES__ (*optional*) optimizes the output to these types (C++ namespaces must be added)    

```cmake
python_transform(SCRIPT transform.py
                 INPUTS  ${OUTPUT_XML}
                 OUTPUTS ${OUTPUT_HPP} ${OUTPUT_CPP}                 
                 ARGS                 
                 # optional/script specific
                 --xml ${OUTPUT_XML}
                 --source ${INPUT_HPP}
                 --hpp ${OUTPUT_HPP}
                 --cpp ${OUTPUT_CPP}
                 --type Calculator Vector3D
                 # optional/script specific
                 )
```

#### Explanation

- __SCRIPT__ (*required*) define the name of the tranformation Python script
- __INPUTS__ (*required*) defines the names of the dependant input files e.g. the previously generatex XML file
- __OUTPUTS__ (*required*) defines the names of generated output files e.g. header and source files
- __ARGS__ (*optional*) defines additional arguments which will be forwarded to the Python script
    - the command line arguments depend on your implementation

### Transformation

```python
# basic CastXML output parsing
import sys
from lxml import etree

tree = etree.parse(sys.argv[1]) # argv[1] == input xml file
root = tree.getroot()

structs = root.xpath("Struct[@name = 'Vector3D']")
for struct_element in structs:
    print(struct_element.get('name'))
    fields = root.xpath("Field[@context = '%s']" % struct_element.get('id'))
    for field_element in fields:
        field_type_id = field_element.get('type')
        field_name = field_element.get('name')
        field_type = root.find("FundamentalType[@id = '%s']" % field_type_id).get('name')
        print(' - %s : %s' % (field_name, field_type))
```

#### Explanation

This Python script uses [XPATH](https://www.w3schools.com/xml/xpath_intro.asp) queries to navigate to the structs of interest, in this case only the struct __Vector3D__. Afterwards it navigates to all fields and prints their names and type names:

```
Vector3D
 - x : double
 - y : double
 - z : double
```

## Focus

- usability
- adaptability
- integratability

## Design Descisions

- __Python__ is an established programming language with a variety of utility modules, as well as many business toolchains relying on it. Furthermore it is easy to learn and due to its runtime interpretation ideal for code synthesis that needs highly individual adaptations.

## Dependencies

- [CastXML](https://github.com/CastXML/CastXML) Version 0.3.6
    - [castxmlcmake](https://github.com/vrcomputing/castxmlcmake) provides CastXML binaries as CMake package by downloading them from [CastXMLSuperbuild](https://github.com/CastXML/CastXMLSuperbuild)
- Python version depends on your scripts (Version 3.9 tested)
- CMake Version 3.10
