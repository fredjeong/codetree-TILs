import sys

input = sys.stdin.readline

class problem():
    def __init__(self):
        """
        n: 게임판의 크기
        m: 게임 턴 수
        p: 산타의 수
        c: 루돌프의 힘
        d: 산타의 힘
        """
        self.n, self.m, self.p, self.c, self.d = map(int, input().split()) 
        self.rudolf_pos = list(map(int, input().split()))
        self.rudolf_pos[0] -= 1
        self.rudolf_pos[1] -= 1
        self.santa_pos = [[] for _ in range(self.p)]
        self.board = [[-1 for _ in range(self.n)] for _ in range(self.n)]
        
        for _ in range(self.p):
            p_n, pos_x, pos_y = map(int, input().split())
            p_n -= 1
            pos_x -=1
            pos_y -= 1
            self.board[pos_x][pos_y] = p_n
            self.santa_pos[p_n] = [pos_x, pos_y]
            

        self.out = [False for _ in range(self.p)] # 격자 밖으로 밀려나 탈락한 산타
        self.stun = [0 for _ in range(self.p)] # 기절 해제까지 남은 시간
        self.score = [0 for _ in range(self.p)] # 각 산타가 얻은 점수
        
    def get_distance(self, pos_1, pos_2):
        """
        input으로 두 개의 포지션 리스트를 받는다
        """
        return (pos_1[0] - pos_2[0])**2 + (pos_1[1] - pos_2[1])**2
    
    def move_rudolf(self):
        """
        루돌프가 게임에서 탈락하지 않은 산타 중 가장 가까운 산타를 향해 1칸 돌진한다
        만약 가장 가까운 산타가 2명 이상이라면 r좌표가 크고, c좌표가 큰 순서대로 돌진한다
        """
        # 가장 가까운 거리에 있는 산타 중 우선순위가 가장 높은 산타를 찾는다
        min_distance = 1e9
        min_distance_santa = 100 # 루돌프와 가장 가까이 있는 산타      
        
        for santa in range(self.p):
            # 게임에서 탈락한 산타는 고려하지 않는다
            if self.out[santa]==True:
                continue
            
            else:
                dist = self.get_distance(self.rudolf_pos, self.santa_pos[santa])
                if dist > min_distance:
                    # 계산한 거리가 최소거리보다 더 크다면 고려하지 않는다
                    continue
                
                elif dist == min_distance:
                    """
                    현재의 최소거리와 동일한 거리만큼 떨어져 있는 산타가 있다면 
                    두 산타의 위치를 비교하여 r좌표가 큰 산타를, r이 동일한 경우 c좌표가 큰 산타를 향해 돌진한다
                    """
                    # 기존 산타의 좌표
                    temp_pos_x_1 = self.santa_pos[min_distance_santa][0]
                    temp_pos_y_1 = self.santa_pos[min_distance_santa][1]

                    # 새 산타의 좌표
                    temp_pos_x_2 = self.santa_pos[santa][0]
                    temp_pos_y_2 = self.santa_pos[santa][1]
                    
                    # 기존 산타의 r좌표가 더 크다면 넘어간다
                    if temp_pos_x_1 > temp_pos_x_2:
                        continue
                    # 두 산타의 r좌표가 동일하다면 
                    elif temp_pos_x_1 == temp_pos_x_2:
                        # 기존 산타의 c좌표가 더 크다면 넘어간다
                        if temp_pos_y_1 > temp_pos_y_2:
                            continue
                        else:
                            min_distance_santa = santa
                    elif temp_pos_x_1 < temp_pos_x_2:
                        min_distance_santa = santa

                else:
                    min_distance = dist
                    min_distance_santa = santa
        
        # min_distance_santa를 향해 8방향 중 가장 가까워지는 방향으로 한 칸 돌진한다
        dx = [1, -1, 0, 0, 1, 1, -1, -1]
        dy = [0, 0, 1, -1, 1, -1, 1, -1]
        
        new_min_distance, min_direction = dist, 100
        for i in range(len(dx)):
            nx = self.rudolf_pos[0] + dx[i]
            ny = self.rudolf_pos[1] + dy[i]
            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                continue
            new_distance = self.get_distance([nx, ny], self.santa_pos[min_distance_santa])
            if new_distance > new_min_distance:
                continue
            else:
                new_min_distance = new_distance
                min_direction = i
        
        # 가장 가까워지는 방향으로 한 칸 이동 (대각선 포함)
        self.rudolf_pos[0] += dx[min_direction]
        self.rudolf_pos[1] += dy[min_direction]
        
        # 루돌프의 위치에 산타가 있다면 충돌 발생
        if self.board[self.rudolf_pos[0]][self.rudolf_pos[1]] >= 0:
            # 해당 위치의 산타는 C만큼의 점수 획득
            santa = self.board[self.rudolf_pos[0]][self.rudolf_pos[1]]
            self.score[santa] += self.c

            # 산타 기절
            self.stun[santa] = min(self.stun[santa] + 2, 2)
            
            # 충돌한 산타는 밀려나므로 원래 있던 자리 빈칸으로 만들어주기
            self.board[self.rudolf_pos[0]][self.rudolf_pos[1]] = -1
                
            # 산타는 루돌프가 이동해온 방향으로 C칸 만큼 밀려난다
            self.santa_pos[santa][0] += dx[min_direction] * self.c
            self.santa_pos[santa][1] += dy[min_direction] * self.c

            # 보드 밖으로 밀려났다면 탈락
            x = self.santa_pos[santa][0]
            y = self.santa_pos[santa][1]
            if x < 0 or x >= self.n or y < 0 or y >= self.n:
                self.out[santa] = True
                self.stun[santa] = -1
                return

            # 보드 밖으로 밀려나지 않았다면 밀려난 위치에 산타가 있는지 확인
            if self.board[x][y] >= 0:
                # 밀려난 위치에 산타가 있다면 상호작용 시작
                self.interaction(santa, dx[min_direction], dy[min_direction])
            else:
                # 보드에 산타의 새로운 위치 표시
                self.mark_board(santa)

    def move_santa(self, santa):
        # 기절했거나 이미 게임에서 탈락한 산타는 움직일 수 없음
        if self.out[santa] == True or self.stun[santa] > 0:
            return
        """
        루돌프와 가장 가까워지는 방향으로 움직인다
        """
        x = self.santa_pos[santa][0]
        y = self.santa_pos[santa][1]

        dx = [0, 1, 0, -1] # 좌하우상
        dy = [-1, 0, 1, 0]
        min_distance, min_direction = self.get_distance(self.santa_pos[santa], self.rudolf_pos), 100
        
        for i in range(len(dx)):
            nx = x + dx[i]
            ny = y + dy[i]
            
            # 게임판 밖으로 움직일 수 없다
            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                continue
            
            # 다른 산타가 있는 칸으로 움직일 수 없다
            if self.board[nx][ny] >= 0:
                continue

            dist = self.get_distance(self.rudolf_pos, [nx, ny])
            
            # 움직일 수 있는 칸이 있더라도 루돌프에게 가까워질 수 있는 방법이 없다면 움직이지 않는다
            if dist > min_distance:
                continue
            else:
                min_distance = dist
                min_direction = i
        
        # 산타가 이동하므로 보드에서 원래 있던 칸의 값을 -1로 바꿔준다
        self.refill_board(santa)

        if min_direction==100:
            self.mark_board(santa)
            return
        
        # 산타의 위치 갱신
        self.santa_pos[santa][0] = self.santa_pos[santa][0] + dx[min_direction]
        self.santa_pos[santa][1] = self.santa_pos[santa][1] + dy[min_direction]
    
        # 새로운 위치에 루돌프가 있다면 충돌 발생
        if self.rudolf_pos == self.santa_pos[santa]:
            # 산타가 D만큼의 점수 획득
            self.score[santa] += self.d

            # 산타 기절
            self.stun[santa] += 2

            # 보드에서 원래 위치 빈칸으로 바꾸어주기
            self.refill_board(santa)
            
            # 산타는 자신이 이동해 온 반대 방향으로 D칸 만큼 밀려난다
            self.santa_pos[santa][0] -= dx[min_direction] * self.d
            self.santa_pos[santa][1] -= dy[min_direction] * self.d

            # 보드 밖으로 밀려났다면 탈락
            temp_x = self.santa_pos[santa][0]
            temp_y = self.santa_pos[santa][1]

            if temp_x < 0 or temp_x >= self.n or temp_y < 0 or temp_y >= self.n:
                self.out[santa] = True
                self.stun[santa] = -1
                return

            # 밀려난 위치에 산타가 있는지 확인
            if self.board[temp_x][temp_y] >= 0:
                # 밀려난 위치에 산타가 있다면 상호작용 시작
                self.interaction(santa, dx[(min_direction + 2)%4], dy[(min_direction + 2)%4])
                return

        # 보드에 산타의 새로운 위치 표시
        self.mark_board(santa)

    def refill_board(self, santa):
        """
        산타가 이동할 때, 원래의 보드 위치를 바꾸어주는 함수
        """
        x = self.santa_pos[santa][0]
        y = self.santa_pos[santa][1]
        self.board[x][y] = -1

    def mark_board(self, santa):
        """
        산타의 새로운 위치를 저장해주는 함수
        """
        x = self.santa_pos[santa][0]
        y = self.santa_pos[santa][1]

        # 게임판 밖으로 밀려났을 경우 산타를 게임에서 탈락시킨다
        if x < 0 or x >= y < 0 or y >= self.n:
            self.out[santa] = True
            self.stun[santa] = -1
        else: 
            self.board[x][y] = santa
    
    def interaction(self, santa, dx, dy):
        """
        상호작용을 구현하는 재귀함수
        맨 처음 santa와 new_santa의 위치는 같다
        """
    
        x = self.santa_pos[santa][0]
        y = self.santa_pos[santa][1]

        # 재귀 상태에서 밀려난 산타가 밖으로 밀려났을 경우
        if x < 0 or x >= self.n or y < 0 or y >= self.n:
            self.out[santa] = True
            self.stun[santa] = -1
            return
        
        if self.board[x][y] == -1:
            self.board[x][y] = santa
            return

        new_santa = self.board[x][y]
        
        # 밀려온 산타가 현재 위치 점거
        self.board[x][y] = santa

        # 밀려나는 산타 이동
        self.santa_pos[new_santa][0] += dx
        self.santa_pos[new_santa][1] += dy

        # 밀려나는 산타에 대해 재귀함수 시행
        self.interaction(new_santa, dx, dy)

    def do_break(self):
        """
        남은 산타가 있는지 확인
        """
        if False in self.out:
            return False
        
        return True
    
    def refresh_stun(self):
        """
        매 턴 종료 후 스턴을 확인한다
        """
        for santa in range(self.p):
            if self.out[santa]==True:
                continue
            if self.stun[santa] > 0:
                self.stun[santa] -= 1
    
    def give_score(self):
        """
        매 턴 종료 후 아직 탈락하지 않은 산타들에게는 1점씩을 추가로 부여한다
        """
        for santa in range(self.p):
            if self.out[santa] == True:
                continue
            self.score[santa] += 1

def main():
    instance = problem()
    for t in range(instance.m):
        """
        매 턴마다 루돌프와 산타들이 순서대로 움직인다
        """

        # 루돌프의 움직임
        instance.move_rudolf()

        # 산타의 움직임
        for santa in range(instance.p):
            instance.move_santa(santa)

        if instance.do_break():
            break
        
        instance.give_score()
        instance.refresh_stun()
        

    print(" ".join(map(str, instance.score)))

if __name__=="__main__":
    main()