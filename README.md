# ROS 移动机器人 SLAM 与自主导航实践

本仓库整理了 10 周移动机器人实践项目，内容覆盖 Ubuntu/ROS 基础、Turtlesim、TF、URDF、深度图转激光、Gmapping 建图，以及真实小车定位与自主导航。

> 当前状态：Week 1–10 已整理到本地候选仓库，尚未提交或推送 GitHub。任务要求、本人 final report、配套图片及代码/配置按周归档。

## 内容索引

| 周次 | 主题 | 当前状态 |
| --- | --- | --- |
| [Week 1](weeks/week01/team4_李响_week1_final.md) | Ubuntu 双系统、VS Code、Git 与 Markdown | 已纳入候选版 |
| [Week 2](weeks/week02/team_李响_week2_final.md) | Linux、Python/C++、ROS1、Catkin 与 Turtlesim | 已纳入候选版 |
| [Week 3](weeks/week03/team4_李响_week3_final.md) | ROS 通信、Launch、TF、RViz 与 Gazebo | 已纳入候选版 |
| [Week 4](weeks/week04/team4_李响_week4_final.md) | URDF 两轮小车、robot_state_publisher 与 TF | 已纳入候选版 |
| [Week 5](weeks/week05/team4_李响_week5_final.md) | rosbag、depthimage_to_laserscan 与参数调整 | 已纳入候选版 |
| [Week 6](weeks/week06/team4_李响_week6_final.md) | Gmapping 编译、数据集建图与地图保存 | 已纳入候选版 |
| [Week 7](weeks/week07/team4_李响_week7_final.md) | Gazebo 小车、深度转激光与仿真建图 | 已纳入候选版 |
| [Week 8](weeks/week08/README.md) | 真实小车、深度相机与实时建图 | 已纳入候选版 |
| [Week 9](weeks/week09/README.md) | 真实小车定位、导航与参数对比 | 已纳入候选版 |
| [Week 10](weeks/week10/README.md) | 项目汇总、操作手册与汇报材料 | 已纳入候选版 |

## 目录结构

```text
.
├── README.md
├── .gitignore
├── LICENSE_REVIEW.md
├── PUBLICATION_REVIEW.md
└── weeks/
    ├── week01/ ... week09/   # 任务要求、final 报告、图片和代码/配置
    └── week10/               # 项目手册、图片、PDF 与汇报材料
```

## 环境说明

报告所用环境以 Ubuntu 20.04、ROS Noetic、RViz、Gazebo 和 Catkin 为主。不同周次的依赖与操作步骤以对应报告为准。本仓库未创建 Dockerfile：现有项目包含 GUI、ROS 主机配置、仿真和真实硬件驱动，当前材料不足以构建经过验证的统一容器环境。

## 使用说明

本仓库以学习记录和实验复盘为主，并非开箱即用的软件发行包。运行代码前，请先核对对应报告中的 ROS 版本、功能包依赖、工作空间路径和硬件条件。

## 公开范围

本候选版包含 Week 1–9 的任务要求原文件和 Week 1–10 的本人项目成果。任务书未见保密或禁止传播标记，但其原文著作权仍归原作者或课程组织方；若仓库设为公开，应保留来源并按课程要求处理。组员汇总、重复 ZIP 和根目录中的重复副本未纳入。完整审查记录见 [PUBLICATION_REVIEW.md](PUBLICATION_REVIEW.md)。

## 许可证

当前不设置仓库级开源许可证。仓库同时包含个人报告、自写代码和可能受第三方权利约束的材料，必须先确认权属和公开许可。建议方案见 [LICENSE_REVIEW.md](LICENSE_REVIEW.md)。

