

file(GLOB ALGOS ./sorts/*)
file(GLOB HEADERS ./*.h)
set(SOURCES ${HEADERS} ${ALGOS})

add_executable(mergesorts main.cpp ${SOURCES})

add_executable(mergesorts-count-cmps main.cpp ${SOURCES})
target_compile_definitions(mergesorts-count-cmps PRIVATE ELEM_T=comp_counter)



add_subdirectory(test)