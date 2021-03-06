import os
import matplotlib.pyplot as plt
from collections import deque
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
                matrix[i][j] = 0 # cho c??c b???c t?????ng mang gi?? tr??? 0

            elif matrix[i][j] == ' ':
                if (i == 0) or (i == len(matrix) - 1) or (j == 0) or (j == len(matrix[0]) - 1):
                    end = (i, j)  # ??i???m k???t th??c ????? tho??t ra ngo??i
                matrix[i][j] = 1 # cho c??c ???????ng ??i mang gi?? tr??? 1

            elif matrix[i][j] == 'S':
                start = (i, j)  # ??i???m b???t ?????u

    return start, end, matrix


# thu???t to??n Breath-First Search
def find_path_BFS(start, end, matrix):
    width = len(matrix[0])
    height = len(matrix)

    # List l??u t???a ????? h?????ng ??i c???a ??i???m ??ang x??t (ph???i, tr??i, l??n, xu???ng)
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    queue = deque()
    # Th??m v??o h??ng ?????i 1 tuple bao g???m: t???a ????? ??i???m, chi ph??, 1 list danh s??ch c??c ??i???m ???? ??i qua
    queue.appendleft((start[0], start[1], 0, [start[0], start[1]]))
    # m???ng ????nh d???u c??c ??i???m ch??a ??i qua
    visited = [[0] * width for i in range(height)]
    while queue:
        # L???y t???a ????? trong h??ng ?????i
        coord = queue.pop()
        # ????nh d???u ??i???m ???? ??i qua
        visited[coord[0]][coord[1]] = 1
        if coord[0] == end[0] and coord[1] == end[1]: #N???u ??i???m l???y ra c?? t???a ????? l?? ??i???m exit:
            route = []  # t???o list l??u ???????ng ??i
            tuple = ()  # t???o tuple l??u c??c ??i???m c???a ???????ng ??i
            for i in range(0, len(coord[3]), 2):
                tuple = (coord[3][i], coord[3][i + 1])
                route.append(tuple)
            return coord[2], route
        for dir in directions: # Duy???t qua c??c h?????ng ??i
            nr = coord[0] + dir[0]
            nc = coord[1] + dir[1]
            # N???u ??i???m ??i ti???p theo n???m trong m?? cung v?? ch??a ???????c ??i qua th?? th??m v??o h??ng ?????i
            if (nr < 0 or nr >= height or nc < 0 or nc >= width or matrix[nr][nc] == 0 or visited[nr][nc] == 1):
                continue
            else:
                # Th??m t???a ????? m???i v??o queue
                queue.appendleft((nr, nc, coord[2] + 1, coord[3] + [nr, nc]))

    return 0  # N???u kh??ng t??m ???????c ???????ng ??i tho??t ra ngo??i m?? cung tr??? v??? 0


# thu???t to??n Depth-First Search
def find_path_DFS(start, end, matrix):
    width = len(matrix[0])
    height = len(matrix)

    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    stack = deque()
    stack.append((start[0], start[1], 0, [start[0], start[1]]))
    visited = [[0] * width for i in range(height)]
    while stack:
        coord = stack.pop() # L???y t???a ????? trong stack
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
                # Th??m t???a ????? m???i v??o stack
                stack.append((nr, nc, coord[2] + 1, coord[3] + [nr, nc]))

    return 0 # N???u kh??ng t??m ???????c ???????ng ??i tho??t ra ngo??i m?? cung tr??? v??? 0


# Heuristic method 1: kho???ng c??ch Euclid
def distance_Euclid(start_x, start_y, end_x, end_y):
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


