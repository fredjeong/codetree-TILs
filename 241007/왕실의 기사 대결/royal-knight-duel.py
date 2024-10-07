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
        
        # 체스판 바깥도 벽으로 취급하므로 체스판의 전체 길이를 (L+2)*(L+2)로 취급
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
        """
        do_interaction = True: 명령을 받은 기사가 이동하는 길에 다른 기사가 최소 하나 존재한다
        do_interaction = False: 명령을 받은 기사가 이동하는 길에 다른 기사가 아무도 없다
        """
        # 동시에 여러 기사가 반응할 수 있고, 그 중 하나라도 연쇄반응 과정에서 벽에 부딪히는 기사가 있다면 이동이 취소되므로 우선 따로 명단을 만들어 관리
        for i in range(nx, nx+h):
            for j in range(ny, ny+w):
                if self.board_knight[i][j] >= 0 and self.board_knight[i][j] != id:
                    do_interaction = True
                    interaction_knights.add(self.board_knight[i][j]) # 일차적으로 영향을 받는 모든 기사들
        
        # 연쇄반응이 없다면 그대로 턴을 종료한다
        if do_interaction == False:
            """
            연쇄반응이 없다면 명령을 받은 기사의 기존 위치를 board_knight에서 지우고
            기사의 위치를 nx, ny로 갱신한 뒤
            board_knight에 새 위치를 표시해준다
            """
            # 보드에 기존 위치 지우기
            self.refill_board(id)

            # 기사의 위치 갱신
            self.knight_pos[id][0] = nx
            self.knight_pos[id][1] = ny

            # 보드에 새로운 위치 저장
            self.mark_board(id)

            return
            
        # 연쇄반응을 시작하는 경우
        """
        연쇄반응을 시작하는 경우 이동하여 한 명이라도 자신의 영역이 벽에 부딪히는 기사가 있다면 명령을 취소한다
        한 명도 벽에 부딪히지 않는다면 연쇄반응을 시작한다
        """
        global do_cancel, check
        check = [False for _ in range(self.n)]
        do_cancel = False

        for sub_id in interaction_knights:
            self.check_interaction(sub_id, direction)
        
        # 연쇄반응이 일어날 때 벽에 부딪히는 기사가 생긴다면 명령을 받은 기사도 이동하지 않고 그대로 턴을 종료
        if do_cancel == True:
            return
        
        # 연쇄반응이 일어날 수 있다면 모든 기사를 연쇄반응에 따라 이동시킨다
        global visited
        visited = [False for _ in range(self.n)]
        
        # 보드에서 명령을 받은 기사의 기존 위치 지우기
        self.refill_board(id)

        # interaction을 통해서 위치 갱신 및 데미지 반영
        global mark_or_refill_arr
        mark_or_refill_arr = set()
        
        for sub_id in interaction_knights:
            self.interaction(sub_id, direction)

        for elem in mark_or_refill_arr:
            self.reflect_damage(elem)
            if self.out[elem] == True:
                self.refill_board(elem)
            else:
                self.mark_board(elem)

        # 기사의 위치 갱신
        self.knight_pos[id][0] = nx
        self.knight_pos[id][1] = ny
        
        # 보드에 새로운 위치 저장
        self.mark_board(id)

    def check_interaction(self, id, direction):
        """
        명령을 받은 기사에 의해 1차적으로 영향받은 기사들에 대해 재귀함수를 시행한다
        재귀함수 시행 도중 이동하는 칸이 벽이라면 do_cancel=True로 바꾸어준다 (명령 취소)
        """
        global do_cancel, check
        if check[id]==True:
            return
        check[id]=True
        temp_set = set()

        h = self.knight_size[id][0]
        w = self.knight_size[id][1]
        nx = self.knight_pos[id][0] + self.dx[direction] # 이동할 위치의 r
        ny = self.knight_pos[id][1] + self.dy[direction] # 이동할 위치의 c
        
        for i in range(nx, nx+h):
            for j in range(ny, ny+w):
                if self.board_map[i][j] == 2:
                    do_cancel = True
                    return
        
        # 새로운 영역에 자신을 제외한 다른 기사가 존재하지 않는다면 리턴
        for i in range(nx, nx+h):
            for j in range(ny, ny+w):
                if self.board_knight[i][j] >= 0 and self.board_knight[i][j] != id:
                    sub_id = self.board_knight[i][j]
                    temp_set.add(sub_id)
        

        for elem in temp_set:
            if check[elem]==True:
                continue
            self.check_interaction(elem, direction)

    def interaction(self, id, direction):
        """
        새로운 위치에 다른 기사가 있다면 이어서 연쇄반응 시작
        이미 check_interaction을 거쳤으므로 벽에 부딪히지 않음이 보장됨
        """
        global mark_or_refill_arr
        global visited

        if visited[id] == True:
            return
        visited[id] = True

        to_be_visited = set()

        h = self.knight_size[id][0]
        w = self.knight_size[id][1]
        nx = self.knight_pos[id][0] + self.dx[direction] # 이동할 위치의 r
        ny = self.knight_pos[id][1] + self.dy[direction] # 이동할 위치의 c

        self.refill_board(id)
        self.knight_pos[id][0] = nx
        self.knight_pos[id][1] = ny

        mark_or_refill_arr.add(id)

        # 다음 구역에 아무 기사도 없다면 연쇄반응 종료
        for i in range(nx, nx+h):
            for j in range(ny, ny+w):
                if self.board_knight[i][j] >= 0 and self.board_knight[i][j] != id:
                    sub_id = self.board_knight[i][j]

                    to_be_visited.add(sub_id)


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
                        return


def main():
    instance = problem()
    for t in range(instance.q):
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