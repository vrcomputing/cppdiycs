#include "transform_xml.h"
#include "transform_xml.hpp"
#include "transform_xsd.hpp"
#include <iostream>
#include <cassert>
#include <sstream>
#include <iomanip>
#include <fstream>

int main()
{
    const Address address{ "Examplestreet", 123, 12345, "Examplecity" };
    const Date date{ 1, 12, 1911 };
    const Person person{ "Max", "Mustermann", date, address, 178, MALE };

    // Address
    {
        std::stringstream xsd;
        std::stringstream xml;
        std::cout << "XSD" << std::endl;
        generated::xsd::root::operator<<(xsd, address);
        generated::xsd::root::operator<<(std::cout, address) << std::endl;
        std::cout << "XML" << std::endl;
        generated::xml::root::operator<<(xml, address);
        generated::xml::root::operator<<(std::cout, address) << std::endl;
    }

    // Date
    {
        std::stringstream xsd;
        std::stringstream xml;
        std::cout << "XSD" << std::endl;
        generated::xsd::root::operator<<(xsd, date);
        generated::xsd::root::operator<<(std::cout, date) << std::endl;
        std::cout << "XML" << std::endl;
        generated::xml::root::operator<<(xml, date);
        generated::xml::root::operator<<(std::cout, date) << std::endl;
    }

    // Person
    {
        std::stringstream xsd;
        std::stringstream xml;
        std::ofstream xsd_file;
        std::ofstream xml_file;

        // write Person's XSD into streams
        std::cout << "XSD" << std::endl;
        generated::xsd::root::operator<<(xsd, person);
        generated::xsd::root::operator<<(xsd_file, person);
        generated::xsd::root::operator<<(std::cout, person) << std::endl;

        // write Person's XML into streams
        std::cout << "XML" << std::endl;
        generated::xml::root::operator<<(xml, person);
        generated::xml::root::operator<<(xml_file, person);
        generated::xml::root::operator<<(std::cout, person) << std::endl;
    }

    return EXIT_SUCCESS;
}