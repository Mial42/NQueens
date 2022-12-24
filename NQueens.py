import time
import random
from heapq import heappush, heappop


def get_next_unassigned_var(state):
    for row in range(0, len(state)):
        if state[row] is None:
            return row
    return None



def no_diagonal_interference(x1, y1, x2, y2):
    dX = abs(x1 - x2)
    dY = abs(y1 - y2)
    return dX != dY


def get_sorted_values(state, row): #The absolute values of the x and y coordinates should NOT be equal to each other
    size = len(state)
    pos = state[row]
    temp = state[:state.index(None)]
    my_set = set(temp)
    ans = []
    for x in range(0, size):
        debug_bool = True
        for previous_row in range(0, len(temp)):
            not_same_diagonal = no_diagonal_interference(previous_row, state[previous_row], row, x)         #if x != pos and not under_attack(state, row, x):
            if not not_same_diagonal:
                debug_bool = False
        if x != pos and x not in my_set and debug_bool: #x != pos
            ans.append(x)
    return ans


def random_get_sorted_values(state, row): #The absolute values of the x and y coordinates should NOT be equal to each other
    my_set = set(state)
    ans = []
    for x in range(0, len(state)):
        debug_bool = True
        if x not in my_set:
            for previous_row in range(0, state.index(None)):
                if not no_diagonal_interference(previous_row, state[previous_row], row, x):
                    debug_bool = False
                    break
            if debug_bool:
                ans.append(x)
    random.shuffle(ans)
    return ans


def print_board(state):
    size = len(state)
    for x in range(size):
        temp = ['.' for z in range(size)]
        temp[state[x]] = 'Q'
        print("  ".join(temp))


def goal_test(state):
    if None in set(state):
        return False
    return True


def csp_backtracking(state):
    if goal_test(state):
        return state
    row = get_next_unassigned_var(state)
    for pos in get_sorted_values(state, row):
        new_state = create_new_state(state, row, pos)
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None


def random_csp_backtracking(state, row):
    my_set = set(state)
    if row == 0:
        global my_start
        my_start = time.perf_counter()
    if time.perf_counter() - my_start > .3:
        return False
    if goal_test(state):
        return state
    for pos in random_get_sorted_values(state, row):
        if pos not in my_set:
            new_state = create_new_state(state, row, pos)
            result = random_csp_backtracking(new_state, row + 1)
            if result is not None:
                return result
    return None


def create_new_state(state, row, pos):
    temp = list(state)
    temp[row] = pos
    return temp


def test_solution(state):
    temp = set(state)
    if None in temp:
        return False
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                # print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                # print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                # print(var, "right", compare)
                return False
    return True


def create_state(x):
    return [None for z in range(x)]


def get_conflicts(state): #Returns the number of conflicts on a board
    conflicts = 0
    for row in range(len(state)):
        for x in range(0, len(state)):
            if row != x:
                if state[x] == state[row]:
                    conflicts = conflicts + 1
                if not no_diagonal_interference(row, state[row], x, state[x]):
                    conflicts = conflicts + 1
    return conflicts


def generate_random_board(size):
    board = [None for z in range(size)]
    for x in range(size):
        my_set = set(board)
        y = random.randint(0, size - 1)
        while y in my_set:
            y = random.randint(0, size - 1)
        board[x] = y
    return board


def incremental_repair(state):
    my_answer = state
    x = get_conflicts(my_answer)
    print(str(x))
    while x > 0:
        my_answer = place_most_conflicted(my_answer)
        x = get_conflicts(my_answer)
        print(str(x))
    return my_answer


def get_most_conflicted(state): #What if I returned a list in order of conflicts of what I've done?
    dict = {} #Number of conflicts : List of rows
    for row in range(len(state)):
        conflicts= 0
        for x in range(0, len(state)):
            if row != x:
                if state[x] == state[row]:
                    conflicts = conflicts + 1
                if not no_diagonal_interference(row, state[row], x, state[x]):
                    conflicts = conflicts + 1
        if conflicts in dict:
            temp = dict[conflicts]
            temp.append(row)
            dict[conflicts] = temp
        else:
            dict[conflicts] = [row]
    most_conflicts = max(dict)
    ans = dict[most_conflicts]
    random.shuffle(ans)
    return ans  #Return the row number in which there are most conflicts


def place_most_conflicted(state): #Randomly choose the space that would cause the fewest conflicts
    most_conflicted = get_most_conflicted(state).pop()
    temp = [] #List of tuples (number of conflicts, board)
    for x in range(len(state)):
        new_state = create_new_state(state, most_conflicted, x)
        new_conflicts = get_conflicts(new_state)
        heappush(temp, (new_conflicts, random.random(), new_state))
    heur, rand, v = heappop(temp)
    return v


def generate_middle_weighted_list(state): #What if I made it so that the last-moved conflicter couldn't be moved again?
    size = len(state) - 1
    ans = []
    for x in range(size // 2 + 1):
        ans.append(x)
        ans.append(size - x)
    ans = ans[::-1]
    if size % 2 == 0:
        ans = ans[1:]
    return ans


my_start = 0


def random_climb_the_beanstalk(state): #implement a timer reset every time if necessary
    while True:
        temp = random_csp_backtracking(state, 0)
        if temp:
            return temp


def incrementally_climb_the_beanstalk(size):
    while True:
        temp = incremental_repair(generate_random_board(size))
        if temp:
            return temp


#This chunk of code is to be run to get the signature for part 1
test_size = 31 #Use 101
# board = create_state(test_size)
# start = time.perf_counter()
# placeholder = random_climb_the_beanstalk(board) #limit: 44
# print(placeholder)
# end = time.perf_counter()
# print(str(end - start) + " seconds")
# print(test_solution(placeholder))

board = generate_random_board(test_size)
#print_board(board)
start = time.perf_counter()
z = incremental_repair(board)
end = time.perf_counter()
print(z)
print(str(end - start) + ' seconds')
print(test_solution(z))
