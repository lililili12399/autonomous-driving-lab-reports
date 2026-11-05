# Week 2：Linux、编程基础与 ROS1 入门

## 本周目标

练习 Linux 常用命令和 Python/C++ 基础程序，验证 ROS1 环境，创建 Catkin 工作空间与功能包，并通过 Turtlesim、Launch 和 `rqt_graph` 理解 ROS 节点与话题通信。

## 目录内容

- [实验报告](team_李响_week2_final.md)：环境、命令、运行结果与问题处理
- [任务要求](task_requirement.pdf)：课程任务原文件，仅用于说明实验背景
- [多乌龟 Launch 文件](multi_turtle.launch)：启动多个 Turtlesim 节点的实验配置
- `images/`：命令行、编译、Turtlesim 与 ROS 工具截图

## 复现重点

1. 熟悉 Linux 文件、进程和软件包管理命令。
2. 编译并运行基础 Python 与 C++ 程序。
3. 验证 ROS Master、环境变量和常用命令。
4. 创建 Catkin 工作空间与功能包。
5. 使用 Turtlesim、Launch 和 `rqt_graph` 观察多节点通信关系。

报告以 Ubuntu 20.04 与 ROS Noetic 为主要环境。复现时应先确认 `source` 了正确的 ROS 与 Catkin 环境。

## 许可说明

本人原创报告按 [CC BY 4.0](../../LICENSE) 许可；本人原创配置按 [MIT License](../../LICENSE) 许可。任务要求和第三方软件界面不纳入本人授权。
