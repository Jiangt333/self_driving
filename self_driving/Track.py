# coding=UTF-8

import Player as player
import Render as renderModel
import State as stateModel

def init():
    global init_v       # 初始速度
    global init_r       # 初始角度
    global sTrack       # 选择的地图
    global nTracks      # 地图总数
    global init_dir
    global init_posx    # 初始化x坐标
    global init_posy    # 初始化y坐标
    global trackNames   # 地图名称
    global trackTopMap
    global trackBaseMap

    sTrack = 0
    nTracks = 4
    trackNames = ["Map 1",
                  "Map 2",
                  "Map 3",
                  "Map 4"]

    trackTopMap = ["model_1.png",
                   "model_2.png",
                   "model_3.png",
                   "model_4.png"]

    trackBaseMap = ["model_1_map.png",
                    "model_2_map.png",
                    "model_3_map.png",
                    "model_4_map.png"]

    init_posx = [312.0, 215, 475, 805]
    init_posy = [495.0, 520, 795, 570]

    init_dir = [[0.0, -1.0],
                [0.0, -1.0],
                [0.0, -1.0],
                [0.0, -1.0]]

    init_v= [1.0, 1.0, 1.0, 1.0]

    init_r = [90.0, 90.0, 180.0, 270.0]

    
def ldTrack():
    global sTrack
    global nTracks
    global trackTopMap
    global trackBaseMap
    global init_posx
    global init_posy
    global init_dir
    global init_v
    global init_r
    
    if (sTrack >= nTracks):
        sTrack = 0
    renderModel.track = loadImage(trackTopMap[sTrack])
    renderModel.trackBaseMap = loadImage(trackBaseMap[sTrack])

    player.posx = init_posx[sTrack]
    player.posy = init_posy[sTrack]
    player.dir = init_dir[sTrack]
    player.v = init_v[sTrack]
    player.r = init_r[sTrack]
    stateModel.init()
    
def initplayer():
    global sTrack
    global nTracks
    global init_posx
    global init_posy
    global init_dir
    global init_v
    global init_r
    
    if (sTrack >= nTracks):
        sTrack = 0
    player.posx = init_posx[sTrack]
    player.posy = init_posy[sTrack]
    player.dir = init_dir[sTrack]
    player.v = init_v[sTrack]
    player.r = init_r[sTrack]
    
def initrender():
    global sTrack
    global trackNames
    global nTracks
    global trackTopMap
    global trackBaseMap
    
    if (sTrack >= nTracks):
        sTrack = 0
    renderModel.track = loadImage(trackTopMap[sTrack])
    renderModel.trackBaseMap = loadImage(trackBaseMap[sTrack])
    print("Loaded track: "+trackNames[sTrack])

def setTrack(number):
    global sTrack
    global nTracks
    
    if (number >= nTracks or number < 0):
        return
    sTrack = number
