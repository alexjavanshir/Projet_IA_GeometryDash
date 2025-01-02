import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
from game import Game

MODE_IA = False  # Permet de choisir entre IA et mode manuel

def main():
    if MODE_IA:
        from train_ia import train_ai
        train_ai()
    else:
        game = Game()
        game.run()

if __name__ == "__main__":
    main()
