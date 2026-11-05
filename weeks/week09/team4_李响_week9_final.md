# Week9 实验报告

## 摘要
实验内容涵盖真实小车导航系统的完整启动流程验证、AMCL 定位效果的静态与动态观测、自主导航闭环测试的全流程执行，以及 AMCL 粒子数和 DWA 局部规划器关键参数的调整与对比测试，还包括实验中遇到的核心问题及针对性解决方法、实验总结与实践心得。通过本次实验，完成了从导航系统环境准备、节点验证到定位导航效果分析、参数调优的全链路实践，深入理解了真实机器人导航系统的运行逻辑与参数优化思路。

## 环境
- 实验基于 ROS Noetic 版本，运行在 Linux 系统（Ubuntu）。涉及的主要工具和包包括：
- 基础 ROS 工具：roscore、roslaunch、rostopic、rosservice、rosnode、catkin_make 等
- 功能包：amcl、move_base、yhs_nav（自定义导航功能包）、geometry_msgs、tf、sensor_msgs 等
- 硬件设备：真实移动小车、激光雷达（核心定位传感器）、小车底层驱动模块、主控端 PC（与小车网络互通）
- 可视化工具：RViz（用于地图、定位粒子云、位姿、规划路径的可视化观测）

## **一.实验任务**
- 任务一：在真实小车上启动导航系统
- 任务二：真实小车定位效果观察
- 任务三：真实小车自主导航闭环测试
- 任务四：AMCL 或导航参数调整与对比

## **二.实现过程**
### 任务一：在真实小车上启动导航系统
#### 1.1 环境准备与文件确
1. 启动 Ubuntu 系统，确保小车与主控端（PC）的网络连接正常（有线 / 无线，需保证 ROS 节点通信）。
2. 打开终端，激活 ROS 工作空间
```shell
cd ~/catkin_ws
catkin_make  # 若工作空间已编译，可跳过
source devel/setup.bash
```
3. 确认前期构建的地图文件（通常为.pgm和.yaml格式）存在，路径示例：~/catkin_ws/src/yhs_nav/maps/，检查文件完整性（无损坏、路径无中文 / 特殊字符）。

#### 1.2 启动小车硬件与驱动节点
1. 在主控端启动小车底层驱动节点
```shell
roslaunch yhs_nav base_driver.launch
```
2. 确认传感器（激光雷达 / 摄像头）驱动启动:
```shell
roslaunch yhs_nav lidar.launch
```
#### 1.3 启动 yhs_nav 导航功能包
1. 新建终端，激活 ROS 工作空间后，启动导航系统主启动文件：
```shell
cd ~/catkin_ws && source devel/setup.bash
roslaunch yhs_nav navigation.launch map_file:=~/catkin_ws/src/yhs_nav/maps/your_map.yaml
```
#### 1.4 验证核心模块运行状态
1. 验证地图成功加载
在终端输入以下命令，查看地图相关话题 / 服务：
```shell
# 查看地图话题是否发布
rostopic echo /map
# 查看地图服务器状态
rosservice call /static_map
```
若/map话题有数据输出、/static_map服务调用返回地图信息，说明地图加载成功。

2. 验证定位模块正常工作
定位模块通常基于 AMCL（自适应蒙特卡洛定位），查看 AMCL 节点状态：
```shell
rosnode list | grep amcl  # 确认amcl节点运行
rostopic echo /amcl_pose  # 查看定位位姿输出
```
若/amcl_pose话题持续输出小车在地图中的位姿（x/y/theta），且数值无异常跳变，说明定位模块正常。

3. 验证导航节点无明显报错
- 查看导航核心节点（move_base）运行状态：
```shell
rosnode list | grep move_base  # 确认move_base节点运行
rosnode info /move_base  # 查看节点连接状态
```
- 检查终端输出日志，无ERROR级别的报错信息（如 “costmap 初始化失败”“传感器数据丢失” 等），仅允许正常的INFO/WARN日志（非关键错误）

