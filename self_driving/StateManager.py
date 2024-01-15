# coding=UTF-8

import Global as glv
import Render as render
import Player as player
import TrackManager as tm

def init():
    # 状态变量
    global state
    global ranges
    global distfront
    global testpoints

    # 检测碰撞是否发生的范围
    distfront = 1.0
    ranges = [i * 0.05 for i in range(21)]
    state = [False, False, False, False, False, False, False]
    testpoints = [[0.0, 0.0] for _ in range(7)]

    calcTestpoints()


# 计算碰撞检测点坐标
def calcTestpoints():
    global testpoints

    rotation_to_radians = radians(player.rotation)
    veinterad = radians(20)

    angles = [PI / 2, PI / 4, veinterad, 0, -veinterad, -PI / 4, -PI / 2]
    distances = [20, 40, 45, 50, 45, 40, 20]

    for i in range(len(testpoints)):
        testpoints[i][0] = distances[i] * cos(rotation_to_radians + angles[i])
        testpoints[i][1] = -distances[i] * sin(rotation_to_radians + angles[i])

    testpoints[3][0] = 50 * player.dir[0]
    testpoints[3][1] = 50 * player.dir[1]


# 绘制车头前面的7条碰撞检测线-无缩放
def renderTestlinesNoScale():
    global state
    global testpoints

    for n in range(0, len(testpoints)):
        if (state[n]):
            stroke(255, 255, 0)
        else:
            stroke(0)
        line(width / 2, height / 2, width / 2 + testpoints[n][0], height / 2 + testpoints[n][1])


# 绘制车头前面的7条碰撞检测线-有缩放
def renderTestlines():
    global state
    global testpoints

    for n in range(0, len(testpoints)):
        if (state[n]):
            stroke(255, 255, 0)  # 黄色
        else:
            stroke(0)  # 黑色
        line(width / 2, height / 2, width / 2 + testpoints[n][0] * render.scale,
             height / 2 + testpoints[n][1] * render.scale)


# 更新状态
def updateState():
    global state

    for n in range(0, len(testpoints)):
        state[n] = checkColl(n)


# 检查该碰撞检测点是否发生碰撞
def checkColl(n):
    global testpoints
    global ranges
    global distfront

    for i in range(0, len(ranges)):
        if (not getTrackmap(player.posx + ranges[i] * testpoints[n][0], player.posy + ranges[i] * testpoints[n][1])):
            if (n == 3):
                # 在QLearning中获得奖赏时有用
                distfront = ranges[i]
            return True
    if (n == 3):
        # 在QLearning中获得奖赏时有用
        distfront = 1.0
    return False

# 取赛道地图上指定位置 (x, y) 处的信息，检测该像素点是否可通过
def getTrackmap(x, y):
    c = render.trackmap.pixels[int(x) + int(y) * 1024]

    if (floor(red(c)) <= 15 and floor(green(c)) >= 240):
        # (0, 255, *) 这样的颜色（*表示任意值），表示这个位置可通过
        return True
    else:
        # 其他像素点颜色不可通过
        return False
