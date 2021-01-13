# Use Case - Generating XML/XSD Encoder

Writing XMLs and XSDs should go hand in hand, but require tedious manual work. Therefore this example can be used a an entry point for creating your own XML/XSD encoders. It shows how to access the required information about structs and their fields and generate code that translates structs into XSD *complexType* ans enums into XSD *simpleType*. Fundamental C++ types are being mapped to XSD types: 

```python
xsd_types = {
    'std::string': 'xs:string',
    'int': 'xs:unsignedInt',
    'float': 'xs:float',
    'double': 'xs:double',
    'unsigned int': 'xs:unsignedInt'
}
```

## Known Limitations

- this example doesn't cover multiple structs with the same name

## Hints

- it would be better to synthesize code around a good XML/XSD library (e.g. [pugixml](https://pugixml.org/), [Xerces-C++](https://xerces.apache.org/xerces-c/), [Libxml2](http://www.xmlsoft.org/), ...) to deal with formatting, encoding, validation, ...

## Input

```cpp
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
```

## Intermediate Output

In this example we are translating C++ structs and enums into XSD *complexType* and *simpleType* respectively. Thefore we need to parse the compiled XML for __Enumeration__, __Struct__ and __Field__ nodes to retreive all required information .

```xml
<?xml version="1.0"?>
<CastXML format="1.1.6">
  <!-- ... -->
  <Enumeration id="_1682" name="Gender" context="_1" location="f51:5" file="f51" line="5" size="32" align="32">
    <EnumValue name="MALE" init="0"/>
    <EnumValue name="FEMALE" init="1"/>
  </Enumeration>
  <!-- ... -->
  <Field id="_3406" name="streetname" type="_2049" context="_1683" access="public" location="f51:13" file="f51" line="13" offset="0"/>
  <Field id="_3407" name="housenumber" type="_1754" context="_1683" access="public" location="f51:14" file="f51" line="14" offset="256"/>
  <Field id="_3408" name="zipcode" type="_1754" context="_1683" access="public" location="f51:15" file="f51" line="15" offset="288"/>
  <Field id="_3409" name="city" type="_2049" context="_1683" access="public" location="f51:16" file="f51" line="16" offset="320"/>  
  <!-- ... -->
  <Struct id="_1683" name="Address" context="_1" location="f51:11" file="f51" line="11" members="_3406 _3407 _3408 _3409 _3410 _3411 _3412 _3413" size="576" align="64"/>
  <Struct id="_1684" name="Date" context="_1" location="f51:19" file="f51" line="19" members="_3414 _3415 _3416 _3417 _3418 _3419 _3420" size="96" align="32"/>
  <Struct id="_1685" name="Person" context="_1" location="f51:26" file="f51" line="26" members="_3421 _3422 _3423 _3424 _3425 _3426 _3427 _3428 _3429 _3430" size="1344" align="64"/>  
</CastXML>
```

# Output (C/C++)

## XSD generator code (excerpt)

The exmaple generates two namespaces *generated::xsd::root* and *generated::xsd::data* separating the XSD *complexType* definition from the actual document definition. Note the *<xs:element name="Person" type="Person"/>* line which will define a node named *Person* of the type *Person* as the XML's root.

```cpp
std::ostream& generated::xsd::root::operator<<(std::ostream& os, const Person& obj)
{
    os << R"(<?xml version="1.0" encoding="UTF-8" ?>)";
    os << R"(<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">)";
    data::operator<<(os, decltype(obj.birthday){});
    data::operator<<(os, decltype(obj.address){});
    data::operator<<(os, decltype(obj.gender){});
    data::operator<<(os, obj);
    os << R"(<xs:element name="Person" type="Person"/>)";
    os << R"(</xs:schema>)";
    return os;
}
```

The actual XSD *complexType* definition is done in the *generated::xsd::data* namespace. All recursively required types (Date, Address, Gender) have their own operator<< implementation. You can therefore use either the root::operator<< to define its type T as the document's root element or use the data::operator<< to only get the definition of a type.

```cpp
std::ostream& generated::xsd::data::operator<<(std::ostream& os, const Person& obj)
{
    os << R"(<xs:complexType name="Person">)";
    os << R"(<xs:sequence>)";
    os << R"(<xs:element name="firstname" type="xs:string" minOccurs="1" maxOccurs="1" />)";
    os << R"(<xs:element name="lastname" type="xs:string" minOccurs="1" maxOccurs="1" />)";
    os << R"(<xs:element name="birthday" type="Date" minOccurs="1" maxOccurs="1" />)";
    os << R"(<xs:element name="address" type="Address" minOccurs="1" maxOccurs="1" />)";
    os << R"(<xs:element name="size" type="xs:double" minOccurs="1" maxOccurs="1" />)";
    os << R"(<xs:element name="gender" type="Gender" minOccurs="1" maxOccurs="1" />)";
    os << R"(</xs:sequence>)";
    os << R"(</xs:complexType>)";
    return os;
}
```

## XML generator code (excerpt)

The exmaple generates two namespaces *generated::xml::root* and *generated::xml::data* separating a XML root node definition from a XML child node. The root::operator<< can be used to get an object encoded as e.g. a XML root node while the data::operator<< only returns the types fields as nodes recursively.

```cpp
std::ostream& generated::xml::root::operator<<(std::ostream& os, const Person& obj)
{
    os << R"(<?xml version="1.0" encoding="UTF-8" ?>)";
    os << R"(<Person>)";
    data::operator<<(os, obj);
    os << R"(</Person>)";
    return os;
}
```

```cpp
std::ostream& generated::xml::data::operator<<(std::ostream& os, const Person& obj)
{
    os << R"(<firstname>)" << obj.firstname << R"(</firstname>)";
    os << R"(<lastname>)" << obj.lastname << R"(</lastname>)";
    os << R"(<birthday>)" << obj.birthday << R"(</birthday>)";
    os << R"(<address>)" << obj.address << R"(</address>)";
    os << R"(<size>)" << obj.size << R"(</size>)";
    os << R"(<gender>)" << obj.gender << R"(</gender>)";
    return os;
}
```

# Usage

```cpp
Address address{ "Examplestreet", 123, 12345, "Examplecity" };
Date date{ 1, 12, 1911 };
Person person{ "Max", "Mustermann", date, address, 178, MALE };

std::stringstream xsd;
std::stringstream xml;
std::ofstream xsd_file;
std::ofstream xml_file;

// write Person's XSD into streams
generated::xsd::root::operator<<(xsd, person);
generated::xsd::root::operator<<(xsd_file, person);
generated::xsd::root::operator<<(std::cout, person) << std::endl;

// write Person's XML into streams
generated::xml::root::operator<<(xml, person);
generated::xml::root::operator<<(xml_file, person);
generated::xml::root::operator<<(std::cout, person) << std::endl;
```

## XSD Output

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:complexType name="Date">
        <xs:sequence>
            <xs:element name="day" type="xs:unsignedInt" minOccurs="1" maxOccurs="1" />
            <xs:element name="month" type="xs:unsignedInt" minOccurs="1" maxOccurs="1" />
            <xs:element name="year" type="xs:unsignedInt" minOccurs="1" maxOccurs="1" />
        </xs:sequence>
    </xs:complexType>
    <xs:complexType name="Address">
        <xs:sequence>
            <xs:element name="streetname" type="xs:string" minOccurs="1" maxOccurs="1" />
            <xs:element name="housenumber" type="xs:unsignedInt" minOccurs="1" maxOccurs="1" />
            <xs:element name="zipcode" type="xs:unsignedInt" minOccurs="1" maxOccurs="1" />
            <xs:element name="city" type="xs:string" minOccurs="1" maxOccurs="1" />
        </xs:sequence>
    </xs:complexType>
    <xs:simpleType name="Gender">
        <xs:restriction base="xs:integer">
            <!-- MALE -->
            <xs:enumeration value="0"/>
            <!-- FEMALE -->
            <xs:enumeration value="1"/>
        </xs:restriction>
    </xs:simpleType>
    <xs:complexType name="Person">
        <xs:sequence>
            <xs:element name="firstname" type="xs:string" minOccurs="1" maxOccurs="1" />
            <xs:element name="lastname" type="xs:string" minOccurs="1" maxOccurs="1" />
            <xs:element name="birthday" type="Date" minOccurs="1" maxOccurs="1" />
            <xs:element name="address" type="Address" minOccurs="1" maxOccurs="1" />
            <xs:element name="size" type="xs:double" minOccurs="1" maxOccurs="1" />
            <xs:element name="gender" type="Gender" minOccurs="1" maxOccurs="1" />
        </xs:sequence>
    </xs:complexType>
    <xs:element name="Person" type="Person"/>
</xs:schema>
```

## XML Output

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<Person>
    <firstname>Max</firstname>
    <lastname>Mustermann</lastname>
    <birthday>
        <day>1</day>
        <month>12</month>
        <year>1911</year>
    </birthday>
    <address>
        <streetname>Examplestreet</streetname>
        <housenumber>123</housenumber>
        <zipcode>12345</zipcode>
        <city>Examplecity</city>
    </address>
    <size>178</size>
    <gender>0</gender>
</Person>
```