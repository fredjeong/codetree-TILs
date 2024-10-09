import sys
from collections import deque

input = sys.stdin.readline

class problem():
    def __init__(self):
        """
        n: 격자의 크기
        m: 사람의 수
        board: 빈 공간과 베이스캠프의 정보를 담은 격자
        locked: 지나갈 수 없는 칸 표시
        destination: i번째 사람들이 가고자 하는 편의점 위치의 행과 열의 정보
        count: 편의점에 도착한 사람의 수

        동일한 칸에 여러 사람이 들어갈 수 있다
        """
        self.n, self.m = map(int, input().split())
        self.board = [list(map(int, input().split())) for _ in range(self.n)]
        self.locked = [[False for _ in range(self.n)] for _ in range(self.n)]
        self.destination = []
        for _ in range(self.m):
            x, y = list(map(int, input().split()))
            self.destination.append([x - 1, y - 1])

        self.count = 0 # count = m일 때 프로글매을 종료하고 count를 리턴한다
        self.player_pos = []
        self.lock_list = []
        self.out = [False for _ in range(self.m)]
    
    def get_distance(self, pos_1, pos_2):
        return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])
    
    def move(self, t, i):
        """
        t: 현재 시간
        i: 움직이는 사람
        """
        """
        본인이 가고자 하는 편의점 방향ㅇ르 향해서 1칸 움직인다. 최단거리로 움직이며, 최단 거리로 움직이는 방법이 여러 가지라면 상/좌/우/하 우선순위로 움직인다.
        만약 편의점에 도착한다면 해당 편의점에서 멈추게 되고, 이 다음 라운드부터 다른 사람들은 해당 편의점이 있는 칸을 지나갈 수 없게 된다.
        i==t인 사람은 자신이 가고 싶은 편의점과 가장 가까이 있는 베이스 캠프에 들어간다
        가장 가까운 베이스 캠프가 여러 가지인 경우 그 중 행이 작은 베이스캠프, 행이 같다면 열이 작은 베이스 캠프로 들어가며, 이 때 시간은 소요되지 않는다
        이 때부터 다른 사람들은 해당 베이스 캠프가 있는 칸을 지나갈 수 없게 된다
        """
        
        if i < t:
            # 이미 편의점에 도착한 사람은 더 이상 이동하지 않는다
            if self.out[i] == True:
                return
            # 최단거리로 본인이 가고 싶은 편의점 방향을 향해서 1칸 움직인다
            # 이것도 bfs를 통해서 이동 가능한 칸으로만 이동하여 도달
            q = deque()
            q.append([self.player_pos[i]])

            visited = [[False for _ in range(self.n)] for _ in range(self.n)]
            
            # 가고 싶은 편의점의 좌표
            cvs_pos = self.destination[i]

            dx = [-1, 0, 0, 1]
            dy = [0, -1, 1, 0]

            while q:
                history = q.popleft()
                
                x, y = history[-1]
                if visited[x][y] == True:
                    continue
                visited[x][y] = True


                if [x, y] == cvs_pos:
                    # 최단거리 경로를 찾았으므로 while문에서 벗어난다
                    break

                for idx in range(len(dx)):
                    nx = x + dx[idx]
                    ny = y + dy[idx]

                    if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                        continue
                    
                    if visited[nx][ny] == True:
                        continue
                    visited[nx][ny]

                    if self.locked[nx][ny] == True:
                        continue

                    q.append(history + [[nx, ny]])
            
            # while문에서 벗어나 저장된 history의 두 번째 칸으로 이동한다
            self.player_pos[i] = history[1]

            # 만약 한 칸 이동한 지점이 편의점의 위치라면 아무도 편의점에서 이동할 수 없도록 한다
            if history[1] == cvs_pos:
                self.out[i] = True
                self.count += 1
                # lock_list에 해당 편의점의 좌표 추가
                self.lock_list.append(cvs_pos)

        # 처음 들어오는 사람은 자신이 가고 싶은 편의점과 가장 가까이 있는 베이스 캠프로 이동한다
        elif i==t:
            # 가고 싶어하는 편의점의 위치
            cvs_pos = self.destination[i]

            # bfs를 이용해서 최단거리 베이스캠프 탐색
            q = deque()
            q.append(cvs_pos)
            
            visited = [[False for _ in range(self.n)] for _ in range(self.n)]
            visited[cvs_pos[0]][cvs_pos[1]] = True
            
            dx = [-1, 0, 0, 1]
            dy = [0, -1, 1, 0]
            
            child = []
            min_pos = None
            while q:
                x, y = q.popleft()
                
                # 베이스캠프를 찾았다면 
                if self.board[x][y] == 1:
                    if min_pos == None:
                        min_pos = [x, y]
                        break

                for idx in range(len(dx)):
                    nx = x + dx[idx]
                    ny = y + dy[idx]

                    # 격자 밖의 위치는 고려하지 않는다
                    if nx < 0 or nx >= self.n or ny < 0 or ny >= self.n:
                        continue
                    
                    # bfs 탐색 과정에서 이미 방문한 곳은 고려하지 않는다
                    if visited[nx][ny] == True:
                        continue
                    visited[nx][ny] = True

                    # 이미 점령된 베이스캠프나 편의점은 고려하지 않는다
                    if self.locked[nx][ny] == True:
                        continue
                    if [nx, ny] in self.lock_list:
                        continue

                    child.append([nx, ny])
                
                if not q:
                    if min_pos != None:
                        break
                    else:
                        q.extend(child)
                        child = []

            # min_pos 위치의 베이스캠프는 이제 아무도 이동할 수 없다
            self.locked[min_pos[0]][min_pos[1]] = True

            # i=t번 사람의 위치가 정해졌으므로 이를 플레이어의 위치판에 추가해준다
            self.player_pos.append(min_pos)

def main():
    instance = problem()
    
    t = 0
    while True:       
        for i in range(instance.m):
            # i분에는 i번 사람까지 움직일 수 있다
            if i > t:
                break
            instance.move(t, i)
        
        # lock_list의 모든 위치들을 이동 불가로 선언해준다
        for elem in instance.lock_list:
            instance.locked[elem[0]][elem[1]] = True

        # lock list를 초기화해준다
        instance.lock_list = []
        

        # 모든 사람이 편의점에 도착했다면 
        if instance.count == instance.m:
            break
    
        t += 1

    print(t+1)

if __name__ == "__main__":
    main()