import sys
from collections import deque

input = sys.stdin.readline

class exploration():
    def __init__(self):
        self.k, self.m = map(int, input().split())
        self.board = [list(map(int, input().split())) for _ in range(5)]
        self.arr_original = list(map(int, input().split()))
    
    def reset(self):
        self.total_value = 0
    
    def reset_arr(self):
        self.arr = deque(self.arr_original[:])
    
    def rotate_board_90(self, x, y):
        """
        중심 좌표: x, y를 기준으로 3*3
        """
        temp = [[0 for _ in range(3)] for _ in range(3)]
        dx = x-1
        dy = y-1
        for i in range(3):
            for j in range(3):
                temp[j][2-i] = self.board[i+dx][j+dy]
        
        for i in range(3):
            for j in range(3):
                self.board[i+dx][j+dy] = temp[i][j]

    def calculate_value(self):
        """
        상하좌우로 인접한 같은 종류의 유물 조각이 3개 이상일 경우 해당 조각들 삭제 (0으로 처리하면 될듯)
        유물의 가치는 모인 조각의 개수와 같다 
        
        처음에 한 번 쓰고, fill_in 쓰고, 또 확인해서 3개 이상 이어진 조각이 없을 때까지 반복 (재귀함수 혹은 while문)
        """
        visited = [[False for _ in range(5)] for _ in range(5)]
        pop_list = set()
        rotate_val = 0
        
        q = deque()
        
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]
        
        for i in range(5):
            for j in range(5):
                if visited[i][j]==True:
                    continue
                visited[i][j] = True
                q.append([i, j])
                count = 1
                stack = set()
                while q:
                    x, y = q.popleft()
                    stack.add((x, y))

                    for n in range(len(dx)):
                        nx = x + dx[n]
                        ny = y + dy[n]
                        
                        if nx < 0 or nx >= 5 or ny < 0 or ny >= 5:
                            continue
                        if visited[nx][ny]==True:
                            continue
                        if self.board[nx][ny]==self.board[x][y]:
                            count += 1
                            visited[nx][ny] = True
                            q.append([nx, ny])
                            stack.add((nx, ny))
                    
                    if not q:
                        if count >= 3:
                            rotate_val += count
                            pop_list = pop_list | stack
                        break
        pop_list = list(pop_list)
        return rotate_val, pop_list

def main():
    game = exploration()
    
    val_arr = []
    game.reset_arr()
    for _ in range(game.k):
        """
        유물 1차 획득
        """
        val_list = []
        game.reset()
        
        for i in range(1, 4):
            for j in range(1, 4):
                for angle in range(1,4):
                    game.rotate_board_90(i, j)
                    rotate_val, pop_list = game.calculate_value()
                    val_list.append([rotate_val, 90*angle, j, i, pop_list])
                game.rotate_board_90(i, j) # 원래대로 돌려놓기
                
        # 우선순위에 따라 best 조합 선택하고 거기에 맞게 배열 회전
        best_choice = sorted(val_list, key=lambda x: [-x[0], x[1], x[2], x[3], x[4]])[0]
        if best_choice[1]==90:
            game.rotate_board_90(best_choice[3], best_choice[2])
        elif best_choice[1]==180:
            for _ in range(2):
                game.rotate_board_90(best_choice[3], best_choice[2])
        elif best_choice[1]==270:
            for _ in range(3):
                game.rotate_board_90(best_choice[3], best_choice[2])
        
        # 아직 K번 반복하지 않았더라도 유물을 획득할 수 없었다면 모든 탐사는 종료한다
        if best_choice[0] == 0:
            break
        game.total_value += best_choice[0]

        pop_list = sorted(best_choice[-1], key=lambda x: [x[1], -x[0]])
        for x, y in pop_list:
            game.board[x][y] = game.arr.popleft()
        
        while True:
            rotate_val, pop_list = game.calculate_value()
            if rotate_val==0:
                break
            pop_list = sorted(pop_list, key=lambda x: [x[1], -x[0]])
            for x, y in pop_list:
                game.board[x][y] = game.arr.popleft()
            game.total_value += rotate_val
        val_arr.append(game.total_value)
    return val_arr
        
if __name__ == "__main__":
    result = main()
    if len(result)==1:
        print(result[0])
    else:
        print(" ".join(map(str, result)))