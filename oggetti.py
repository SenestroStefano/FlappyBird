import random

class Tubo():
    def __init__(self, img, posT, distanza, posF, width, height, VEL, SCREEN_dim, MULT):
        
        self.flappy = img
        
        self.distanza = distanza * MULT
        self.x = SCREEN_dim[0] * posT
        self.y = random.randint(-200, -80) * MULT

        self.flappy_x = posF[0]
        self.flappy_y = posF[1]

        self.width = width
        self.height = height

        self.vel = VEL

        self.mult = MULT
        self.screen_dim = (SCREEN_dim[0], SCREEN_dim[1])

    def setPlayerPosition(self,x ,y):
        self.flappy_x = x
        self.flappy_y = y

    def getNewHeight(self):
        self.y = random.randint(-200, -80) * self.mult

    def muovi(self):
        self.x -= self.vel


    def checkCollision(self):

        flappy_height = self.flappy.get_height()
        flappy_width = self.flappy.get_width()

        dist = self.distanza

        # Se la posX di flappy <= punto destro della base del tubo e  la posX di flappy => punto sinistro della base del tubo e non (posY di flappy <= posY bassa della distanza e posY di flappy <= posY alta della distanza)
        if self.flappy_x <= (self.width+self.x) and self.flappy_x >= self.x-flappy_width and not (self.flappy_y <= (self.height+self.y+dist-flappy_height) and self.flappy_y >= (self.y+self.height)):
            return True
        else:
            return False

    def update(self):
        self.muovi()

        if self.x <= -self.screen_dim[0]:
            self.getNewHeight()
            self.x = self.screen_dim[0]


class Base():
    def __init__(self, posB, VEL, MULT):

        self.vel = VEL

        self.x = posB[0]
        self.y = posB[1]

        self.mult = MULT

    def muovi(self):
        self.x -= self.vel

    def update(self):
        self.muovi()
        
        #CONTROLLI DELLA POSIZIONE DEGLI OGGETTI
        if self.x < -48 * self.mult:
            self.x = 0