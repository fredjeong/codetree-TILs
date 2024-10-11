from collections import deque

class Problem():
    def __init__(self):
        self.n, self.m, self.k, self.c = map(int, input().split())
        self.board = [list(map(int, input().split())) for _ in range(self.n)]
        self.toxic = [[0 for _ in range(self.n)] for _ in range(self.n)] # 제초제 남은 시간
        self.score = 0

    def tree_grow(self):
        self.reproduce_counts = [[0 for _ in range(self.n)] for _ in range(self.n)]
        temp = [self.board[i][:] for i in range(self.n)]

        # 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장한다
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]

        for i in range(self.n):
            for j in range(self.n):
                # 나무가 없다면 패스
                if self.board[i][j] <= 0:
                    continue
                count = 0
                reproduce_count = 0
                # 나무가 있다면
                for k in range(len(dx)):
                    nx = i + dx[k]
                    ny = j + dy[k]
                    if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                        continue
                    if self.board[nx][ny] > 0:
                        count += 1
                    if self.board[nx][ny] == 0:
                        reproduce_count += 1

                self.board[i][j] += count
                self.reproduce_counts[i][j] = reproduce_count

    def tree_reproduce(self):
        temp = [self.board[i][:] for i in range(self.n)]

        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]

        for i in range(self.n):
            for j in range(self.n):
                # 나무가 없다면 패스
                if self.board[i][j] <= 0:
                    continue
                for k in range(len(dx)):
                    nx = i + dx[k]
                    ny = j + dy[k]
                    if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                        continue
                    # 아직 제초제가 뿌려져 있는 칸에는 번식을 진행하지 않는다
                    if self.board[nx][ny] == 0 and self.toxic[nx][ny]==0:
                        temp[nx][ny] += self.board[i][j] // self.reproduce_counts[i][j]

        self.board = temp

    def get_tree_to_kill(self):
        tree_to_kill = None
        maximum_trees_to_kill = 0

        # 제초제를 뿌릴 나무를 찾는다
        # 가장 많은 나무를 죽일 수 있는 칸에 제초제를 뿌린다

        dx = [1, 1, -1, -1]
        dy = [1, -1, 1, -1]

        for i in range(self.n):
            for j in range(self.n):
                # 나무가 없는 칸에 제초제를 뿌리면 박멸되는 나무가 없다
                if self.board[i][j] <= 0:
                    continue
                # 나무가 있는 칸에 제초제를 뿌리게 되면 4개의 대각선 방향으로 k칸만큼 전파된다
                count = self.board[i][j]
                for direction in range(len(dx)):
                    for k in range(1, self.k+1):
                        nx = i + dx[direction]*k
                        ny = j + dy[direction]*k

                        if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                            break

                        # 전파되는 도중 벽이 있거나 나무가 아예 없는 칸이 있는 경우 제초제가 전파되지 않는다
                        if self.board[nx][ny] == -1 or self.board[nx][ny] == 0:
                            break

                        count += self.board[nx][ny]

                if count > maximum_trees_to_kill:
                    maximum_trees_to_kill = count
                    tree_to_kill = [i, j]

        return tree_to_kill, maximum_trees_to_kill

    def kill_tree(self):
        """
        get_tree_to_kill로 죽일 나무를 찾아고 거기서
        """
        tree_to_kill, maximum_trees_to_kill = self.get_tree_to_kill()

        # 이미 모든 나무가 박멸되었다면 제초제를 뿌리지 않는다
        if maximum_trees_to_kill == 0:
            return

        x = tree_to_kill[0]
        y = tree_to_kill[1]
        self.score += maximum_trees_to_kill

        dx = [1, 1, -1, -1]
        dy = [1, -1, 1, -1]

        # 우선 시작하는 칸에 제초제를 뿌린다
        self.board[x][y] = 0
        self.toxic[x][y] = self.c

        # 4개의 대각선 방향으로 k칸만큼 전파된다
        for direction in range(len(dx)):
            for k in range(1, self.k + 1):
                nx = x + dx[direction]*k
                ny = y + dy[direction]*k

                if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                    break

                self.toxic[nx][ny] = self.c
                # 전파되는 도중 벽이 있거나 나무가 아예 없는 칸이 있는 경우 그 칸 까지만 제초제를 뿌린다
                if self.board[nx][ny] == -1 or self.board[nx][ny] == 0:
                    break

                #self.score += self.board[nx][ny]
                self.board[nx][ny] = 0

def main():
    instance = Problem()

    for _ in range(instance.m):
        # 나무의 성장
        instance.tree_grow()

        # 나무의 번식
        instance.tree_reproduce()

        # 제초제 지우기
        for i in range(instance.n):
            for j in range(instance.n):
                if instance.toxic[i][j] > 0:
                    instance.toxic[i][j] -= 1

        # 제초제를 뿌리는 작업 진행
        instance.kill_tree()

    print(instance.score)

if __name__ == "__main__":
    main()