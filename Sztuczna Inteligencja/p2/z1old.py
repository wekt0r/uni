def solve3(n, m, row_values, column_values): #n is k
    queue = PriorityQueue() #append, pop

    def transpose(matrix):
        return [[matrix[a][b] for a in range(n)] for b in range(m)]

    def h(board,i):
        return -sum(sum(seq[:i] == column[:i] for seq in generate_all(column_values[j], n)) for j,column in enumerate(transpose(board)))

    board = [[0 for _ in range(m)] for _ in range(n)]
    #print(board, row_values, column_values)
    queue.put((h(board, 0), board,0))
    already_visited = set()

    def valid(board):
        return (not any(opt_dist(row, val) for row,val in zip(board, row_values))
               and not any(opt_dist(col, val) for col, val in zip(transpose(board), column_values)))

    def possibly_valid(board,i):
        for j,column in enumerate(transpose(board)):
            print("Hello {}, values {} - is matching {}".format(column[:i], column_values[j], matching_prefix(column[:i],column_values[j])))
        res = all(matching_prefix(column[:i],column_values[j]) for j,column in enumerate(transpose(board)))
        #if not res:
        #    print(print_board(board))
        #    print(row_values, column_values)
        return res

    while True:
        v, board, i = queue.get_nowait()
        if repr(board) not in already_visited:
            already_visited.add(repr(board))
            if i == n:
                if valid(board):
                    print("\n".join("".join("#" if char else "." for char in row) for row in board))
                    return "\n".join("".join("#" if char else "." for char in row) for row in board)
            else:
                for possible_row in generate_all(row_values[i], m):
                    new_board = dpcp(board)
                    new_board[i] = possible_row
                    if possibly_valid(new_board, i):
                        queue.put((h(new_board, i+1), new_board, i+1))

def solve(n, m, row_values, column_values): #n is k
    stack = deque() #append, pop

    preprocessed = [generate_all(row_values[i], m) for i in range(n)]
    board = [[0 for _ in range(m)] for _ in range(n)]
    #print(board, row_values, column_values)
    stack.append((board,0))
    already_visited = set()
    def transpose(matrix):
        return [[matrix[a][b] for a in range(n)] for b in range(m)]

    def valid(board):
        return (all(block_values(row) == val for row,val in zip(board, row_values))
               and all(block_values(col) == val for col, val in zip(transpose(board), column_values)))

    def possibly_valid(board,i):
        return all(matching_prefix(column[:i],column_values[j]) for j,column in enumerate(transpose(board)))

    while stack:
        board, i = stack.pop()
        if repr(board) not in already_visited:
            already_visited.add(repr(board))
            if i == n:
                if valid(board):
                    print("\n".join("".join("#" if char else "." for char in row) for row in board))
                    return "\n".join("".join("#" if char else "." for char in row) for row in board)
            else:
                all_possiblities = preprocessed[i]
                shuffle(all_possiblities)
                for possible_row in all_possiblities:
                    new_board = dpcp(board)
                    new_board[i] = possible_row
                    if possibly_valid(new_board, i):
                        stack.append((new_board, i+1))

def solve2(k, m, row_values, column_values):
    #row_values :: [int]
    #column_values :: [int]
    all_colored = reduce(lambda x,y: x + sum(y), row_values, 0)
    all_on_board = k*m
    n = k
    seed = [1]*all_colored + [0]*(all_on_board-all_colored)
    preprocessed_rows = [generate_all(row_values[i], m) for i in range(n)]
    preprocessed_columns = [generate_all(column_values[i], n) for i in range(m)]
    def transpose(matrix):
        return [[matrix[j][i] for j in range(n)] for i in range(m)]

    def valid(board):
        return (all(block_values(row) == val for row,val in zip(board, row_values))
               and all(block_values(col) == val for col, val in zip(transpose(board), column_values)))

    timeout = 30*n*(n+2)
    board = [[choice(seed) for _ in range(m)] for _ in range(n)]
    #fillable_rows = [i for i,a in enumerate(row_values) if board[i] not in list(generate_all(a,m))]
    counter = 0
    while not valid(board):
        counter += 1
        if counter == timeout:
        #    print("\n".join("".join("#" if char else "." for char in row) for row in board))
            print("COUNTER {} REACHED - I'M DRAWING BOARD AGAIN".format(timeout))
            timeout += 100
            counter = 0
            for _ in range(n*n//2):
                i,j = choice([(x,y) for x in range(n) for y in range(m)])
                board[i][j] = 1 - board[i][j]
            #board = [[choice([0,1]) for _ in range(m)] for _ in range(n)]
        i = randint(0,k-1)
        best_j = None
        v= opt_dist(board[i], row_values[i], preprocessed_rows[i]) + n
        t = list(range(m))
        shuffle(t)
        for j in t:
            new_board = dpcp(board)
            new_board[i][j] = 1 - new_board[i][j]
    #        print("Hello - i have {}, {}".format(new_board[i], row_values[i]))
            value = opt_dist(new_board[i], row_values[i], preprocessed_rows[i])
            #print("hi", new_board[i], row_values[i])
            value += opt_dist([new_board[k][j] for k in range(n)], column_values[j], preprocessed_columns[j])
            if value < v:
                v = value
                best_j = j
        board[i][best_j] = 1 - new_board[i][best_j]
        if(choice([1] + [0]*70)):
            board[randint(0,k-1)][randint(0,m-1)] = 0
    #    print(fillable_rows)
    print("FINALLY:")
    print(counter)
    #print("\n".join(" ".join(map(str,row)) for row in board))
    print("\n".join("".join("#" if char else "." for char in row) for row in board))
    return "\n".join("".join("#" if char else "." for char in row) for row in board)
