cmake_minimum_required(VERSION 3.9)
project(mergesorts)

set(CMAKE_CXX_STANDARD 17)
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -W -Wall -O2 -g")

if (NOT CMAKE_BUILD_TYPE)
    message("No build type selected!")
endif()

add_subdirectory(src)



