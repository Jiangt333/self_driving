# coding=UTF-8
# 这个文件主要是在进行渲染绘图、碰撞点检测

import Global as glv
import Player as player
import StateManager as sm
import TrackManager as tm
import Timer as timer
import Points as points

def init():
    # 字体
    global font
    font = createFont("Hooge0553", 18)
    
    # 车辆、赛道、赛道区域地图
    global car
    global track
    global trackmap
    
    # 缩放比例
    global scale

    # 设置缩放比例（整数）
    scale = 3

    
    # 加载小车图像
    car = loadImage("car.png")
    # TODO？
    tm.initrender()

### 渲染模式，进行了缩放 ###
def drawSpritesAltRenderer():
    # 车辆、赛道
    global car
    global track
    
    # 缩放比例
    global scale
    
    ###  Display 赛道 ###
    image(track, -(player.posx*scale)+(width/2), -(player.posy*scale)+(height/2), 1024*scale, 1024*scale)
    if (glv.renderTrackmap):
        image(trackmap, -(player.posx*scale)+(width/2), -(player.posy*scale)+(height/2), 1024*scale, 1024*scale)
    
    ###  Display 车辆 ###
    pushMatrix()
    translate(width/2, height/2)
    rotate(radians(90.0-player.rotation))
    rotate(radians(-player.innerce))
    translate(-width/2, -height/2)
    image(car, (width/2)-10*scale, (height/2)-22*scale, 21*scale, 45*scale)
    popMatrix()
    
    ### 绘制车头前面的7条碰撞检测线 ###
    if (glv.renderCollisionLines):
        sm.renderTestlines()

### 渲染模式，未进行了缩放，原始尺寸显示 ###
def drawSpritesNoScaleAltRenderer():
    # 车辆，赛道
    global car
    global track
    
    ###  Display 赛道 ###
    image(track, -player.posx+(width/2), -player.posy+(height/2))
    if (glv.renderTrackmap):
        image(trackmap, -player.posx+(width/2), -player.posy+(height/2))
        
    ###  Display 车辆 ###
    pushMatrix()
    translate(width/2, height/2)
    rotate(radians(90.0-player.rotation))
    rotate(radians(-player.innerce))
    translate(-width/2, -height/2)
    image(car, (width/2)-10, (height/2)-22)
    popMatrix()
    
    ### 绘制车头前面的7条碰撞检测线 ###
    if (glv.renderCollisionLines):
        sm.renderTestlinesNoScale()

### HUD Renderer ###
def drawHUD():
    #Font
    global font
    
    # 开始游戏的指南
    if(player.flag == True):
        textFont(font, 50)
        textAlign(CENTER, CENTER)
        textWithBorders("Tip:  Before playing, choose your player \n which 'j' or 'J' is AI play and 'k' or 'K' is people play", 670, 300)


def drawTimer():
    #Font
    global font
    
    # 右上角信息显示
    textFont(font, 18)
    textAlign(RIGHT)
    textWithBorders(tm.tracknames[tm.selectedTrack], width-23, 20)
    textWithBorders("EPOCH " + str(glv.Try), width - 23, 40)
    textWithBorders("TIME "+str(int(timer.frames)), width-23, 60)
    textWithBorders("BEST TIME "+str(int(timer.best)), width-23, 80)
    textWithBorders("REWARD "+str(int(points.points)), width-23, 100)
    
    
def textWithBorders(txt, x, y):
    offsets = [(-1, 0), (-1, -1), (0, -1), (1, 0), (1, 1), (0, 1)]  # 不同方向的偏移

    fill(0)             # 设置文本的填充颜色为黑色
    for offset in offsets:
        text(txt, x + offset[0], y + offset[1])

    fill(255)           # 设置文本的填充颜色为白色
    text(txt, x, y)     # 在原始位置绘制文本
    
### 获取赛道地图上指定位置 (x, y) 处的信息，检测该像素点是否可通过 ###
def getTrackmap(x, y):

    # trackmap被禁用就返回True #
    if (not glv.EnableTrackmap):
        return True
    
    global trackmap
    
    c = trackmap.pixels[int(x) + int(y)*1024]
    
    if (floor(red(c)) <= 15 and floor(green(c)) >= 240):
        # (0, 255, *) 这样的颜色（*表示任意值），表示这个位置可通过
        return True
    else:
        # 其他像素点颜色不可通过
        return False
