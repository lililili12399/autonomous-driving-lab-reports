# Week8 实验报告

## 摘要
实验内容涵盖真实小车与 HP60C 深度相机驱动的启动与验证、深度图像到二维激光数据的转换实现与质量校验、基于 Gmapping 算法的实时 SLAM 建图及结果保存、里程计话题与 TF 坐标变换链的完整性检查，还包括实验中各环节的核心验证方法、可视化调试手段，以及建图过程中参数适配、坐标系关联等问题的处理思路。
## 环境
实验基于 ROS Noetic 版本，运行在 Linux 系统。涉及的主要工具和包包括：
- 基础 ROS 工具：roscore、rosrun、roslaunch、rostopic、rosmsg、rviz 等
- 功能包：std_msgs、roscpp、rospy、geometry_msgs、depthimage_to_laserscan、gmapping、map_server、tf2_ros、teleop_twist_keyboard、ascamera_listener（深度相机驱动）、your_car_package（小车驱动）
- 硬件适配：HP60C 深度相机、真实移动小车
- 可视化工具：RViz（用于图像、激光、地图可视化）

## **一.实验任务**
- 任务一：启动真实小车与深度相机驱动
- 任务二：生成二维激光数据并检查质量
- 任务三：运行 Gmapping 并实时建图
- 任务四：里程计与 TF 检查


## **二.实现过程**
### 任务一：启动真实小车与深度相机驱动
#### 1.1 启动小车系统并确认 ROS 环境正常
1.  启动 ROS 核心节点
```shell
roscore
```
2. 启动小车系统
```shell
roslaunch your_car_package car_base.launch
```
3. 验证 ROS 环境
在新终端执行以下命令，检查 ROS 节点是否正常运行：
```shell
rosnode list
```
预期结果：输出包含/rosout（ROS 核心节点），若小车驱动启动成功，还会显示小车相关节点（如/car_base）；无ERROR: Unable to communicate with master!报错。

#### 1.2 启动深度相机驱动节点并验证核心内容
1. 启动深度相机驱动
新开终端，先配置 ROS 工作空间环境（若相机驱动包在自定义工作空间），再启动驱动节点：
```shell
# 进入ROS工作空间（假设为catkin_ws，需替换为实际路径）
cd ~/catkin_ws
# 加载工作空间环境
source devel/setup.bash
# 启动HP60C深度相机驱动
roslaunch ascamera_listener hp60c.launch
```
2. 逐项验证相机数据发布
- RGB 图像话题正常发布,Depth 图像话题正常发布
```shell
rostopic list
```
- RGB 与 Depth 图像对齐正常
    启动rviz
    rviz
    1. 添加 2 个Image显示项；
    2. 分别关联 RGB 和 Depth 话题

#### 1.3 使用命令行工具查看相关话题
```shell
rostopic list
```

#### 1.4 使用可视化工具检查深度图质量
1. 启动 RViz：
```shell
rviz
```
2. 配置深度图显示：

    左侧Displays面板 → 点击Add → 选择Image → 确定；
    选中新增的Image项，Topic选择 Depth 话题（如/ascamera/depth/image_raw）；
    可选：修改Color Transformer为Jet.
![rviz](images/1)


