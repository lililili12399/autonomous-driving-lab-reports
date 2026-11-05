# Week 4：URDF 两轮小车与 TF 发布

## 本周目标

使用 URDF 建立最小两轮小车模型，通过 `robot_state_publisher` 发布机器人坐标变换，并在 RViz 中验证模型结构和 TF 关系。

## 目录内容

- [实验报告](team4_李响_week4_final.md)：建模、发布和 RViz 验证过程
- [任务要求](task_requirement.pdf)：课程任务原文件，仅用于说明实验背景
- [URDF 模型](two_wheeled_car.urdf)：两轮小车机器人描述
- [Launch 文件](car_tf.launch)：模型加载与 TF 发布入口
- `images/`：URDF 模型、RViz 与 TF 验证截图

## 复现重点

1. 定义车体、车轮及其几何与连接关系。
2. 检查 link、joint、parent、child 和 origin 配置。
3. 启动 `robot_state_publisher` 与相关节点。
4. 在 RViz 中设置正确的 Fixed Frame 并检查模型和 TF。

本模型用于学习 URDF 与 TF 基础，不代表真实车辆的精确尺寸、动力学或控制系统。

## 许可说明

本人原创报告按 [CC BY 4.0](../../LICENSE) 许可；本人原创 URDF 与 Launch 配置按 [MIT License](../../LICENSE) 许可。第三方材料不纳入本人授权。
