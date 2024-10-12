class Problem():
    def __init__(self):
        """
        l: 체스판의 크기 (l+2 x l+2)
        n: 기사의 수
        q: 명령의 수
        """
        self.l, self.n, self.q = map(int, input().split())

        # 함정과 벽, 빈칸을 기록할 보드
        self.board = [[2 for _ in range(self.l + 2)]]
        for _ in range(self.l):
            arr = list(map(int, input().split()))
            self.board.append([2] + arr + [2])
        self.board.append([2 for _ in range(self.l + 2)])

        # 기사의 위치를 기록할 보드
        self.board_knight = [[-1 for _ in range(self.l+2)] for _ in range(self.l+2)]

        # 각 기사의 좌측 상단 위치
        self.knight_pos = []

        # 각 기사가 차지하는 영역의 높이와 너비
        self.knight_info = []

        # 각 기사의 현재 체력
        self.knight_hp = []

        # 각 기사의 탈락 유무
        self.out = [False for _ in range(self.n)]

        for _ in range(self.n):
            r, c, h, w, k = map(int, input().split())
            self.knight_pos.append([r, c])
            self.knight_info.append([h, w])
            self.knight_hp.append(k)

        self.knight_hp_original = self.knight_hp[:]

        for id in range(self.n):
            # 기사 보드에 기사들 위치 표시
            self.fill(id)

        # 방향 우선순위: 상/우/하/좌
        self.dx = [-1, 0, 1, 0]
        self.dy = [0, 1, 0, -1]

    def clear(self, id):
        """
        id번 기사가 board_knight에서 차지하고 있던 영역을 지운다
        """
        x = self.knight_pos[id][0]
        y = self.knight_pos[id][1]
        h = self.knight_info[id][0]
        w = self.knight_info[id][1]
        for i in range(x, x + h):
            for j in range(y, y + w):
                if self.board_knight[i][j] == id:
                    self.board_knight[i][j] = -1

    def fill(self, id):
        """
        id번 기사가 차지하는 영역을 board_knight에 표시한다
        """
        x = self.knight_pos[id][0]
        y = self.knight_pos[id][1]
        h = self.knight_info[id][0]
        w = self.knight_info[id][1]
        for i in range(x, x + h):
            for j in range(y, y + w):
                self.board_knight[i][j] = id

    def move(self, id, dir):
        x = self.knight_pos[id][0]
        y = self.knight_pos[id][1]
        h = self.knight_info[id][0]
        w = self.knight_info[id][1]

        # 명령을 받은 기사는 상하좌우 중 한 칸 이동할 수 있다
        nx = x + self.dx[dir]
        ny = y + self.dy[dir]

        ## 새 영역 내에 벽이 하나라도 있다면 명령 취소
        #for i in range(nx, nx + h):
        #    for j in range(ny, ny + w):
        #        if self.board[nx][ny] == 2:
        #            return

        # 새 영역 내에 다른 기사가 있다면 연쇄반응이 가능한지 본다
        global is_wall, s, visited
        is_wall = False
        s = set()
        s.add((id, nx, ny))
        visited = [False for _ in range(self.n)]
        self.interaction([nx, ny], id, dir)

        # 벽이 존재한다면 명령을 취소한다
        if is_wall:
            return

        # 벽이 존재하지 않는다면 연쇄반응을 시작한다
        for sub_id, sub_x, sub_y in s:
            # board_knight에서 기존 영역을 제거한다
            self.clear(sub_id)

            # 기사의 좌측 상단 위치를 갱신해준다
            self.knight_pos[sub_id] = [sub_x, sub_y]

            # 새 영역을 board_knight에 표시한다
            self.fill(sub_id)

            # 새 영역 내에 함정이 있다면 명령을 받은 기사를 제외하고는 피해를 입는다
            if sub_id == id:
                continue
            damage = 0
            for i in range(sub_x, sub_x + self.knight_info[sub_id][0]):
                for j in range(sub_y, sub_y + self.knight_info[sub_id][1]):
                    if self.board[i][j] == 1:
                        damage += 1
            self.knight_hp[sub_id] -= damage

            # 체력이 0 이하로 떨어진 기사는 탈락하며 board_knight에서 영역이 지워진다
            if self.knight_hp[sub_id] <= 0:
                self.out[sub_id] = True
                self.clear(sub_id)

    def interaction(self, pos, id, dir):
        """
        id: 이동한 기사의 번호
        pos: id번 기사가 밀려나서 자리한 좌측 상단
        """
        global is_wall, s, visited
        x = pos[0]
        y = pos[1]
        h = self.knight_info[id][0]
        w = self.knight_info[id][1]
        visited[id] = True

        # 새 영역에 벽이 있으면 명령은 취소된다
        for i in range(x, x + h):
            for j in range(y, y + w):
                if self.board[i][j] == 2:
                    is_wall = True
                    return

        do_break = True
        # 다른 기사가 있다면 집합에 그 기사의 id를 추가한다
        for i in range(x, x + h):
            for j in range(y, y + w):
                num = self.board_knight[i][j]
                if num >= 0 and not visited[num]:
                    visited[num] = True
                    do_break = False
                    # 다른 기사가 이동했을 때의 좌측 상단 좌표를 구한다
                    nx = self.knight_pos[num][0] + self.dx[dir]
                    ny = self.knight_pos[num][1] + self.dy[dir]
                    s.add((num, nx, ny))
                    self.interaction([nx, ny], num, dir)


        # 빈칸이라면 그대로 종료한다
        if do_break:
            return

def main():
    instance = Problem()

    for round in range(instance.q):
        id, dir = map(int, input().split())
        # 이미 탈락한 기사에게 내려지는 명령은 무시한다
        if instance.out[id-1]:
            continue
        instance.move(id-1, dir)

    # 생존한 기사들이 받은 데미지의 합 출력
    total_damage = 0
    for id in range(instance.n):
        if instance.out[id]:
            continue
        total_damage += instance.knight_hp_original[id] - instance.knight_hp[id]
    print(total_damage)

if __name__ == "__main__":
    main()