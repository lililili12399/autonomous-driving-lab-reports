# Week 7：Gazebo 小车与仿真环境建图

## 本周目标

在 Gazebo 中启动带深度相机的移动机器人，将深度图转换为 `/scan`，运行 Gmapping 完成仿真建图，并在 RViz 中验证地图、激光数据和 TF。

## 目录内容

- [实验报告](team4_李响_week7_final.md)：仿真小车、数据转换、建图与排错记录
- [任务要求](task_requirement.pdf)：课程任务原文件，仅用于说明实验背景
- [仿真地图](turtlebot3_gmapping_map.pgm) / [地图元数据](turtlebot3_gmapping_map.yaml)
- [TF 图（PDF）](frames.pdf) / [TF 图源文件](frames.gv)
- `images/` 与 `rviz`：Gazebo、RViz、话题和建图结果

## 复现重点

1. 准备独立 Catkin 工作空间和仿真功能包。
2. 启动带深度相机的 Gazebo 机器人模型。
3. 检查深度图、相机信息和 `/scan` 话题。
4. 启动 Gmapping 与键盘控制，逐步构建地图。
5. 检查 TF 连通性并保存地图。

仿真模型、世界文件和软件包版本会影响话题名与 TF。报告中保留了节点缺失、工作空间冲突和地图异常等实际问题，复现时应结合当前环境调整。

## 许可说明

本人原创报告与实验结果按 [CC BY 4.0](../../LICENSE) 许可。TurtleBot3、Gazebo、课程任务和其他第三方内容不纳入本人授权。
