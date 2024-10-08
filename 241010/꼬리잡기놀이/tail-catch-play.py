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

                            if self.board[nx][ny] == 3:
                                # 꼬리사람 좌표 저장
                                tail_pos = [nx, ny]
                                self.tail_pos.append(tail_pos)
                                visited[nx][ny] = True
                                continue

                            if self.board[nx][ny] == 2:
                                q.append([nx, ny])
                                length += 1
                                continue

                                # child.append([nx, ny])

                        #if not q:
                        #    length += 1
                        #    q.extend(child)
                        #    child = []
                    self.sizes.append(length + 1)


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
                    nnx = nx + self.dx[j]
                    nny = ny + self.dy[j]
                    if nnx < 0 or nnx >= self.n or nny < 0 or nny >= self.n:
                        continue
                    # 그러면 꼬리사람의 위치 (nx, ny)가 머리사람의 위치가 된다
                    if self.board[nnx][nny] == 2:
                        # 머리사람 새 위치 저장
                        self.board[nx][ny] = 1

                        self.head_pos[team] = [nx, ny]

                        # 꼬리사람 새 위치 저장
                        self.board[nnx][nny] = 3
                        self.tail_pos[team] = [nnx, nny]
                        self.board[x][y] = 2
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


    #def throw_ball(self, round):
    #    direction = (round // self.n) % 4
    #    """
    #    0: 왼쪽에서 오른쪽으로 공을 던진다
    #    1: 아랫쪽에서 윗쪽으로 공을 던진다
    #    2: 오른쪽에서 왼쪽으로 공을 던진다
    #    3: 윗쪽에서 아랫쪽으로 공을 던진다
    #    """
    #    position =

    def throw_ball(self, round):
        # 4*n 라운드마다 반복된다
        direction = (round // self.n) % 4
        if direction < 2:
            position = round % self.n
        else:
            position = (self.n - 1) - (round % self.n)

        """
        direction이 0, 1일 때: idx는 0부터 시작
        direction이 2, 3일 때: idx는 self.n - 1부터 시작
        """
        global do_break
        if direction==0:
            do_break = False
            idx = 0
            while idx < self.n:
                self.run(position, idx)
                if do_break:
                    break
                idx += 1
        elif direction==1:
            do_break = False
            idx = self.n - 1
            while idx >= 0:
                self.run(idx, position)
                if do_break:
                    break
                idx -= 1
        elif direction==2:
            do_break = False
            idx = self.n - 1
            while idx >= 0:
                self.run(position, idx)
                if do_break:
                    break
                idx -= 1
        elif direction==3:
            do_break = False
            idx = 0
            while idx < self.n:
                self.run(idx, position)
                if do_break:
                    break
                idx += 1

    def run(self, arg_1, arg_2):
        """
        direction이 0, 2일 때: arg_1 = position, arg_2 = idx
        direction이 1, 3일 때: arg_1 = idx, arg_2 = position
        """
        # 빈 칸을 지나가는 경우 바로 종료
        if self.board[arg_1][arg_2]==0 or self.board[arg_1][arg_2]==4:
            return

        # 처음 맞춘 게 어떤 팀의 머리사람이라면
        if self.board[arg_1][arg_2]==1:
            # 소속 팀 찾기
            team = self.head_pos.index([arg_1, arg_2])

            # 머리사람은 앞에 아무도 없으므로 점수 1만큼 증가
            score = 1

        # 처음 맞춘 게 어떤 팀의 꼬리사람이라면
        elif self.board[arg_1][arg_2]==3:
            # 소속 팀 찾기
            team = self.tail_pos.index([arg_1, arg_2])

            # 그 팀의 사이즈의 제곱만큼 점수 주기
            score = self.sizes[team]**2

        # 처음 맞춘 게 어떤 팀의 중간 사람이라면
        elif self.board[arg_1][arg_2]==2:
            # bfs로 1번까지 가는 최단거리 찾기
            q = deque()
            q.append([arg_1, arg_2])
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

            score = count ** 2

        self.scores[team] += score

        # 머리, 꼬리 위치 바꾸기
        self.head_pos[team], self.tail_pos[team] = self.tail_pos[team], self.head_pos[team]
        self.board[self.head_pos[team][0]][self.head_pos[team][1]] = 1
        self.board[self.tail_pos[team][0]][self.tail_pos[team][1]] = 3

        global do_break
        do_break = True

        return

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