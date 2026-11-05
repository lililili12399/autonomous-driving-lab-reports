# Week 3：ROS 通信、Launch、TF 与仿真工具

## 本周目标

进一步理解 ROS Publisher/Subscriber 通信，使用命名空间和 Launch 管理多节点系统，建立乌龟跟随与 TF 关系，并在 RViz 和 Gazebo 中观察坐标系与模型。

## 目录内容

- [实验报告](team4_李响_week3_final.md)：五项实验的完整过程与排错记录
- [任务要求](task_requirement.pdf)：课程任务原文件，仅用于说明实验背景
- [跟随节点](follower_node.py)：乌龟跟随控制实验代码
- [Launch 文件](turtle_follower.launch)：多节点、命名空间与 TF 实验入口
- [TF 图（PDF）](frames.pdf) / [TF 图源文件](frames.gv)
- `images/`：ROS 通信、TF、RViz 与 Gazebo 截图

## 复现重点

1. 创建并运行 Publisher 与 Subscriber。
2. 使用 Launch 和 namespace 管理多个 Turtlesim 节点。
3. 生成 TF 树并检查坐标变换关系。
4. 在 RViz 中显示 TF。
5. 启动 Gazebo 并加载基础模型。

运行前需检查脚本执行权限、功能包编译状态和环境变量。若节点重名或 TF 不可见，应先核对 namespace、节点名称与 frame 名称。

## 许可说明

本人原创报告按 [CC BY 4.0](../../LICENSE) 许可；本人原创代码与配置按 [MIT License](../../LICENSE) 许可。第三方软件与课程材料不纳入本人授权。
