from src.game import *

def event_func(event, x, y, flags, param):
    if the_game.status == "Ended":
        return
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

the_game = game(game_size)
cv2.setMouseCallback(the_game.windowName, event_func)

frame = 0
while (True):
    if the_game.isUpdated or the_game.isAnimating:
        frame += 1
        if the_game.point == the_game.total_mine and the_game.status != "Ended":
            the_game.endAnimation("GOOD", frame)
        elif the_game.status == "Ended":
            the_game.endAnimation("BAD", frame)
        cv2.imshow(the_game.windowName, the_game.img)
        the_game.isUpdated = False
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
