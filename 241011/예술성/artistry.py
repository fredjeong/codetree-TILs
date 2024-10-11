import sys
from collections import deque

input = sys.stdin.readline

class Problem():
    def __init__(self):
        self.n = int(input())
        self.board = [list(map(int, input().split())) for _ in range(self.n)]
        self.score = 0

        # 동일한 숫자가 상하좌우로 인접해있는 경우 동일한 그룹이라고 본다

    def get_group(self):
        """
        매번 그룹을 새로 설정해줘야 한다
        """
        self.groups = []
        self.colours = []

        visited = [[False for _ in range(self.n)] for _ in range(self.n)]

        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]

        for i in range(self.n):
            for j in range(self.n):
                # 이미 방문했다면 고려하지 않는다
                if visited[i][j]:
                    continue
                visited[i][j] = True

                colour = self.board[i][j]

                q = deque()
                q.append([i, j])

                history = [[i, j]]

                while q:
                    x, y = q.popleft()

                    for k in range(len(dx)):
                        nx = x + dx[k]
                        ny = y + dy[k]

                        if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                            continue

                        if visited[nx][ny]:
                            continue

                        if self.board[nx][ny] != colour:
                            continue

                        history.append([nx, ny])
                        q.append([nx, ny])
                        visited[nx][ny] = True

                self.groups.append(history)
                self.colours.append(colour)

    def get_adjacent_sides(self, group_1, group_2):
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]

        group_1_arr = self.groups[group_1]
        group_2_arr = self.groups[group_2]

        count = 0

        for elem in group_1_arr:
            x = elem[0]
            y = elem[1]
            for i in range(len(dx)):
                nx = x + dx[i]
                ny = y + dy[i]
                if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                    continue
                if self.board[nx][ny] == self.board[x][y]:
                    continue
                # 색깔이 다르다면 그게 그룹 2에 속한 칸인지 확인
                if self.board[nx][ny] != self.board[x][y]:
                    if [nx, ny] in group_2_arr:
                        count += 1

        return count

    def get_harmony(self, group_1, group_2):
        """
        맞닿아 있는 변의 수를 구하는 것이 난관
        """
        adjacent_sides = self.get_adjacent_sides(group_1, group_2)
        harmony = (len(self.groups[group_1]) + len(self.groups[group_2])) * self.colours[group_1] * self.colours[group_2] * adjacent_sides
        self.score += harmony

    def cross_rotate(self):
        # 반시계방향 회전
        temp = [self.board[i][:] for i in range(self.n)]
        temp = list(map(list, zip(*temp)))[::-1]
        return temp


    def square_rotate(self):
        # 구역은 총 네 개로 나뉜다
        temp = [self.board[i][:] for i in range(self.n)]

        # zone 1: 시작점 0, 0
        start_x = 0
        start_y = 0
        for i in range(self.n//2):
            for j in range(self.n//2):
                temp[start_x + j][start_y + 1 - i] = self.board[start_x + i][start_y + j]

        # zone 2: 시작점 0, self.n//2 + 1
        start_x = 0
        start_y = self.n//2 + 1
        for i in range(self.n//2):
            for j in range(self.n//2):
                temp[start_x + j][start_y + 1 - i] = self.board[start_x + i][start_y + j]

        # zone 3: 시작점 self.n//2 + 1, 0
        start_x = self.n//2 + 1
        start_y = 0
        for i in range(self.n//2):
            for j in range(self.n//2):
                temp[start_x + j][start_y + 1 - i] = self.board[start_x + i][start_y + j]

        # zone 4: self.n//2 + 1, self.n//2 + 1
        start_x = self.n//2 + 1
        start_y = self.n//2 + 1
        for i in range(self.n//2):
            for j in range(self.n//2):
                temp[start_x + j][start_y + 1 - i] = self.board[start_x + i][start_y + j]

        return temp

    def create_new_board(self):
        cross_rotated = self.cross_rotate()
        square_rotated = self.square_rotate()

        self.board = square_rotated
        for i in range(self.n):
            self.board[self.n//2][i] = cross_rotated[self.n//2][i]
            self.board[i][self.n//2] = cross_rotated[i][self.n//2]

def main():
    instance = Problem()

    # 그룹 나누기
    instance.get_group()

    # 초기 예술 점수 구하기
    for i in range(len(instance.groups)):
        for j in range(len(instance.groups)):
            if i<j:
                instance.get_harmony(i, j)

    # 배열 회전
    instance.create_new_board()

    for round in range(3):
        # 그룹 나누기
        instance.get_group()

        # 초기 예술 점수 구하기
        for i in range(len(instance.groups)):
            for j in range(len(instance.groups)):
                if i < j:
                    instance.get_harmony(i, j)

        if round==2:
            break

        # 배열 회전
        instance.create_new_board()

    print(instance.score)

if __name__ == "__main__":
    main()