### 任务二：生成二维激光数据并检查质量
#### 2.1 安装并启动深度图到二维激光的转换节点
1. 安装depthimage_to_laserscan功能包
打开终端（Ctrl+Alt+T），执行以下命令安装 ROS 官方深度图转激光包：
```shell
# 更新软件源，避免安装失败
sudo apt-get update
# 安装Noetic版本功能包
sudo apt-get install ros-noetic-depthimage-to-laserscan
```
2. 编写自定义 launch 配置文件
为适配 HP60C 深度相机的参数，创建自定义 launch 文件
```shell
# 进入工作空间src目录，创建自定义包（若无）
cd ~/catkin_ws/src
catkin_create_pkg depth2laser std_msgs rospy roscpp depthimage_to_laserscan
cd depth2laser && mkdir launch && cd launch
# 编辑launch文件
gedit depthimage_to_laserscan.launch
```
```xml
<launch>
  <!-- 深度图转激光核心节点 -->
  <node name="depthimage_to_laserscan" pkg="depthimage_to_laserscan" type="depthimage_to_laserscan_node" output="screen">
    <!-- 输入：深度图话题（与任务一的Depth话题一致） -->
    <param name="depth_image_topic" value="/ascamera/depth/image_raw" />
    <!-- 输出：二维激光话题（标准LaserScan话题名） -->
    <param name="scan_topic" value="/scan" />
    <!-- 激光扫描参数配置 -->
    <param name="range_min" value="0.1" />    <!-- 最小检测距离（米） -->
    <param name="range_max" value="5.0" />    <!-- 最大检测距离（米） -->
    <param name="output_frame_id" value="camera_depth_frame" />  <!-- 激光坐标系 -->
    <param name="scan_height" value="10" />   <!-- 深度图取行数量（激光密度） -->
    <param name="horizontal_fov" value="60.0" /> <!-- 水平视场角（匹配HP60C相机） -->
  </node>
</launch>
```
3. 编译并加载工作空间
```shell
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```
4. 启动转换节点（需先启动前置节点）
启动顺序（关键）：确保任务一的roscore、深度相机驱动已运行，再新开终端执行：

```shell
# 加载工作空间环境
source ~/catkin_ws/devel/setup.bash
# 启动深度图转激光节点
roslaunch depth2laser depthimage_to_laserscan.launch
```

#### 2.2 确认二维激光数据核心内容
1. 验证 LaserScan 话题已生成
在新终端执行以下命令，检查激光话题状态：
```shell
# 1. 查看是否存在/scan话题
rostopic list | grep scan
# 2. 查看话题详细信息（验证消息类型）
rostopic info /scan
# 3. 检查话题发布频率
rostopic hz /scan
```
2. 验证扫描范围合理
```shell
rostopic echo /scan
```
3. 验证无明显跳变或异常点
保持rostopic echo /scan运行，将手缓慢靠近 / 远离相机（0.5~2 米），观察ranges数组数值：

    正常现象：数值随距离平滑变化（如 0.5→0.6→0.7）；
    异常现象：数值突然从 0.5 跳变到 5.0，或大面积出现nan（需调整scan_height/range_min参数）。

#### 2.3 在 RViz 中观察二维激光扫描效果
1. 启动 RViz 并配置可视化
```shell
rviz
```
2. 设置固定坐标系：顶部Fixed Frame选择camera_depth_frame（与激光坐标系一致）；
添加激光显示项：

    左侧Displays → Add → 选择LaserScan → OK；
    选中LaserScan项，Topic选择/scan，Size (m)设为 0.05（激光点更清晰）；
 
    叠加深度图：添加Image显示项，关联/ascamera/depth/image_raw，对比激光与深度图的对应关系。

![rviz](images/2)

