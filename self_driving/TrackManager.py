# coding=UTF-8

import Player as player
import Render as render
import StateManager as sm

def init():
    global selectedTrack
    global nTracks
    global tracknames
    global trackSprite
    global trackBaseMapSprite
    global initial_posx
    global initial_posy
    global initial_dir
    global initial_velocity
    global initial_rotation

    selectedTrack = 0
    nTracks = 4
    tracknames = ["Map 1",
                  "Map 2",
                  "Map 3",
                  "Map 4"]

    trackSprite = ["model_1.png",
                     "model_2.png",
                     "model_3.png",
                     "model_4.png"]

    trackBaseMapSprite  = ["model_1_map.png",
                        "model_2_map.png",
                        "model_3_map.png",
                        "model_4_map.png"]

    initial_posx = [312.0, 215, 475, 805]
    initial_posy = [495.0, 520, 795, 570]
    initial_dir = [[0.0, -1.0], [0.0, -1.0], [0.0, -1.0], [0.0, -1.0]]
    initial_velocity = [1.0, 1.0, 1.0, 1.0]
    initial_rotation = [90.0, 90.0, 180.0, 270.0]

    
def ldTrack():
    global selectedTrack
    global nTracks
    global trackSprite
    global trackBaseMapSprite 
    global initial_posx
    global initial_posy
    global initial_dir
    global initial_velocity
    global initial_rotation
    
    if (selectedTrack >= nTracks):
        selectedTrack = 0
    render.track = loadImage(trackSprite[selectedTrack])
    render.trackBaseMap = loadImage(trackBaseMapSprite [selectedTrack])
    player.posx = initial_posx[selectedTrack]
    player.posy = initial_posy[selectedTrack]
    player.dir = initial_dir[selectedTrack]
    player.velocity = initial_velocity[selectedTrack]
    player.rotation = initial_rotation[selectedTrack]
    sm.init()
    
def initplayer():
    global selectedTrack
    global nTracks
    global initial_posx
    global initial_posy
    global initial_dir
    global initial_velocity
    global initial_rotation
    
    if (selectedTrack >= nTracks): 
        selectedTrack = 0
    player.posx = initial_posx[selectedTrack]
    player.posy = initial_posy[selectedTrack]
    player.dir = initial_dir[selectedTrack]
    player.velocity = initial_velocity[selectedTrack]
    player.rotation = initial_rotation[selectedTrack]
    
def initrender():
    global selectedTrack
    global tracknames
    global nTracks
    global trackSprite
    global trackBaseMapSprite 
    
    if (selectedTrack >= nTracks): 
        selectedTrack = 0
    render.track = loadImage(trackSprite[selectedTrack])
    render.trackBaseMap = loadImage(trackBaseMapSprite [selectedTrack])
    print("Loaded track: "+tracknames[selectedTrack])

def setTrack(number):
    global selectedTrack
    global nTracks
    
    if (number >= nTracks or number < 0):
        return
    selectedTrack = number
