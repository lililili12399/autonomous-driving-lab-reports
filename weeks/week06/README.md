# Week 6：Gmapping 建图与地图保存

## 本周目标

在 Catkin 工作空间中准备 Gmapping，使用 `/scan` 数据和 TF 运行二维 SLAM，完成室内环境建图，并保存和验证 PGM/YAML 地图文件。

## 目录内容

- [实验报告](team4_李响_week6_final.md)：Gmapping 编译、建图、保存与排错过程
- [任务要求](task_requirement.pdf)：课程任务原文件，仅用于说明实验背景
- [地图图像](indoor_map.pgm) / [地图元数据](indoor_map.yaml)
- `images/` 及根目录结果截图：LaserScan、地图和叠加效果记录

## 复现重点

1. 安装或编译 Gmapping 及相关依赖。
2. 确认 `/scan` 数据能够正常发布。
3. 建立 `odom → base_link → laser` 的有效 TF 链。
4. 启动 Gmapping，在 RViz 中观察地图更新。
5. 使用 map server 工具保存并重新加载地图。

现有地图是特定实验数据和参数下的结果，只用于复现记录，不是通用导航地图。地图的原点、分辨率与占用阈值以 YAML 文件为准。

## 许可说明

本人原创报告与实验结果按 [CC BY 4.0](../../LICENSE) 许可。Gmapping、数据来源、课程任务和其他第三方内容仍受各自条款约束。