### 任务三：运行 Gmapping 并实时建图
#### 3.1 安装并启动 Gmapping SLAM 节点
1. 安装 Gmapping 功能包
打开终端（Ctrl+Alt+T），执行以下命令安装 ROS 官方 Gmapping 包：
```shell
# 更新软件源
sudo apt-get update
# 安装Noetic版本Gmapping包
sudo apt-get install ros-noetic-gmapping
```
2. 编写 Gmapping 自定义 launch 配置文件
为适配小车和激光参数，创建自定义 launch 文件（复用depth2laser包）：
```shell
# 进入launch目录
cd ~/catkin_ws/src/depth2laser/launch
# 编辑Gmapping launch文件
gedit gmapping.launch
```
```xml
<launch>
  <!-- Gmapping SLAM核心节点 -->
  <node name="gmapping" pkg="gmapping" type="slam_gmapping" output="screen">
    <!-- 输入：激光话题（与任务二一致） -->
    <param name="scan_topic" value="/scan" />
    <!-- 坐标系配置 -->
    <param name="odom_frame" value="odom" />        <!-- 里程计坐标系 -->
    <param name="base_frame" value="camera_depth_frame" />  <!-- 激光/小车基坐标系 -->
    <param name="map_frame" value="map" />          <!-- 地图坐标系 -->
    <!-- Gmapping核心参数 -->
    <param name="maxRange" value="5.0" />           <!-- 激光最大有效距离 -->
    <param name="minRange" value="0.1" />           <!-- 激光最小有效距离 -->
    <param name="delta" value="0.05" />             <!-- 地图分辨率（米/像素） -->
    <param name="particles" value="30" />           <!-- 粒子数（平衡精度与性能） -->
    <param name="xmin" value="-10.0" />             <!-- 地图初始X范围 -->
    <param name="ymin" value="-10.0" />             <!-- 地图初始Y范围 -->
    <param name="xmax" value="10.0" />              <!-- 地图初始X范围 -->
    <param name="ymax" value="10.0" />              <!-- 地图初始Y范围 -->
  </node>

  <!-- 静态TF变换（解决坐标系关联问题） -->
  <node name="tf_static" pkg="tf2_ros" type="static_transform_publisher" args="0 0 0 0 0 0 map odom" />
</launch>
```
3. 按顺序启动所有依赖节点
Gmapping 依赖roscore、相机驱动、激光转换、小车里程计，需分终端启动（建议 4 个终端分工）：
```shell
roscore
```
```shell
cd ~/catkin_ws && source devel/setup.bash
roslaunch ascamera_listener hp60c.launch
```
```shell
cd ~/catkin_ws && source devel/setup.bash
roslaunch depth2laser depthimage_to_laserscan.launch
```
```shell
roslaunch your_car_package car_base.launch
```
```shell
cd ~/catkin_ws && source devel/setup.bash
roslaunch depth2laser gmapping.launch
```
#### 3.2 确认 Gmapping 建图核心内容
1. 验证 /map 话题正常发布
```shell
# 1. 查看是否存在/map话题
rostopic list | grep map
# 2. 查看话题消息类型
rostopic info /map
# 3. 检查话题发布频率
rostopic hz /map
```
2. 验证地图随小车运动实时更新
2.1 启动小车键盘控制
```shell
# 安装键盘控制包
sudo apt-get install ros-noetic-teleop-twist-keyboard
# 启动键盘控制节点
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```
2.2 验证地图更新
保持键盘控制终端运行，缓慢移动小车，同时执行：
```shell
# 打印/map话题的栅格数据
rostopic echo /map
```
小车运动时，data数组（地图栅格值）持续变化；小车静止时，data数组基本不变。

#### 3.3 在 RViz 中观察建图效果
1. 启动 RViz 并配置可视化
```shell
rviz
```
设置固定坐标系：顶部Fixed Frame选择map（Gmapping 地图坐标系）；
添加地图显示项：

    左侧Displays → Add → 选择Map → OK；
    选中Map项，Topic选择/map，Color Scheme设为Occupancy Grid；

    添加LaserScan项，Topic选/scan（观察激光与地图匹配）；
    添加RobotModel项（显示小车位姿）。

2. 保存建图结果
```shell
# 创建地图保存目录
mkdir -p ~/catkin_ws/map
# 保存地图
rosrun map_server map_saver -f ~/catkin_ws/map/my_gmapping_map
```

![rviz](images/4)
![rviz](images/5)

### 任务四：里程计与 TF 检查
#### 4.1 确认 /odom 话题正常发布
1. 检查话题是否存在
```shell
# 查看是否存在/odom话题
rostopic list | grep odom
```
2. 验证话题消息类型与发布频率
```shell
# 查看/odom话题的消息类型
rostopic info /odom
# 检查话题发布频率
rostopic hz /odom
```
3. 查看里程计具体数据
```shell
# 打印/odom话题的实时数据
rostopic echo /odom
```
#### 4.2 确认 TF 链完整（odom → base_link → camera_link）
1. 检查 TF 变换关系
```shell
# 列出当前所有TF变换
rosrun tf tf_echo odom base_link
rosrun tf tf_echo base_link camera_link
```
2. 验证 TF 链无断裂
检查TF链是否完整
```shell
rosrun tf view_frames
```
#### 4.3 生成并查看 TF 树
1.  生成 TF 树文件
```shell
# 打开生成的TF树PDF文件
evince frames.pdf
```
![rqt](images/3)


### 五.简要实验说明
1. 深度图质量情况：

    本次实验使用 HP60C 深度相机采集深度图，经 RViz 可视化验证，深度图整体质量良好，图像无明显噪点，近处（0.1~3 米）物体的深度信息准确，远处（3~5 米）深度值略有波动但在可接受范围，RGB 图像与 Depth 图像对齐正常，无明显偏移。

