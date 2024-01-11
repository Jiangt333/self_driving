# coding=UTF-8

import Player as player
import Render as render
import StateManager as sm

def init():
    global selectedTrack
    global nTracks
    global tracknames
    global track_sprites
    global trackmap_sprites
    global initial_posx
    global initial_posy
    global initial_dir
    global initial_velocity
    global initial_rotation
    
    ### EDIT THIS TO ADD MORE TRACKS ###
    selectedTrack = 0
    nTracks = 5
    tracknames = ["Donut Plains",
                  "model_1",
                  "model_2",
                  "model_3",
                  "model_4"]

    track_sprites = ["Donut_Plains_2.png",
                     "model_1.png",
                     "model_2.png",
                     "model_3.png",
                     "model_4.png"]

    trackmap_sprites = ["Donut_Plains_2-map.png",
                        "model_1_map.png",
                        "model_2_map.png",
                        "model_3_map.png",
                        "model_4_map.png"]

    initial_posx = [920.0, 312.0, 215, 475, 805]
    initial_posy = [619.0, 495.0, 520, 795, 570]
    initial_dir = [[0.0, -1.0], [0.0, -1.0], [0.0, -1.0], [0.0, -1.0], [0.0, -1.0]]
    initial_velocity = [1.0, 1.0, 1.0, 1.0, 1.0]
    initial_rotation = [90.0, 90.0, 90.0, 180.0, 270.0]
    #######################################
    
def ldTrack():
    global selectedTrack
    global nTracks
    global track_sprites
    global trackmap_sprites
    global initial_posx
    global initial_posy
    global initial_dir
    global initial_velocity
    global initial_rotation
    
    if (selectedTrack >= nTracks):
        selectedTrack = 0
    render.track = loadImage(track_sprites[selectedTrack])
    render.trackmap = loadImage(trackmap_sprites[selectedTrack])
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
    global track_sprites
    global trackmap_sprites
    
    if (selectedTrack >= nTracks): 
        selectedTrack = 0
    render.track = loadImage(track_sprites[selectedTrack])
    render.trackmap = loadImage(trackmap_sprites[selectedTrack])
    print("Loaded track: "+tracknames[selectedTrack])

def setTrack(number):
    global selectedTrack
    global nTracks
    
    if (number >= nTracks or number < 0):
        return
    selectedTrack = number
