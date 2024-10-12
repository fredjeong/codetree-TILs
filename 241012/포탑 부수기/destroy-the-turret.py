from collections import deque

class Problem():
    def __init__(self):
        self.n, self.m, self.k = map(int, input().split())

        # 포탑의 공격력을 나타낸 격자
        self.board = [list(map(int, input().split())) for _ in range(self.n)]

        # 각 포탑의 가장 최근 공격 시점을 나타낸 격자
        self.time = [[0 for _ in range(self.m)] for _ in range(self.n)]

        # 가장 약한 포탑에 주는 핸디캡
        self.bonus = self.n + self.m

    def select_attacker_target(self, turn):
        """
        공격자와 타겟 선정
        """
        arr = []

        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] <= 0:
                    continue
                arr.append([self.board[i][j], self.time[i][j], i, j])

        # 우선순위에 따라 공격자와 타겟 선정
        attacker = sorted(arr, key=lambda x:[x[0], -x[1], -(x[2]+x[3]), -x[3]])[0]
        attacker_pos = [attacker[2], attacker[3]]


        target = sorted(arr, key=lambda x: [-x[0], x[1], x[2]+x[3], x[3]])[0]
        target_pos = [target[2], target[3]]

        # 공격자의 공격력 추가
        self.board[attacker_pos[0]][attacker_pos[1]] += self.bonus

        # 공격 시점 표시
        self.time[attacker_pos[0]][attacker_pos[1]] = turn
        return attacker_pos, target_pos

    def attack(self, turn):
        """
        attacker가 target을 공격
        """
        """
        1. 레이저 공격
        """
        attacker_pos, target_pos = self.select_attacker_target(turn)

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        visited = [[False for _ in range(self.m)] for _ in range(self.n)]

        q = deque()
        q.append([[attacker_pos, None]])


        best_history = None

        while q:
            history = q.popleft()
            # 이렇게 할 경우 뒤에서 history의 시작점은 잘라줘야 한다
            pos, dir = history[-1]
            x = pos[0]
            y = pos[1]

            if visited[x][y]:
                continue
            visited[x][y] = True

            # 목표 지점에 도착했다면 경로를 반환한다
            if [x, y] == target_pos:
                # 경로 반환
                #history.append([[x, y], dir])
                if best_history == None:
                    best_history = history
                else:
                    if len(history) < len(best_history):
                        best_history = history
                    elif len(history) == len(best_history):
                        for idx in range(len(history)):
                            if history[idx][1] < best_history[idx][1]:
                                best_history = history
                                break
                            elif history[idx][1] == best_history[idx][1]:
                                continue
                            elif history[idx][1] > best_history[idx][1]:
                                break

            for i in range(len(dx)):
                nx = x + dx[i]
                ny = y + dy[i]

                # 격자를 벗어났다면 반대 방향으로 나오게 해줘야한다
                if nx < 0:
                    nx += self.n
                elif nx >= self.n:
                    nx -= self.n
                if ny < 0:
                    ny += self.m
                elif ny >= self.m:
                    ny -= self.m

                # 이미 방문했다면 고려하지 않는다
                if visited[nx][ny]:
                    continue

                # 부서진 포탑이라면 고려하지 않는다
                if self.board[nx][ny] <= 0:
                    continue

                # 아닌 경우 history에 넣는다
                q.append(history + [[[nx, ny], i]])

        # best_history가 존재한다면 레이저 공격을 할 수 있다는 뜻
        if best_history != None:
            affected = [[False for _ in range(self.m)] for _ in range(self.n)]
            affected[target_pos[0]][target_pos[1]] = True
            affected[attacker_pos[0]][attacker_pos[1]] = True
            # 타겟에게 공격자의 공격력만큼 피해를 준다
            self.board[target_pos[0]][target_pos[1]] -= self.board[attacker_pos[0]][attacker_pos[1]]

            # 경로상의 다른 포탑들에게 공격자의 공격력//2만큼의 피해를 준다
            # 처음과 마지막은 attacker와 target이므로 고려하지 않는다
            for id in range(1, len(best_history)-1):

                self.board[best_history[id][0][0]][best_history[id][0][1]] -= self.board[attacker_pos[0]][attacker_pos[1]] // 2
                affected[best_history[id][0][0]][best_history[id][0][1]] = True

            # 영향받지 않은 포탑들은 공격력을 1씩 올려준다
            for i in range(self.n):
                for j in range(self.m):
                    if affected[i][j]:
                        continue
                    if self.board[i][j] <= 0:
                        continue
                    self.board[i][j] += 1
            return

        # best_history가 없다면 포탄 공격을 한다
        dx = [1, -1, 0, 0, 1, 1, -1, -1]
        dy = [0, 0, 1, -1, 1, -1, 1, -1]

        x = target_pos[0]
        y = target_pos[1]
        power = self.board[attacker_pos[0]][attacker_pos[1]]

        # 타겟에게 공격
        self.board[x][y] -= power

        for i in range(len(dx)):
            nx = x + dx[i]
            ny = y + dy[i]

            # 격자를 벗어났다면 반대 방향으로 나오게 해줘야한다
            if nx < 0:
                nx += self.n
            elif nx >= self.n:
                nx -= self.n
            if ny < 0:
                ny += self.m
            elif ny >= self.m:
                ny -= self.m

            # 부서진 포탑이라면 고려하지 않는다
            if self.board[nx][ny] <= 0:
                continue

            # 자기 자신은 피해를 입지 않는다
            if [nx, ny] == attacker_pos:
                continue

            self.board[nx][ny] -= power // 2

def main():
    instance = Problem()

    for turn in range(instance.k):
        instance.attack(turn)

    # 남아있는 포탑 중 가장 강한 포탑의 공격력 출력
    max_power = 0
    for row in range(instance.n):
        local_max = max(instance.board[row])
        if local_max > max_power:
            max_power = local_max
    print(max_power)

if __name__ == "__main__":
    main()