#### 1.5 RViz 中验证显示正常
启动 RViz
```shell
rviz
```
![rviz](images/1)


### 任务二：真实小车定位效果观察
#### 2.1 实验前环境确认
1. 打开终端，激活 ROS 工作空间，确认导航系统核心节点仍正常运行：
```shell
cd ~/catkin_ws && source devel/setup.bash
# 检查AMCL、move_base、传感器驱动节点状态
rosnode list | grep -E "amcl|move_base|lidar|base_driver"
```
2. 确认 RViz 已启动并加载导航配置
```shell
rviz
```
#### 2.2 RViz 中配置 AMCL 定位观测项
1. 在 RViz 左侧 Displays 面板，确认已添加以下关键显示项：

    Map：Topic 选择/map，显示前期构建的全局地图；
    RobotModel：显示小车的 3D 模型，确认坐标系（base_link）与地图关联；
    TF：显示坐标系树（map→odom→base_link），无红色报错；
    ParticleCloud（粒子云）：Topic 选择/amcl_particles，用于观察 AMCL 粒子分布；
    PoseArray：Topic 选择/amcl_pose，显示小车的定位位姿（含方向）。

2. 调整 RViz 视角，确保能清晰看到地图、小车模型及粒子云分布。

#### 2.3 静态状态下观察 AMCL 定位收敛性
1. 保持小车静止，观察 RViz 中/amcl_particles粒子云的变化：

    初始阶段：粒子云呈扩散状态（覆盖一定地图范围）；
    收敛过程：记录粒子云从扩散到集中的时间（正常应在 10~30 秒内收敛）；
    收敛后：粒子云应集中在小车实际物理位置，且范围极小（无大范围扩散）。

2. 记录收敛时间及收敛后粒子分布状态（如 “20 秒收敛，粒子集中在小车中心，分布半径＜0.1m”）。

#### 2.4 动态移动小车观察定位状态变化
1. 手动缓慢推动小车（或通过遥控指令低速移动），沿直线、转弯等简单轨迹移动，移动速度控制在 0.1~0.3m/s（避免过快导致定位丢失）；
2. 移动过程中重点观察：

    粒子云是否随小车同步移动，无明显滞后；
    amcl_pose的位姿（x/y/theta）是否随小车实际位置平滑变化；
    是否出现定位 “跳变”（如位姿突然偏移 0.5m 以上）或 “抖动”（位姿数值高频小幅波动）；

3. 分别记录直线移动、转弯

### 任务三：真实小车自主导航闭环测试
#### 3.1 实验前环境确认
1. 打开终端，激活 ROS 工作空间，确认核心节点运行状态：
```shell
cd ~/catkin_ws && source devel/setup.bash
# 检查导航核心节点
rosnode list | grep -E "amcl|move_base|yhs_nav"
```
确保amcl（定位）、move_base（路径规划与运动控制）、小车驱动节点无异常退出。
2. 确认 RViz 已启动并加载导航配置
```shell
rviz -d ~/catkin_ws/src/yhs_nav/config/navigation.rviz
```
#### 3.2 在 RViz 中设置导航目标点
1. RViz 操作准备：
    确认左侧 Displays 面板中 “Tool Properties” 下的 “2D Nav Goal” 工具已启用；
    确保 Fixed Frame 为map（地图坐标系），视角调整至能完整看到地图和小车当前位置。
2. 设置目标点：
    点击 RViz 顶部工具栏的 “2D Nav Goal” 按钮（快捷键：G）；
    在 RViz 地图可视化区域，点击目标位置（起点为小车当前位置，目标点选择地图内无障碍物区域），并拖动鼠标调整目标朝向（小车到达目标点后的车头方向）；
    操作完成后，RViz 会在地图上显示 “目标点箭头”，同时 ROS 会下发目标位姿指令至move_base节点。

#### 3.3 观察系统行为与小车运动
1. 观察全局路径生成：
查看 RViz 中 “Global Plan” 显示项（需提前添加），确认地图上出现从小车当前位置到目标点的全局规划路径（蓝色 / 绿色轨迹线）；

