class Problem():
    def __init__(self):
        self.n, self.m, self.p, self.c, self.d = map(int, input().split())
        self.scores = [0 for _ in range(self.p)]

        self.rudolf_pos = list(map(int, input().split()))
        self.rudolf_pos[0] -= 1
        self.rudolf_pos[1] -= 1

        self.santa_pos = [[] for _ in range(self.p)]
        for _ in range(self.p):
            id, x, y = map(int, input().split())
            self.santa_pos[id-1] = [x-1, y-1]

        self.out = [False for _ in range(self.p)]
        self.stun = [0 for _ in range(self.p)]

    def get_distance(self, pos_1, pos_2):
        return (pos_1[0] - pos_2[0])**2 + (pos_1[1] - pos_2[1])**2

    def rudolf_move(self):
        # 루돌프는 가장 가까운 산타를 향해 1칸 돌진한다
        # 단, 게임에서 탈락하지 않은 산타 중 가장 가까운 산타를 선택해야 한다
        arr = []

        for id in range(self.p):
            if self.out[id]:
                continue
            dist = self.get_distance(self.rudolf_pos, self.santa_pos[id])
            arr.append([dist, id, self.santa_pos[id][0], self.santa_pos[id][1]])

        target_id = sorted(arr, key=lambda x:[x[0], -x[2], -x[3]])[0][1]
        # 루돌프는 타겟을 향해 8방향 중 가장 가까워지는 방향으로 돌진한다

        arr = []
        dx = [1, -1, 0, 0, 1, 1, -1, -1]
        dy = [0, 0, 1, -1, 1, -1, 1, -1]

        for i in range(len(dx)):
            nx = self.rudolf_pos[0] + dx[i]
            ny = self.rudolf_pos[1] + dy[i]

            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                continue

            dist = self.get_distance([nx, ny], self.santa_pos[target_id])
            arr.append([dist, [nx, ny], i])

        best = sorted(arr, key=lambda x:[x[0]])[0]
        self.rudolf_pos = best[1]
        dir = best[2]

        # 루돌프가 움직여서 충돌이 일어난 겨우
        if self.rudolf_pos in self.santa_pos:
            # 해당 산타는 C만큼의 점수를 얻게 된다
            id = self.santa_pos.index(self.rudolf_pos)
            self.scores[id] += self.c
            # 그리고 산타는 루돌프가 이동해온 방향으로 c칸만큼 밀려나게 된다
            x = self.santa_pos[id][0] + dx[dir]*self.c
            y = self.santa_pos[id][1] + dy[dir]*self.c

            # 밀려난 위치가 게임판 밖이라면 산타는 게임에서 탈락한다
            if x < 0 or x >= self.n or y < 0 or y >= self.n:
                self.out[id] = True
                self.santa_pos[id] = [100, 100]
                return

            # 산타는 루돌프와 충돌한 후 기절하게 된다
            self.stun[id] = 2

            # 밀려난 칸에 다른 산타가 있다면 상호작용이 발생한다
            self.interaction([x, y], id, dir, "rudolf")

    def interaction(self, pos, id, dir, type):
        if pos not in self.santa_pos:
            # 밀려온 산타의 위치 저장
            self.santa_pos[id] = pos
            return

        if type == "rudolf":
            dx = [1, -1, 0, 0, 1, 1, -1, -1]
            dy = [0, 0, 1, -1, 1, -1, 1, -1]
        elif type == "santa":
            dx = [-1, 0, 1, 0]
            dy = [0, 1, 0, -1]


        # 밀려난 위치에 원래 있던 산타 찾기
        new_id = self.santa_pos.index(pos)

        # 밀려온 산타의 위치 저장
        self.santa_pos[id] = pos

        # 밀려난 위치에 있던 산타는 한 칸 밀려난다
        x = pos[0] + dx[dir]
        y = pos[1] + dy[dir]

        # 밀려난 위치가 게임판 밖이라면 산타는 게임에서 탈락한다
        if x < 0 or x >= self.n or y < 0 or y >= self.n:
            self.out[new_id] = True
            return

        # 다른 산타가 있다면 재귀함수 실행
        self.interaction([x, y], new_id, dir, type)

    def santa_move(self, id):
        # 기절해있거나 격자 밖으로 빠져나가 탈락한 산타들은 움직일 수 없다
        if self.out[id] or self.stun[id] > 0:
            return

        threshold = self.get_distance(self.rudolf_pos, self.santa_pos[id])

        arr = []

        # 산타는 상하좌우 중 루돌프에게 가장 가까워지는 방향으로 1칸 이동한다
        # 방향이 작을수록 우선순위가 높다
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]

        for i in range(len(dx)):
            nx = self.santa_pos[id][0] + dx[i]
            ny = self.santa_pos[id][1] + dy[i]

            # 게임판 밖으로 움직일 수 없다
            if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                continue

            # 다른 산타가 있는 칸으로 움직일 수 없다
            if [nx, ny] in self.santa_pos:
                continue

            # 루돌프로푸터 가까워질 수 없다면 움직이지 않는다
            dist = self.get_distance(self.rudolf_pos, [nx, ny])
            if dist > threshold:
                continue

            arr.append([dist, i, [nx, ny]])

        if not arr:
            return


        best = sorted(arr, key=lambda x:[x[0], x[1]])[0]
        self.santa_pos[id] = best[2]
        dir = (best[1] + 2)%4


        # 산타와 루돌프가 같은 칸에 있게 되면 충돌 발생
        if self.santa_pos[id] == self.rudolf_pos:
            # 해당 산타는 D만큼의 점수를 얻는다
            self.scores[id] += self.d

            # 산타는 자신이 이동해온 반대 방향으로 D칸 만큼 밀려나게 된다
            x = self.santa_pos[id][0] + dx[dir] * self.d
            y = self.santa_pos[id][1] + dy[dir] * self.d
            # 밀려난 위치가 게임판 밖이라면 산타는 게임에서 탈락한다
            if x < 0 or x >= self.n or y < 0 or y >= self.n:
                self.out[id] = True
                self.santa_pos[id] = [100, 100]
                return

            # 산타는 루돌프와 충돌한 후 기절하게 된다
            self.stun[id] = 2

            # 밀려난 칸에 다른 산타가 있다면 상호작용이 발생한다
            self.interaction([x, y], id, dir, "santa")

def main():
    instance = Problem()

    # 게임은 총 m개의 턴에 걸쳐 진행된다
    for _ in range(instance.m):
    #for _ in range(1):
        # 매 턴마다 루돌프가 한 번 움직이고
        instance.rudolf_move()

        # 0번 산타부터 p-1번 산타까지 순서대로 움직인다
        for id in range(instance.p):
            instance.santa_move(id)

        # 모두 탈락하면 그 즉시 게임이 종료된다
        if False not in instance.out:
            break

        # 매 턴 이후 아직 탈락하지 않은 산타들에게는 1점씩을 추가로 부여한다
        # 스턴 회복
        for id in range(instance.p):
            if instance.out[id]:
                continue
            instance.scores[id] += 1
            if instance.stun[id] == 0:
                continue
            instance.stun[id] -= 1

    print(" ".join(map(str, instance.scores)))

if __name__ == "__main__":
    main()