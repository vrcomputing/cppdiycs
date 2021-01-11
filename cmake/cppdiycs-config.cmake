if(NOT cppdiycs_FOUND)

    find_package(castxml REQUIRED)

    get_filename_component(cppdiycs_DIR "${CMAKE_CURRENT_LIST_DIR}" ABSOLUTE)
    include(${cppdiycs_DIR}/cppdiycs-macros.cmake)
    include(${cppdiycs_DIR}/cppdiycs-targets.cmake)
endif()
set(cppdiycs_FOUND TRUE)