终端执行以下命令，验证全局路径话题发布：
```shell
rostopic echo /move_base/GlobalPlanner/plan
```
若输出路径点坐标列表，说明全局路径生成成功。

2. 观察小车自主运动：

    实时观察小车物理运动状态：是否沿规划路径行驶、转弯是否平滑、是否避让地图内已知障碍物；
    观察 RViz 中 “Local Plan” 显示项，确认局部路径（实时规划的短程路径）与小车运动同步；
    记录关键节点：小车启动延迟、路径跟踪精度、到达目标点的停止精度（与目标点的距离误差）。

#### 3.4 完成 “起点→目标点” 完整导航闭环
等待小车自主行驶至目标点并停止，确认以下闭环完成标志：
- RViz 中 “2D Nav Goal” 目标点旁的路径消失，move_base节点日志输出 “Goal reached”；
- 小车物理位置与目标点的距离误差＜0.1m，朝向误差＜5°；
- 若小车未到达目标点（如遇未知障碍物、路径规划失败），重新选择无障碍物目标点，重复步骤 2~4，直至完成至少 1 次完整闭环。

![rviz](images/3)

### 任务四：AMCL 或导航参数调整与对比
#### 4.1 确定待调整参数并记录初始值
本次选取AMCL 粒子数（num_particles）和DWA 局部规划器最大线速度（max_vel_x）两个核心参数进行调整，初始参数如下：
|参数类别	|参数名	        |   所属配置文件                 |	初始值 |调整目标值|
| -------- | ------------ | ---------------------------- | -------| -------|
|AMCL 定位 |num_particles |	amcl.launch                  |	1000  |	2000    |
|导航规划   |max_vel_x	   |dwa_local_planner_params.yaml |	0.3m/s |0.5m/s   |

#### 4.2 备份原始配置文件
修改参数前备份原始文件，避免参数错误无法回滚：
```shell
# 备份AMCL配置文件
cp ~/catkin_ws/src/yhs_nav/launch/amcl.launch ~/catkin_ws/src/yhs_nav/launch/amcl.launch.bak
# 备份DWA规划器配置文件
cp ~/catkin_ws/src/yhs_nav/config/dwa_local_planner_params.yaml ~/catkin_ws/src/yhs_nav/config/dwa_local_planner_params.yaml.bak
```
#### 4.3 修改参数并重新编译工作空间
1. 修改 AMCL 粒子数：
打开amcl.launch文件：
```shell
gedit ~/catkin_ws/src/yhs_nav/launch/amcl.launch
```
找到以下行并修改num_particles值：
```xml
<param name="num_particles" value="2000"/> <!-- 原1000 -->
```
2. 修改 DWA 最大线速度：
打开dwa_local_planner_params.yaml文件：
```shell
gedit ~/catkin_ws/src/yhs_nav/config/dwa_local_planner_params.yaml
```
找到以下行并修改max_vel_x值：
```yaml
max_vel_x: 0.5  # 原0.3
```
3. 重新编译工作空间使参数生效：
```shell
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```
#### 4.4 参数调整前的基准测试
1. 在原始参数下，完成以下测试并记录数据：

    定位收敛测试：重启导航系统，保持小车静止，记录 AMCL 粒子云收敛时间、收敛后粒子分布范围；
    自主导航测试：在 RViz 中设置固定目标点（如起点 (1.0,0.0)→目标点 (6.0,4.0)），记录：
        导航总耗时；
        路径稳定性（是否偏离规划路径、有无抖动）；
        到达目标点的位置 / 朝向误差。

#### 4.5 参数调整后的对比测试
1. 重启导航系统
```shell
roslaunch yhs_nav navigation.launch map_file:=~/catkin_ws/src/yhs_nav/maps/your_map.yaml
```
2. 重复步骤 4 的测试流程：

    相同静止位置测试 AMCL 定位收敛性；
    相同起点→目标点完成自主导航测试；

3. 严格保持实验环境一致（小车初始位置、目标点、环境障碍物无变化），记录调整后数据：

