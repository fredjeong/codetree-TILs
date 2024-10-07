import sys

input = sys.stdin.readline

class problem():
    def __init__(self):
        """
        N: 미로의 크기 N * N
        M: 참가자의 수
        K: 게임 시간
        """
        self.n, self.m, self.k = map(int, input().split())
        
        # 참가자들의 탈출 성공 여부
        self.out = [False for _ in range(self.m)]

        # 모든 참가자들의 누적 이동 거리
        self.cum_distance = {}
        for id in range(self.m):
            self.cum_distance[id] = 0
        
        # 미로의 정보 등록
        self.board = [list(map(int, input().split())) for _ in range(self.n)]

        # 참가자들의 좌표 등록
        self.user_pos = []
        for id in range(self.m):
            x, y = map(int, input().split())
            self.user_pos.append([x-1, y-1])

        # 출구의 좌표
        x, y = map(int, input().split())
        self.exit_pos = [x-1, y-1]
    
    def move(self, id):
        """
        id번 참가자의 이동
        """
        # 이미 탈출했다면 고려하지 않는다
        if self.out[id] == True:
            return

        # 상하좌우로 움직일 수 있다
        x = self.user_pos[id][0]
        y = self.user_pos[id][1]

        # 상하로 움직이는 것이 좌우로 움직이는 것보다 우선시된다
        dx = [0, 0, 1, -1]
        dy = [1, -1, 0, 0]

        original_dist = self.get_distance(self.user_pos[id], self.exit_pos)
        min_dist = self.get_distance(self.user_pos[id], self.exit_pos)
        new_pos = [x, y]

        for i in range(len(dx)):
            nx = x + dx[i]
            ny = y + dy[i]
            
            # 이동하려는 칸이 미로 밖에 있다면 고려하지 않는다
            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                continue

            # 이동하려는 칸이 벽이라면 고려하지 않는다
            if self.board[nx][ny] > 0:
                continue

            dist = self.get_distance([nx, ny], self.exit_pos)
            if dist <= min_dist:
                min_dist = dist
                new_pos = [nx, ny]
        
        # 위치 갱신
        if min_dist != original_dist:
            self.user_pos[id] = new_pos
            self.cum_distance[id] += 1
        
        # 출구에 도착했다면 탈출시킨다
        if new_pos == self.exit_pos:
            self.out[id] = True
            self.user_pos[id] = [100, 100]

    def get_target(self):
        length = 1
        while length <= self.n:
            for i in range(self.exit_pos[0] - (length -1), self.exit_pos[0] + 1, 1):
                for j in range(self.exit_pos[1] - (length - 1), self.exit_pos[1] + 1, 1):
                    
                    # 가장 좌상단에 있는 점수터 수색 시작
                    if i < 0 or i >= self.n or j < 0 or j >= self.n:
                        continue
                                        
                    # [i, j]를 좌상단으로 하는 길이 length만큼의 정사각형 
                    for row in range(i, i + length):
                        for col in range(j, j + length):
                            if [row, col] in self.user_pos:
                                target_x = i
                                target_y = j
                                return target_x, target_y, length

            length += 1

    def rotate(self):

        target_x, target_y, length = self.get_target()

        # 정사각형을 회전시키자
        temp = [self.board[i][:] for i in range(self.n)]
        
        changed_exit_pos = False
        visited = [False for _ in range(self.m)]
        
        for i in range(length):
            for j in range(length):
                temp[target_x + j][target_y + length - 1 - i] = self.board[target_x + i][target_y + j]

                if temp[target_x + j][target_y + length - 1 - i] > 0:
                    temp[target_x + j][target_y + length - 1 - i] -= 1
                if [target_x + i, target_y + j] == self.exit_pos:
                    if changed_exit_pos != True:
                        changed_exit_pos = True
                        self.exit_pos = [target_x + j, target_y + length - 1 - i]
                for user in range(self.m):
                    if [target_x + i, target_y + j] == self.user_pos[user]:
                        if visited[user]==True:
                            continue
                        visited[user] = True
                        self.user_pos[user] = [target_x + j, target_y + length - 1 - i] 

        self.board = temp

    def get_distance(self, pos_1, pos_2):
        """
        입력값은 두 개의 배열이다
        """
        return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])

def main():
    instance = problem()

    # 매 초마다
    for _ in range(instance.k):
        # 모든 참가자가 이동
        for id in range(instance.m):
            instance.move(id)
        
        # 게임을 조기에 종료하는지 확인
        if False not in instance.out:
            break
        
        # 배열 회전
        instance.rotate()
    
    # 모든 참가자들의 이동 거리 합 계산
    print(sum(instance.cum_distance.values()))

    # 출구의 좌표 입력
    print(instance.exit_pos[0] + 1, instance.exit_pos[1] + 1)

if __name__ == "__main__":
    main()