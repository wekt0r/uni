from collections import deque


fields = offroad, road, oil, finish, start = '.#oes'

reward, penalty = 100, -200
gamma = .99
move_cost = .1

min_v, max_v = -3, 3
possible_dvs = {-1, 0, 1}
possible_rs = {-1, 0, 1}


def extract_start(track):
    new_track = []
    endpoints = set()

    for y, row in enumerate(track):
        new_row = []

        for x, field in enumerate(row):
            if field == start:
                start_pos = x, y
                new_row += [road]
            else:
                if field == finish:
                    endpoints |= {(x, y)}
                new_row += [field]

        if new_row:
            new_track += [new_row]

    return start_pos, endpoints, new_track     # I assume there is start in the track


def on_road(x, y, track):
    w, h = len(track[0]), len(track)
    return 0 <= x < w and 0 <= y < h and track[y][x] != offroad


def moves(x, y, vx, vy, track):
    actions = {(dvx, dvy) for dvx in possible_dvs for dvy in possible_dvs}

    if track[y][x] == oil:
        actions = {(dvx + rx, dvy + ry) for dvx, dvy in actions for rx in possible_rs for ry in possible_rs}

    vs = {(vx + dvx, vy + dvy) for dvx, dvy in actions}
    return {(x + new_vx, y + new_vy, new_vx, new_vy) for new_vx, new_vy in vs if min_v <= new_vx <= max_v and min_v <= new_vy <= max_v}


def possible_states(track, start_pos):
    states = set()
    to_check = deque({(*start_pos, 0, 0)})

    while to_check:
        state = x, y, vx, vy = to_check.pop()
        states |= {state}

        if on_road(x, y, track):
            to_check.extend(moves(x, y, vx, vy, track) - states)

    return states


def track_at_state(x, y, vx, vy, board):
    return board[y][x]


def value_iteration(start_pos, endpoints, track, iterations):
    def init_value_at(x, y, vx, vy):
        if not on_road(x, y, track):
            return penalty
        elif track[y][x] == finish:
            return reward
        else:
            return 0

    state_to_value = {state: init_value_at(*state) for state in possible_states(track, start_pos)}

    for i in range(iterations):
        for state in state_to_value:
            x, y, _, _ = state      # I discard vx and vy

            if on_road(x, y, track):
                if state_to_value[state] not in {reward, penalty}:
                    if track[y][x] != oil:
                        state_to_value[state] = -move_cost + gamma * state_to_value[max(moves(*state, track),
                                                                                        key = lambda new_state: state_to_value[new_state])]
                    else:
                        possibilities = moves(*state, track)
                        state_to_value[state] = -move_cost + gamma * sum(state_to_value[move] for move in possibilities) / len(possibilities)

    return state_to_value


def correct_vs(vx, vy):
    return min(max_v, max(min_v, vx)), min(max_v, max(min_v, vy))


def expected_value(x, y, vx, vy, dvx, dvy, track, state_to_value):
    if not on_road(x, y, track):
        return penalty
    elif track[y][x] == finish:
        return reward

    new_vx, new_vy = vx + dvx, vy + dvy

    if track[y][x] == road:
        new_vx, new_vy = correct_vs(new_vx, new_vy)
        return state_to_value[(x + new_vx, y + new_vy, new_vx, new_vy)]
    else:
        # cannot be set, because some new states are more probable than other ones
        new_vs = [correct_vs(new_vx + rx, new_vy + ry) for rx in possible_rs for ry in possible_rs]
        return sum(state_to_value[(x + rvx, y + rvy, rvx, rvy)] for rvx, rvy in new_vs) / len(new_vs)


def values_to_policy(state_to_value, track):
    policy = {state: max(((dvx, dvy) for dvx in possible_dvs for dvy in possible_dvs),
                         key = lambda action: expected_value(*state, *action, track, state_to_value)) for state in state_to_value}
    return policy


def compute_policy(track, iterations):
    start_pos, endpoints, track = extract_start(track)
    return values_to_policy(value_iteration(start_pos, endpoints, track, iterations), track)


def policy_to_file(policy, filename):
    with open(filename, 'w') as file:
        file.writelines(str(x) + ' ' + str(y) + ' ' + str(vx) + ' ' + str(vy) + ' ' + str(dvx) + ' ' + str(dvy) + '\n'
                        for (x, y, vx, vy), (dvx, dvy) in policy.items())


def track_from_file(filename):
    with open(filename) as file:
        return [line for line in [[char for char in line if char in fields] for line in file.readlines()] if line]

for i in [10]:
    track = track_from_file("task{}.txt".format(i))
    policy = compute_policy(track, 2000)
    policy_to_file(policy, "policy_for_task{}.txt".format(i))
