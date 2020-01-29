cmake_minimum_required(VERSION 3.16)

project(RSA VERSION 1.0.0)

set (CMAKE_CXX_FLAGS "-lgmp -lgmpxx -I/usr/include/python3.8")

add_library(rsa SHARED
    src/rsa.cpp
    src/rsamodule.cpp
)

set_target_properties(rsa PROPERTIES VERSION ${PROJECT_VERSION})
set_target_properties(rsa PROPERTIES SOVERSION 1)
target_include_directories(rsa PRIVATE include)
