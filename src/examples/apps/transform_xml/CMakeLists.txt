cmake_minimum_required(VERSION 3.10)

set(TARGET_NAME transform_xml)

project(${TARGET_NAME})

find_package(cppdiycs REQUIRED)

add_executable(${TARGET_NAME} 
    main.cpp
    transform_xml.h
    transform_xml.py)

add_test(${TARGET_NAME}_test ${TARGET_NAME})

set_property(TARGET ${TARGET_NAME} PROPERTY FOLDER "examples")

# working with absolute paths/filenames just to be absolutely safe
get_filename_component(INPUT_HPP  ${CMAKE_CURRENT_LIST_DIR}/transform_xml.h ABSOLUTE)
get_filename_component(OUTPUT_XML ${CMAKE_CURRENT_BINARY_DIR}/transform_xml.xml ABSOLUTE)
get_filename_component(OUTPUT_XML_HPP ${CMAKE_CURRENT_BINARY_DIR}/transform_xml.hpp ABSOLUTE)
get_filename_component(OUTPUT_XML_CPP ${CMAKE_CURRENT_BINARY_DIR}/transform_xml.cpp ABSOLUTE)
get_filename_component(OUTPUT_XSD_HPP ${CMAKE_CURRENT_BINARY_DIR}/transform_xsd.hpp ABSOLUTE)
get_filename_component(OUTPUT_XSD_CPP ${CMAKE_CURRENT_BINARY_DIR}/transform_xsd.cpp ABSOLUTE)

castxml_compile(XML ${OUTPUT_XML} 
                SOURCES ${INPUT_HPP} 
                INCLUDE_DIRS ${CMAKE_CURRENT_LIST_DIR})

python_transform(SCRIPT transform_xml.py
                 INPUTS  ${OUTPUT_XML}
                 OUTPUTS ${OUTPUT_XML_HPP} ${OUTPUT_XML_CPP} ${OUTPUT_XSD_HPP} ${OUTPUT_XSD_CPP}
                 ARGS
                 --xml ${OUTPUT_XML}
                 --source ${INPUT_HPP}
                 --xml_hpp ${OUTPUT_XML_HPP}
                 --xml_cpp ${OUTPUT_XML_CPP}
                 --xsd_hpp ${OUTPUT_XSD_HPP}
                 --xsd_cpp ${OUTPUT_XSD_CPP})

# add the generated files to the target 
target_include_directories(${TARGET_NAME} PRIVATE ${CMAKE_CURRENT_LIST_DIR} ${CMAKE_CURRENT_BINARY_DIR})
target_sources(${TARGET_NAME} PRIVATE ${OUTPUT_XML} ${OUTPUT_XML_HPP} ${OUTPUT_XML_CPP} ${OUTPUT_XSD_HPP} ${OUTPUT_XSD_CPP})

# group the generated files into folders
source_group("generated" FILES ${OUTPUT_XML_HPP} ${OUTPUT_XML_CPP} ${OUTPUT_XSD_HPP} ${OUTPUT_XSD_CPP} ${OUTPUT_XML})
source_group("python" FILES transform_xml.py)
