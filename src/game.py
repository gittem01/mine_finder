import numpy as np
import cv2
import random


around = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
N = 60
game_size = [15, 15] # This two must be same or BAD things happen...
num_color = {1:(0, 255, 0), 2:(255, 125, 0), 3:(255, 0, 255),
             4:255, 5:255, 6:255, 7:255, 8:255, 9:255}
directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

class game:
    def __init__(self, game_size):
        self.windowName = "do_not_find_anything"
        cv2.namedWindow(self.windowName)
        self.game_size = game_size
        self.mine_list = []
        self.img = np.zeros((game_size[0]*N,game_size[1]*N, 3), np.uint8)
        self.game_map = np.zeros((self.game_size[0], self.game_size[1])).tolist()
        self.status = "Initalized"
        self.isUpdated = True
        self.isAnimating = False
        self.animPos = 0
        self.point = 0
        self.total_mine = 15
        self.plant_mines(self.total_mine)
        self.draw_game()


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
            for j in around:
                if i[0] + j[0] == -1 or i[1] + j[1] == -1 or i[0] + j[0] == self.game_size[0] or i[1] + j[1] == self.game_size[1]:
                    continue
                try:
                    self.game_map[i[0] + j[0]][i[1] + j[1]] += 1
                except:
                    pass

    def draw_game(self):
        self.status = "Started"
        for i in range(self.game_size[0] + 1):
            cv2.line(self.img, (0, N * i), (N * self.game_size[1], N * i),
                                                             (255,0,0),2)

        for i in range(self.game_size[1] + 1):
            cv2.line(self.img, (N * i, 0), (N * i, N * self.game_size[0]),
                                                             (255,0,0),2)
    def define_square(self, coord):
        coordx = (coord[0]//N)
        coordy = (coord[1]//N)

        return [coordx, coordy]

    def markit(self, pos, type, optional=0, optional2 = 0):
        self.isUpdated = True
        if type == "color":
            avg = self.img[pos[1]*N + 2:pos[1]*N + N - 1, pos[0]*N + 2:pos[0]*N + N - 1]
            if avg.sum() != 0 and optional == (0, 0, 255):
                return
            if optional == (0, 0, 255):
                if self.game_map[pos[0]][pos[1]] == "M":
                    self.point += 1
                else:
                    self.point -= 1
            if optional == (0, 0, 0):
                if np.all(avg[:, :, 2] == 255) and np.all(avg[:, :, 0] == 0):
                    self.point += 1
                    self.img[pos[1]*N + 2:pos[1]*N + N - 1, pos[0]*N + 2:pos[0]*N + N - 1] = optional
            else:
                self.img[pos[1]*N + 2:pos[1]*N + N - 1, pos[0]*N + 2:pos[0]*N + N - 1] = optional

        elif type == "number":
            self.markit(pos, "color", (0, 0, 0))
            if optional2 == 0:
                self.markit(pos, "color", (255, 255, 255))
                return
            cv2.putText(self.img, str(optional2), (pos[0]*N + int(N * 0.3), pos[1]*N + int(N*0.7)), cv2.FONT_HERSHEY_SIMPLEX, N/50,
            num_color[optional2], 2)

    def show_mines(self):
        self.status = "Ended"
        for i in range(game_size[0]):
            for j in range(game_size[1]):
                self.markit([i, j], "color", (0, 0, 0))
        for i in self.mine_list:
            self.markit(i, "color", (0, 0, 255))

    def open_area(self, coord, dl):
        empties = []
        self.markit(coord, "number", optional2=int(self.game_map[coord[0]][coord[1]]))
        for i in around:
            if coord[0] + i[0] == -1 or coord[1] + i[1] == -1 or coord[0] + i[0] == self.game_size[0] or coord[1] + i[1] == self.game_size[1]:
                continue
            if self.game_map[coord[0] + i[0]][coord[1] + i[1]] == "M":
                continue

            if self.game_map[coord[0] + i[0]][coord[1] + i[1]] == 0 and [coord[0] + i[0], coord[1] + i[1]] not in dl:
                empties.append([coord[0] + i[0], coord[1] + i[1]])

            self.markit([coord[0] + i[0], coord[1] + i[1]], "number", optional2=int(self.game_map[coord[0] + i[0]][coord[1] + i[1]]))
        return empties

    def empty_open(self, coordlst, dl = []):
        empty_coords = []
        for j in coordlst:
            if j not in dl:
                dl.append(j)
        for i in coordlst:
            ec = self.open_area(i, dl)
            empty_coords.extend(ec)
            dl.extend(ec)
        if len(empty_coords) > 0:
            self.empty_open(empty_coords, dl)

    def endAnimation(self, type, frame):
        global xx
        self.isAnimating = True
        if type == "GOOD":
            if frame % 10 == 0:
                self.markit(self.mine_list[self.animPos%len(self.mine_list)], "color",
                            optional=(random.randrange(255), 128, random.randrange(255)))
                self.animPos += 1
        elif type == "BAD":
            self.markit(self.mine_list[self.animPos%len(self.mine_list)], "color",
                        optional=(0, 0, random.randrange(255)))
            self.animPos += 1
