# ROS 移动机器人 SLAM 与自主导航：10 周实验复现记录

本仓库记录了我在 2025 年 12 月至 2026 年 2 月完成的一组 ROS 移动机器人实验。内容从 Ubuntu、Git、ROS 基础与 Turtlesim 开始，逐步进入 TF、URDF、深度图转二维激光、Gmapping 建图，并最终在真实移动机器人上完成定位与自主导航。

这是个人学习、实验复现与问题排查记录，不是实验室官方仓库，也不是可直接部署的完整产品。仓库保留了每周报告、关键代码与配置、运行截图、地图结果及必要的任务背景，便于理解完整的实验推进过程。

## 项目概览

| 周次 | 主要内容 | 入口 |
| --- | --- | --- |
| Week 1 | Ubuntu 双系统、VS Code、Git 与 Markdown | [查看](weeks/week01/README.md) |
| Week 2 | Linux、Python/C++、ROS1、Catkin 与 Turtlesim | [查看](weeks/week02/README.md) |
| Week 3 | ROS 通信、Launch、TF、RViz 与 Gazebo | [查看](weeks/week03/README.md) |
| Week 4 | URDF 两轮小车与 TF 发布 | [查看](weeks/week04/README.md) |
| Week 5 | rosbag、深度图转 LaserScan 与参数调整 | [查看](weeks/week05/README.md) |
| Week 6 | Gmapping 编译、数据集建图与地图保存 | [查看](weeks/week06/README.md) |
| Week 7 | Gazebo 小车、深度转激光与仿真建图 | [查看](weeks/week07/README.md) |
| Week 8 | 真实小车驱动、传感器检查与实时建图 | [查看](weeks/week08/README.md) |
| Week 9 | AMCL 定位、Move Base 导航与参数对比 | [查看](weeks/week09/README.md) |
| Week 10 | 系统操作手册、结果整理与项目总结 | [查看](weeks/week10/README.md) |

## 技术路线

```text
基础环境与工具
  → ROS 节点、话题、Launch 与 TF
  → URDF 机器人模型与 RViz 可视化
  → 深度图转换为二维 LaserScan
  → Gmapping 建图与地图保存
  → 仿真环境完整验证
  → 真实移动机器人建图
  → AMCL 定位与 Move Base 自主导航
```

## 主要环境

- Ubuntu 20.04
- ROS Noetic
- Catkin 工作空间
- RViz 与 Gazebo
- `depthimage_to_laserscan`
- Gmapping、AMCL 与 Move Base
- 深度相机和真实移动机器人（Week 8–9）

具体软件包、参数和硬件条件以各周报告为准。不同 ROS 工作空间、设备驱动和网络配置可能需要调整路径、话题名与 Launch 参数。

## 仓库结构

```text
.
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── PUBLICATION_REVIEW.md
└── weeks/
    ├── week01/ ... week09/
    │   ├── README.md
    │   ├── task_requirement.pdf
    │   ├── *final.md
    │   ├── images/
    │   └── 代码、配置或实验结果
    └── week10/
        ├── README.md
        ├── Week10_实操手册_李响.md
        ├── Week10_实操手册_李响.pdf
        ├── Week10_项目汇报_李响.pptx
        └── images/
```

## 如何使用本仓库复现

1. 先阅读目标周次的 `README.md`，确认该周的目标、依赖和文件入口。
2. 阅读对应的 final report，按报告中的环境和命令准备 ROS 工作空间。
3. 仿真实验优先在隔离的 Catkin 工作空间中执行，避免与已有功能包冲突。
4. 涉及真实硬件时，先确认设备型号、驱动、网络连接、急停状态和话题名称。
5. 使用 `rostopic`、`rosnode`、TF 与 RViz 逐层验证数据链路，再启动建图或导航。
6. 报告中的路径和参数来自当时的实验环境，复现时应替换为本机实际配置。

建议按 Week 1 到 Week 10 的顺序学习；如果已有 ROS 基础，可以从 Week 5 或 Week 6 开始查看建图部分。

## 复现范围与限制

- 仓库提供学习过程和关键实验材料，但不保证在所有设备或 ROS 环境中直接运行。
- Week 8–9 依赖真实移动机器人与深度相机，缺少对应硬件时只能复现软件流程或仿真部分。
- 截图与地图用于记录当时的实验结果，不构成通用数据集。
- 报告保留了实际遇到的问题与解决过程；个别命令可能需要根据软件版本更新。
- 本仓库未提供 Dockerfile，因为 GUI、ROS 网络、硬件驱动和真实设备接口尚未形成经过验证的统一容器环境。

## 内容来源与权利边界

- final report、本人编写的说明、原创代码和配置由李响在 2025–2026 年整理完成。
- `task_requirement.pdf` 等课程任务材料用于说明实验背景，不是本人原创。
- ROS、Gazebo、RViz、Gmapping、厂商软件界面、商标以及可能出现的第三方代码或素材，权利归各自权利人。
- 公开本仓库不代表课程组织方、实验室、设备厂商或第三方对本项目进行认可或背书。

详细说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 许可证

Copyright © 2025–2026 李响（Li Xiang）。

- 本人原创的代码与配置采用 [MIT License](https://opensource.org/license/mit) 许可。
- 本人原创的报告、README、操作手册和图片采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可，使用时需要署名、链接许可证并说明是否修改。
- 课程任务、第三方代码、截图、商标和其他非本人原创内容不在上述授权范围内。

完整适用范围见 [LICENSE](LICENSE)。MIT 与 CC BY 4.0 均允许商业使用，但只能授权本人拥有相应权利的原创部分。

## 学术诚信

本仓库可以用于学习和复现，但不应被直接作为他人的课程作业、实验报告或考核成果提交。引用或改编本人原创内容时，请注明作者、仓库链接、许可证以及是否进行了修改。

## 作者

作者：李响（Li Xiang）

实验周期：2025 年 12 月—2026 年 2 月
