# coding=UTF-8

import Render as render
import Player as player
import TrackManager as tm

def init():
    # State vars
    global state
    global distfront
    global testpoints
    
    # 检测碰撞是否发生的范围
    global ranges
    ranges = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
    
    state = [False, False, False, False, False, False, False]
    distfront = 1.0
    testpoints = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
    
    calcTestpoints()

# 计算碰撞检测点坐标
def calcTestpoints():
    global testpoints
    
    rotation_to_radians = radians(player.rotation)
    veinterad = radians(20)
    
    testpoints[0][0] = 20*cos(rotation_to_radians+PI/2)
    testpoints[0][1] = -20*sin(rotation_to_radians+PI/2)
    
    testpoints[1][0] = 40*cos(rotation_to_radians+PI/4)
    testpoints[1][1] = -40*sin(rotation_to_radians+PI/4)
    
    testpoints[2][0] = 45*cos(rotation_to_radians+veinterad)
    testpoints[2][1] = -45*sin(rotation_to_radians+veinterad)
    
    testpoints[3][0] = 50*player.dir[0]
    testpoints[3][1] = 50*player.dir[1]
    
    testpoints[4][0] = 45*cos(rotation_to_radians-veinterad)
    testpoints[4][1] = -45*sin(rotation_to_radians-veinterad)
    
    testpoints[5][0] = 40*cos(rotation_to_radians-PI/4)
    testpoints[5][1] = -40*sin(rotation_to_radians-PI/4)
    
    testpoints[6][0] = 20*cos(rotation_to_radians-PI/2)
    testpoints[6][1] = -20*sin(rotation_to_radians-PI/2)

# 绘制车头前面的7条碰撞检测线-无缩放
def renderTestlinesNoScale():
    global state
    global testpoints
    
    for n in range(0, len(testpoints)):
        if (state[n]):
            stroke(255, 255, 0)
        else:
            stroke(0)
        line(width/2, height/2, width/2+testpoints[n][0], height/2+testpoints[n][1])

# 绘制车头前面的7条碰撞检测线-有缩放
def renderTestlines():
    global state
    global testpoints
    
    for n in range(0, len(testpoints)):
        if (state[n]):
            stroke(255, 255, 0)  # 黄色
        else:
            stroke(0)   # 黑色
        line(width/2, height/2, width/2+testpoints[n][0]*render.displayscale, height/2+testpoints[n][1]*render.displayscale)

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
        if (not render.getTrackmap(player.posx+ranges[i]*testpoints[n][0], player.posy+ranges[i]*testpoints[n][1])):
            if (n == 3):
                # TODO ？？？
                distfront = ranges[i]
            return True
    if (n == 3):
        # TODO ？？？
        distfront = 1.0
    return False
