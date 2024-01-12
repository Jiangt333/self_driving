# coding=UTF-8

import Global as glv
import Player as player
import StateManager as sm


def init():
    # q-learning的超参数
    global scores
    global qTable
    global alpha_
    global gama_

    scores = 0.0
    qTable = [[0.0 for x in range(3)] for y in range(int(2 ** (len(sm.state))))]
    alpha_ = 0.1
    gama_ = 0.9


# 奖赏函数
def getReward(action):
    global scores

    # 初始 0 分
    scores = 0.0
    if (player.isAlive):
        if any(sm.state):
            # 如果有碰撞检测线点未检测出碰撞，给出对应分数
            scores = 5.0 - (1.0 - sm.distfront) * 60.0
        else:
            # 如果所有检测线都没有检测出碰撞
            if (action == 0):
                # 汽车直行，分数=20
                scores = 20.0
            else:
                # 汽车采取左转或右转
                scores = 10.0
    else:
        # 如果车撞到障碍了，游戏重新开始，并给予惩罚
        scores = -3000.0

    return scores


def saveQTableToFile():
    global qTable
    with open("Q_Table.txt", 'w') as file:
        for row in qTable:
            file.write(','.join(map(str, row)) + '\n')


def loadQTableFromFile():
    q_table = []
    with open("Q_Table.txt", 'r') as file:
        for line in file:
            row = [float(value) for value in line.strip().split(',')]
            q_table.append(row)
    print("Data Loading Successful!")
    return q_table


# 计算状态
def calcstate():
    st = 0
    for n in range(0, len(sm.state)):
        st = st + (2 ** n) * int(sm.state[n])
    return st


# 选择动作
def select_action(state, explore_flag):
    global qTable

    selected_action = 0
    val = -float("inf")

    # ε-greedy贪心，选择动作
    for n in range(0, 3):
        if (qTable[state][n] > val):
            val = qTable[state][n]
            selected_action = n

    # 如果explore_flag为True，用ε-贪心策略选择动作
    # 如果生成的随机数大于给定的ε，则随机选择一个动作
    # 否则就保持前面用贪心策略得到的动作
    if (explore_flag and random(0, 100) >= 99):
        selected_action = floor(random(0, 3))

    return selected_action


# 执行选择的动作
def perform_action(action):
    if (action == 1):
        player.turnLeft()
    if (action == 2):
        player.turnRight()

    player.run()
    player.updatePos()
    player.checkBounds()
    sm.calcTestpoints()
    sm.updateState()


def qlearn():
    global qTable  # Q-table
    global alpha_  # 学习率
    global gama_  # 折扣因子

    current_state = calcstate()  # 得到当前状态
    action = select_action(current_state, True)  # 为当前状态选择动作（行为策略：ε-greedy）
    perform_action(action)  # 执行动作

    # 更新Q-table
    if (not glv.BlockLearning):
        reward = getReward(action)  # 采样得到奖赏

        fstate = calcstate()  # 得到跳转到的下一个状态
        # 更新Q-table时选择maxq对应的动作（目标策略：greedy）
        faction = select_action(fstate, False)

        # 更新Q-table
        qTable[current_state][action] = qTable[current_state][action] + alpha_ * (
                    reward + gama_ * qTable[fstate][faction] - qTable[current_state][action])

