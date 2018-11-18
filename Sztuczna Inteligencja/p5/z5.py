from collections import namedtuple
from random import choice

CarState = namedtuple("CarState", ["x", "y", "vx", "vy"])
Action = namedtuple("Action", ["dvx", "dvy"])

ACCELERATIONS = [-1,0,1]
ACTIONS = [Action(dvx, dvy) for dvx in ACCELERATIONS for dvy in ACCELERATIONS]



def move(car_state: CarState, action: Action): #-> CarState
    x,y,vx,vy = car_state
    dvx, dvy = action

    vx, vy = sorted([-3,vx + dvx, 3])[1], sorted([-3,vy + dvy,3])[1]
    x,y = x + vx, y + vy
    return CarState(x,y,vx,vy)

def oily_move(car_state: CarState, action: Action):
    dvx, dvy = action
    rx,ry = choice(ACCELERATIONS), choice(ACCELERATIONS)
    dvx, dvy = dvx + rx, dvy + ry
    return move(car_state, Action(dvx, dvy))
