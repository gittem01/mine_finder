from src.game import *

def event_func(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        game_square = the_game.define_square([x, y])
        if the_game.game_map[game_square[0]][game_square[1]] != "M":
            the_game.markit(game_square, "number", (255, 0, 160), int(the_game.game_map[game_square[0]][game_square[1]]))

        else:
            the_game.show_mines()

        if the_game.game_map[game_square[0]][game_square[1]] == 0:
            the_game.empty_open([game_square])
    if event == cv2.EVENT_RBUTTONDOWN:
        game_square = the_game.define_square([x, y])
        the_game.markit(game_square, "color", (0, 0, 255))

img = np.zeros((game_size[0]*N,game_size[1]*N, 3), np.uint8)

cv2.namedWindow(windowName)
cv2.setMouseCallback(windowName, event_func)

the_game = game(game_size, img)
the_game.plant_mines(total_mine)
the_game.draw_game()

while (True):
    cv2.imshow(windowName, the_game.img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
