cmake_minimum_required(VERSION 3.18)

project(cppdiycs)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

find_package(cppdiycs PATHS cmake NO_DEFAULT_PATH)

add_subdirectory(cmake)
add_subdirectory(src)