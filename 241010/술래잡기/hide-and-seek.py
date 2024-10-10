import sys
from collections import deque

input = sys.stdin.readline

class Problem():
    def __init__(self):
        """
        n: 격자의 크기
        m: 도망자의 수
        h: 나무의 수
        k: 턴의 횟수
        """
        self.score = 0
        self.n, self.m, self.h, self.k = map(int, input().split())
        self.out = [False for _ in range(self.m)]
        self.runner_pos = []
        self.runner_direction = []
        for _ in range(self.m):
            x, y, d = map(int, input().split())
            self.runner_pos.append([x-1, y-1]) # d=0: 좌우 움직임, d=1: 상하 움직임
            self.runner_direction.append(d-1)

        self.catcher_pos = [self.n//2, self.n//2]

        # 나무의 위치 (변하지 않음)
        self.tree_pos = []
        for _ in range(self.h):
            x, y = map(int, input().split())
            self.tree_pos.append([x-1, y-1])

        # 술래의 이동 경로
        self.route = []
        self.catcher_direction = []

        visited = [[False for _ in range(self.n)] for _ in range(self.n)]
        q = deque()
        q.append([0, 0])
        self.route.append([0, 0])

        self.dx = [1, 0, -1, 0]
        self.dy = [0, 1, 0, -1]
        direction = 0
        self.catcher_direction.append((direction + 2)%4)
        while q:
            x, y = q.popleft()
            if visited[x][y]:
                continue
            visited[x][y] = True
            if [x, y] == [self.n//2, self.n//2]:
                break

            nx = x + self.dx[direction]
            ny = y + self.dy[direction]

            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n or visited[nx][ny]:
                direction += 1
                if direction > 3:
                    direction -= 4
                nx = x + self.dx[direction]
                ny = y + self.dy[direction]

            q.append([nx, ny])

            self.route.append([nx, ny])
            self.catcher_direction.append((direction + 2) % 4)


        temp = self.route[::-1]
        temp_2 = self.catcher_direction[::-1]
        self.route = temp + self.route[1:-1]
        self.catcher_direction = temp_2 + self.catcher_direction[1:-1]
        self.period = len(self.route)

    def get_distance(self, pos_1, pos_2):
        return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])

    def runner_move(self, runner):
        # 술래와의 거리가 3 이하인 도망자, 아직 남아있는 도망자만 움직인다
        if self.get_distance(self.runner_pos[runner], self.catcher_pos) > 3 or self.out[runner]:
            return

        x = self.runner_pos[runner][0]
        y = self.runner_pos[runner][1]
        d = self.runner_direction[runner]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        nx = x + dx[d]
        ny = y + dy[d]

        # 격자를 벗어나는 경우 방향을 반대로 틀어준다
        if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
            d = (d + 2)%4
            # 바뀐 방향 저장
            self.runner_direction[runner] = d
            # 새로 nx, ny 정의
            nx = x + dx[d]
            ny = y + dy[d]

        # 움직이는 칸에 술래가 있지 않다면 해당 칸으로 이동
        if [nx, ny] != self.catcher_pos:
            self.runner_pos[runner] = [nx, ny]

    def catcher_move(self, turn):
        # 술래 이동
        self.catcher_pos = self.route[turn % self.period]
        x = self.catcher_pos[0]
        y = self.catcher_pos[1]

        # 술래의 방향
        d = self.catcher_direction[turn % self.period]

        # 시야 내에 도망자가 있는지 확인
        count = 0
        for i in range(3):
            nx = x + self.dx[d]*i
            ny = y + self.dy[d]*i

            if [nx, ny] in self.runner_pos:
                if [nx, ny] in self.tree_pos:
                    continue
                for runner in range(self.m):
                    if self.runner_pos[runner] != [nx, ny]:
                        continue
                    if self.out[runner]:
                        continue
                    self.out[runner] = True
                    count += 1

        self.score += turn * count

def main():
    instance = Problem()

    # 술래의 이동경로
    for turn in range(1, instance.k+1):
        for runner in range(instance.m):
            instance.runner_move(runner)
        instance.catcher_move(turn)
    print(instance.score)

if __name__ == "__main__":
    main()