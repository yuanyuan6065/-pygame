import pygame
import sys
from os import path
from map import list
from pygame import mixer
import math

pygame.init()
screen = pygame.display.set_mode((532, 532), 0, 0)
pygame.display.set_caption('Box Game')
boxList = []
ballList = []
wallList = []
bg1List = []
bg2List = []
peopleDir = {'x': 0, 'y': 0}#人所在的位置
clock = pygame.time.Clock()


def initData(level):
    boxList.clear()
    ballList.clear()
    wallList.clear()
    bg1List.clear()
    bg2List.clear()
    data = list[level]
    index = -1
    for i in range(0, 16):
        for j in range(0, 16):
            index += 1
            item = data[index]
            if item == 1:
                wallList.append(1)
            else:
                wallList.append(0)

            if item == 2:
                ballList.append(2)
            else:
                ballList.append(0)

            if item == 3:
                boxList.append(3)
            else:
                boxList.append(0)

            if item == 5:
                bg1List.append(5)
            else:
                bg1List.append(0)

            if item == 4:
                peopleDir['x'] = j
                peopleDir['y'] = i

            if item !=1 and item!=5:
                bg2List.append(6)
            else:
                bg2List.append(0)



class GameApp:
    level = 0  # 第一关
    map = None
    wall = None
    ball = None
    box = None
    people = None
    bg1 = None
    bg2 = None

    direction = 'down'
    levelFont = None#字体
    ballNum = 0

    def __init__(self):
        self.loadFile()
        self.menuFont = pygame.font.SysFont("Arial", 20)
        self.smallFont = pygame.font.SysFont(None, 15)

        self.level1Button = pygame.Rect(450, 40, 50, 15)
        self.level2Button = pygame.Rect(450, 60, 50, 15)
        self.level3Button = pygame.Rect(450, 80, 50, 15)
        self.level4Button = pygame.Rect(450, 100, 50, 15)
        self.level5Button = pygame.Rect(450, 120, 50, 15)
        self.restartButton = pygame.Rect(450, 140, 50, 15)
        icon = pygame.image.load(self.resolve('bmp/Bmp3.gif'))
        pygame.display.set_icon(icon)
        mixer.music.load(self.resolve('bmp/background.wav'))
        self.levelFont = pygame.font.SysFont(None, 20)
        self.font = pygame.font.SysFont("Arial", 72)  # 设置较大的字体大小
        mixer.music.play(-1)
        self.runGame()

    def loadFile(self):
        self.bg1 = pygame.image.load(self.resolve('bmp/Bmp0.gif'))
        self.bg2 = pygame.image.load(self.resolve('bmp/Bmp2.gif'))
        self.wall = pygame.image.load(self.resolve('bmp/Bmp1.gif'))
        self.ball = pygame.image.load(self.resolve('bmp/Bmp5.gif'))
        self.box = pygame.image.load(self.resolve('bmp/Bmp3.gif'))
        self.people = pygame.image.load(self.resolve('bmp/Bmp6.gif'))
    def resolve(self, filename):
        dirName = path.dirname(__file__)
        return dirName + '/' + filename

    def renderLevel(self):
        levelshow = pygame.Rect(100,5,300,20)
        levelText = self.levelFont.render('BoxMan Author: zyf          Level:  ' + str(self.level + 1) , True, (0, 0, 0))
        pygame.draw.rect(screen,(255,255,255),levelshow)
        screen.blit(levelText, (150, 10))

    def renderData(self):
        index = -1
        for i in range(0, 16):
            for j in range(0, 16):
                index += 1
                if bg1List[index]==5:
                    screen.blit(self.bg1,(j * 33, i * 33))
                if bg2List[index]==6:
                    screen.blit(self.bg2,(j * 33, i * 33))
                if wallList[index] == 1:
                    screen.blit(self.wall, (j * 33 , i * 33 ))
                if ballList[index] == 2:
                    self.ballNum += 1
                    screen.blit(self.ball, (j * 33 , i * 33 ))
                if boxList[index] == 3:
                    screen.blit(self.box, (j * 33 , i * 33 ))
                if peopleDir['x'] == j and peopleDir['y'] == i:
                    screen.blit(self.people, (j * 33, i * 33))

    def hasGo(self, preItem, nextItem, preIndex, nextIndex, x, y,):
        if preItem == 0 :
            peopleDir['x'] = x
            peopleDir['y'] = y
            # bg2List[curIndex] = 6#人往前走
            # bg2List[preIndex] = 3
            return True
        if preItem == 2:
            peopleDir['x'] = x
            peopleDir['y'] = y
            return True
        if preItem == 3:  # 下一个是箱子
            if nextItem == 0 or nextItem == 2:
                boxList[preIndex] = 0
                boxList[nextIndex] = 3
                peopleDir['x'] = x
                peopleDir['y'] = y
                self.checkGameover(nextIndex)

                return True
        return False

    def checkGameover(self, nextIndex):
        y = math.floor(nextIndex / 16)
        x = nextIndex % 16
        preItem = 0
        if ballList[nextIndex] != 2:
            checkList = [
                wallList[(y - 1) * 16 + x],
                wallList[y * 16 + x - 1],
                wallList[(y + 1) * 16 + x],
                wallList[y * 16 + x + 1],
                wallList[(y - 1) * 16 + x]
            ]
            for item in checkList:
                if item == 0:
                    preItem = 0
                elif item == 1 and preItem == 0:
                    preItem = 1
                elif item == 1 and preItem == 1:  # 如果相邻是两面墙及失败了
                    gameOverText = self.font.render("GAME OVER", True, (255, 0, 0))
                    restartButton = pygame.Rect(100, 300, 150, 50)
                    quitButton = pygame.Rect(300, 300, 150, 50)

                    while True:
                        # screen.fill((0, 0, 0))
                        screen.blit(gameOverText, (110, 200))
                        pygame.draw.rect(screen, (0, 255, 0), restartButton)
                        pygame.draw.rect(screen, (255, 0, 0), quitButton)

                        restartText = self.levelFont.render("RESTART", True, (255, 255, 255))
                        quitText = self.levelFont.render("EXIT", True, (255, 255, 255))

                        screen.blit(restartText, (150, 320))
                        screen.blit(quitText, (350, 320))

                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if restartButton.collidepoint(event.pos):
                                    # self.level = 0
                                    initData(self.level)
                                    return
                                if quitButton.collidepoint(event.pos):
                                    pygame.quit()
                                    sys.exit()


    def checkWin(self):
        index = -1
        winNum = 0
        self.ballNum = 0
        for i in range(0, 16):
            for j in range(0, 16):
                index += 1
                if ballList[index] == 2:
                    self.ballNum += 1
                    if (boxList[index] == 3):
                        winNum += 1
        if self.ballNum == winNum:
            self.level += 1
            if self.level==5:
                gameOverText = self.font.render("YOU WIN!", True, (255, 0, 0))
                restartButton = pygame.Rect(100, 300, 150, 50)
                quitButton = pygame.Rect(300, 300, 150, 50)

                while True:
                    # screen.fill((0, 0, 0))
                    screen.blit(gameOverText, (110, 200))
                    pygame.draw.rect(screen, (0, 255, 0), restartButton)
                    pygame.draw.rect(screen, (255, 0, 0), quitButton)

                    restartText = self.levelFont.render("RESTART", True, (255, 255, 255))
                    quitText = self.levelFont.render("EXIT", True, (255, 255, 255))

                    screen.blit(restartText, (150, 320))
                    screen.blit(quitText, (350, 320))

                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if restartButton.collidepoint(event.pos):
                                self.level = 0
                                initData(self.level)
                                return
                            if quitButton.collidepoint(event.pos):
                                pygame.quit()
                                sys.exit()
            else:
                initData(self.level)

    def pushData(self, type):
        x = peopleDir['x']
        y = peopleDir['y']
        curIndex = y * 16 + x
        if type == 'left':
            preIndex = y * 16 + x - 1
            nextIndex = y * 16 + x - 2
            preItem = max([boxList[preIndex], ballList[preIndex], wallList[preIndex]],)
            nextItem = max([boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]],)
            if self.hasGo(preItem, nextItem, preIndex, nextIndex, x - 1, y):
                self.direction = 'left'
        if type == 'right':
            preIndex = y * 16 + x + 1
            nextIndex = y * 16 + x + 2
            preItem = max([boxList[preIndex], ballList[preIndex], wallList[preIndex]])
            nextItem = max([boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
            if self.hasGo(preItem, nextItem, preIndex, nextIndex, x + 1, y):
                self.direction = 'right'
        if type == 'up':
            preIndex = (y - 1) * 16 + x
            nextIndex = (y - 2) * 16 + x
            preItem = max([boxList[preIndex], ballList[preIndex], wallList[preIndex]])
            nextItem = max([boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
            if self.hasGo(preItem, nextItem, preIndex, nextIndex, x, y - 1):
                self.direction = 'up'
        if type == 'down':
            preIndex = (y + 1) * 16 + x
            nextIndex = (y + 2) * 16 + x
            preItem = max([boxList[preIndex], ballList[preIndex], wallList[preIndex]])
            nextItem = max([boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
            if self.hasGo(preItem, nextItem, preIndex, nextIndex, x, y + 1):
                self.direction = 'down'


    def runMenu(self):
        titleText = self.menuFont.render("Select Level", True, (0, 0, 0))
        screen.blit(titleText, (430, 5))

        pygame.draw.rect(screen, (255, 255, 255), self.level1Button)
        pygame.draw.rect(screen, (255, 255, 255), self.level2Button)
        pygame.draw.rect(screen, (255, 255, 255), self.level3Button)
        pygame.draw.rect(screen, (255, 255, 255), self.level4Button)
        pygame.draw.rect(screen, (255, 255, 255), self.level5Button)
        pygame.draw.rect(screen, (255, 255, 255), self.restartButton)

        level1Text = self.smallFont.render("Level 1", True, (0, 0, 0))
        level2Text = self.smallFont.render("Level 2", True, (0, 0, 0))
        level3Text = self.smallFont.render("Level 3", True, (0, 0, 0))
        level4Text = self.smallFont.render("Level 4", True, (0, 0, 0))
        level5Text = self.smallFont.render("Level 5", True, (0, 0, 0))
        restartText = self.smallFont.render("Restart", True, (0, 0, 0))

        screen.blit(level1Text, (460, 40))
        screen.blit(level2Text, (460, 60))
        screen.blit(level3Text, (460, 80))
        screen.blit(level4Text, (460, 100))
        screen.blit(level5Text, (460, 120))
        screen.blit(restartText, (460, 140))


    def runGame(self):
        while True:
            clock.tick(300)
            screen.fill((0, 0, 0))

            self.renderData()
            self.renderLevel()
            self.runMenu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                    pygame.quit()  # 退出pygame
                    sys.exit()  # 退出系统
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.pushData('left')
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.pushData('right')
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.pushData('down')
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.pushData('up')
                    if event.key == pygame.K_r:  # 重置当前关卡
                        initData(self.level)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level1Button.collidepoint(event.pos):
                        self.level = 0
                    elif self.level2Button.collidepoint(event.pos):
                        self.level = 1
                    elif self.level3Button.collidepoint(event.pos):
                        self.level = 2
                    elif self.level4Button.collidepoint(event.pos):
                        self.level = 3
                    elif self.level5Button.collidepoint(event.pos):
                        self.level = 4
                    elif self.restartButton.collidepoint(event.pos):
                        pass  # Handle restart functionality here if needed

                    initData(self.level)
                    self.runGame()  # Start the selected level
            self.checkWin()
            pygame.display.update()


if __name__ == '__main__':
    initData(0)
    GameApp()
