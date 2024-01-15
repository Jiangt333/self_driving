# coding=UTF-8

import Global as glv
import Render as render
import TrackManager as tm
import QLearning as qlearn
from math import cos, sin, radians, floor

# 初始化游戏
def init():
    # 玩家和车辆配置信息
    global posx
    global posy
    global current_sector
    global last_sector
    global dir
    global velocity  # 速度
    global rotation
    global innerce  # 左转右转时的偏移
    global isAlive  # 车辆是否存活
    global isAI  # 是AI自动玩还是人玩
    global flag  # 限定只能游戏开始时选择AI还是人玩，开始后不能再改变

    # 时间数据
    global frames
    global best
    global started

    # 初始化玩家数据
    tm.initplayer()
    innerce = 0.0
    isAlive = True
    isAI = True
    flag = True

    # 初始化时间数据
    frames = 0.0
    best = 0.0
    started = True

# 更新玩家位置
def updatePos():
    # 玩家数据
    global posx
    global posy
    global dir
    global velocity
    global rotation
    global innerce

    # 方向向量更新
    rotation_to_radians = radians(rotation)  # 将旋转角度转换为弧度
    dir[0] = cos(rotation_to_radians)  # 计算X方向上的方向向量
    dir[1] = -sin(rotation_to_radians)  # 计算Y方向上的方向向量

    # 近似
    if -1e-4 < dir[0] < 1e-4:
        dir[0] = 0.0
    if -1e-4 < dir[1] < 1e-4:
        dir[1] = 0.0

    # 旋转角度更新计算
    rotation = rotation % 360
    rotation = rotation + innerce / 30.0  # 根据车辆的偏移innerce更新旋转角度

    # 速度范围约束
    velocity = max(0.2, min(velocity, 2.0))

    # 位置更新计算
    posx = posx + dir[0] * velocity  # 根据X方向上的方向向量和速度更新X坐标
    posy = posy + dir[1] * velocity  # 根据Y方向上的方向向量和速度更新Y坐标

    # 偏移重置计算
    if (glv.pressKey == 0):
        innerce = 9.0 / 10.0 * innerce  # 根据偏移的十分之一减小偏移
        if (-1e-4 < innerce < 1e-4):
            innerce = 0.0
    if (glv.pressKey > 0):
        glv.pressKey = glv.pressKey - 1  # 如果按键按下，减小按键按下的计数


# 检查玩家是否存活
def checkBounds():
    global posx
    global posy
    global isAlive
    if (not getTrackmap()):
        isAlive = False

# 获取车道信息
def getTrackmap():
    global posx
    global posy
    global current_sector

    # 获取小车中心点的像素信息
    c = render.trackmap.pixels[int(posx) + int(posy) * 1024]

    if (floor(red(c)) <= 15 and floor(green(c)) >= 240):
        # 判断是否成功越过终点线
        if (floor(blue(c)) >= 240):
            glv.passFlag = True
        else:
            if (glv.passFlag):
                glv.STry = glv.STry + 1
                print(" # Finish line crossed at try " + str(glv.Try))
                print(" # Timestamp: " + str(frames) + " frames.")
                print(" # Total Successful laps: " + str(glv.STry) + ". ")
                glv.passFlag = False
        return True
    else:
        return False

# 向左转
def turnLeft():
    global isAlive
    global innerce
    # 如果玩家已死亡，则退出函数
    if (not isAlive):
        return
    # 设置状态为2
    glv.pressKey = 2
    if (innerce < 30.0):
        if (innerce < 0.0):
            innerce = innerce + 25.0
        innerce = innerce + 20.0

# 向右转
def turnRight():
    global innerce
    global isAlive
    if (not isAlive):
        return
    # 设置状态为2
    glv.pressKey = 2
    if (innerce > -30.0):
        if (innerce > 0.0):
            innerce = innerce - 25.0
        innerce = innerce - 20.0

# 向左漂移
def driftLeft():
    global velocity
    global innerce
    global isAlive
    # 如果玩家已死亡，则退出函数
    if (not isAlive):
        return
    # 设置状态为2
    glv.pressKey = 2
    if (innerce < 30.0):
        if (innerce < 0.0):
            innerce = innerce + 25.0
        innerce = innerce + 50.0
        velocity = velocity + 0.1

# 向右漂移
def driftRight():
    global velocity
    global innerce
    global isAlive
    # 如果玩家已死亡，则退出函数
    if (not isAlive):
        return
    # 设置状态为2
    glv.pressKey = 2
    if (innerce > -30.0):
        if (innerce > 0.0):
            innerce = innerce - 25.0
        innerce = innerce - 50.0
        velocity = velocity + 0.1

# 加速
def accel():
    global isAlive
    global velocity
    # 如果玩家已死亡，则退出函数
    if (not isAlive):
        return
    # 速度增加0.1
    velocity = velocity + 0.1

# 减速
def deccel():
    global isAlive
    global velocity
    # 如果玩家已死亡，则退出函数
    if (not isAlive):
        return
    # 速度减少0.1
    velocity = velocity - 0.1

# 重置游戏状态
def resetGame():
    global innerce
    global isAlive
    # 载入轨道
    tm.ldTrack()
    # 重置计时器
    reset()
    # 分数重置为0.0
    qlearn.points = 0.0
    # 偏移重置为0.0
    innerce = 0.0
    # 玩家状态设为存活
    isAlive = True
    # 按键状态设为0
    glv.pressKey = 0
    # 强制重置标志设为False
    glv.forceReset = False

# 开始游戏
def startt():
    global started
    started = True

# 暂停游戏
def pauset():
    global started
    started = False

# 重置计时器
def reset():
    global frames
    global best
    if (frames > best):
        best = frames
    frames = 0.0

# 运行游戏
def run():
    global frames
    global started
    if (started):
        frames = frames + 1
