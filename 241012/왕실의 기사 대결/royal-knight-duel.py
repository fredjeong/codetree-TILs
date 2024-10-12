class Problem():
    def __init__(self):
        self.l, self.n, self.q = map(int, input().split())
        self.board = [[2 for _ in range(self.l + 2)]]
        for _ in range(self.l):
            arr = list(map(int, input().split()))
            self.board.append([2] + arr + [2])
        self.board.append([2 for _ in range(self.l + 2)])

        self.board_knight = [[-1 for _ in range(self.l+2)] for _ in range(self.l+2)]

        self.knight_pos = []
        self.knight_info = []
        self.knight_hp = []
        self.out = [False for _ in range(self.n)]
        self.total_damage = 0

        for _ in range(self.n):
            r, c, h, w, k = map(int, input().split())
            self.knight_pos.append([r, c])
            self.knight_info.append([h, w])
            self.knight_hp.append(k)

        for id in range(self.n):
            # 기사 보드에 기사들 위치 표시
            self.fill(id)

        self.dx = [-1, 0, 1, 0]
        self.dy = [0, 1, 0, -1]

    def clear(self, id):
        for i in range(self.knight_pos[id][0] + self.knight_info[id][0]):
            for j in range(self.knight_pos[id][1] + self.knight_info[id][1]):
                self.board_knight[i][j] = -1

    def fill(self, id):
        x = self.knight_pos[id][0]
        y = self.knight_pos[id][1]
        h = self.knight_info[id][0]
        w = self.knight_info[id][1]
        for i in range(x, x + h):
            for j in range(y, y + w):
                self.board_knight[i][j] = id

    def move(self, id, dir):
        """
        방향 dir는 0, 1, 2, 3 중 하나이며, 각각 상, 우, 하, 좌를 의미한다
        """
        x = self.knight_pos[id][0]
        y = self.knight_pos[id][1]
        h = self.knight_info[id][0]
        w = self.knight_info[id][1]

        # 명령을 받은 기사는 상하좌우 중 한 칸 이동할 수 있다
        nx = x + self.dx[dir]
        ny = y + self.dy[dir]

        # 이동하려는 위치에 벽이 있다면 명령 취소
        for i in range(nx, nx + h):
            for j in range(ny, ny + w):
                if self.board[i][j] == 2:
                    return

        # 이동하려는 모든 칸이 빈칸인지 검사
        is_empty = True
        for i in range(nx, nx + h):
            for j in range(ny, ny + w):
                if self.board_knight[i][j] != -1 and self.board_knight[i][j] != id:
                    is_empty = False
                    break
            if not is_empty:
                break

        # 빈칸이라면 위치 옮기기
        if is_empty:
            # 원래 위치로 저장되어있던 칸들 지우기
            self.clear(id)
            # 새 위치 저장
            self.knight_pos[id][0] = nx
            self.knight_pos[id][1] = ny
            # 보드에 채우기
            self.fill(id)
            return

        # 여기까지 왔다는 것은 다른 기사가 존재한다는 뜻
        # 여기서 원래 위치는 아직 비워지지 않았음
        global s, is_wall
        s = set()
        s.add((id, nx, ny))
        is_wall = False
        self.interaction(id, [nx, ny], dir)

        if is_wall:
            return
        for knight, pos_x, pos_y in s:
            # 기존 영역 지우기
            self.clear(knight)
            # 새 좌측상단 위치 등록
            self.knight_pos[knight] = [pos_x, pos_y]
            # 새 영역 표시
            self.fill(knight)
            # 이동한 칸에 함정이 있다면 첫 번째 기사를 제외하고 데미지 입힌다
            if knight == id:
                continue
            damage = 0
            x = self.knight_pos[knight][0]
            y = self.knight_pos[knight][1]
            h = self.knight_info[knight][0]
            w = self.knight_info[knight][1]
            for i in range(x, x + h):
                for j in range(y, y + w):
                    if self.board[i][j] == 1:
                        damage += 1
            self.knight_hp[knight] -= damage
            self.total_damage += damage
            if self.knight_hp[knight]  <= 0:
                self.out[knight] = True
                self.clear(knight)

    def interaction(self, id, pos, dir):
        global s, is_wall
        """
        id: 옮겨온 기사의 번호
        pos: 옮겨온 좌표 (좌측상단 기준)
        dir: 방향 
        """
        # 새 구역에서 영향을 받는 기사가 있는지 찾는다
        x = pos[0]
        y = pos[1]
        h = self.knight_info[id][0]
        w = self.knight_info[id][1]

        new_ids = set()
        for i in range(x, x + h):
            for j in range(y, y + w):
                # 벽이 있다면 즉시 모든 명령을 취소한다
                if self.board[i][j] == 2:
                    is_wall = True
                    return
                # 다른 기사가 있다면 그 기사를 new_ids에 추가한다
                if self.board[i][j] != 2 and self.board_knight[i][j] != -1 and (self.board_knight[i][j], x, y) not in s:
                    new_ids.add((self.board_knight[i][j], x, y))

        # 새롭게 발견된 기사가 없다면 그대로 종료
        if not new_ids:
            return

        # 새롭게 발견된 기사가 있다면 재귀함수를 작동시킨다
        s = s | new_ids
        for knight, _, _ in new_ids:

            nx = self.knight_pos[knight][0] + self.dx[dir]
            ny = self.knight_pos[knight][1] + self.dy[dir]
            self.interaction(knight, [nx, ny], dir)



def main():
    instance = Problem()

    for _ in range(instance.q):
        id, dir = map(int, input().split())
        if instance.out[id-1]:
            continue
        instance.move(id-1, dir)

    print(instance.total_damage)

if __name__ == "__main__":
    main()