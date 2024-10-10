import sys
from collections import deque

input = sys.stdin.readline

class Problem():
    def __init__(self):
        """
        n: 격자의 크기
        m: 팀의 개수
        k: 라운드 수

        board: 격자
        score: 팀별 점수판
        """
        self.n, self.m, self.k = map(int, input().split())
        self.board = [list(map(int, input().split())) for _ in range(self.n)]
        self.scores = [0 for _ in range(self.m)]
        self.directions = [None for _ in range(self.m)]

        self.pos = [] # 팀별 위치 저장
        self.head_pos = []
        self.tail_pos = []
        self.sizes = []

        self.dx = [1, -1, 0, 0]
        self.dy = [0, 0, 1, -1]

        for i in range(self.n):
            for j in range(self.n):
                # 머리사람이 나오면 저장하고 bfs 시작
                if self.board[i][j] == 1:
                    # 머리사람 좌표 저장
                    self.head_pos.append([i, j])

                    q = deque()
                    q.append([i, j])

                    visited = [[False for _ in range(self.n)] for _ in range(self.n)]
                    length = 1
                    child = []
                    while q:
                        x, y = q.popleft()

                        # 이미 방문했다면 고려하지 않는다
                        if visited[x][y]:
                            continue
                        visited[x][y] = True

                        for k in range(len(self.dx)):
                            nx = x + self.dx[k]
                            ny = y + self.dy[k]

                            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                continue

                            if visited[nx][ny]:
                                continue

                            if self.board[nx][ny]==2:
                                child.append([nx, ny])

                            if self.board[nx][ny] == 3:
                                # 꼬리사람 좌표 저장
                                tail_pos = [nx, ny]
                                self.tail_pos.append(tail_pos)
                                visited[nx][ny] = True
                        if not q:
                            length += 1
                            q.extend(child)
                            child = []
                    self.sizes.append(length)


    def move(self, team):
        head = self.head_pos[team]
        x = head[0]
        y = head[1]
        tail = self.tail_pos[team]

        # 각 팀은 머리사람을 따라 한 칸 이동한다
        # 이동 방향 결정
        for i in range(len(self.dx)):
            nx = x + self.dx[i]
            ny = y + self.dy[i]
            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                continue

            # 꼬리사람이 있다면 그건 루트가 꽉 차있다는 말
            if self.board[nx][ny] == 3:
                for j in range(len(self.dx)):
                    nnx = x + self.dx[j]
                    nny = y + self.dy[j]
                    if nnx < 0 or nnx >= self.n or nny < 0 or nny >= self.n:
                        continue
                    if self.board[nnx][nny] == 2:
                        # 머리사람 새 위치 저장
                        self.board[nnx][nny] = 1

                        self.head_pos[team] = [nnx, nny]

                        # 꼬리사람 새 위치 저장
                        self.board[x][y] = 3
                        self.tail_pos[team] = [x, y]
                        self.board[nx][ny] = 2
                        return

        for i in range(len(self.dx)):
            nx = head[0] + self.dx[i]
            ny = head[1] + self.dy[i]
            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                continue
            # 빈칸이라면 거기로 이동한다
            elif self.board[nx][ny] == 4:
                self.board[nx][ny] = 1
                # 머리사람 새 위치 저장
                self.head_pos[team] = [nx, ny]
                # 머리사람이 원래 있던 자리는 2번으로 채운다
                self.board[head[0]][head[1]] = 2
                # 꼬리사람이 있던 자리는 빈 칸이 된다
                self.board[tail[0]][tail[1]] = 4
                # 꼬리사람 새 위치 저장
                for i in range(len(self.dx)):
                    nx = tail[0] + self.dx[i]
                    ny = tail[1] + self.dy[i]

                    if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                        continue
                    if self.board[nx][ny] == 2:
                        # 꼬리사람 위치 저장
                        self.tail_pos[team] = [nx, ny]
                        self.board[nx][ny] = 3

    def throw_ball(self, round):
        # 4*n 라운드마다 반복된다
        direction = (round // self.n) % 4
        position = round % self.n

        if direction == 0:
            # 왼쪽에서 오른쪽
            # round % self.n 행
            idx = 0
            while idx < self.n:
                if self.board[position][idx]==1:
                    # head_pos에서 찾아서 점수 주기
                    team = self.head_pos.index([position, idx])

                    self.scores[team] += 1

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3

                    return

                elif self.board[position][idx]==3:
                    # tail_pos에서 찾아서 점수 주기
                    team = self.tail_pos.index([position, idx])

                    for i in range(len(self.dx)):
                        nx = self.head_pos[team][0] + self.dx[i]
                        ny = self.head_pos[team][1] + self.dy[i]
                        if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                            continue

                        # 머리사람이 있다면 그건 루트가 꽉 차있다는 말이므로 내버려둔다 (굳이 바꿀 필요 없다)
                        if self.board[nx][ny] == 3:
                            self.scores[team] += self.sizes[team] ** 2

                            # 머리, 꼬리 위치 바꾸기
                            self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                            self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                            self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                            return

                    # bfs로 팀 내에서 몇 번째 사람인지 찾기
                    q = deque()
                    q.append([position, idx])
                    count = 1
                    child = []
                    visited = [[False for _ in range(self.n)] for _ in range(self.n)]
                    while q:
                        x, y = q.popleft()

                        if visited[x][y]:
                            continue
                        visited[x][y] = True

                        if self.board[x][y] == 1:
                            break

                        for i in range(len(self.dx)):
                            nx = x + self.dx[i]
                            ny = y + self.dy[i]

                            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                continue

                            if visited[nx][ny]:
                                continue

                            if self.board[nx][ny] == 4 or self.board[nx][ny] == 0:
                                continue

                            child.append([nx, ny])

                        if not q:
                            count += 1
                            q.extend(child)
                            child = []

                    self.scores[team] += count ** 2

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                    return

                elif self.board[position][idx]==2:
                    # bfs로 팀 내에서 몇 번째 사람인지 찾기
                    q = deque()
                    q.append([position, idx])
                    count = 1
                    child = []
                    visited = [[False for _ in range(self.n)] for _ in range(self.n)]
                    while q:
                        x, y = q.popleft()

                        if visited[x][y]:
                            continue
                        visited[x][y] = True

                        if self.board[x][y] == 1:
                            team = self.head_pos.index([x, y])
                            break

                        for i in range(len(self.dx)):
                            nx = x + self.dx[i]
                            ny = y + self.dy[i]

                            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                continue

                            if visited[nx][ny]:
                                continue

                            if self.board[nx][ny] == 4 or self.board[nx][ny] == 0 or self.board[nx][ny] == 3:
                                continue

                            child.append([nx, ny])

                        if not q:
                            count += 1
                            q.extend(child)
                            child = []

                    self.scores[team] += count ** 2

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3

                    return

                idx += 1

        elif direction == 1:
            # 아래에서 위쪽
            # round % self.n 열
            idx = self.n-1
            while idx >= 0:
                if self.board[idx][position] == 1:
                    # head_pos에서 찾아서 점수 주기
                    team = self.head_pos.index([idx, position])

                    self.scores[team] += 1

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                    return

                elif self.board[idx][position] == 3:
                    # tail_pos에서 찾아서 점수 주기
                    team = self.tail_pos.index([idx, position])

                    # bfs로 팀 내에서 몇 번째 사람인지 찾기
                    q = deque()
                    q.append([idx, position])
                    count = 1
                    child = []
                    visited = [[False for _ in range(self.n)] for _ in range(self.n)]
                    while q:
                        x, y = q.popleft()

                        if visited[x][y]:
                            continue
                        visited[x][y] = True

                        if self.board[x][y] == 1:
                            break

                        for i in range(len(self.dx)):
                            nx = x + self.dx[i]
                            ny = y + self.dy[i]

                            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                continue

                            if visited[nx][ny]:
                                continue

                            if self.board[nx][ny] == 4 or self.board[nx][ny] == 0:
                                continue

                            child.append([nx, ny])

                        if not q:
                            count += 1
                            q.extend(child)
                            child = []

                    self.scores[team] += count ** 2

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                    return

                elif self.board[idx][position] == 2:
                    # bfs로 팀 내에서 몇 번째 사람인지 찾기
                    q = deque()
                    q.append([idx, position])
                    count = 1
                    child = []
                    visited = [[False for _ in range(self.n)] for _ in range(self.n)]
                    while q:
                        x, y = q.popleft()

                        if visited[x][y]:
                            continue
                        visited[x][y] = True

                        if self.board[x][y] == 1:
                            team = self.head_pos.index([x, y])

                            for i in range(len(self.dx)):
                                nx = self.head_pos[team][0] + self.dx[i]
                                ny = self.head_pos[team][1] + self.dy[i]
                                if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                    continue

                                # 머리사람이 있다면 그건 루트가 꽉 차있다는 말
                                if self.board[nx][ny] == 3:
                                    self.scores[team] += self.sizes[team] ** 2

                                # 머리, 꼬리 위치 바꾸기
                                self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                                self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                                self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                                return
                            break

                        for i in range(len(self.dx)):
                            nx = x + self.dx[i]
                            ny = y + self.dy[i]

                            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                continue

                            if visited[nx][ny]:
                                continue

                            if self.board[nx][ny] == 4 or self.board[nx][ny] == 0 or self.board[nx][ny] == 3:
                                continue

                            child.append([nx, ny])

                        if not q:
                            count += 1
                            q.extend(child)
                            child = []

                    self.scores[team] += count ** 2

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                    return

                idx += 1

        elif direction == 2:
            # 오른쪽에서 왼쪽
            # self.n - round % self.n 행
            idx = self.n - 1
            while idx >= 0:
                if self.board[position][idx] == 1:
                    # head_pos에서 찾아서 점수 주기
                    team = self.head_pos.index([position, idx])

                    self.scores[team] += 1

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                    return

                elif self.board[position][idx] == 3:
                    # tail_pos에서 찾아서 점수 주기
                    team = self.tail_pos.index([position, idx])

                    for i in range(len(self.dx)):
                        nx = self.head_pos[team][0] + self.dx[i]
                        ny = self.head_pos[team][1] + self.dy[i]
                        if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                            continue

                        # 머리사람이 있다면 그건 루트가 꽉 차있다는 말
                        if self.board[nx][ny] == 3:
                            self.scores[team] += self.sizes[team] ** 2

                            # 머리, 꼬리 위치 바꾸기
                            self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                            self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                            self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                            return

                    # bfs로 팀 내에서 몇 번째 사람인지 찾기
                    q = deque()
                    q.append([position, idx])
                    count = 1
                    child = []
                    visited = [[False for _ in range(self.n)] for _ in range(self.n)]
                    while q:
                        x, y = q.popleft()

                        if visited[x][y]:
                            continue
                        visited[x][y] = True

                        if self.board[x][y] == 1:
                            break

                        for i in range(len(self.dx)):
                            nx = x + self.dx[i]
                            ny = y + self.dy[i]

                            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                continue

                            if visited[nx][ny]:
                                continue

                            if self.board[nx][ny] == 4 or self.board[nx][ny] == 0:
                                continue

                            child.append([nx, ny])

                        if not q:
                            count += 1
                            q.extend(child)
                            child = []

                    self.scores[team] += count ** 2

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                    return

                elif self.board[position][idx] == 2:
                    # bfs로 팀 내에서 몇 번째 사람인지 찾기
                    q = deque()
                    q.append([position, idx])
                    count = 1
                    child = []
                    visited = [[False for _ in range(self.n)] for _ in range(self.n)]
                    while q:
                        x, y = q.popleft()

                        if visited[x][y]:
                            continue
                        visited[x][y] = True

                        if self.board[x][y] == 1:
                            team = self.head_pos.index([x, y])
                            for i in range(len(self.dx)):
                                nx = self.head_pos[team][0] + self.dx[i]
                                ny = self.head_pos[team][1] + self.dy[i]
                                if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                    continue

                                # 머리사람이 있다면 그건 루트가 꽉 차있다는 말
                                if self.board[nx][ny] == 3:
                                    self.scores[team] += self.sizes[team] ** 2

                                # 머리, 꼬리 위치 바꾸기
                                self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                                self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                                self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                                return
                            break

                        for i in range(len(self.dx)):
                            nx = x + self.dx[i]
                            ny = y + self.dy[i]

                            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                continue

                            if visited[nx][ny]:
                                continue

                            if self.board[nx][ny] == 4 or self.board[nx][ny] == 0 or self.board[nx][ny] == 3:
                                continue

                            child.append([nx, ny])

                        if not q:
                            count += 1
                            q.extend(child)
                            child = []

                    self.scores[team] += count ** 2

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                    return

                idx -= 1

        elif direction == 3:
            # 위에서 아래쪽
            # self.n - round % self.n 열
            idx = 0
            while idx < self.n:
                if self.board[idx][position] == 1:
                    # head_pos에서 찾아서 점수 주기
                    team = self.head_pos.index([idx, position])
                    self.scores[team] += 1

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                    return

                elif self.board[idx][position] == 3:
                    # tail_pos에서 찾아서 점수 주기
                    team = self.tail_pos.index([idx, position])

                    for i in range(len(self.dx)):
                        nx = self.head_pos[team][0] + self.dx[i]
                        ny = self.head_pos[team][1] + self.dy[i]
                        if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                            continue

                        # 머리사람이 있다면 그건 루트가 꽉 차있다는 말
                        if self.board[nx][ny] == 3:
                            self.scores[team] += self.sizes[team] ** 2

                        # 머리, 꼬리 위치 바꾸기
                        self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                        self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                        self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                        return

                    # bfs로 팀 내에서 몇 번째 사람인지 찾기
                    q = deque()
                    q.append([idx, position])
                    count = 1
                    child = []
                    visited = [[False for _ in range(self.n)] for _ in range(self.n)]
                    while q:
                        x, y = q.popleft()

                        if visited[x][y]:
                            continue
                        visited[x][y] = True

                        if self.board[x][y] == 1:
                            break

                        for i in range(len(self.dx)):
                            nx = x + self.dx[i]
                            ny = y + self.dy[i]

                            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                continue

                            if visited[nx][ny]:
                                continue

                            if self.board[nx][ny] == 4 or self.board[nx][ny] == 0:
                                continue

                            child.append([nx, ny])

                        if not q:
                            count += 1
                            q.extend(child)
                            child = []

                    self.scores[team] += count ** 2

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                    return

                elif self.board[idx][position] == 2:
                    # bfs로 팀 내에서 몇 번째 사람인지 찾기
                    q = deque()
                    q.append([idx, position])
                    count = 1
                    child = []
                    visited = [[False for _ in range(self.n)] for _ in range(self.n)]
                    while q:
                        x, y = q.popleft()

                        if visited[x][y]:
                            continue
                        visited[x][y] = True

                        if self.board[x][y] == 1:
                            team = self.head_pos.index([x, y])

                            for i in range(len(self.dx)):
                                nx = self.head_pos[team][0] + self.dx[i]
                                ny = self.head_pos[team][1] + self.dy[i]
                                if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                    continue

                                # 머리사람이 있다면 그건 루트가 꽉 차있다는 말
                                if self.board[nx][ny] == 3:
                                    self.scores[team] += self.sizes[team] ** 2

                                # 머리, 꼬리 위치 바꾸기
                                self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                                self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                                self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                                return

                            break

                        for i in range(len(self.dx)):
                            nx = x + self.dx[i]
                            ny = y + self.dy[i]

                            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                                continue

                            if visited[nx][ny]:
                                continue

                            if self.board[nx][ny] == 4 or self.board[nx][ny] == 0 or self.board[nx][ny] == 3:
                                continue

                            child.append([nx, ny])

                        if not q:
                            count += 1
                            q.extend(child)
                            child = []

                    self.scores[team] += count ** 2

                    # 머리, 꼬리 위치 바꾸기
                    self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
                    self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
                    self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3
                    return

                idx += 1

def main():
    # 인스턴스 생성
    instance = Problem()

    # k번의 라운드마다 각 팀별 이동, 공 던지기, 점수 배정, 머리/꼬리 바꾸기
    for round in range(instance.k):
        # 각 팀의 이동
        for team in range(instance.m):
            instance.move(team)

        # 공 던지기
        instance.throw_ball(round)

    print(sum(instance.scores))

if __name__ == "__main__":
    main()