from collections import deque

class Problem():
    def __init__(self):
        self.n, self.m, self.k = map(int, input().split())

        # 미로 정의
        self.board = [list(map(int, input().split())) for _ in range(self.n)]

        # 참가자의 좌표 정의
        self.player_pos = []
        for _ in range(self.m):
            x, y = map(int, input().split())
            self.player_pos.append([x-1, y-1])

        # 참가자들의 탈출 여부
        self.out = [False for _ in range(self.m)]

        # 참가자들의 이동 거리 합
        self.score = 0

        # 출구 좌표 정의
        self.exit_pos = list(map(int, input().split()))
        self.exit_pos[0] -= 1
        self.exit_pos[1] -= 1

    def get_distance(self, pos_1, pos_2):
        return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])

    def move(self):
        # 모든 참가자들이 동시에 움직인다
        # 방향에서 상하가 좌우보다 우선시된다
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]
        for id in range(self.m):
            # 이미 탈출에 성공한 참가자는 고려하지 않는다
            if self.out[id]:
                continue

            threshold = self.get_distance(self.player_pos[id], self.exit_pos)

            x = self.player_pos[id][0]
            y = self.player_pos[id][1]

            arr = []
            for i in range(len(dx)):
                nx = x + dx[i]
                ny = y + dy[i]

                # 격자 바깥으로 나가는 경우는 고려하지 않는다
                if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                    continue

                # 벽이 있다면 움직이지 않는다
                if self.board[nx][ny] > 0:
                    continue

                dist = self.get_distance([nx, ny], self.exit_pos)
                # 움직이려는 칸은 현재 칸보다 출구까지의 최단 거리가 가까워야 한다
                if dist >= threshold:
                    continue

                arr.append([dist, i, [nx, ny]])

            if arr:
                # 거리가 같으면 상하가 우선시된다
                best = sorted(arr, key=lambda x: [x[0], x[1]])[0]

                # 참가자의 위치 갱신
                self.player_pos[id] = best[2]

                # 총 이동 거리 더해주기
                self.score += 1

                # 이동한 칸이 출구라면 탈출
                if self.player_pos[id] == self.exit_pos:
                    self.out[id] = True
                    self.player_pos[id] = [100, 100]

    def find_start(self):
        # 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형의 좌상단 좌표를 찾는다
        length = 2
        while length <= self.n:
            # 가능한 모든 좌상단 좌표를 탐색해보기
            for i in range(self.n - length + 1):
                for j in range(self.n - length + 1):
                    # 좌상단 좌표: i, j
                    exit_check = False
                    player_check = False

                    # [i,j]로부터 만들어지는 길이 length의 정사각형 안에 참가자와 출구가 있다면 즉시 종료
                    for sub_i in range(i, i + length):
                        for sub_j in range(j, j + length):
                            if [sub_i, sub_j] in self.player_pos:
                                player_check = True

                            if [sub_i, sub_j] == self.exit_pos:
                                exit_check = True

                            if player_check and exit_check:
                                return i, j, length

            length += 1

    def rotate(self):
        # find_start 함수를 통해 회전시킬 좌상단을 찾는다
        start_x, start_y, length = self.find_start()

        temp = [self.board[row][:] for row in range(self.n)]

        s = set()
        rotate_exit = False
        for i in range(length):
            for j in range(length):
                temp[start_x + j][start_y + length - 1 - i] = self.board[start_x + i][start_y + j]
                # 회전하는 칸이 벽이라면 내구도를 1 깎아준다
                if temp[start_x + j][start_y + length - 1 - i] > 0:
                    temp[start_x + j][start_y + length - 1 - i] -= 1

                # 참가자가 회전하는 정사각형 안에 있다면 위치를 같이 바꾸어주어야 한다
                for id in range(self.m):
                    if self.player_pos[id] == [start_x + i, start_y + j]:
                        s.add(id)

                # 출구가 회전하는 정사각형 안에 있다면 위치를 같이 바꾸어주어야 한다
                if self.exit_pos == [start_x + i, start_y + j]:
                    rotate_exit = True

        if rotate_exit:
            i = self.exit_pos[0] - start_x
            j = self.exit_pos[1] - start_y

            self.exit_pos = [start_x + j, start_y + length - 1 - i]
            #self.exit_pos = [start_x + j, start_y + length - 1 - i]
        for player in s:
            i = self.player_pos[player][0] - start_x
            j = self.player_pos[player][1] - start_y

            self.player_pos[player] = [start_x + j, start_y + length - 1 - i]



        self.board = temp

def main():
    instance = Problem()

    # K초 동안 참가자들의 이동과 미로의 회전을 반복한다
    for _ in range(instance.k):
        # 참가자의 이동
        instance.move()

        # 미로의 회전
        instance.rotate()

        # 모든 참가자가 탈출에 성공했다면 게임을 조기에 종료한다
        if False not in instance.out:
            break

    print(instance.score)
    print(instance.exit_pos[0] + 1, instance.exit_pos[1] + 1)

if __name__ == "__main__":
    main()