import cv2
import random
import numpy as np

windowName = 'Drawing'
game_size = [8, 8]
N = 50

class game:
    def __init__(self, game_size, img):
        self.game_size = game_size
        self.mine_list = []
        self.img = img

    def plant_mine(self, n, area_size): # Returns a list of coordinates which includes the positions of the mines

        def give_coord(AS):
            coordx = random.randrange(AS[0])
            coordy = random.randrange(AS[1])
            return [coordx, coordy]

        while len(self.mine_list) < n:
            coord = give_coord(area_size)
            if coord not in self.mine_list:
                self.mine_list.append(coord)
            else:
                continue

    def draw_game(self):
        for i in range(self.game_size[0] + 1):
            cv2.line(self.img, (N * i, 0), (N * i, N * self.game_size[1]),
                                                             (255,0,0),2)

        for i in range(self.game_size[1] + 1):
            cv2.line(self.img, (0, N * i), (N * self.game_size[0], N * i),
                                                             (255,0,0),2)

    def define_square(self, coord):
        coordx = (coord[0]//N) * N
        coordy = (coord[1]//N) * N
        self.img[coordy + 2:coordy + N - 1, coordx + 2:coordx + N - 1] = 255

def event_func(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x,y), 1, (255, 0, 0), -1)
        the_game.define_square([x, y])
        #Do smth else in here

img = np.zeros((game_size[0]*N,game_size[1]*N, 3), np.uint8)

cv2.namedWindow(windowName)
cv2.setMouseCallback(windowName, event_func)

the_game = game(game_size, img)
the_game.draw_game()

while (True):
    cv2.imshow(windowName, the_game.img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
