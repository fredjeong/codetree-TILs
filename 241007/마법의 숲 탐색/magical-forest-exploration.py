import sys
from collections import deque

input = sys.stdin.readline

class create_game():
    def __init__(self):
        self.score = 0
    
    def load_info(self):
        self.row, self.col, self.k = map(int, input().split())
        self.row +=3

    def reset(self):
        self.board = [[0 for _ in range(self.col)] for _ in range(self.row)]
        self.exits = set()

    def mark(self):
        """
        더 이상 움직일 수 없을 때, 정령의 위치를 기록하고 점수 산정
        """
        max_row = 0
        visited = [[False for _ in range(self.col)] for _ in range(self.row)]
        
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]

        q = deque()
        q.append([self.x, self.y])
        visited[self.x][self.y] = True

        while q:
            pos_x, pos_y = q.popleft()
            # 이동하고자 하는 칸을 이미 방문했다면 continue
            if pos_x > max_row:
                max_row = pos_x

            for i in range(len(dx)):
                nx = pos_x + dx[i]
                ny = pos_y + dy[i]

                # 이동하고자 하는 칸이 숲 밖이라면 continue
                if nx < 3 or nx >= self.row or ny < 0 or ny >= self.col:
                    continue

                # 이동하고자 하는 칸을 이미 방문했다면 continue
                if visited[nx][ny]==True:
                    continue

                
                # 이동하고자 하는 칸에 골렘이 없다면 continue
                if self.board[nx][ny]==0:
                    visited[nx][ny] = True
                    continue

                # 번호가 다른 칸으로 이동하려 하는데 현재 위치가 출구가 아니라면 continue
                if self.board[pos_x][pos_y]!=self.board[nx][ny] and (pos_x, pos_y) not in self.exits:
                    continue
                visited[nx][ny] = True
                q.append([nx, ny])

        return max_row
        
    
    def record(self):
        # 보드에 위치 기록
        self.board[self.x][self.y] = self.id
        self.board[self.x+1][self.y] = self.id
        self.board[self.x-1][self.y] = self.id
        self.board[self.x][self.y-1] = self.id
        self.board[self.x][self.y+1] = self.id

        # 출구 기록
        if self.d==0:
            self.exits.add((self.x-1, self.y))
        elif self.d==1:
            self.exits.add((self.x, self.y+1))
        elif self.d==2:
            self.exits.add((self.x+1, self.y))
        elif self.d==3:
            self.exits.add((self.x, self.y-1))

        # 정령 이동 및 score 추가
        row_score = self.mark()
        self.score += row_score - 2
    
    def change_direction(self):
        if self.direction=="south":
            self.direction = "west"
        if self.direction == "west":
            self.direction = "east"

    def can_go_south(self, x, y, direction):
        if x==self.row-2:
            return False
        if direction=="west":
            if y ==1:
                return False
            if self.board[x-1][y-1]!=0 or self.board[x][y-2]!=0 or self.board[x+1][y-1]!=0:
                return False
            y -= 1
        elif direction=="east":
            if y == self.col - 2:
                return False
            if self.board[x-1][y+1]!=0 or self.board[x][y+2]!=0 or self.board[x+1][y+1]!=0:
                return False
            y += 1
        if self.board[x+2][y]==0 and self.board[x+1][y-1]==0 and self.board[x+1][y+1]==0:
            return True
        return False

    def play(self, id):
        self.c, self.d = map(int, input().split())
        self.id = id
        self.x = 1
        self.y = self.c - 1
        
        # 0: 북, 1: 동, 2: 남, 3: 서
        
        while True:
            if self.can_go_south(self.x, self.y, "south"):
                self.x += 1
            elif self.can_go_south(self.x, self.y, "west"):
                self.x += 1
                self.y -= 1
                self.d -= 1
                if self.d < 0:
                    self.d += 4
            elif self.can_go_south(self.x, self.y, "east"):
                self.x += 1
                self.y += 1
                self.d += 1
                if self.d > 3:
                    self.d -= 4
            else:
                if self.x <= 3:
                    self.reset()
                else:
                    self.record()
                break

def run():
    # 인스턴스 생성
    game = create_game()

    # 행, 열, 입력값 개수 불러오기
    game.load_info()

    # board, exits 초기화
    game.reset()
    
    for id in range(1, game.k+1):
        game.play(id)

    return game.score

if __name__=="__main__":
    result = run()
    print(result)