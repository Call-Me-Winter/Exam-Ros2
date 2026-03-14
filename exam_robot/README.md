# Exam Robot

## Архитектура системы
Система состоит из четырёх пользовательских узлов и одного стандартного:
- `battery_node` – публикует уровень заряда батареи (/battery_level, 1 Гц).
- `distance_sensor` – публикует расстояние до препятствия (/distance, 5 Гц) на основе скорости /cmd_vel.
- `status_display` – вычисляет статус робота (/robot_status, 2 Гц) по батарее и расстоянию.
- `robot_controller` – управляет движением (/cmd_vel, 10 Гц) согласно статусу.
- `robot_state_publisher` – публикует TF и robot_description из URDF.

### Топики и связи
![Граф узлов](docs/graph.png)

## Запуск
```bash
cd ~/ros2_ws
colcon build --packages-select exam_robot
source install/setup.bash
ros2 launch exam_robot robot_system.launch.py