if(WIN32)
    find_program(python_EXECUTABLE NAMES python PATHS $ENV{PATH})
else()
    find_program(python_EXECUTABLE NAMES python3 PATHS $ENV{PATH})
endif()

if(NOT python_EXECUTABLE)
    message(FATAL_ERROR "python executable not found")
endif()

function (castxml_compile)

    cmake_parse_arguments(castxml "" "XML" "SOURCES;INCLUDE_DIRS;TYPES" ${ARGN})

    # check existence of required arguments
    foreach(castxml_ARG_NAME XML;SOURCES;INCLUDE_DIRS)
        if (NOT castxml_${castxml_ARG_NAME})
            message(FATAL_ERROR "Missing argument '${castxml_ARG_NAME}'")
        endif()
    endforeach()

    get_filename_component(castxml_XML ${castxml_XML} DIRECTORY)
    file(MAKE_DIRECTORY ${castxml_XML})

    get_filename_component(castxml_C_COMPILER ${CMAKE_C_COMPILER} ABSOLUTE)
    get_filename_component(castxml_CXX_COMPILER ${CMAKE_CXX_COMPILER} ABSOLUTE)    

    # create castxml command
    list(APPEND castxml_CMD --castxml-output=1)
    if (WIN32)
            list(APPEND castxml_CMD --castxml-cc-msvc)
            list(APPEND castxml_CMD "\"(\"")
            list(APPEND castxml_CMD ${castxml_CXX_COMPILER})
            list(APPEND castxml_CMD /std:c++14)
            list(APPEND castxml_CMD "\")\"")
    else()
            list(APPEND castxml_CMD --castxml-cc-gnu)
            list(APPEND castxml_CMD "\"(\"")
            list(APPEND castxml_CMD ${castxml_CXX_COMPILER})
            list(APPEND castxml_CMD -std=c++14)
            list(APPEND castxml_CMD "\")\"")
    endif()

    list(APPEND castxml_CMD -o)
    list(APPEND castxml_CMD ${castxml_XML})

    # optional types argument
    if(castxml_TYPES)
        string (REGEX REPLACE ";" "," castxml_TYPES "${castxml_TYPES}")
        list(APPEND castxml_CMD --castxml-start)
        list(APPEND castxml_CMD ${castxml_TYPES})
    endif()

    # include directories
    foreach(castxml_INCLUDE_DIR ${castxml_INCLUDE_DIRS})
            get_filename_component(castxml_INCLUDE_DIR ${castxml_INCLUDE_DIR} ABSOLUTE)
            list(APPEND castxml_CMD -I)
            list(APPEND castxml_CMD ${castxml_INCLUDE_DIR})
    endforeach()

    # input sources
    list(APPEND castxml_CMD -x)
    list(APPEND castxml_CMD c++)
            foreach(castxml_SOURCE ${castxml_SOURCES})
            get_filename_component(castxml_SOURCE ${castxml_SOURCE} ABSOLUTE)
            list(APPEND castxml_CMD ${castxml_SOURCE})
    endforeach()

    # disable warnings
    list(APPEND castxml_CMD -Wno-pragma-once-outside-header)

    # compile the sources into an xml
    add_custom_command(OUTPUT ${castxml_XML}
                                        COMMAND ${castxml_EXECUTABLE} ${castxml_CMD}
                                        DEPENDS ${castxml_SOURCES}
                                        USES_TERMINAL)

endfunction()

function (python_transform)

    cmake_parse_arguments(python "" "SCRIPT" "INPUTS;OUTPUTS;ARGS" ${ARGN})

    # check existence of required arguments
    foreach(python_ARG_NAME SCRIPT;INPUTS;OUTPUTS)
        if (NOT python_${python_ARG_NAME})
            message(FATAL_ERROR "Missing argument '${python_ARG_NAME}'")
        endif()
    endforeach()

    get_filename_component(python_SCRIPT ${python_SCRIPT} ABSOLUTE)

    # create python command
    list(APPEND Python_CMD ${python_SCRIPT})

    # forward additional arguments
    if(python_ARGS)
        foreach(python_ARG ${python_ARGS})
            list(APPEND Python_CMD ${python_ARG})
        endforeach()
    endif()

    get_filename_component(python_UTIL_SCRIPT_DIR ${cppdiycs_DIR}/scripts ABSOLUTE)

    # transform the xml into c++ code
    add_custom_command(OUTPUT ${python_OUTPUTS}
                       COMMAND ${CMAKE_COMMAND} -E env PYTHONPATH=${python_UTIL_SCRIPT_DIR} ${python_EXECUTABLE} ${Python_CMD}
                       DEPENDS ${python_INPUTS}
                       USES_TERMINAL)
endfunction()
