import random
import os
import time
import msvcrt


class Snake:
    def __init__(self, n):
        self.length = n
        self.head = []
        self.tail = []


class SnakeGame:
    direction = {"LEFT": -2, "DOWN": -1, "NON_DIR": 0, "UP": 1, "RIGHT": 2}
    sprite = {"EMPTY": 0, "BODY": 1, "HEAD": 2, "FOOD": 3}
    element = {"SPRITE": 0, "DIRECTION": 1}

    def __init__(self, w, h, length, delay):
        self.W = w
        self.H = h
        self.initLen = length
        self.snake = Snake(length)
        self.delay = delay
        self.board = [[[0] * 2 for x in range(self.W)] for y in range(self.H)]
        # self.board[a][b][c]

        self.snake.head = [self.H // 2, self.snake.length - 1]
        self.snake.tail = [self.H // 2, 0]

        for i in range(0, self.snake.length):
            self.board[self.H // 2][i][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]
            self.board[self.H // 2][i][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]

        self.board[self.H // 2][self.snake.length - 1][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
        self.board[self.H // 2][self.snake.length - 1][SnakeGame.element["DIRECTION"]] = SnakeGame.direction["RIGHT"]

        x = random.randint(0, self.W - 1)
        y = random.randint(0, self.H - 1)
        while self.board[y][x][SnakeGame.element["SPRITE"]] != SnakeGame.sprite["EMPTY"]:
            x = random.randint(0, self.W - 1)
            y = random.randint(0, self.H - 1)

        self.board[y][x][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"]

    def DrawScene(self):
        os.system('cls||clear')
        for x in range(0, self.W + 2):
            print("=", end="")
        print("")
        for y in range(0, self.H):
            print("|", end="")
            for x in range(0, self.W):
                if self.board[y][x][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["BODY"]:
                    print("+", end="")
                elif self.board[y][x][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["HEAD"]:
                    print("@", end="")
                elif self.board[y][x][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["FOOD"]:
                    print("*", end="")
                else:
                    print(" ", end="")
            print("|")

        for x in range(0, self.W + 2):
            print("=", end="")
        print("")

    @staticmethod
    def GetDirection():
        rtn = SnakeGame.direction["NON_DIR"]
        msvcrt.getch()
        ch = msvcrt.getch().decode()
        if ch == chr(72):
            print("UP")
            rtn = SnakeGame.direction["UP"]
        elif ch == chr(75):
            print("LEFT")
            rtn = SnakeGame.direction["LEFT"]
        elif ch == chr(77):
            print("RIGHT")
            rtn = SnakeGame.direction["RIGHT"]
        elif ch == chr(80):
            print("DOWN")
            rtn = SnakeGame.direction["DOWN"]
        else:
            print("Nothing")

        return rtn

    def GameLoop(self):
        self.DrawScene()

        current = SnakeGame.direction["RIGHT"]
        ret = SnakeGame.direction["RIGHT"]
        tail_dir = [SnakeGame.direction["RIGHT"], SnakeGame.direction["RIGHT"], SnakeGame.direction["RIGHT"]]

        while True:
            start = time.time()
            while (time.time() - start) <= self.delay / 1000:
                if msvcrt.kbhit():
                    print("in")
                    current = SnakeGame.GetDirection()


            #LAB01
            #좌우 방향 설정
            if abs(current) != abs(ret):
                ret = current
            elif abs(current) == abs(ret):
                pass

            #헤드의 정보를 갱신한다
            self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["BODY"]

            if ret == 2:
                self.snake.head[1] += 1

            elif ret == 1: #UP
                self.snake.head[0] -= 1

            elif ret == -1: #Down
                self.snake.head[0] += 1
            
            elif ret == -2: #LEFT
                self.snake.head[1] -= 1

            #머리랑 몸이랑 닿으면 사망
            if self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["BODY"]:
                break
            

            #먹이 랜덤 생성 및 점수 관리(꼬리길이)
            if self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] == SnakeGame.sprite["FOOD"]:
                x = random.randint(0, self.W - 1)
                y = random.randint(0, self.H - 1)
                while self.board[y][x][SnakeGame.element["SPRITE"]] != SnakeGame.sprite["EMPTY"]:
                    x = random.randint(0, self.W - 1)
                    y = random.randint(0, self.H - 1)

                self.board[y][x][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["FOOD"]
                self.snake.length += 1
                

            else: #먹이를 안 먹었을 때, 기본 이동시 꼬리 옮기기
                self.board[self.snake.tail[0]][self.snake.tail[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["EMPTY"]
                
                #꼬리 정하기
                if tail_dir[0] == SnakeGame.direction["RIGHT"]:
                    self.snake.tail[1] += 1
                elif tail_dir[0] == SnakeGame.direction["LEFT"]:
                    self.snake.tail[1] -= 1
                elif tail_dir[0] == SnakeGame.direction["DOWN"]:
                    self.snake.tail[0] += 1
                elif tail_dir[0] == SnakeGame.direction["UP"]:
                    self.snake.tail[0] -= 1
                tail_dir.pop(0)
            tail_dir.append(ret)


            self.board[self.snake.head[0]][self.snake.head[1]][SnakeGame.element["SPRITE"]] = SnakeGame.sprite["HEAD"]
           
            #벽에 도달하면 사망
            if self.snake.head[0] < 0 or self.snake.head[0] > 23:
                break
            elif self.snake.head[1] < 0 or self.snake.head[1] > 59:
                break
            

            self.DrawScene()
            print("Score: {}".format(self.snake.length - self.initLen))



if __name__ == '__main__':
    game = SnakeGame(60, 24, 4, 300)
    game.GameLoop()