2. 是否存在地面误测或激光跳变：

    通过rostopic echo /scan和 RViz 激光可视化检查，激光数据无明显跳变现象，物体距离变化时 ranges 数组数值平滑过渡；地面误测情况轻微，仅在相机高度贴近地面（<0.3 米）时出现少量地面反射点误判，通过调整scan_height=10和range_min=0.1参数后，误测点显著减少，不影响建图效果。



## **三.遇到问题与解决方法**
### 1. 深度图转激光后 /scan 话题存在但无数据

    原因分析：深度图话题与转换节点配置的输入话题不匹配，或参数设置不合理。
    解决方法：使用rostopic list确认深度图话题名称，修改 launch 文件中depth_image_topic参数；调整range_min和range_max参数，确保检测范围内有物体；增大scan_height参数提高激光数据密度。

### 2. 启动 Gmapping 后无 /map 话题输出

    原因分析：Gmapping 未订阅到 /scan 话题，或 TF 变换链断裂。
    解决方法：使用rqt_graph查看话题订阅关系，确认 /scan 话题正常发布；检查 TF 变换链odom→base_link→camera_depth_frame是否完整，通过rosrun tf tf_echo验证各坐标系变换关系；在 Gmapping launch 文件中添加静态 TF 变换节点，关联 map 与 odom 坐标系。

### 3. tf view_frames 提示 “No tf data received”
        原因分析：无 TF 变换节点发布数据，或坐标系名称不匹配。
        解决方法：检查小车底盘是否正常发布 odom→base_link 的 TF 变换；确认相机驱动是否发布 base_link→camera_depth_frame 的 TF 变换；添加静态 TF 变换节点，补充缺失的坐标系关联。



## **总结与心得
本周实验围绕真实硬件（小车 + 深度相机）的 ROS 驱动适配、激光数据生成及 SLAM 建图展开，通过全流程实践加深了对 ROS 在实际机器人系统中应用的理解，主要收获如下：

- 硬件驱动与数据验证：成功实现深度相机和真实小车的驱动启动，掌握了通过rostopic list/info/hz/echo等命令行工具验证话题发布状态、数据格式及频率的方法，以及利用 RViz 可视化检查深度图、激光数据质量的技巧。深刻认识到硬件驱动启动顺序、话题名称匹配是后续功能实现的基础，任何驱动环节的异常都会直接导致下游功能失效。
- 深度图转激光数据：学会安装并配置官方depthimage_to_laserscan功能包，通过自定义 launch 文件适配 HP60C 相机的视场角、检测距离等参数，理解了scan_height、range_min/max等参数对激光数据密度和有效性的影响。调试过程中发现，参数不合理会导致激光点云出现大量 nan 或跳变，需结合硬件特性反复调整。
- Gmapping SLAM 建图：掌握了 Gmapping 算法的核心参数配置（粒子数、地图分辨率、激光有效距离等），明确了建图所需的依赖节点（roscore、相机驱动、激光转换、小车里程计）启动顺序。通过键盘控制小车运动实现实时建图，并利用map_saver保存地图，体会到里程计精度、激光数据质量、TF 坐标系关联对建图效果的关键影响 ——TF 链断裂或里程计误差过大会导致地图偏移、畸变。
- 坐标系与 TF 管理：熟悉了里程计话题/odom的验证方法，掌握了tf_echo、view_frames等工具检查 TF 变换链（odom→base_link→camera_link）完整性的手段。理解了静态 TF 变换在坐标系关联中的作用，以及 Fixed Frame 选择对 RViz 可视化建图效果的影响，认识到机器人系统中坐标系统一是多模块协同的核心前提。
- 工程化实践经验：在真实硬件实验中，遇到了驱动兼容性、参数适配、话题名称不匹配等工程问题，学会了通过终端报错信息定位问题、逐步验证每个环节的方法。深刻体会到 ROS 系统 “模块化” 的特点 —— 每个功能节点独立但又相互依赖，调试时需从底层驱动到上层应用逐一排查，同时也认识到参数调优是提升机器人性能的关键步骤。