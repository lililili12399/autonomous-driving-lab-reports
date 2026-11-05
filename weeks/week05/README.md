# Week 5：深度图转二维激光数据

## 本周目标

使用 rosbag 回放深度相机数据，通过 `depthimage_to_laserscan` 生成 `/scan`，在 RViz 中显示 LaserScan，并通过参数调整改善数据稳定性和有效范围。

## 目录内容

- [实验报告](team4_李响_week5_final.md)：数据回放、转换、可视化和排错过程
- [任务要求](task_requirement.pdf)：课程任务原文件，仅用于说明实验背景
- [参数配置说明](参数配置说明.txt)：实验中使用的关键参数记录
- `images/` 与 `rviz截图.jpeg`：rosbag、话题、RQT、RViz 和 LaserScan 截图

## 复现重点

1. 检查 rosbag 文件是否可读并确认深度图话题。
2. 启动深度图转 LaserScan 节点。
3. 使用 `rostopic` 检查 `/scan` 类型、数据与频率。
4. 在 RViz 中设置正确的 Fixed Frame。
5. 对扫描高度、角度和距离参数进行调整与对比。

本目录没有包含原始 rosbag 数据集。复现时需自行准备具有匹配深度图与相机信息话题的数据，并根据实际话题名称修改配置。

## 许可说明

本人原创报告与参数说明按 [CC BY 4.0](../../LICENSE) 许可。数据集、课程任务和第三方软件界面不纳入本人授权。
