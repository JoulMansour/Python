from typing import List, Tuple, Set, Optional



Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    if picture[row][col] == 0:
        return 0
    seen_cells = 1
    rows = len(picture)
    cols = len(picture[0])
    for i in range(col+1, cols):
        if picture[row][i] == 0:
            break
        else:
            seen_cells += 1
    for j in range(col-1, -1, -1):
        if picture[row][j] == 0:
            break
        else:
            seen_cells += 1
    for y in range(row-1, -1, -1):
        if picture[y][col] == 0:
            break
        else:
            seen_cells += 1
    for z in range(row+1, rows):
        if picture[z][col] == 0:
            break
        else:
            seen_cells += 1
    return seen_cells




def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    if picture[row][col] != 1:
        return 0
    seen_cells = 1
    rows = len(picture)
    cols = len(picture[0])
    for i in range(col+1, cols):
        if picture[row][i] == 0 or picture[row][i] == -1:
            break
        else:
            seen_cells += 1
    for j in range(col-1, -1, -1):
        if picture[row][j] == 0 or picture[row][j] == -1:
            break
        else:
            seen_cells += 1
    for y in range(row-1, -1, -1):
        if picture[y][col] == 0 or picture[y][col] == -1:
            break
        else:
            seen_cells += 1
    for z in range(row+1, rows):
        if picture[z][col] == 0 or picture[z][col] == -1:
            break
        else:
            seen_cells += 1
    return seen_cells




def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    for (row, col, seen) in constraints_set:
        min_seen = min_seen_cells(picture, row, col)
        max_seen = max_seen_cells(picture, row, col)

        if not (min_seen <= seen <= max_seen):
            return 0

    if all(seen == min_seen_cells(picture, row, col) == max_seen_cells(picture, row, col) for (row, col, seen) in constraints_set):
        return 1
    else:
        return 2



def solve_puzzle(constraints_set: Set[Tuple[int, int, int]], n: int, m: int) -> Optional[List[List[int]]]:
    def is_valid(picture: List[List[int]], row: int, col: int) -> bool:
        return check_constraints(picture, constraints_set) != 0

    def solve_puzzle_helper(picture: List[List[int]], row: int, col: int) -> bool:
        if row == n:
            return check_constraints(picture, constraints_set) == 1
        next_row, next_col = (row, col + 1) if col + 1 < m else (row + 1, 0)
        picture[row][col] = 0
        if is_valid(picture, row, col) and solve_puzzle_helper(picture, next_row, next_col):
            return True
        picture[row][col] = 1
        if is_valid(picture, row, col) and solve_puzzle_helper(picture, next_row, next_col):
            return True
        picture[row][col] = -1
        return False
    picture = [[-1 for _ in range(m)] for _ in range(n)]
    if solve_puzzle_helper(picture, 0, 0):
        return picture
    else:
        return None

def count_solutions(picture: Picture, constraints_set: Set[Constraint], n: int, m: int, row: int, col: int) -> int:
    if row == n:
        return 1 if check_constraints(picture, constraints_set) == 1 else 0
    next_row, next_col = (row, col + 1) if col + 1 < m else (row + 1, 0)
    if picture[row][col] != -1:
        return count_solutions(picture, constraints_set, n, m, next_row, next_col)
    count = 0
    for i in [0, 1]:
        picture[row][col] = i
        if check_constraints(picture, constraints_set) != 0:
            count += count_solutions(picture, constraints_set, n, m, next_row, next_col)
    picture[row][col] = -1
    return count
def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    initial_picture = [[-1] * m for _ in range(n)]
    return count_solutions(initial_picture, constraints_set, n, m, 0, 0)


def generate_puzzle(picture: Picture) -> Set[Tuple[int, int, int]]:
    constraints_set = set()
    n = len(picture)
    m = len(picture[0])

    for row in range(n):
        for col in range(m):
            if picture[row][col] == 1:
                seen_cells = count_visible_cells(picture, row, col)
                constraints_set.add((row, col, seen_cells))

    return constraints_set


def count_visible_cells(picture: Picture, row: int, col: int) -> int:
    seen_cells = 0
    n = len(picture)
    m = len(picture[0])

    # Check cells to the right
    for j in range(col + 1, m):
        if picture[row][j] != -1:
            seen_cells += 1
        if picture[row][j] == 0:
            break

    # Check cells to the left
    for j in range(col - 1, -1, -1):
        if picture[row][j] != -1:
            seen_cells += 1
        if picture[row][j] == 0:
            break

    # Check cells below
    for i in range(row + 1, n):
        if picture[i][col] != -1:
            seen_cells += 1
        if picture[i][col] == 0:
            break

    # Check cells above
    for i in range(row - 1, -1, -1):
        if picture[i][col] != -1:
            seen_cells += 1
        if picture[i][col] == 0:
            break

    return seen_cells


# Example usage:
picture = [
    [1, 0, 0],
    [1, 1, 1]
]

print(generate_puzzle(picture))