# thu???t to??n Greedy Best-First Search
def find_path_Greedy(start, end, matrix):
    width = len(matrix[0])
    height = len(matrix)

    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    # ch???n heuristic
    print('-----------------------------MENU-HEURISTIC-DISTANCE-----------------------------')
    print('Ch???n 1 trong 2 heuristic sau b???ng c??ch ???n s??? t????ng ???ng')
    print('1. distance Euclid')
    print('2. distance Manhattan')
    print('---------------------------------------------------------------------------------')
    choose = int(input('Nh???p l???a ch???n: '))
    while choose != 1 and choose != 2:
        choose = int(input('Nh???p l???i l???a ch???n (ch??? ???????c nh???p 1 ho???c 2): '))

    if choose == 1:
        dist_original = distance_Euclid(start[0], start[1], end[0], end[1])
    else:
        dist_original = distance_Manhattan(start[0], start[1], end[0], end[1])

    lst = [] # t???o list l??u kho???ng c??ch t??? ??i???m hi???n t???i ??ang x??t ?????n ????ch
    lst.append(dist_original)
    queue = []
    # th??m v??o h??ng ?????i 1 tuple bao g???m: t???a ????? ??i???m, chi ph??, 1 list danh s??ch c??c ??i???m ???? ??i qua, kho???ng c??ch t??? ??i???m ??ang x??t ?????n ????ch
    queue.append((start[0], start[1], 0, [start[0], start[1]], dist_original))
    visited = [[0] * width for i in range(height)]
    while queue:
        lst.sort()
        for i in range(0, len(queue)): # T??m ??i???m trong queue c?? gi?? tr??? kho???ng c??ch t???i ????ch nh??? nh???t
            if (lst[0] == queue[i][4]): break
        coord = queue[i] # L???y t???a ????? ??i???m c?? kho???ng c??ch t???i ????ch nh??? nh???t
        queue.pop(i) # X??a ??i???m ???? ra kh???i queue
        lst.pop(0) # X??a kho???ng c??ch nh??? nh???t hi???n t???i ra kh???i queue
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
                # T??nh kho???ng c??ch t??? ??i???m ti???p theo ???? t???i ????ch
                if choose == 1:
                    dist = distance_Euclid(nr, nc, end[0], end[1])
                else:
                    dist = distance_Manhattan(nr, nc, end[0], end[1])
                lst.append(dist) # th??m kho???ng c??ch t??? ??i???m ti???p theo t???i ????ch v??o list
                queue.append((nr, nc, coord[2] + 1, coord[3] + [nr, nc], dist))

    return 0 # N???u kh??ng t??m ???????c ???????ng ??i tho??t ra ngo??i m?? cung tr??? v??? 0


# thu???t to??n A*
def find_path_AStar(start, end, matrix):
    width = len(matrix[0])
    height = len(matrix)

    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    # ch???n heuristic
    print('-----------------------------MENU-HEURISTIC-DISTANCE-----------------------------')
    print('Ch???n 1 trong 2 heuristic sau b???ng c??ch ???n s??? t????ng ???ng')
    print('1. distance Euclid')
    print('2. distance Manhattan')
    print('---------------------------------------------------------------------------------')
    choose = int(input('Nh???p l???a ch???n: '))
    while choose != 1 and choose != 2:
        choose = int(input('Nh???p l???i l???a ch???n (ch??? ???????c nh???p 1 ho???c 2): '))
    if choose == 1:
        dist_original = distance_Euclid(start[0], start[1], end[0], end[1])
    else:
        dist_original = distance_Manhattan(start[0], start[1], end[0], end[1])

    lst = [] # list l??u t???ng kho???ng c??ch t??? start->??i???m hi???n t???i + ??i???m hi???n t???i->end
    lst.append(dist_original)
    queue = []
    # th??m v??o h??ng ?????i 1 tuple bao g???m: t???a ????? ??i???m, chi ph??, 1 list danh s??ch c??c ??i???m ???? ??i qua, kho???ng c??ch t??? ??i???m ??ang x??t ?????n ????ch
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
                    dist_start_to_x = distance_Euclid(start[0], start[1], nr, nc)
                    dist_x_to_end = distance_Euclid(nr, nc, end[0], end[1])
                else:
                    dist_start_to_x = distance_Manhattan(start[0], start[1], nr, nc)
                    dist_x_to_end = distance_Manhattan(nr, nc, end[0], end[1])
                # T??nh t???ng kho???ng c??ch t??? start ?????n ??i???m hi???n t???i v?? kho???ng c??ch t??? ??i???m hi???n t???i ?????n end
                dist = dist_start_to_x + dist_x_to_end
                lst.append(dist)
                queue.append((nr, nc, coord[2] + 1, coord[3] + [nr, nc], dist))

    return 0 # N???u kh??ng t??m ???????c ???????ng ??i tho??t ra ngo??i m?? cung tr??? v??? 0


