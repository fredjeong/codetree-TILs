from collections import deque

class Problem():
    def __init__(self):
        """
        공장 설립
        """
        self.q = int(input())
        arr = list(map(int, input().split()))
        self.n = arr[1]
        self.m = arr[2]

        self.belt = [deque() for _ in range(self.m)] # 벨트는 총 m개 존자
        self.out = [False for _ in range(self.m)] # 고장난 벨트 체크

        self.parcel_info = {}
        for i in range(self.n):
            idx = i//(self.n//self.m)
            id = arr[3+i]
            weight = arr[3 + self.n + i]
            self.parcel_info[id] = weight
            self.belt[idx].append(id)

    def load(self, w_max):
        """
        물건 하차
        0번부터 m-1번까지 순서대로 벨트를 보며 각 벨트의 맨 앞에 있는 선물 중 해당 선물의 무게가 w_max 이하라면 하차
        그렇지 않다면 해당 선물을 벨트 맨 뒤로 보냄
        """
        score = 0
        for idx in range(self.m):
            if self.out[idx]:
                continue
            id = self.belt[idx].popleft()
            if self.parcel_info[id] <= w_max:
                score += self.parcel_info[id]
            else:
                self.belt[idx].append(id)
        print(score)

    def kill(self, r_id):
        """
        물건 제거
        해당 고유 번호에 해당하는 상자가 놓여있는 벨트가 있다면 해당 벨트에서 상자를 제거한다
        """
        for idx in range(self.m):
            if self.out[idx]:
                continue
            if r_id in self.belt[idx]:
                self.belt[idx].remove(r_id)
                print(r_id)
                return
        print(-1)

    def check(self, f_id):
        """
        물건 확인
        해당 고유 번호에 해당하는 상자가 놓여있는 벨트가 있다면 해당 벨트의 번호를 출력
        없다면 -1을 출력

        """
        for idx in range(self.m):
            if self.out[idx]:
                continue
            if f_id in self.belt[idx]:
                print(idx+1)
                while self.belt[idx][0] != f_id:
                    self.belt[idx].appendleft(self.belt[idx].pop())
                return
        print(-1)

    def broken(self, b_num):
        """
        벨트 고장
        해당 벨트는 다시는 사용할 수 없게 된다
        b_num 벨트의 바로 오른쪽 벨트부터 순서대로 보며 아직 고장나지 않은 최초의 벨트 위로
        b_num 벨트에 놓여 있던 상자들을 아래에서부터 순서대로 하나씩 옮겨준다
        """
        b_num -= 1
        # 이미 망가져 있었다면 -1 출력
        if self.out[b_num]:
            print(-1)
            return
        self.out[b_num] = True
        idx = b_num
        while True:
            idx = (idx + 1)%self.m
            if not self.out[idx]:
                self.belt[idx].extend(self.belt[b_num])
                print(b_num + 1)
                break

def main():
    instance = Problem()

    for _ in range(instance.q-1):
        arr = list(map(int, input().split()))

        # 물건 하차
        if arr[0] == 200:
            w_max = arr[1]
            instance.load(w_max)

        # 물건 제거
        elif arr[0] == 300:
            r_id = arr[1]
            instance.kill(r_id)

        # 물건 확인
        elif arr[0] == 400:
            f_id = arr[1]
            instance.check(f_id)

        # 벨트 고장
        elif arr[0] == 500:
            b_num = arr[1]
            instance.broken(b_num)

if __name__ == "__main__":
    main()