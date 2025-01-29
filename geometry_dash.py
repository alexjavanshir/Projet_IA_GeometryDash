import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
from game import Game

MODE_IA = True  # Permet de choisir entre IA et mode manuel

def main():
    if MODE_IA:
        from agent import Agent
        agent = Agent()
        agent.train_ai(is_training=True)
    else:
        game = Game()
        game.run()

if __name__ == "__main__":
    main()
