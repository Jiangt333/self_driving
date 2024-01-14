import Global as glv
import TrackManager as tm
import Render as render
import Player as player
import StateManager as sm
import QLearning as qlearn

def setup():
    # 初始化：设置画布大小，初始化各种模块和参数
    size(1280, 720)

    glv.init()
    tm.init()
    render.init()
    player.init()
    sm.init()
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

    # 画布的背景设置为黑色
    background(0)
    if (not glv.disableScaling):
        render.drawSpritesAltRenderer()
    else:
        render.drawSpritesNoScaleAltRenderer()
    
    # AI actions and physics
    if(player.flag == False):
        if (player.isAlive):
            # 玩家是电脑，则开启训练模式
            if (player.isAI):
                qlearn.qlearn()     # 学习
                if (glv.ForceReset):
                    player.resetGame()
                if (not player.isAlive):
                    print("-AI died in try "+str(glv.Try)+". Timestamp: "+str(player.frames)+" frames.")
                    glv.Try = glv.Try+1
                    player.resetGame()
                if (glv.Try + glv.STry) % 30 == 0:
                    qlearn.saveQTableToFile()
            # 玩家是人
            else:
                player.run()
                player.updatePos()
                player.checkBounds()
                sm.calcTestpoints()
                sm.updateState()
                if (not player.isAlive or glv.ForceReset):
                    player.resetGame()
    
    # Render HUD
    if (glv.HUDEnabled):
        render.drawHUD()
        render.drawTimer()

# player handler
def keyPressed():
    # 游戏开始前选择玩家是AI自动玩还是人玩
    if(player.flag == True):
        if key == 'j' or key == 'J':
            # AI玩
            player.isAI = True
            player.flag = False
            print("you are AI!")
            qlearn.qTable = qlearn.loadQTableFromFile()
        if key == 'k' or key == 'K':
            # 人玩
            player.isAI = False
            player.flag = False
            print("you are people!")

    if player.isAI:
        if key == 'i' or key == 'I':
            qlearn.qTable = [[0.0 for x in range(3)] for y in range(int(2**(len(sm.state))))]
            print("Q_Table has been initialized")

    if not player.isAI:
        if key == 'a' or key == 'A':
            player.turnLeft()
        if key == 'd' or key == 'D':
            player.turnRight()
        if key == 'w' or key == 'W':
            player.accel()
        if key == 's' or key == 'S':
            player.deccel()
        if key == 'q' or key == 'Q':
            player.driftLeft()
            player.velocity = player.velocity-0.1
        if key == 'e' or key == 'E':
            player.driftRight()
            player.velocity = player.velocity-0.1
        if key == ' ':
            player.reset()

    if key == 'z' or key == 'Z':
        glv.disableScaling = not glv.disableScaling
    if key == 'h' or key == 'H':
        glv.HUDEnabled = not glv.HUDEnabled
    if key == 'm' or key == 'M':
        glv.renderTrackmap = not glv.renderTrackmap
    if key == 'l' or key == 'L':
        glv.renderCollisionLines = not glv.renderCollisionLines


    if key == '1' or key == '2' or key == '3' or key == '4':
        track_index = int(key) - 1
        tm.setTrack(track_index % tm.nTracks)
        glv.ForceReset = True
        print("Loaded track: " + tm.tracknames[tm.selectedTrack])
