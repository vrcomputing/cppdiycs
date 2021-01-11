cmake_minimum_required(VERSION 3.18)

set(TARGET_NAME transform_to_string)

project(${TARGET_NAME})

find_package(Python REQUIRED COMPONENTS Interpreter)
find_package(castxml REQUIRED)

add_executable(${TARGET_NAME} 
    main.cpp
    transform_to_string.h
    transform_to_string.py)

set_property(TARGET ${TARGET_NAME} PROPERTY FOLDER "examples")

# working with absolute paths/filenames jsut to be absolutely safe
get_filename_component(INPUT_HPP  ${CMAKE_CURRENT_LIST_DIR}/transform_to_string.h ABSOLUTE)
get_filename_component(OUTPUT_HPP ${CMAKE_CURRENT_BINARY_DIR}/generated/transform_to_string.hpp ABSOLUTE)
get_filename_component(OUTPUT_CPP ${CMAKE_CURRENT_BINARY_DIR}/generated/transform_to_string.cpp ABSOLUTE)
get_filename_component(OUTPUT_XML ${CMAKE_CURRENT_BINARY_DIR}/generated/transform_to_string.xml ABSOLUTE)

castxml_compile(XML ${OUTPUT_XML} 
                SOURCES ${INPUT_HPP} 
				INCLUDE_DIRS ${CMAKE_CURRENT_LIST_DIR} 
				TYPES Vector3D)

python_transform(SCRIPT transform_to_string.py
                 INPUTS  ${OUTPUT_XML}
				 OUTPUTS ${OUTPUT_HPP} ${OUTPUT_CPP}
				 ARGS
				 --xml ${OUTPUT_XML}
				 --source ${INPUT_HPP}
				 --hpp ${OUTPUT_HPP}
				 --cpp ${OUTPUT_CPP}
				 --type Vector3D)

# add the generated files to the target 
target_include_directories(${TARGET_NAME} PRIVATE ${CMAKE_CURRENT_LIST_DIR} ${CMAKE_CURRENT_BINARY_DIR}/generated)
target_sources(${TARGET_NAME} PRIVATE ${OUTPUT_HPP} ${OUTPUT_CPP} ${OUTPUT_XML})

# group the generated files into folders
source_group("generated" FILES ${OUTPUT_HPP} ${OUTPUT_CPP} ${OUTPUT_XML})
source_group("python" FILES transform_to_string.py)