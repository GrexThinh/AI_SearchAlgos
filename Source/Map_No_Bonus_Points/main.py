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
                matrix[i][j] = 0 # cho các bức tường mang giá trị 0

            elif matrix[i][j] == ' ':
                if (i == 0) or (i == len(matrix) - 1) or (j == 0) or (j == len(matrix[0]) - 1):
                    end = (i, j)  # điểm kết thúc để thoát ra ngoài
                matrix[i][j] = 1 # cho các đường đi mang giá trị 1

            elif matrix[i][j] == 'S':
                start = (i, j)  # điểm bắt đầu

    return start, end, matrix


# thuật toán Breath-First Search
def find_path_BFS(start, end, matrix):
    width = len(matrix[0])
    height = len(matrix)

    # List lưu tọa độ hướng đi của điểm đang xét (phải, trái, lên, xuống)
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    queue = deque()
    # Thêm vào hàng đợi 1 tuple bao gồm: tọa độ điểm, chi phí, 1 list danh sách các điểm đã đi qua
    queue.appendleft((start[0], start[1], 0, [start[0], start[1]]))
    # mảng đánh dấu các điểm chưa đi qua
    visited = [[0] * width for i in range(height)]
    while queue:
        # Lấy tọa độ trong hàng đợi
        coord = queue.pop()
        # Đánh dấu điểm đã đi qua
        visited[coord[0]][coord[1]] = 1
        if coord[0] == end[0] and coord[1] == end[1]: #Nếu điểm lấy ra có tọa độ là điểm exit:
            route = []  # tạo list lưu đường đi
            tuple = ()  # tạo tuple lưu các điểm của đường đi
            for i in range(0, len(coord[3]), 2):
                tuple = (coord[3][i], coord[3][i + 1])
                route.append(tuple)
            return coord[2], route
        for dir in directions: # Duyệt qua các hướng đi
            nr = coord[0] + dir[0]
            nc = coord[1] + dir[1]
            # Nếu điểm đi tiếp theo nằm trong mê cung và chưa được đi qua thì thêm vào hàng đợi
            if (nr < 0 or nr >= height or nc < 0 or nc >= width or matrix[nr][nc] == 0 or visited[nr][nc] == 1):
                continue
            else:
                # Thêm tọa độ mới vào queue
                queue.appendleft((nr, nc, coord[2] + 1, coord[3] + [nr, nc]))

    return 0  # Nếu không tìm được đường đi thoát ra ngoài mê cung trả về 0


# thuật toán Depth-First Search
def find_path_DFS(start, end, matrix):
    width = len(matrix[0])
    height = len(matrix)

    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    stack = deque()
    stack.append((start[0], start[1], 0, [start[0], start[1]]))
    visited = [[0] * width for i in range(height)]
    while stack:
        coord = stack.pop() # Lấy tọa độ trong stack
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
                # Thêm tọa độ mới vào stack
                stack.append((nr, nc, coord[2] + 1, coord[3] + [nr, nc]))

    return 0 # Nếu không tìm được đường đi thoát ra ngoài mê cung trả về 0


# Heuristic method 1: khoảng cách Euclid
def distance_Euclid(start_x, start_y, end_x, end_y):
    if (start_x == end_x and start_y == end_y):
        return 0
    elif (start_x == end_x):
        return abs(end_y - start_y)
    elif (start_y == end_y):
        return abs(end_x - start_x)
    else:
        return math.sqrt((end_y - start_y) * (end_y - start_y) + (end_x - start_x) * (end_x - start_x))


# Heuristic method 2: khoảng cách Manhattan
def distance_Manhattan(start_x, start_y, end_x, end_y):
    return abs(start_x - end_x) + abs(start_y - end_y)


# thuật toán Greedy Best-First Search
def find_path_Greedy(start, end, matrix):
    width = len(matrix[0])
    height = len(matrix)

    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    # chọn heuristic
    print('-----------------------------MENU-HEURISTIC-DISTANCE-----------------------------')
    print('Chọn 1 trong 2 heuristic sau bằng cách ấn số tương ứng')
    print('1. distance Euclid')
    print('2. distance Manhattan')
    print('---------------------------------------------------------------------------------')
    choose = int(input('Nhập lựa chọn: '))
    while choose != 1 and choose != 2:
        choose = int(input('Nhập lại lựa chọn (chỉ được nhập 1 hoặc 2): '))

    if choose == 1:
        dist_original = distance_Euclid(start[0], start[1], end[0], end[1])
    else:
        dist_original = distance_Manhattan(start[0], start[1], end[0], end[1])

    lst = [] # tạo list lưu khoảng cách từ điểm hiện tại đang xét đến đích
    lst.append(dist_original)
    queue = []
    # thêm vào hàng đợi 1 tuple bao gồm: tọa độ điểm, chi phí, 1 list danh sách các điểm đã đi qua, khoảng cách từ điểm đang xét đến đích
    queue.append((start[0], start[1], 0, [start[0], start[1]], dist_original))
    visited = [[0] * width for i in range(height)]
    while queue:
        lst.sort()
        for i in range(0, len(queue)): # Tìm điểm trong queue có giá trị khoảng cách tới đích nhỏ nhất
            if (lst[0] == queue[i][4]): break
        coord = queue[i] # Lấy tọa độ điểm có khoảng cách tới đích nhỏ nhất
        queue.pop(i) # Xóa điểm đó ra khỏi queue
        lst.pop(0) # Xóa khoảng cách nhỏ nhất hiện tại ra khỏi queue
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
                # Tính khoảng cách từ điểm tiếp theo đó tới đích
                if choose == 1:
                    dist = distance_Euclid(nr, nc, end[0], end[1])
                else:
                    dist = distance_Manhattan(nr, nc, end[0], end[1])
                lst.append(dist) # thêm khoảng cách từ điểm tiếp theo tới đích vào list
                queue.append((nr, nc, coord[2] + 1, coord[3] + [nr, nc], dist))

    return 0 # Nếu không tìm được đường đi thoát ra ngoài mê cung trả về 0


