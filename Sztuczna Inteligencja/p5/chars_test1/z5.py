from collections import deque

FIELDS = OFFROAD, ROAD, OIL, FINISH, START = '.#oes'

REWARD, PENALTY = 100, -100
DISCOUNT = 0.99
MOVE_COST = 0.1
ITERATIONS = 100

MIN_V, MAX_V = -3, 3
ALL_DVS = {-1, 0, 1}
ALL_RS = {-1, 0, 1}

def parse(track):
    start_position = x, y = next((x,y) for y, row in enumerate(track) for x, field in enumerate(row) if track[y][x] == START)
    end_points = {(x,y) for y, row in enumerate(track) for x, field in enumerate(row) if track[y][x] == FINISH}
    parsed_track = [row for row in track if row]
    parsed_track[y][x] = ROAD

    return start_position, end_points, parsed_track

def on_road(x, y, track):
    w, h = len(track[0]), len(track)
    return 0 <= x < w and 0 <= y < h and track[y][x] != OFFROAD


def moves(x, y, vx, vy, track):
    actions = {(dvx, dvy) for dvx in ALL_DVS for dvy in ALL_DVS}

    if track[y][x] == OIL:
        actions = {(dvx + rx, dvy + ry) for dvx, dvy in actions for rx in ALL_RS for ry in ALL_RS}

    vs = {(vx + dvx, vy + dvy) for dvx, dvy in actions}
    return {(x + new_vx, y + new_vy, new_vx, new_vy) for new_vx, new_vy in vs if MIN_V <= new_vx <= MAX_V and MIN_V <= new_vy <= MAX_V}


def possible_states(track, start_pos):
    states = set()
    to_check = deque({(*start_pos, 0, 0)})

    while to_check:
        state = x, y, vx, vy = to_check.pop()
        states.add(state)

        if on_road(x, y, track):
            to_check.extend(moves(x, y, vx, vy, track) - states)

    return states


def value_iteration(start_pos, endpoints, track, iterations):
    def init_value_at(x, y, vx, vy):
        return (PENALTY if not on_road(x, y, track) else
                REWARD if track[y][x] == FINISH else
                0)

    state_to_value = {state: init_value_at(*state) for state in possible_states(track, start_pos)}

    for _ in range(iterations):
        for state in state_to_value:
            x, y, _, _ = state

            if on_road(x, y, track):
                if state_to_value[state] not in {REWARD, PENALTY}:
                    if track[y][x] != OIL:
                        state_to_value[state] = -MOVE_COST + DISCOUNT * max(state_to_value[new_state] for new_state in moves(*state, track))
                    else:
                        possibilities = moves(*state, track)
                        state_to_value[state] = -MOVE_COST + DISCOUNT * sum(state_to_value[move] for move in possibilities) / len(possibilities)

    return state_to_value


def _validated(vx, vy):
    return sorted([MIN_V, vx, MAX_V])[1], sorted([MIN_V, vy, MAX_V])[1]


def expected_value(x, y, vx, vy, dvx, dvy, track, state_to_value):
    if not on_road(x, y, track):
        return PENALTY
    if track[y][x] == FINISH:
        return REWARD

    new_vx, new_vy = vx + dvx, vy + dvy

    if track[y][x] == ROAD:
        new_vx, new_vy = _validated(new_vx, new_vy)
        return state_to_value[(x + new_vx, y + new_vy, new_vx, new_vy)]
    else:
        new_vs = [_validated(new_vx + rx, new_vy + ry) for rx in ALL_RS for ry in ALL_RS]
        return sum(state_to_value[(x + rvx, y + rvy, rvx, rvy)] for rvx, rvy in new_vs) / len(new_vs)


def values_to_policy(state_to_value, track):
    return {state: max(((dvx, dvy) for dvx in ALL_DVS for dvy in ALL_DVS),
                         key=lambda action: expected_value(*state, *action, track, state_to_value)) for state in state_to_value}

#for i in [1,2,3,6,8,9,10,11]:
for i in [10]:
    with open("task{}.txt".format(i)) as f:
        track = [line for line in [[char for char in line if char in FIELDS] for line in f.readlines()] if line]

    policy = values_to_policy(value_iteration(*parse(track), ITERATIONS), track)

    with open("policy_for_task{}.txt".format(i), 'w') as f:
        f.writelines("{} {} {} {} {} {}\n".format(*state, *change)
                        for state, change in policy.items())

    print("Policy done for task{}.txt".format(i))
