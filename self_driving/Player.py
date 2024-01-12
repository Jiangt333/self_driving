# coding=UTF-8

import Global as glv
import Render as render
import TrackManager as tm
import Timer as timer


def init():
    # 车辆配置信息
    global posx             # 车辆X坐标
    global posy             # 车辆Y坐标
    global current_sector   # 当前所在赛道区域
    global last_sector      # 上一个赛道区域
    global dir              # 车辆方向向量
    global velocity         # 速度
    global rotation         # 旋转角度
    global innerce          # 左转右转时的偏移
    global isAlive          # 车辆是否存活
    global isAI             # 是否训练AI
    global flag             # 限定只能游戏开始时选择AI还是人玩，开始后不能再改变

    # 初始化玩家数据
    tm.initplayer()
    innerce = 0.0
    isAlive = True
    isAI = True
    flag = True


def updatePos():
    global posx
    global posy
    global dir
    global velocity
    global rotation
    global innerce

    # 方向向量更新
    rotation_to_radians = radians(rotation) # 将旋转角度转换为弧度
    dir[0] = cos(rotation_to_radians)       # 计算X方向上的方向向量
    dir[1] = -sin(rotation_to_radians)      # 计算Y方向上的方向向量

    # 近似
    dir[0] = 0.0 if -1e-4 < dir[0] < 1e-4 else dir[0]
    dir[1] = 0.0 if -1e-4 < dir[1] < 1e-4 else dir[1]

    # 旋转角度更新计算
    if (rotation > 360.0):
        rotation = rotation - 360.0
    if (rotation < 0.0):
        rotation = 360.0 + rotation
    rotation = rotation + innerce / 30.0  # 根据车辆的偏移innerce更新旋转角度

    # 速度范围约束
    velocity = max(0.2, min(velocity, 2.0))

    # 位置更新计算
    posx = posx + dir[0] * velocity  # 根据X方向上的方向向量和速度更新X坐标
    posy = posy + dir[1] * velocity  # 根据Y方向上的方向向量和速度更新Y坐标

    # 偏移重置计算
    if (glv.press == 0):
        innerce = 9.0 / 10.0 * innerce          # 根据偏移的十分之一减小偏移
        if (-1e-4 < innerce < 1e-4):
            innerce = 0.0
    if (glv.press > 0):
        glv.press = glv.press - 1               # 如果按键按下，减小按键按下的计数


def checkBounds():
    global posx
    global posy
    global isAlive
    if (glv.EnableTrackmap and not getTrackmap()):
        isAlive = False


def getTrackmap():
    global posx
    global posy
    global current_sector

    # /!\ If trackmap disabled it will always return true /!\ #
    if (not glv.EnableTrackmap):
        return True

    c = render.trackmap.pixels[int(posx) + int(posy) * 1024]

    if (floor(red(c)) <= 15 and floor(green(c)) >= 240):
        if (floor(blue(c)) >= 240):
            glv.FLC = True
        else:
            if (glv.FLC):
                glv.STry = glv.STry + 1
                print(" # Finish line crossed at try " + str(glv.Try))
                print(" # Timestamp: " + str(timer.frames) + " frames.")
                print(" # Total Successful laps: " + str(glv.STry) + ". ")
                glv.FLC = False
        return True
    else:
        return False
