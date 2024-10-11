from collections import deque

class Problem():
    def __init__(self):
        self.r, self.c, self.k = map(int, input().split())
        self.board = [[0 for _ in range(self.c)] for _ in range(self.r+3)]
        self.exits = [[False for _ in range(self.c)] for _ in range(self.r+3)]
        self.score = 0

    def move(self, id, c, d):
        # 골렘은 [1, c]에서 시작
        x = 1
        y = c
        # 방향 d는 0, 1, 2, 3 중 하나이며 각각 북, 동, 남, 서를 의미한다
        while True:
            if x==self.r+1:
                self.terminate(id, x, y, d)
                return

            # 남쪽으로 내려갈 수 있는 경우
            if 1 <= y < self.c and self.board[x+2][y]==0 and self.board[x+1][y-1]==0 and self.board[x+1][y+1]==0:
                # 남쪽으로 한 칸 내려간다
                x += 1

            # 위의 방법으로 이동할 수 없다면 서쪽 방향으로 한 칸 회전한다
            # 서쪽으로 갔을 때 내려갈 수 있다면
            else:
                # 서쪽으로 이동할 수 있다면
                if y > 1 and self.board[x][y-2]==0 and self.board[x-1][y-1]==0 and self.board[x+1][y-1]==0:
                    temp_y = y - 1
                    # 이동해서 아래로 내려갈 수 있는지 확인
                    if self.board[x+2][temp_y]==0 and self.board[x+1][temp_y-1]==0 and self.board[x+1][temp_y+1]==0:
                        y = temp_y
                        d -= 1
                        if d < 0:
                            d += 4
                        continue
                # 동쪽으로 이동할 수 있다면
                if y < self.c - 2 and self.board[x][y+2]==0 and self.board[x-1][y+1]==0 and self.board[x+1][y+1]==0:
                    temp_y = y + 1
                    # 이동해서 아래로 내려갈 수 있는지 확인
                    if self.board[x+2][temp_y]==0 and self.board[x+1][temp_y-1]==0 and self.board[x+1][temp_y+1]==0:
                        y = temp_y
                        d += 1
                        if d > 3:
                            d -= 4
                        continue
                self.terminate(id, x, y, d)
                return

    def terminate(self, id, x, y, d):
        # 이동을 종료한다

        # 골렘의 몸 일부가 여전히 숲을 벗어난 상태라면 숲을 리셋한다
        if x <= 2:
            self.board = [[0 for _ in range(self.c)] for _ in range(self.r + 3)]
            self.exits = [[False for _ in range(self.c)] for _ in range(self.r + 3)]
            return

        # 위치 마킹
        self.board[x][y] = id
        self.board[x - 1][y] = id
        self.board[x + 1][y] = id
        self.board[x][y - 1] = id
        self.board[x][y + 1] = id

        # 출구 마킹 (북, 동, 남, 서)
        if d == 0:
            self.exits[x - 1][y] = True
        elif d == 1:
            self.exits[x][y + 1] = True
        elif d == 2:
            self.exits[x + 1][y] = True
        elif d == 3:
            self.exits[x][y - 1] = True

        # 정령은 bfs를 통해 이동 시작
        q = deque()
        q.append([x, y])

        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]

        max_row = 0
        visited = [[False for _ in range(self.c)] for _ in range(self.r + 3)]
        while q:
            row, col = q.popleft()
            if visited[row][col]:
                continue
            visited[row][col] = True

            if row > max_row:
                max_row = row

            for i in range(len(dx)):
                nx = row + dx[i]
                ny = col + dy[i]

                if nx < 0 or nx >= self.r + 3 or ny < 0 or ny >= self.c:
                    continue
                if visited[nx][ny]:
                    continue
                if self.board[nx][ny] == 0:
                    continue
                if self.board[nx][ny] != self.board[row][col] and self.exits[row][col] == False:
                    continue
                q.append([nx, ny])
        self.score += max_row - 2

def main():
    instance = Problem()

    # 각 골렘의 정보가 주어진다
    for id in range(1, instance.k+1):
    #for id in range(1, 3):
        c, d = map(int, input().split())
        c -= 1

        # 골렘 이동
        instance.move(id, c, d)
        
    print(instance.score)

if __name__ == "__main__":
    main()