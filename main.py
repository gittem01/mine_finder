import cv2
import random
import numpy as np

windowName = 'Drawing'
game_size = [12, 12]

def plant_mine(n, area_size): # Returns a list of coordinates which shows the positions of the mines

    mine_list = []

    def give_coord(AS):
        coordx = random.randrange(AS[0])
        coordy = random.randrange(AS[1])
        return [coordx, coordy]

    while len(mine_list) < n:
        coord = give_coord(area_size)
        if coord not in mine_list:
            mine_list.append(coord)
        else:
            continue
    return mine_list

def draw_circle(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x,y), 10, (255, 0, 0), -1)
        #Do smth else in here




img = np.zeros((game_size[0]*50,game_size[1]*50, 3), np.uint8)
cv2.namedWindow(windowName)
cv2.setMouseCallback(windowName, draw_circle)

while (True):
    cv2.imshow(windowName, img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
