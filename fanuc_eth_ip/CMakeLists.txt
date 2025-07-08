cmake_minimum_required(VERSION 3.8)
project(fanuc_eth_ip)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(EIPScanner REQUIRED)

find_package(rcpputils REQUIRED)

include_directories(${EIPScanner_INCLUDE_DIRS})
include_directories(${EIPScanner_INCLUDE_DIRS}/EIPScanner)
include_directories(include)


set(HW_IF_INCLUDE_DEPENDS
  rcpputils
  rclcpp
)

add_library(fanuc_eth_ip SHARED  src/fanuc_eth_ip.cpp)

target_link_libraries(fanuc_eth_ip EIPScanner)
target_include_directories(fanuc_eth_ip
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<BUILD_INTERFACE:${EIPScanner_INCLUDE_DIRS}>
    $<BUILD_INTERFACE:${EIPScanner_INCLUDE_DIRS}/EIPScanner>
    $<INSTALL_INTERFACE:include>
)

install(
  DIRECTORY include/
  DESTINATION include/
)

install(
  TARGETS fanuc_eth_ip
  EXPORT fanuc_eth_ip
  RUNTIME DESTINATION bin
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  INCLUDES DESTINATION include
)
ament_export_libraries(fanuc_eth_ip)
ament_export_include_directories(
  ${EIPScanner_INCLUDE_DIRS}
  ${EIPScanner_INCLUDE_DIRS}/EIPScanner
)

ament_export_targets(fanuc_eth_ip HAS_LIBRARY_TARGET)
ament_export_dependencies(${THIS_PACKAGE_INCLUDE_DEPENDS})
ament_export_dependencies(EIPScanner)


ament_package()
