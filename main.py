import cv2
import random
import numpy as np

windowName = 'Drawing'
game_size = [12, 12]
N = 50
arround = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]

class game:
    def __init__(self, game_size, img):
        self.game_size = game_size
        self.mine_list = []
        self.img = img
        self.game_map = np.zeros((self.game_size[0], self.game_size[1])).tolist()

    def plant_mines(self, n): # Returns a list of coordinates which includes the positions of the mines

        def give_coord(S):

            coordx = random.randrange(S[0])
            coordy = random.randrange(S[1])
            return [coordx, coordy]

        while len(self.mine_list) < n:
            coord = give_coord(self.game_size)
            if coord not in self.mine_list:
                self.mine_list.append(coord)
            else:
                continue

        for i in self.mine_list:
            self.game_map[i[0]][i[1]] = "M"
            for j in arround:
                if i[0] + j[0] == -1 or i[1] + j[1] == -1 or i[0] + j[0] == self.game_size[0] or i[1] + j[1] == self.game_size[1]:
                    continue
                try:
                    self.game_map[i[0] + j[0]][i[1] + j[1]] += 1
                except:
                    pass
    def draw_game(self):
        for i in range(self.game_size[0] + 1):
            cv2.line(self.img, (N * i, 0), (N * i, N * self.game_size[1]),
                                                             (255,0,0),2)

        for i in range(self.game_size[1] + 1):
            cv2.line(self.img, (0, N * i), (N * self.game_size[0], N * i),
                                                             (255,0,0),2)

    def define_square(self, coord):
        coordx = (coord[0]//N)
        coordy = (coord[1]//N)

        return [coordx, coordy]

    def markit(self, pos, type, optional=0, optional2 = 0):
        if type == "img":
            pass
        elif type == "color":
            self.img[pos[1]*N + 2:pos[1]*N + N - 1, pos[0]*N + 2:pos[0]*N + N - 1] = optional
        elif type == "number":
            cv2.putText(self.img, str(optional2), (pos[0]*N + int(N * 0.3), pos[1]*N + int(N*0.7)), cv2.FONT_HERSHEY_SIMPLEX, 1,
            optional, 2)
        else:
            print("Incorrect type of data argument")

    def show_mines(self):
        for i in self.mine_list:
            self.img[i[1]*N + 2:i[1]*N+N - 1, i[0]*N + 2:i[0]*N+N - 1] = (0, 0, 255)

    def open_area(self, coord, dl):
        empties = []

        self.markit(coord, "number", (255, 255, 255), int(self.game_map[coord[0]][coord[1]]))
        for i in arround:
            if coord[0] + i[0] == -1 or coord[0] + i[0] == -1 or coord[0] + i[0] == self.game_size[0] or coord[1] + i[1] == self.game_size[1]:
                continue
            if self.game_map[coord[0] + i[0]][coord[1] + i[1]] == "M":
                continue

            if self.game_map[coord[0] + i[0]][coord[1] + i[1]] == 0 and [coord[0] + i[0], coord[1] + i[1]] not in dl:
                empties.append([coord[0] + i[0], coord[1] + i[1]])

            self.markit([coord[0] + i[0], coord[1] + i[1]], "number", (255, 255, 255), int(self.game_map[coord[0] + i[0]][coord[1] + i[1]]))
        return empties

    def empty_open(self, coordlst, dl = []):
        empty_coords = []
        for j in coordlst:
            if j not in dl:
                dl.append(j)
        for i in coordlst:
            empty_coords.extend(self.open_area(i, dl))
        if len(empty_coords) > 0:
            self.empty_open(empty_coords, dl)

def event_func(event, x, y, flags, param):
    game_square = the_game.define_square([x, y])
    if event == cv2.EVENT_LBUTTONDOWN:
        if the_game.game_map[game_square[0]][game_square[1]] != "M":
            the_game.markit(game_square, "number", (255, 0, 160), int(the_game.game_map[game_square[0]][game_square[1]]))

        else:
            the_game.img = np.zeros((game_size[0]*N,game_size[1]*N, 3), np.uint8)
            the_game.draw_game()
            the_game.show_mines()

        if the_game.game_map[game_square[0]][game_square[1]] == 0:
            the_game.empty_open([game_square])
    if event == cv2.EVENT_RBUTTONDOWN:
        the_game.markit(game_square, "color", (125, 45, 255))

img = np.zeros((game_size[0]*N,game_size[1]*N, 3), np.uint8)

cv2.namedWindow(windowName)
cv2.setMouseCallback(windowName, event_func)

the_game = game(game_size, img)
the_game.plant_mines(12)
the_game.draw_game()
the_game.show_mines()

while (True):
    cv2.imshow(windowName, the_game.img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
