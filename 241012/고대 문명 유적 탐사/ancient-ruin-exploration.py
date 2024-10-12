from collections import deque

class Problem():
    def __init__(self):
        self.k, self.m = map(int, input().split())
        self.board = [list(map(int, input().split())) for _ in range(5)]
        self.score = []
        self.treasure = deque(map(int, input().split()))
        self.do_break = False

    def explore(self):
        arr = []
        score = 0

        # 3x3 격자 선택
        for i in range(3):
            for j in range(3):
                # start_x: i, start_y: j
                # 90도 회전
                self.rotate(i, j)
                history, value = self.get_value()
                arr.append([value, 1, i, j, history])

                # 180도 회전
                self.rotate(i, j)
                history, value = self.get_value()
                arr.append([value, 2, i, j, history])

                # 270도 회전
                self.rotate(i, j)
                history, value = self.get_value()
                arr.append([value, 3, i, j, history])

                # 원래대로 돌리기
                self.rotate(i, j)

        # arr 정렬해서 가장 좋은 선택지 뽑기
        best_choice = sorted(arr, key=lambda x:[-x[0], x[1], x[3], x[2]])[0]
        for i in range(best_choice[1]):
            self.rotate(best_choice[2], best_choice[3])

        # 만약 어떤 경우에도 유물을 획득할 수 없었다면 모든 탐사는 종료한다
        if best_choice[0] == 0:
            self.do_break = True
            return

        score += best_choice[0]

        # history에 있는 유물 제거하고 새로 채워넣기
        temp_arr = sorted(best_choice[4], key=lambda x:[x[1], -x[0]])
        for elem in temp_arr:
            self.board[elem[0]][elem[1]] = self.treasure.popleft()



        while True:
            history, value = self.get_value()
            if value == 0:
                break
            score += value

            temp_arr = sorted(history, key=lambda x: [x[1], -x[0]])
            for elem in temp_arr:
                self.board[elem[0]][elem[1]] = self.treasure.popleft()

        self.score.append(score)

    def rotate(self, start_x, start_y):
        """
        self.board를 90도 회전
        """
        temp = [self.board[row][:] for row in range(5)]

        for i in range(3):
           for j in range(3):
               temp[start_x + j][start_y + 2 - i] = self.board[start_x + i][start_y + j]
        self.board = temp

    def get_value(self):
        """
        주어진 보드의 가치 계산
        """
        value = 0
        history = []
        visited = [[False for _ in range(5)] for _ in range(5)]

        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]

        for i in range(5):
           for j in range(5):
               if visited[i][j]:
                   continue
               child = [[i, j]]
               count = 1
               colour = self.board[i][j]
               q = deque()
               q.append([i, j])
               while q:
                   x, y = q.popleft()
                   if visited[x][y]:
                       continue
                   visited[x][y] = True

                   for k in range(4):
                       nx = x + dx[k]
                       ny = y + dy[k]

                       if nx < 0 or nx >= 5 or ny < 0 or ny >= 5:
                           continue
                       if visited[nx][ny]:
                           continue
                       if self.board[nx][ny] != colour:
                           continue


                       if [nx, ny] not in child:
                           child.append([nx, ny])
                           count += 1
                       q.append([nx, ny])

               if count >= 3:
                   history.extend(child)
                   value += count

        return history, value

def main():
    instance = Problem()

    for _ in range(instance.k):
        instance.explore()
        if instance.do_break:
            break
    print(" ".join(map(str, instance.score)))

if __name__ == "__main__":
    main()