# h??m ch????ng tr??nh ch??nh
def main():
    while True:

        # ch???n b???n ????? ????? t??m ki???m l???i ??i
        print('-----------------------------MENU-MAZE-MAP-NO-BONUS-POINTS-----------------------------')
        print('Nh???p l???a ch???n b???n ????? b???ng c??ch nh???p s??? t????ng ???ng v???i b???n ?????')
        print('1: B???n ????? b??nh th?????ng (kh??ng ph???c t???p)')
        print('2: B???n ????? c?? kho???ng c??ch t??? ??i???m b???t ?????u g???n ??i???m k???t th??c (theo ???????ng chim bay)')
        print('3: B???n ????? tr???ng (kh??ng c?? v???t c???n)')
        print('4: B???n ????? nhi???u v???t c???n ch??? c?? 1 ???????ng tho??t duy nh???t')
        print('5: B???n ????? l???n ph???c t???p, ch???t h???p v???i nhi???u v???t c???n')
        print('N???u mu???n tho??t (EXIT), k???t th??c phi??n l??m vi???c th?? nh???p s??? kh??c')
        print('----------------------------------------------------------------------------------------')
        choose_map = int(input('Nh???p l???a ch???n c???a b???n: '))
        if choose_map == 1:
            filename = 'maze_map_1.txt'
        elif choose_map == 2:
            filename = 'maze_map_2.txt'
        elif choose_map == 3:
            filename = 'maze_map_3.txt'
        elif choose_map == 4:
            filename = 'maze_map_4.txt'
        elif choose_map == 5:
            filename = 'maze_map_5.txt'
        else:
            print('Ch????ng tr??nh k???t th??c!')
            return 0
        start, end, binary_matrix = standardized_matrix(filename)

        # ch???n thu???t to??n t??m ki???m
        print('-----------------------------MENU-SEARCH-ALGORITHMS-----------------------------')
        print('H??y ch???n 1 trong 4 thu???t to??n t??m ki???m sau ????? gi???i quy???t b???ng c??ch nh???p s??? t????ng ???ng')
        print('1. Breadth-First Search')
        print('2. Depth-First Search')
        print('3. Greedy Best-First Search')
        print('4. A* algorithm')
        print('---------------------------------------------------------------------------------')
        choose_algorithm = int(input('Nh???p l???a ch???n c???a b???n: '))
        while choose_algorithm < 1 or choose_algorithm > 4:
            choose_algorithm = int(input('Nh???p l???i l???a ch???n (ch??? ???????c nh???p 1->4): '))
        if choose_algorithm == 1:
            value, route = find_path_BFS(start, end, binary_matrix)
        elif choose_algorithm == 2:
            value, route = find_path_DFS(start, end, binary_matrix)
        elif choose_algorithm == 3:
            value, route = find_path_Greedy(start, end, binary_matrix)
        else:
            value, route = find_path_AStar(start, end, binary_matrix)

        bonus_points, matrix = read_file(filename)
        print('Chi ph??:', value, '\nPath:', route)
        visualize_maze(matrix, bonus_points, start, end, route)


if __name__ == "__main__":
    main()