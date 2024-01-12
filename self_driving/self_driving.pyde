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
                if (glv.Try + glv.STry) % 30 == 0:
                    qlearn.saveQTableToFile()

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
        if key in 'jJ':
            # AI玩
            player.isAI = True
            player.flag = False
            qlearn.q = qlearn.loadQTableFromFile()
        if key in 'kK':
            # 人玩
            player.isAI = False
            player.flag = False

    if player.isAI:
        if key in 'iI':
            qlearn.q = [[0.0 for x in range(3)] for y in range(int(2**(len(sm.state))))]
            print("Q_Table has been initialized")
        
    if not player.isAI:
        if key in 'aA':
            controls.turnLeft()
        if key in 'dD':
            controls.turnRight()
        if key in 'wW':
            controls.accel()
        if key in 'sS':
            controls.deccel()
        if key == ' ':
            controls.reset()

    if key in 'zZ':
        glv.disableScaling = not glv.disableScaling
    if key in 'hH':
        glv.HUDEnabled = not glv.HUDEnabled
    if key in 'mM':
        glv.renderTrackmap = not glv.renderTrackmap
    if key in 'lL':
        glv.renderCollisionLines = not glv.renderCollisionLines


    if (key == '1' or key == '2' or key == '3' or key == '4' or key == '5' or key == '6' or key == '7' or key == '8' or key == '9'):
        track_index = int(key) - 1
        tm.setTrack(track_index % tm.nTracks)
        glv.ForceReset = True
        print("Loaded track: " + tm.tracknames[tm.selectedTrack])

