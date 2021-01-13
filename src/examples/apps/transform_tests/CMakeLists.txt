cmake_minimum_required(VERSION 3.10)

set(TARGET_NAME transform_tests)

project(${TARGET_NAME})

find_package(cppdiycs REQUIRED)

add_executable(${TARGET_NAME} main.cpp main.h transform_tests.py)

add_test(${TARGET_NAME}_test ${TARGET_NAME})

set_property(TARGET ${TARGET_NAME} PROPERTY FOLDER "examples")

# working with absolute paths/filenames just to be absolutely safe
get_filename_component(INPUT_HPP  ${CMAKE_CURRENT_LIST_DIR}/main.h ABSOLUTE)
get_filename_component(OUTPUT_HPP ${CMAKE_CURRENT_BINARY_DIR}/generated/transform_tests.hpp ABSOLUTE)
get_filename_component(OUTPUT_CPP ${CMAKE_CURRENT_BINARY_DIR}/generated/transform_tests.cpp ABSOLUTE)
get_filename_component(OUTPUT_XML ${CMAKE_CURRENT_BINARY_DIR}/generated/transform_tests.xml ABSOLUTE)

castxml_compile(XML ${OUTPUT_XML} 
                SOURCES ${INPUT_HPP} 
				INCLUDE_DIRS ${CMAKE_CURRENT_LIST_DIR} 
				TYPES Calculator)

python_transform(SCRIPT transform_tests.py
                 INPUTS  ${OUTPUT_XML}
				 OUTPUTS ${OUTPUT_HPP} ${OUTPUT_CPP}
				 ARGS
				 --xml ${OUTPUT_XML}
				 --source ${INPUT_HPP}
				 --hpp ${OUTPUT_HPP}
				 --cpp ${OUTPUT_CPP}
				 --type Calculator)
                 
# add the generated files to the target 
target_include_directories(${TARGET_NAME} PRIVATE ${CMAKE_CURRENT_LIST_DIR} ${CMAKE_CURRENT_BINARY_DIR}/generated)
target_sources(${TARGET_NAME} PRIVATE ${OUTPUT_HPP} ${OUTPUT_CPP} ${OUTPUT_XML})

# group the generated files into folders
source_group("generated" FILES ${OUTPUT_HPP} ${OUTPUT_CPP} ${OUTPUT_XML})
source_group("python" FILES ${CMAKE_CURRENT_LIST_DIR}/transform_tests.py)