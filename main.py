import cv2
import random
import numpy as np

windowName = 'Drawing'
game_size = [2, 2]
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
        for i in range(1, self.game_size[0]):
            cv2.line(self.img, (N * i, 0), (N * i, N * self.game_size[1]),
                                                             (255,0,0),2)

        for i in range(1, self.game_size[1]):
            cv2.line(self.img, (0, N * i), (N * self.game_size[0], N * i),
                                                             (255,0,0),2)

    def define_square(self, coord):
        pass # This function will find the simple coordinate from complex one

    def def_square_coords(self, coord):
        pass # This function will find the covering area of the square according to the point

def event_func(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x,y), 1, (255, 0, 0), -1)
        #Do smth else in here

img = np.zeros((game_size[0]*N,game_size[1]*N, 3), np.uint8)

cv2.namedWindow(windowName)
cv2.setMouseCallback(windowName, event_func)

the_game = game(game_size, img)
the_game.draw_game()

the_game.img[40:60, 40:60] = 0

while (True):
    cv2.imshow(windowName, img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
