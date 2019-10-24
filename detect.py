import sys

import detect_fortnite as fortnite
import detect_pubg as pubg
import detect_lol as lol
import detect_hearthstone as hearthstone

if __name__ == "__main__":
    img = sys.argv[1]
    game = sys.argv[2]
    # print img, game
    if img and game:
        if game == "fortnite":
            fortnite.detect_image(img)
        elif game == "pubg" or game == "cjzc":
            pubg.detect_image(img, game)
        elif game == "lol":
            lol.detect_img(img)
        elif game == "hearthstone":
            hearthstone.detect_img(img)