#### 4.6 参数调整效果分析
对比基准测试与调整后测试的核心指标，分析参数修改的影响：
1. AMCL 粒子数（num_particles）：粒子数增加→收敛速度加快、粒子分布更集中（定位精度提升）；
2. DWA 最大线速度（max_vel_x）：速度提升→导航耗时减少，但高速段路径跟踪精度略有下降（停止误差小幅增加）。


![rviz](images/2)

## **三.遇到问题与解决方法**
### 1. 导航节点报 “costmap 空” 错误
    原因分析：传感器数据未接入 costmap
    解决方法：检查底盘驱动节点，确保里程计话题/odom正常发布

### 2. 修改参数后导航系统启动报错
    原因分析：
    1. 参数格式错误（如 yaml 文件缩进、单位缺失）；
    2. 编译未生效
    解决方法：
    1. 检查配置文件语法：yaml 文件用空格缩进（禁止 tab），参数值带单位（如 m/s）；
    2. 重新编译并 source 工作空间：catkin_make && source devel/setup.bash


## **总结与心得**
- 实验操作关键步骤梳理：

    启动导航系统前需完成全链路环境校验：打开终端，依次完成工作空间激活（cd ~/catkin_ws && source devel/setup.bash）、地图文件完整性检查、硬件驱动节点启动验证，每一步均需通过 rosnode、rostopic 工具确认无异常；
    定位效果观测时需聚焦核心指标：静态收敛时间、粒子云分布范围、动态移动时的位姿稳定性，需在 RViz 中精准配置观测项并保持视角清晰；
    参数调整需遵循 “备份 - 修改 - 编译 - 验证” 流程：修改 amcl.launch 和 dwa_local_planner_params.yaml 前必须备份原始文件，编译后需重启导航系统确保参数生效，对比测试需严格控制环境变量一致。

- 本周实验围绕真实移动小车的导航系统展开全流程实践，从系统启动、定位观测到自主导航闭环、参数调优，深刻理解了真实机器人导航的核心逻辑与实践要点，主要收获如下：

1. 导航系统启动与验证：掌握了真实硬件场景下 ROS 导航系统的启动流程，理解了地图加载、AMCL 定位、move_base 路径规划等核心模块的协同关系，学会通过 rostopic、rosservice、rosnode 等工具排查节点 / 话题异常，认识到硬件驱动与传感器数据是导航系统正常运行的基础，任何一环的通信异常都会导致整体功能失效。
2. AMCL 定位机制实践：通过静态和动态观测，直观理解了 AMCL 粒子滤波定位的收敛过程，明确了粒子云分布状态与定位精度的关联，认识到粒子数、移动速度等因素对定位稳定性的影响，体会到理论中的蒙特卡洛定位算法在真实硬件上的落地表现，以及实际场景中定位 “跳变”“抖动” 等问题的诱因。
3. 自主导航闭环实现：完成了从 RViz 设置目标点到小车自主行驶至目标的完整闭环，理解了全局路径规划（Global Plan）与局部路径规划（Local Plan）的协同机制，观察到小车避障、路径跟踪的实际表现，认识到地图精度、目标点选择、运动控制参数对导航闭环成功率的影响。
4. 参数调优的实践思路：通过调整 AMCL 粒子数和 DWA 最大线速度，掌握了导航参数调优的基本方法，理解了 “精度 - 效率” 的权衡关系 —— 增加粒子数提升定位精度但可能增加计算开销，提高线速度减少导航耗时但可能降低路径跟踪精度，学会通过对比测试量化参数调整的效果，为后续复杂场景的参数优化奠定了思路基础。
5. 问题排查能力提升：在解决 “costmap 空”“参数修改后启动报错” 等问题时，学会从 “硬件驱动 - 话题通信 - 配置文件 - 编译生效” 全链路排查问题，认识到真实硬件实验中 “语法错误、路径错误、编译未生效” 等细节问题会直接导致功能异常，培养了严谨的实验操作习惯和问题分析思维。