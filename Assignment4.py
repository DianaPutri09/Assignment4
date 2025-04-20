import heapq
import time

grid = [
    ['S', '1', '2', '3', '#', '5', 'G'],
    ['4', '5', '6', '7', '#', '8', '9'],
    ['5', '6', '#', '8', '9', '10', '11'],
    ['#', '7', '8', '9', '#', '11', '12'],
    ['6', '8', '10', '#', '12', '13', '14'],
    ['7', '9', '11', '12', '#', '14', '15'],
]

rows = len(grid)
cols = len(grid[0])

def find_position(symbol):
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == symbol:
                return r, c
    return None
def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


def elevation_cost(current, neighbor):
    
    if grid[current[0]][current[1]] in ['S', 'G']:
        current_cost = 0
    else:
        current_cost = int(grid[current[0]][current[1]])
    
    if grid[neighbor[0]][neighbor[1]] in ['S', 'G']:
        neighbor_cost = 0
    else:
        neighbor_cost = int(grid[neighbor[0]][neighbor[1]])
    
    return abs(current_cost - neighbor_cost)


def a_star(start, goal):
    open_list = []
    heapq.heappush(open_list, (0 + manhattan_distance(start, goal), 0, start, []))  # f, g, current, path
    visited = set()
    nodes_explored = 0
    
    while open_list:
        f, g, current, path = heapq.heappop(open_list)
        
        if current in visited:
            continue
        
        visited.add(current)
        path = path + [current]
        nodes_explored += 1
        
        if current == goal:
            return path, nodes_explored
        
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = current[0] + direction[0], current[1] + direction[1]
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] != '#' and (r, c) not in visited:
                g_new = g + elevation_cost(current, (r, c))
                f_new = g_new + manhattan_distance((r, c), goal)
                heapq.heappush(open_list, (f_new, g_new, (r, c), path))
    
    return None, nodes_explored  

def gbfs(start, goal):
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(start, goal), start, []))  # f, current, path
    visited = set()
    nodes_explored = 0
    
    while open_list:
        f, current, path = heapq.heappop(open_list)
        
        if current in visited:
            continue
        
        visited.add(current)
        path = path + [current]
        nodes_explored += 1
        
        if current == goal:
            return path, nodes_explored
        
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = current[0] + direction[0], current[1] + direction[1]
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] != '#' and (r, c) not in visited:
                heapq.heappush(open_list, (manhattan_distance((r, c), goal), (r, c), path))
    
    return None, nodes_explored 

def visualize_grid(path):
    grid_copy = [row.copy() for row in grid]
    for r, c in path:
        if grid_copy[r][c] != 'S' and grid_copy[r][c] != 'G' and grid_copy[r][c] != '#':
            grid_copy[r][c] = '*'
    return "\n".join(["".join(row) for row in grid_copy])


def run_comparison(start_symbol, goal_symbol):
    start = find_position(start_symbol)
    goal = find_position(goal_symbol)
    
    # GBFS
    start_time = time.time()
    gbfs_path, gbfs_nodes = gbfs(start, goal)
    gbfs_time = (time.time() - start_time) * 1000  # waktu dalam ms
    
    print("GBFS:")
    if gbfs_path:
        print("Path:")
        print(visualize_grid(gbfs_path))
        print(f"Nodes explored: {gbfs_nodes}")
        print(f"Time (ms): {gbfs_time:.4f}")
    else:
        print("No path found!")
    
    # A* 
    start_time = time.time()
    a_star_path, a_star_nodes = a_star(start, goal)
    a_star_time = (time.time() - start_time) * 1000  # waktu dalam ms
    
    print("\nA* :")
    if a_star_path:
        print("Path:")
        print(visualize_grid(a_star_path))
        print(f"Nodes explored: {a_star_nodes}")
        print(f"Time (ms): {a_star_time:.4f}")
    else:
        print("No path found!")

run_comparison('S', 'G')
