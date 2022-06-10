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


# Heuristic method 1: khoảng cách Euclid
def distance_Educlid(start_x, start_y, end_x, end_y):
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


# thuật toán A*
def find_path_AStar(start, end, matrix, choose):
    width = len(matrix[0])
    height = len(matrix)
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    # Gọi hàm Heuristic đã chọn cho việc ăn điểm thưởng trong hàm
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


# hàm tìm khoảng cách ngắn nhất từ điểm đang xét đến các điểm tiếp theo trả về vị trí và tọa độ điểm đó trong danh sách
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


# Sử dụng thuật toán A* ăn tất cả điểm thưởng theo khoảng cách gần nhất với điểm đang đứng sau đó thoát ra ngoài
def find_matrix_with_bonus_points_Astar(start, end, bonus_points, matrix):
    current_pos = start
    n = len(bonus_points)
    route = []
    cost = 0
    sum_bonus = 0

    # chọn heuristic phục vụ tìm điểm thưởng gần nhất
    print('-----------------------------MENU-HEURISTIC-DISTANCE-----------------------------')
    print('Chọn 1 trong 2 heuristic sau bằng cách ấn số tương ứng')
    print('1. distance Euclid')
    print('2. distance Manhattan')
    print('---------------------------------------------------------------------------------')
    choose = int(input('Nhập lựa chọn: '))
    while choose != 1 and choose != 2:
        choose = int(input('Nhập lại lựa chọn (chỉ được nhập 1 hoặc 2): '))

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


# hàm chương trình chính
def main():
    while True:
        # chọn bản đồ để tìm kiếm lối đi
        print('-----------------------------MENU-MAZE-MAP-HAVE-BONUS-POINTS-----------------------------')
        print('Nhập lựa chọn bản đồ bằng cách nhập số tương ứng với bản đồ')
        print('1: Bản đồ bình thường (không phức tạp) có 2 điểm thưởng')
        print('2: Bản đồ có khoảng cách từ điểm bắt đầu gần điểm kết thúc (theo đường chim bay) có 5 điểm thưởng')
        print('3: Bản đồ lớn phức tạp, chật hẹp với nhiều vật cản có 10 điểm thưởng')
        print('Nếu muốn thoát (EXIT), kết thúc phiên làm việc thì nhập số khác')
        print('----------------------------------------------------------------------------------------')
        choose_map = int(input('Nhập lựa chọn của bạn: '))
        if choose_map == 1:
            filename = 'maze_bonusPoints_1.txt'
        elif choose_map == 2:
            filename = 'maze_bonusPoints_2.txt'
        elif choose_map == 3:
            filename = 'maze_bonusPoints_3.txt'
        else:
            print('Chương trình kết thúc!')
            return 0
        start, end, binary_matrix = standardized_matrix(filename)
        bonus_points, matrix = read_file(filename)
        value, sum_bonus, route = find_matrix_with_bonus_points_Astar(start, end, bonus_points, binary_matrix)
        print('Chi phí:', value, '\nChi phí thật sự (đã cộng điểm thưởng):', value + sum_bonus, '\nPath:', route)
        bonus_points, matrix = read_file(filename)
        visualize_maze(matrix, bonus_points, start, end, route)


if __name__ == "__main__":
    main()