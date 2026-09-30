cmake_minimum_required(VERSION 3.10)
project(td2port C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

find_package(SDL2 REQUIRED)

file(GLOB_RECURSE TD_SOURCES CONFIGURE_DEPENDS src/*.c)

add_executable(td2port ${TD_SOURCES})
target_include_directories(td2port PRIVATE src ${SDL2_INCLUDE_DIRS})
target_link_libraries(td2port PRIVATE ${SDL2_LIBRARIES})
if(MSVC)
    target_compile_options(td2port PRIVATE /W3)
else()
    target_compile_options(td2port PRIVATE -Wall -Wextra -Wno-unused-parameter -fno-strict-aliasing)
    if(CMAKE_C_COMPILER_ID STREQUAL "GNU")
        target_compile_options(td2port PRIVATE -Wno-format-truncation)
    endif()
endif()
if(WIN32)
    add_custom_command(TARGET td2port POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_RUNTIME_DLLS:td2port> $<TARGET_FILE_DIR:td2port>
        COMMAND_EXPAND_LISTS)
endif()
