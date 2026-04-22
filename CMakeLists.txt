cmake_minimum_required(VERSION 3.8)
project(robot_final)

find_package(ament_cmake REQUIRED)

# Lệnh này copy folder sang thư mục install
install(DIRECTORY
  launch
  urdf
  meshes
  # rviz  <-- thêm vào nếu bạn có thư mục rviz
  DESTINATION share/${PROJECT_NAME}
)
ament_package()
