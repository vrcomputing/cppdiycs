# Use Case - Generating CSV Writers For Structs

## Input (C/C++, transform_csv.h)

```cpp
#pragma once

#include <string>

struct ExampleA
{
	char c;
	short s;
	int i;
	float f;
	double d;
	std::string name = "empty";
};
```

## Intermediate Output (XML, transform_csv.xml)

```xml
<?xml version="1.0"?>
<CastXML format="1.1.6">
  <!-- ... -->
  <Struct id="_1681" name="ExampleA" context="_1" location="f51:5" file="f51" line="5" members="_3404 _3405 _3406 _3407 _3408 _3409 _3410 _3411 _3412 _3413" size="448" align="64"/>
  <!-- ... -->
  <Field id="_3404" name="c" type="_3335" context="_1681" access="public" location="f51:7" file="f51" line="7" offset="0"/>
  <Field id="_3405" name="s" type="_3056" context="_1681" access="public" location="f51:8" file="f51" line="8" offset="16"/>
  <Field id="_3406" name="i" type="_1753" context="_1681" access="public" location="f51:9" file="f51" line="9" offset="32"/>
  <Field id="_3407" name="f" type="_2978" context="_1681" access="public" location="f51:10" file="f51" line="10" offset="64"/>
  <Field id="_3408" name="d" type="_2975" context="_1681" access="public" location="f51:11" file="f51" line="11" offset="128"/>
  <Field id="_3409" name="name" type="_2047" context="_1681" access="public" location="f51:12" file="f51" line="12" offset="192"/>
  <!-- ... -->
  <File id="f51" name="transform_csv.h"/>
  <!-- ... -->
</CastXML>
```

- __Struct__ These elements are the most important entry points for this use case
    - __name__ The struct's name without potential namespaces (can be resolved via the *__context__* attribute)
    - __file__ The struct's origin file, relevant for identifying relevant structs 
    - __...__
- __Field__ These elements represent fields of structs or classes and are important for this use case
    - __id__ The field's unique id in the compilation
    - __name__ The field's name required for the output
    - __type__ The field's type may need further resolving, since structs can have fields of structs recursively
    - __...__
- __File__ These tags help us to limit the parsing effort and output since most likely only structs from the input sources are relevant
    - __id__ The file's unique id in the compilation, relevant for identifying relevant structs
    - __name__ The absolute filename required for comparison with the input filenames
    - __...__

# Output (C/C++)

## Output (C/C++, transform_csv.hpp)

```cpp
#pragma once
#include <ostream>
#include <transform_csv.h>

namespace csv 
{
namespace header 
{
    std::ostream& operator<<(std::ostream& os, const ExampleA& obj);
}
namespace data 
{
    std::ostream& operator<<(std::ostream& os, const ExampleA& obj);
}
}
```

## Output (C/C++, transform_csv.cpp)

```cpp
#include <transform_csv.hpp>

std::ostream& csv::header::operator<<(std::ostream& os, const ExampleA& obj)
{
	os << "c,s,i,f,d,name";
	return os;
}
std::ostream& csv::data::operator<<(std::ostream& os, const ExampleA& obj)
{
	os << obj.c << "," << obj.s << "," << obj.i << "," << obj.f << "," << obj.d << "," << obj.name;
	return os;
}
```