from collections import deque

class Problem():
    def __init__(self):
        self.k, self.m = map(int, input().split())
        self.board = [list(map(int, input().split())) for _ in range(5)]
        self.treasure = deque(map(int, input().split()))
        self.score = []
        self.do_break = False

    def explore(self):
        max_board = None
        max_value = 0
        score = 0
        min_angle = 1e9

        for i in range(3):
            for j in range(3):

                # 시작하는 지점 선택
                start_x = i
                start_y = j

                # 90도 회전
                temp_1 = [self.board[row][:] for row in range(5)] # 보드 복사
                temp_90 = self.rotate(temp_1, self.board, start_x, start_y)
                temp_board, temp_value = self.get_value(temp_90)
                temp_angle = 90

                if temp_value > max_value:
                    max_value = temp_value
                    max_board = temp_board
                elif temp_value == max_value:
                    if temp_angle < min_angle:
                        max_value = temp_value
                        max_board = temp_board

                # 180도 회전
                temp_2 = [temp_1[row][:] for row in range(5)]
                temp_180 = self.rotate(temp_2, temp_1, start_x, start_y)
                temp_board, temp_value = self.get_value(temp_180)

                if temp_value > max_value:
                    max_value = temp_value
                    max_board = temp_board
                elif temp_value == max_value:
                    if temp_angle < min_angle:
                        max_value = temp_value
                        max_board = temp_board

                # 270도 회전
                temp_3 = [temp_2[row][:] for row in range(5)]
                temp_270 = self.rotate(temp_3, temp_2, start_x, start_y)
                temp_board, temp_value = self.get_value(temp_270)

                if temp_value > max_value:
                    max_value = temp_value
                    max_board = temp_board
                elif temp_value == max_value:
                    if temp_angle < min_angle:
                        max_value = temp_value
                        max_board = temp_board

        if max_value==0:
            self.do_break = True
            return
        self.board = max_board

        score += max_value

        while True:
            for j in range(5):
                for i in range(4, -1, -1):

                    if self.board[i][j]==0:

                        num = self.treasure.popleft()
                        self.board[i][j] = num

            new_board, new_val = self.get_value(self.board)
            if new_val == 0:
                break
            score += new_val
            self.board = new_board
        self.score.append(score)

    def rotate(self, new, old, start_x, start_y):
        # 3x3 격자를 선택하여 90도, 180도, 270도 중 하나의 각도로 회전시킬 수 있다
        for i in range(3):
            for j in range(3):
                new[start_x + j][start_y + 2 - i] = old[start_x + i][start_y + j]
        return new

    def get_value(self, board):
        # 유물의 1차 획득 가치 계산
        temp = [board[i][:] for i in range(5)]

        visited = [[False for _ in range(5)] for _ in range(5)]
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]

        value = 0

        for i in range(5):
            for j in range(5):
                if visited[i][j]:
                    continue

                q = deque()
                q.append([i, j])
                history = []
                history.append([i, j])
                count = 1
                while q:
                    x, y = q.popleft()
                    if visited[x][y]:
                        continue
                    visited[x][y] = True

                    for k in range(len(dx)):
                        nx = x + dx[k]
                        ny = y + dy[k]

                        if nx < 0 or nx >= 5 or ny < 0 or ny >= 5:
                            continue

                        if visited[nx][ny]:
                            continue

                        if temp[nx][ny] == temp[x][y]:
                            count += 1
                            q.append([nx, ny])
                            history.append([nx, ny])

                if count >= 3:
                    value += count
                    for elem in history:
                        temp[elem[0]][elem[1]] = 0

        return temp, value

def main():
    instance = Problem()
    for _ in range(instance.k):
        # 탐사 진행
        instance.explore()
        if instance.do_break:
            break

    print(" ".join(map(str, instance.score)))

if __name__ == "__main__":
    main()