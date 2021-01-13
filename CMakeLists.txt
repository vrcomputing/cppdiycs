cmake_minimum_required(VERSION 3.10)

project(cppdiycs)

enable_testing()

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

find_package(cppdiycs REQUIRED PATHS cmake NO_DEFAULT_PATH)

add_subdirectory(cmake)
add_subdirectory(src)
