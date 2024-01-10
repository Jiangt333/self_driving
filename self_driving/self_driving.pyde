import Global as glv
import TrackManager as tm
import Render as render
import Player as player
import Controls as controls
import StateManager as sm
import Timer as timer
import Points as points
import QLearning as qlearn

def setup():
    # 初始化：设置画布大小，初始化各种模块和参数
    size(1280, 720)
    
    glv.init()
    tm.init()
    render.init()
    player.init()
    sm.init()
    timer.init()
    points.init()
    qlearn.init()

    # 设置帧速率为999帧每秒
    frameRate(999)

    # 关闭平滑处理
    noSmooth()

    if (glv.EnableTrackmap):
        # 加载画布上的像素数据到程序中
        loadPixels()
        # 加载赛道地图的像素数据
        render.trackmap.loadPixels()
    
def draw():
    glv.eventDelta = 1.0/frameRate

    # Render sprite
    background(0)   # 画布的背景设置为黑色
    if (not glv.disableScaling):
        render.drawSpritesAltRenderer()
    else:
        render.drawSpritesNoScaleAltRenderer()
    
    ### AI actions and physics ###
    if(player.flag == False):
        if (player.isAlive):
            # 玩家是电脑，则开启训练模式
            if (player.isAI):
                qlearn.qlearn()     # 学习
                if (glv.ForceReset):
                    controls.reset()
                if (not player.isAlive):
                    print("-AI died in try "+str(glv.Try)+". Timestamp: "+str(timer.frames)+" frames.")
                    glv.Try = glv.Try+1
                    controls.reset()
            ### 玩家是人，则人来玩 ###
            else:
                timer.run()
                player.updatePos()
                player.checkBounds()
                sm.calcTestpoints()
                sm.updateState()
                if (not player.isAlive or glv.ForceReset):
                    controls.reset()
    
    ### Render HUD ###
    if (glv.HUDEnabled):
        render.drawHUD()
        render.drawTimer()

### Controls handler ###
def keyPressed():
    # 游戏开始前选择玩家是AI自动玩还是人玩
    if(player.flag == True):
        if (key == 'j' or key == 'J'):
            # AI玩
            player.isAI = True
            player.flag = False
        if (key == 'k' or key == 'K'):
            # 人玩
            player.isAI = False
            player.flag = False
        
    if (not player.isAI):
        if (key == 'a' or key == 'A'):
            controls.turnLeft()
        if (key == 'd' or key == 'D'):
            controls.turnRight()
        if (key == 'w' or key == 'W'):
            controls.accel()
        if (key == 's' or key == 'S'):
            controls.deccel()
        if (key == ' '):
            controls.reset()
    if (key == 'z' or key == 'Z'):
        glv.disableScaling = not glv.disableScaling
    if (key == 'h' or key == 'H'):
        glv.HUDEnabled = not glv.HUDEnabled
    if (key == 'm' or key == 'M'):
        glv.renderTrackmap = not glv.renderTrackmap
    if (key == 'l' or key == 'L'):
        glv.renderCollisionLines = not glv.renderCollisionLines
    if (key == 'r' or key == 'R'):
        if (glv.renderer == 0):
            glv.renderer = 1
        else:
            if (glv.renderer == 1):
                glv.renderer = 2
            else:
                if (glv.renderer == 2):
                    glv.renderer = 0
    if (key == 'n' or key == 'N'):
        glv.BlockLearning = not glv.BlockLearning
        print("*BlockLearning set to: "+str(glv.BlockLearning))
    if (key == '0'):
        tm.setTrack(0)
        glv.ForceReset = True
        print("Loaded track: "+tm.tracknames[tm.selectedTrack])
    if (key == '1'):
        tm.setTrack(1)
        glv.ForceReset = True
        print("Loaded track: "+tm.tracknames[tm.selectedTrack])
    if (key == '2'):
        tm.setTrack(2)
        glv.ForceReset = True
        print("Loaded track: "+tm.tracknames[tm.selectedTrack])
    if (key == '3'):
        tm.setTrack(3)
        glv.ForceReset = True
        print("Loaded track: "+tm.tracknames[tm.selectedTrack])
    if (key == '4'):
        tm.setTrack(4)
        glv.ForceReset = True
        print("Loaded track: "+tm.tracknames[tm.selectedTrack])
    if (key == '5'):
        tm.setTrack(5)
        glv.ForceReset = True
        print("Loaded track: "+tm.tracknames[tm.selectedTrack])
    if (key == '6'):
        tm.setTrack(6)
        glv.ForceReset = True
        print("Loaded track: "+tm.tracknames[tm.selectedTrack])
    if (key == '7'):
        tm.setTrack(7)
        glv.ForceReset = True
        print("Loaded track: "+tm.tracknames[tm.selectedTrack])
    if (key == '8'):
        tm.setTrack(8)
        glv.ForceReset = True
        print("Loaded track: "+tm.tracknames[tm.selectedTrack])
    if (key == '9'):
        tm.setTrack(9)
        glv.ForceReset = True
        print("Loaded track: "+tm.tracknames[tm.selectedTrack])
