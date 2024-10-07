import sys

input = sys.stdin.readline

class problem():
    def __init__(self):
        """
        L: 체스판의 크기 (L*L)
        N: 기사의 수
        Q: 전체 턴 수

        board_map: 함정, 벽, 빈 칸의 위치 표시
        board_knight: 기사들의 위치 표시
        out: 탈락한 기사
        knight_pos: 각 기사들의 왼쪽 상단 (r, c) 표시
        knight_size: 각 기사들의 크기 (h, w) 표시
        """
        self.l, self.n, self.q = map(int, input().split())
        
        self.knight_pos = [[] for _ in range(self.n)]
        self.knight_size = [[] for _ in range(self.n)]
        # 기사의 탈락 여부 관리
        self.out = [False for _ in range(self.n)]
        
        # 체스판 바깥도 벽으로 취급하므로 체스판의 전체 길이를 (L+1)*(L+1)로 취급
        self.board_map = [[2 for _ in range(self.l+2)]]
        for _ in range(self.l):
            self.board_map.append([2] + list(map(int, input().split())) + [2])
        self.board_map.append([2 for _ in range(self.l+2)])
        
        # 기사의 체력
        self.hp = [0 for _ in range(self.n)]

        self.board_knight = [[-1 for _ in range(self.l+2)] for _ in range(self.l+2)]
        for id in range(self.n):
            r, c, h, w, k = map(int, input().split())

            # 기사의 위치 추가
            self.knight_pos[id] = [r, c]

            # 기사의 크기 추가
            self.knight_size[id] = [h, w]
            
            # 보드에 기사가 차지하는 영역 추가
            for i in range(r, r+h):
                for j in range(c, c+w):
                    self.board_knight[i][j] = id

            # 기사의 체력 추가
            self.hp[id] = k
        self.board_knight.append([2 for _ in range(self.l+2)])
        
        self.hp_original = self.hp[:]
        # 방향 d는 0, 1, 2, 3 중 하나이며, 각각 위쪽, 오른쪽, 아래쪽, 왼쪽을 의미한다
        self.dx = [-1, 0, 1, 0]
        self.dy = [0, 1, 0, -1]

    def move_knight(self, id, direction):
        """
        id번 기사를 direction 방향으로 한 칸 움직이고
        그 위치에 다른 기사가 있다면 연쇄반응을 시작하되, 
        최종적으로 밀려나는 기사가 벽에 있다면 모든 기사는 이동할 수 없다
        """
        do_interaction = False
        interaction_knights = set()
        
        # 체스판에서 사라진 기사에게 명령을 내리면 아무런 반응이 없다
        if self.out[id] == True:
            return
        
        # 왕의 명령을 받은 기사는 지정된 방향으로 한 칸 이동한다
        h = self.knight_size[id][0]
        w = self.knight_size[id][1]
        nx = self.knight_pos[id][0] + self.dx[direction] # 이동할 위치의 r
        ny = self.knight_pos[id][1] + self.dy[direction] # 이동할 위치의 c
        
        # 단, 이동하려는 위치에 벽이 있다면 이동을 취소하고 턴을 종료한다
        for i in range(nx, nx+h):
            for j in range(ny, ny+w):
                if self.board_map[i][j] == 2:
                    return

        # 새로운 위치에 다른 기사가 있다면 연쇄반응을 시작한다
        # 동시에 여러 기사가 반응할 수 있고, 그 중 하나라도 연쇄반응 과정에서 벽에 부딪히는 기사가 있다면 이동이 취소되므로 우선 따로 명단을 만들어 관리
        for i in range(nx, nx+h):
            for j in range(ny, ny+h):
                if self.board_knight[i][j] >= 0 and self.board_knight[i][j] != id:
                    do_interaction = True
                    interaction_knights.add(self.board_knight[i][j])
        
        # 연쇄반응이 없다면 그대로 턴을 종료한다
        if do_interaction == False:
            # 보드에 기존 위치 지우기
            self.refill_board(id)

            # 기사의 위치 갱신
            self.knight_pos[id][0] = nx
            self.knight_pos[id][1] = ny

            # 보드에 새로운 위치 저장
            self.mark_board(id)

            return
            
        # 연쇄반응을 시작하는 경우
        global do_cancel
        do_cancel = False

        for sub_id in interaction_knights:
            self.check_interaction(sub_id, direction)
        
        # 연쇄반응이 일어날 때 벽에 부딪히는 기사가 생긴다면 명령을 받은 기사도 이동하지 않고 그대로 턴을 종료
        if do_cancel == True:
            return
        
        # 연쇄반응이 일어날 수 있다면 모든 기사를 연쇄반응에 따라 이동시킨다
        #for sub_id in interaction_knights:
        #    self.interaction(sub_id, direction)
        global visited
        visited = [False for _ in range(self.n)]
        self.refill_board(id)
        for sub_id in interaction_knights:
            self.interaction(sub_id, direction)
        
        # 기사의 위치 갱신
        self.knight_pos[id][0] = nx
        self.knight_pos[id][1] = ny
        
        # 보드에 새로운 위치 저장
        self.mark_board(id)


    def check_interaction(self, id, direction):
        """
        명령을 받은 기사에 의해 부딪힌 각 기사에 대해 연쇄반응 시작
        """
        global do_cancel

        h = self.knight_size[id][0]
        w = self.knight_size[id][1]
        nx = self.knight_pos[id][0] + self.dx[direction] # 이동할 위치의 r
        ny = self.knight_pos[id][1] + self.dy[direction] # 이동할 위치의 c
        
        # 벽이 있다면 do_cancel을 참으로 바꾸고 return
        # 단, 이동하려는 위치에 벽이 있다면 이동을 취소하고 턴을 종료한다
        for i in range(nx, nx+h):
            for j in range(ny, ny+w):
                if self.board_map[i][j] == 2:
                    do_cancel = True
                    return

    def interaction(self, id, direction):
        """
        새로운 위치에 다른 기사가 있다면 이어서 연쇄반응 시작
        이미 check_interaction을 거쳤으므로 벽에 부딪히지 않음이 보장됨
        """
        global visited
        if visited[id] == True:
            return
        visited[id] = True

        to_be_visited = []

        h = self.knight_size[id][0]
        w = self.knight_size[id][1]
        nx = self.knight_pos[id][0] + self.dx[direction] # 이동할 위치의 r
        ny = self.knight_pos[id][1] + self.dy[direction] # 이동할 위치의 c

        # 다음 구역에 아무 기사도 없다면 연쇄반응 종료
        do_end = True
        for i in range(nx, nx+h):
            for j in range(ny, ny+w):
                if self.board_knight[i][j] <= 0 and self.board_knight[i][j] != id and visited[self.board_knight[i][j] == False]:
                    do_end = False
                    to_be_visited.append(self.board_knight[i][j])
        
        if do_end == True:
            # 기사의 위치 갱신
            self.knight_pos[id][0] = nx
            self.knight_pos[id][1] = ny

            # 보드에 새로운 위치 저장
            self.mark_board(id)

            # 데미지 계산
            self.reflect_damage(id)

            return
        
        # 연쇄반응을 종료하지 않는다면 재귀함수로 이어서
        self.knight_pos[id][0] = nx
        self.knight_pos[id][1] = ny
        self.mark_board(id)
        self.reflect_damage(id)
        
        for sub_id in to_be_visited:
            self.interaction(sub_id, direction)
    
    def refill_board(self, id):
        """
        기사가 이동을 할 때 board_knight에서 원래 위치를 지운다
        """
        x = self.knight_pos[id][0]
        y = self.knight_pos[id][1]
        h = self.knight_size[id][0]
        w = self.knight_size[id][1]
        
        for i in range(x, x+h):
            for j in range(y, y+w):
                self.board_knight[i][j] = -1

    def mark_board(self, id):
        """
        기사가 이동했을 때 새로운 위치를 저장한다
        """
        x = self.knight_pos[id][0]
        y = self.knight_pos[id][1]
        h = self.knight_size[id][0]
        w = self.knight_size[id][1]
        
        for i in range(x, x+h):
            for j in range(y, y+w):
                self.board_knight[i][j] = id
        
    def reflect_damage(self, id):
        """
        새로운 칸에서 데미지 계산하고
        체력이 0 이하로 떨어졌다면 보드에서 지우고 out에 표시
        """
        x = self.knight_pos[id][0]
        y = self.knight_pos[id][1]
        h = self.knight_size[id][0]
        w = self.knight_size[id][1]
        
        # 데미지 계산
        for i in range(x, x+h):
            for j in range(y, y+w):
                if self.board_map[i][j]==1:
                    self.hp[id] -= 1
                    if self.hp[id] == 0:
                        self.out[id] = True
                        self.refill_board(id)
                        return

def main():
    instance = problem()
    for _ in range(instance.q):
        # i번 기사에게 방향 d로 한 칸 이동하라는 명령
        i, d = map(int, input().split())
        i -= 1

        instance.move_knight(i, d)
    
    # 생존한 기사들이 받은 데미지의 총합
    total_damage = 0

    for id in range(instance.n):
        if instance.out[id] == True:
            continue
        total_damage += instance.hp_original[id] - instance.hp[id]
    print(total_damage)

if __name__=="__main__":
    main()