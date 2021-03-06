import os
import matplotlib.pyplot as plt
import math


def visualize_maze(matrix, bonus, start, end, route=[]):
    '''
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
  '''
    # 1. Define walls and array of direction based on the route
    walls = [(i, j) for i in range(len(matrix))
             for j in range(len(matrix[0])) if matrix[i][j] == 'x']

    if route:
        direction = []
        for i in range(1, len(route)):
            if route[i][0] - route[i - 1][0] > 0:
                direction.append('v')  # ^
            elif route[i][0] - route[i - 1][0] < 0:
                direction.append('^')  # v
            elif route[i][1] - route[i - 1][1] > 0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)

    # 2. Drawing the map
    ax = plt.figure(dpi=100).add_subplot(111)

    for i in ['top', 'bottom', 'right', 'left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls], [-i[0] for i in walls],
                marker='X', s=100, color='black')

    plt.scatter([i[1] for i in bonus], [-i[0] for i in bonus],
                marker='P', s=100, color='green')

    plt.scatter(start[1], -start[0], marker='*',
                s=100, color='gold')

    if route:
        for i in range(len(route) - 2):
            plt.scatter(route[i + 1][1], -route[i + 1][0],
                        marker=direction[i], color='silver')

    plt.text(end[1], -end[0], 'EXIT', color='red',
             horizontalalignment='center',
             verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')

    for _, point in enumerate(bonus):
        print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')


def read_file(file_name: str = 'maze.txt'):
    f = open(file_name, 'r')
    n_bonus_points = int(next(f)[:-1])
    bonus_points = []
    for i in range(n_bonus_points):
        x, y, reward = map(int, next(f)[:-1].split(' '))
        bonus_points.append((x, y, reward))

    text = f.read()
    matrix = [list(i) for i in text.splitlines()]
    f.close()

    return bonus_points, matrix


def standardized_matrix(filename):
    bonus_points, matrix = read_file(filename)
    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 'x':
                matrix[i][j] = 0

            elif matrix[i][j] == ' ':
                if (i == 0) or (i == len(matrix) - 1) or (j == 0) or (j == len(matrix[0]) - 1):
                    end = (i, j)
                matrix[i][j] = 1

            elif matrix[i][j] == 'S':
                start = (i, j)

    return start, end, matrix


# Heuristic method 1: kho???ng c??ch Euclid
def distance_Educlid(start_x, start_y, end_x, end_y):
    if (start_x == end_x and start_y == end_y):
        return 0
    elif (start_x == end_x):
        return abs(end_y - start_y)
    elif (start_y == end_y):
        return abs(end_x - start_x)
    else:
        return math.sqrt((end_y - start_y) * (end_y - start_y) + (end_x - start_x) * (end_x - start_x))


# Heuristic method 2: kho???ng c??ch Manhattan
def distance_Manhattan(start_x, start_y, end_x, end_y):
    return abs(start_x - end_x) + abs(start_y - end_y)


# thu???t to??n A*
def find_path_AStar(start, end, matrix, choose):
    width = len(matrix[0])
    height = len(matrix)
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    # G???i h??m Heuristic ???? ch???n cho vi???c ??n ??i???m th?????ng trong h??m
    if choose == 1:
        dist_original = distance_Educlid(start[0], start[1], end[0], end[1])
    elif choose == 2:
        dist_original = distance_Manhattan(start[0], start[1], end[0], end[1])
    lst = []
    lst.append(dist_original)
    queue = []
    queue.append((start[0], start[1], 0, [start[0], start[1]], dist_original))
    visited = [[0] * width for i in range(height)]
    while queue:
        lst.sort()
        for i in range(0, len(queue)):
            if (lst[0] == queue[i][4]): break
        coord = queue[i]
        queue.pop(i)
        lst.pop(0)
        visited[coord[0]][coord[1]] = 1
        if coord[0] == end[0] and coord[1] == end[1]:
            route = []
            tuple = ()
            for i in range(0, len(coord[3]), 2):
                tuple = (coord[3][i], coord[3][i + 1])
                route.append(tuple)
            return coord[2], route
        for dir in directions:
            nr = coord[0] + dir[0]
            nc = coord[1] + dir[1]
            if (nr < 0 or nr >= height or nc < 0 or nc >= width or matrix[nr][nc] == 0 or visited[nr][nc] == 1):
                continue
            else:
                if choose == 1:
                    dist_start_to_x = distance_Educlid(start[0], start[1], nr, nc)
                    dist_x_to_end = distance_Educlid(nr, nc, end[0], end[1])
                else:
                    dist_start_to_x = distance_Manhattan(start[0], start[1], nr, nc)
                    dist_x_to_end = distance_Manhattan(nr, nc, end[0], end[1])
                dist = dist_start_to_x + dist_x_to_end
                lst.append(dist)
                queue.append((nr, nc, coord[2] + 1, coord[3] + [nr, nc], dist))

    return 0


# h??m t??m kho???ng c??ch ng???n nh???t t??? ??i???m ??ang x??t ?????n c??c ??i???m ti???p theo tr??? v??? v??? tr?? v?? t???a ????? ??i???m ???? trong danh s??ch
def dist_min(current, next_poins, choose):
    point = []
    min_dist = 999999
    index = -1
    for i in range(len(next_poins)):
        if choose == 1:
            dist = distance_Educlid(current[0], current[1], next_poins[i][0], next_poins[i][1])
        else:
            dist = distance_Manhattan(current[0], current[1], next_poins[i][0], next_poins[i][1])
        if min_dist > dist:
            min_dist = dist
            point = next_poins[i]
            index = i

    return index, point


# S??? d???ng thu???t to??n A* ??n t???t c??? ??i???m th?????ng theo kho???ng c??ch g???n nh???t v???i ??i???m ??ang ?????ng sau ???? tho??t ra ngo??i
def find_matrix_with_bonus_points_Astar(start, end, bonus_points, matrix):
    current_pos = start
    n = len(bonus_points)
    route = []
    cost = 0
    sum_bonus = 0

    # ch???n heuristic ph???c v??? t??m ??i???m th?????ng g???n nh???t
    print('-----------------------------MENU-HEURISTIC-DISTANCE-----------------------------')
    print('Ch???n 1 trong 2 heuristic sau b???ng c??ch ???n s??? t????ng ???ng')
    print('1. distance Euclid')
    print('2. distance Manhattan')
    print('---------------------------------------------------------------------------------')
    choose = int(input('Nh???p l???a ch???n: '))
    while choose != 1 and choose != 2:
        choose = int(input('Nh???p l???i l???a ch???n (ch??? ???????c nh???p 1 ho???c 2): '))

    for i in range(n):
        index, next_point = dist_min(current_pos, bonus_points, choose)
        if find_path_AStar(current_pos, next_point, matrix, choose) == 0:
            bonus_points.pop(index)
        else:
            current_cost, current_route = find_path_AStar(current_pos, next_point, matrix, choose)
            cost += current_cost
            route.extend(current_route)
            bonus_points.pop(index)
            current_pos = next_point
            sum_bonus += current_pos[2]

    current_cost, current_route = find_path_AStar(current_pos, end, matrix, choose)
    cost += current_cost
    route.extend(current_route)

    return cost, sum_bonus, route


# h??m ch????ng tr??nh ch??nh
def main():
    while True:
        # ch???n b???n ????? ????? t??m ki???m l???i ??i
        print('-----------------------------MENU-MAZE-MAP-HAVE-BONUS-POINTS-----------------------------')
        print('Nh???p l???a ch???n b???n ????? b???ng c??ch nh???p s??? t????ng ???ng v???i b???n ?????')
        print('1: B???n ????? b??nh th?????ng (kh??ng ph???c t???p) c?? 2 ??i???m th?????ng')
        print('2: B???n ????? c?? kho???ng c??ch t??? ??i???m b???t ?????u g???n ??i???m k???t th??c (theo ???????ng chim bay) c?? 5 ??i???m th?????ng')
        print('3: B???n ????? l???n ph???c t???p, ch???t h???p v???i nhi???u v???t c???n c?? 10 ??i???m th?????ng')
        print('N???u mu???n tho??t (EXIT), k???t th??c phi??n l??m vi???c th?? nh???p s??? kh??c')
        print('----------------------------------------------------------------------------------------')
        choose_map = int(input('Nh???p l???a ch???n c???a b???n: '))
        if choose_map == 1:
            filename = 'maze_bonusPoints_1.txt'
        elif choose_map == 2:
            filename = 'maze_bonusPoints_2.txt'
        elif choose_map == 3:
            filename = 'maze_bonusPoints_3.txt'
        else:
            print('Ch????ng tr??nh k???t th??c!')
            return 0
        start, end, binary_matrix = standardized_matrix(filename)
        bonus_points, matrix = read_file(filename)
        value, sum_bonus, route = find_matrix_with_bonus_points_Astar(start, end, bonus_points, binary_matrix)
        print('Chi ph??:', value, '\nChi ph?? th???t s??? (???? c???ng ??i???m th?????ng):', value + sum_bonus, '\nPath:', route)
        bonus_points, matrix = read_file(filename)
        visualize_maze(matrix, bonus_points, start, end, route)


if __name__ == "__main__":
    main()