# thuật toán A*
def find_path_AStar(start, end, matrix):
    width = len(matrix[0])
    height = len(matrix)

    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    # chọn heuristic
    print('-----------------------------MENU-HEURISTIC-DISTANCE-----------------------------')
    print('Chọn 1 trong 2 heuristic sau bằng cách ấn số tương ứng')
    print('1. distance Euclid')
    print('2. distance Manhattan')
    print('---------------------------------------------------------------------------------')
    choose = int(input('Nhập lựa chọn: '))
    while choose != 1 and choose != 2:
        choose = int(input('Nhập lại lựa chọn (chỉ được nhập 1 hoặc 2): '))
    if choose == 1:
        dist_original = distance_Euclid(start[0], start[1], end[0], end[1])
    else:
        dist_original = distance_Manhattan(start[0], start[1], end[0], end[1])

    lst = [] # list lưu tổng khoảng cách từ start->điểm hiện tại + điểm hiện tại->end
    lst.append(dist_original)
    queue = []
    # thêm vào hàng đợi 1 tuple bao gồm: tọa độ điểm, chi phí, 1 list danh sách các điểm đã đi qua, khoảng cách từ điểm đang xét đến đích
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
                # Tính tổng khoảng cách từ start đến điểm hiện tại và khoảng cách từ điểm hiện tại đến end
                dist = dist_start_to_x + dist_x_to_end
                lst.append(dist)
                queue.append((nr, nc, coord[2] + 1, coord[3] + [nr, nc], dist))

    return 0 # Nếu không tìm được đường đi thoát ra ngoài mê cung trả về 0


# hàm chương trình chính
def main():
    while True:

        # chọn bản đồ để tìm kiếm lối đi
        print('-----------------------------MENU-MAZE-MAP-NO-BONUS-POINTS-----------------------------')
        print('Nhập lựa chọn bản đồ bằng cách nhập số tương ứng với bản đồ')
        print('1: Bản đồ bình thường (không phức tạp)')
        print('2: Bản đồ có khoảng cách từ điểm bắt đầu gần điểm kết thúc (theo đường chim bay)')
        print('3: Bản đồ trống (không có vật cản)')
        print('4: Bản đồ nhiều vật cản chỉ có 1 đường thoát duy nhất')
        print('5: Bản đồ lớn phức tạp, chật hẹp với nhiều vật cản')
        print('Nếu muốn thoát (EXIT), kết thúc phiên làm việc thì nhập số khác')
        print('----------------------------------------------------------------------------------------')
        choose_map = int(input('Nhập lựa chọn của bạn: '))
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
            print('Chương trình kết thúc!')
            return 0
        start, end, binary_matrix = standardized_matrix(filename)

        # chọn thuật toán tìm kiếm
        print('-----------------------------MENU-SEARCH-ALGORITHMS-----------------------------')
        print('Hãy chọn 1 trong 4 thuật toán tìm kiếm sau để giải quyết bằng cách nhập số tương ứng')
        print('1. Breadth-First Search')
        print('2. Depth-First Search')
        print('3. Greedy Best-First Search')
        print('4. A* algorithm')
        print('---------------------------------------------------------------------------------')
        choose_algorithm = int(input('Nhập lựa chọn của bạn: '))
        while choose_algorithm < 1 or choose_algorithm > 4:
            choose_algorithm = int(input('Nhập lại lựa chọn (chỉ được nhập 1->4): '))
        if choose_algorithm == 1:
            value, route = find_path_BFS(start, end, binary_matrix)
        elif choose_algorithm == 2:
            value, route = find_path_DFS(start, end, binary_matrix)
        elif choose_algorithm == 3:
            value, route = find_path_Greedy(start, end, binary_matrix)
        else:
            value, route = find_path_AStar(start, end, binary_matrix)

        bonus_points, matrix = read_file(filename)
        print('Chi phí:', value, '\nPath:', route)
        visualize_maze(matrix, bonus_points, start, end, route)


if __name__ == "__main__":
    main()