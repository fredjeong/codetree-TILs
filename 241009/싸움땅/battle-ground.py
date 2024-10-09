import sys
import heapq

input = sys.stdin.readline

class problem():
    def __init__(self):
        """
        n: 격자의 크기
        m: 플레이어의 수
        k: 라운드의 수

        board: 격자에 있는 총의 정보
        player_pos: 0번 플레이어부터 m-1번 플레이어까지의 [행, 열]
        player_info: 0번 플레이어부터 m-1번 플레이어까지의 [점수, 방향, 초기 능력치, 가지고 있는 총의 공격력]
        방향 0, 1, 2, 3은 순서대로 상 우 하 좌를 의미
        out: 탈락한 플레이어
        """
        self.n, self.m, self.k = map(int, input().split())
        self.board = [[[] for _ in range(self.n)] for _ in range(self.n)]
        for i in range(self.n):
            arr = list(map(int, input().split()))
            for j in range(self.n):
                heapq.heappush(self.board[i][j], -arr[j])
                #self.board[i][j].append(arr[j])

        self.player_pos = []
        self.player_info = []
        for _ in range(self.m):
            x, y, d, s = map(int, input().split())
            self.player_pos.append([x-1, y-1]) # 행, 열
            self.player_info.append([0, d, s, 0]) # 점수, 방향, 초기 능력치, 가지고 있는 총의 공격력
        self.out = [False for _ in range(self.m)]

        self.dx = [-1, 0, 1, 0]
        self.dy = [0, 1, 0, -1]

    def play(self, player):
        x = self.player_pos[player][0] 
        y = self.player_pos[player][1]
        d = self.player_info[player][1]
        ability = self.player_info[player][2]
        power = self.player_info[player][3]

        # 본인이 향하고 있는 방향대로 한 칸만큼 이동
        nx = x + self.dx[d]
        ny = y + self.dy[d]

        # 만약 격자를 벗어나는 경우 방향을 바꾸어 1만큼 이동
        if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
            # 방향 변경
            d = (d + 2)%4
            
            # 바꾼 방향 저장
            self.player_info[player][1] = d

            # 새로운 위치 정의
            nx = x + self.dx[d]
            ny = y + self.dy[d]
                
        # 이동한 방향에 플레이어가 없는 경우
        if [nx, ny] not in self.player_pos:
            # 새 위치 저장
            self.player_pos[player][0] = nx
            self.player_pos[player][1] = ny
            
            # 총이 있는 경우
            if self.board[nx][ny]:
                # 플레이어가 이미 총을 가지고 있는 경우
                if power > 0:
                    # 놓여있는 총들 중 가장 공격력이 높은 총을 뽑는다
                    max_on_board = -heapq.heappop(self.board[nx][ny])
                    # 그 총이 더 공격력이 높다면 플레이어가 갖고, 원래 총은 내려놓는다
                    if power < max_on_board:
                        heapq.heappush(self.board[nx][ny], -power)
                        power = max_on_board
                        # 새 공격력 저장
                        self.player_info[player][3] = power
                    
                    # 원래 총이 더 공격력이 높다면 뽑은 총은 다시 내려놓는다
                    else:
                        heapq.heappush(self.board[nx][ny], -max_on_board)

                # 플레이어가 총을 가지고 있지 않은 경우
                else:
                    # 놓여있는 총들 중 가장 공격력이 높은 총을 뽑는다
                    max_on_board = -heapq.heappop(self.board[nx][ny])
                    power = max_on_board
                    # 새 공격력 저장
                    self.player_info[player][3] = power
        
        # 이동한 방향에 플레이어가 있는 경우
        else:
            """
            여기서 player의 위치는 아직 x, y로 저장되어 있음
            """
            new_player = self.player_pos.index([nx, ny])
            new_x = self.player_pos[new_player][0] 
            new_y = self.player_pos[new_player][1]
            new_d = self.player_info[new_player][1]
            new_ability = self.player_info[new_player][2]
            new_power = self.player_info[new_player][3]
            # 싸움 시작
            # player와 new_player의 초기 능력치와 가지고 있는 총의 공격력의 합을 비교하여 더 큰 플레이어가 이긴다
            if power + ability > new_power + new_ability:
                winner = player
                loser = new_player
            
            elif power + ability == new_power + new_ability:
                if ability > new_ability:
                    winner = player
                    loser = new_player
                else:
                    winner = new_player
                    loser = player
            else:
                winner = new_player
                loser = player
            
            # 이긴 플레이어는 각 플레이어의 초기 능력치와 가지고 있는 총의 공격력의 합의 차이만큼을 포인트로 획득
            self.player_info[winner][0] += abs((ability + power) - (new_ability + new_power))

            # player 위치 저장
            self.player_pos[player][0] = nx
            self.player_pos[player][1] = ny

            self.loser_move(loser)
            self.winner_move(winner)
            

    def loser_move(self, loser):
        x = self.player_pos[loser][0]
        y = self.player_pos[loser][1]
        d = self.player_info[loser][1]
        power = self.player_info[loser][3]
                       
        # 본인이 가지고 있던 총을 해당 격자에 내려놓는다
        heapq.heappush(self.board[x][y], -power)
        
        # 본인의 공격력은 0이 된다
        self.player_info[loser][3] = 0

        # 플레이어가 원래 가지고 있던 방향대로 한 칸 이동한다
        while True:
            nx = x + self.dx[d]
            ny = y + self.dy[d]
            
            # 격자 범위 밖인 경우, 또는 이동하려는 칸에 다른 플레이어가 있는 경우 오른쪽으로 90도 회전한다
            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n or [nx, ny] in self.player_pos:
                d += 1
                if d > 3:
                    d -= 4
                continue
            
            # 빈 칸이 보이면 이동한다
            # 해당 칸에 총이 있다면
            if self.board[nx][ny]:
                # 가장 공격력이 높은 총을 획득
                max_power = -heapq.heappop(self.board[nx][ny])
                self.player_info[loser][3] = max_power
            
            # 위치, 방향 저장
            self.player_pos[loser][0] = nx
            self.player_pos[loser][1] = ny
            self.player_info[loser][1] = d
            break
    
    def winner_move(self, winner):
        """
        이긴 플레이어는 승리한 칸에 떨어져 있는 총들과 원래 들고 있던 총 중 가장 공격력
        """
        x = self.player_pos[winner][0]
        y = self.player_pos[winner][1]
        d = self.player_info[winner][1]
        power = self.player_info[winner][3]

        # 놓여있는 총들 중 가장 공격력이 높은 총을 뽑는다
        max_on_board = -heapq.heappop(self.board[x][y])
        
        # 그 총이 더 공격력이 높다면 플레이어가 갖고, 원래 총은 내려놓는다
        if power < max_on_board:
            heapq.heappush(self.board[x][y], -power)
            power = max_on_board
            
            # 새 공격력 저장
            self.player_info[winner][3] = power
        
        # 원래 총이 더 공격력이 높다면 뽑은 총은 다시 내려놓는다
        else:
            heapq.heappush(self.board[x][y], -max_on_board)

def main():
    instance = problem()

    # k라운드 동안 게임 진행
    for _ in range(instance.k):
        # 각 라운드마다 첫 번째 플레이어부터 게임 시작
        for player in range(instance.m):
            instance.play(player)

    # 최종적으로 각 플레이어들이 획득한 점수 출력
    scores = []
    for player in range(instance.m):
        scores.append(instance.player_info[player][0])

    print(" ".join(map(str, scores)))

if __name__ == "__main__":
    main()