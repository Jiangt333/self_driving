# coding=UTF-8

def init():

    global eventDelta           # 事件时间差
    global renderer             # 渲染器类型
    
    # 控制变量
    global press                # 记录按键事件的状态
    global disableScaling       # 是否禁用缩放
    global HUDEnabled           # 是否启用HUD悬浮显示
    global EnableTrackmap       # 是否启用轨迹地图
    global renderTrackmap       # 是否渲染轨迹地图
    global renderCollisionLines # 是否渲染碰撞线
    global ForceReset           # 是否强制重置
    
    # Q-Learning控制变量
    global BlockLearning        # 是否阻止学习
    global Try                  # 当前尝试的次数
    global FLC                  # 是否通过
    global STry                 # 成功次数
    
    # 初始化时间差为0, 渲染器类型为1
    eventDelta = 0.0
    renderer = 1
    
    # 初始化控制变量
    press = 0
    disableScaling = False
    HUDEnabled = True
    EnableTrackmap = True
    renderTrackmap = False
    renderCollisionLines = True
    ForceReset = False
    
    # Q-learning 参数初始化
    BlockLearning = False
    Try = 1
    STry = 0
    FLC = False
