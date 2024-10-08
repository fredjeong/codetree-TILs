import sys

input = sys.stdin.readline

class problem():
    def __init__(self):
        """
        n: row 개수
        m: col 개수
        k: 전체 턴 수
        
        board_power: 각 포탑의 공격력을 나타낸 2차원 배열
        """
        self.n, self.m, self.k = map(int, input().split())
        
        self.board_power = [list(map(int, input().split())) for _ in range(self.n)]
        self.board_time = [[-1 for _ in range(self.m)] for _ in range(self.n)]
    
    def select_player(self, t):
        """
        첫 번째 액션: 공격자 선정
        가장 공격력이 낮은 포탑 선정
        두 개 이상이라면 가장 최근에 공격한 포탑 선정
        두 개 이상이라면 각 포탑 위치의 행과 열의 합이 가장 큰 포탑 선정
        두 개 이상이라면 각 포탑 위치의 열 값이 가장 큰 포탑 선정
        """
        min_power = 1e9
        player = None
        for i in range(self.n):
            for j in range(self.m):
                power = self.board_power[i][j]
                # 이미 부서진 포탑은 고려하지 않는다
                if power == 0:
                    continue
                # 초기 단계
                if player == None:
                    min_power = power
                    player = [i, j]
                    continue
                # 이후 단계
                if power < min_power:
                    player = [i, j]
                elif power == min_power:
                    # 가장 최근에 공격한 포탑 선택
                    if self.board_time[i][j] > self.board_time[player[0]][player[1]]:
                        player = [i, j]
                    elif self.board_time[i][j] == self.board_time[player[0]][player[1]]:
                        # 새 포탑의 행과 열의 합이 더 크면 선택
                        if i+j > sum(player):
                            player = [i, j]
                        
                        # 새 포탑의 열 값이 가장 큰 포탑 선택
                        elif i+j == sum(player):
                            if j > player[1]:
                                player = [i, j]

        # 공격자로 선정된 포탑의 공격치 올려주기
        self.board_power[player[0]][player[1]] += self.n + self.m

        # self.board_time 갱신
        self.board_time[player[0]][player[1]] = t

        return player

    def select_target(self):
        """
        가장 공격력이 높은 포탑 선정
        두 개 이상이라면 가장 공격한지 가장 오래된 포탑 선정
        두 개 이상이라면 각 포탑 위치의 행과 열의 합이 가장 작은 포탑 선정
        두 개 이상이라면 각 포탑 위치의 열 값이 가장 작은 포탑 선정
        """
        max_power = 0
        target = None
        for i in range(self.n):
            for j in range(self.m):
                power = self.board_power[i][j]
                # 이미 부서진 포탑은 고려하지 않는다
                if power == 0:
                    continue
                
                # 초기 단계
                if target == None:
                    max_power = power
                    target = [i, j]
                    continue
                # 이후 단계
                if power > max_power:
                    target = [i, j]
                elif power == max_power:
                    # 가장 공격한지 오래된 포탑 선택
                    if self.board_time[i][j] < self.board_time[target[0]][target[1]]:
                        target = [i, j]
                    elif self.board_time[i][j] == self.board_time[target[0]][target[1]]:
                        # 새 포탑의 행과 열의 합이 더 작으면 선택
                        if i+j < sum(target):
                            target = [i, j]
                        
                        # 새 포탑의 열 값이 가장 작은 포탑 선택
                        elif i+j == sum(target):
                            if j < target[1]:
                                target = [i, j]

        return target

    def attack(self, t):
        """
        두 번째 액션: 공격자의 공격
        세 번째 액션: 포탑 부서짐
        """
        # 공격자의 좌표 선택
        player_pos = self.select_player(t)

        # 공격을 받는 포탑의 좌표 선택
        target_pos = self.select_target()

        # 레이저 공격 시도
        global laser_success
        laser_success = True
        self.laser(player_pos, target_pos)
        
        if laser_success == True:
            return
        
        # 포탄 공격 시도
        self.bomb(player_pos, target_pos)
    
    def laser(self, player, target):
        """
        1차적으로 시도하는 레이저 공격
        레이저는 상하좌우 4개 방향으로 움직일 수 있다
        부서진 포탑이 있는 위치는 지날 수 없다
        가장자리에서 막힌 방향으로 진행하고자 한다면 반대편으로 나온다
        player에서 target까지 최단 경로로 공격한다
        경로의 길이가 똑같은 최단 경로가 2개 이상이라면 우/하/좌/상의 우선순위대로 먼저 움직인 경로가 선택된다
        """
        global best_history, best_direction, laser_success
        best_history = None
        best_direction = None
        visited = [[False for _ in range(self.m)] for _ in range(self.n)]

        self.laser_dfs(player, target, [], [], visited)

        if best_history == None:
            laser_success = False
            return
        

        # 공격 대상에는 공격자의 공격력만큼 피해를 입힌다
        self.board_power[target[0]][target[1]] = max(0, self.board_power[target[0]][target[1]] - self.board_power[player[0]][player[1]])
        
        for i in range(len(best_history)-1):
            self.board_power[best_history[i][0]][best_history[i][1]] = max(0, self.board_power[best_history[i][0]][best_history[i][1]] - (self.board_power[player[0]][player[1]] // 2))
        
        # 부서지지 않은 포탑 중 공격과 무관한 포탑의 공격력 증가
        for i in range(self.n):
            for j in range(self.m):
                if self.board_power[i][j] == 0:
                    continue
                if [i, j] in best_history:
                    continue
                if [i, j] == player:
                    continue
                if [i, j] == target:
                    continue
                self.board_power[i][j] += 1

    def laser_dfs(self, cur_pos, target, history, direction, visited):
        global best_history, best_direction
        x, y = cur_pos
        new_visited = []
        for i in range(len(visited)):
            new_visited.append(visited[i][:])
        
        if new_visited[x][y] == True:
            return
        new_visited[x][y] = True
        
        if cur_pos == target:
            if best_history == None:
                best_history = history
                best_direction = direction
                return
            if len(history) < len(best_history):
                best_history = history
                best_direction = direction
                return
            elif len(history) == len(best_history):
                temp = [direction, best_direction]
                temp = sorted(temp)
                
                if direction == temp[0]:
                    best_history = history
                    best_direction = direction
                return

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        #arr = []
        for i in range(len(dx)):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 0:
                nx += self.n
            elif nx >= self.n:
                nx -= self.n

            if ny < 0:
                ny += self.m
            elif ny >= self.m:
                ny -= self.m
            
            if self.board_power[nx][ny] == 0:
                continue
            if new_visited[nx][ny] == True:
                continue
            self.laser_dfs([nx, ny], target, history + [[nx, ny]], direction + [i], new_visited)

    def bomb(self, player, target):
        # 공격 대상에는 공격자의 공격력만큼 피해를 입힌다
        self.board_power[target[0]][target[1]] = max(0, self.board_power[target[0]][target[1]] - self.board_power[player[0]][player[1]])
        
        x, y = target

        history = []

        dx = [1, -1, 0, 0, 1, 1, -1, -1]
        dy = [0, 0, 1, -1, 1, -1, 1, -1]

        for i in range(len(dx)):
            nx = x + dx[i]
            ny = y + dy[i]

            if nx < 0:
                nx += self.n
            elif nx >= self.n:
                nx -= self.n
            if ny < 0:
                ny += self.m
            elif ny >= self.m:
                ny -= self.m

            # 공격자는 영향을 받지 않는다
            if [nx, ny] == player:
                continue
            else:
                history.append([nx, ny])
                self.board_power[nx][ny] = max(0, self.board_power[nx][ny] - (self.board_power[player[0]][player[1]] // 2))
        
        # 부서지지 않은 포탑 중 공격과 무관한 포탑의 공격력 증가
        for i in range(self.n):
            for j in range(self.m):
                if self.board_power[i][j] == 0:
                    continue
                if [i, j] in history:
                    continue
                if [i, j] == player:
                    continue
                self.board_power[i][j] += 1

    
    def fix(self, player, target):
        """
        수정 필요
        player와 target, 그리고 영향을 받은 포탑들을 제외한 나머지 포탑들의 공격력이 1씩 올라간다
        """
        """
        포탑 정비
        player와 target을 제외한 포탑들의 공격력은 1씩 올라간다
        """
        for i in range(self.n):
            for j in range(self.m):
                if self.board_power[i][j]==0:
                    continue
                if i==player[0] and j==player[1]:
                    continue
                if i==target[0] and j==target[1]:
                    continue
                self.board_power[i][j] += 1

    def do_break(self):
        count = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.board_power[i][j] > 0:
                    count += 1
        
        if count == 1:
            return True

        return False

def main():
    instance = problem()

    for t in range(instance.k):
        instance.attack(t)
        if instance.do_break():
            break
    
    max_power = 0
    for i in range(instance.n):
        for j in range(instance.m):
            if instance.board_power[i][j] > max_power:
                max_power = instance.board_power[i][j]
    print(max_power)

if __name__ == "__main__":
    main()