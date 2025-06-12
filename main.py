### SNAKE GAME
# A snake controlled on a screen 
# Use arrow keys to move
# Aim: eat red apples without leaving screen or eating self 
# Game speeds up as score increases

# Libraries
import tkinter as tk
import random, time 
from _tkinter import TclError

# Global variables
HEIGHT = 600
WIDTH = 800

snake = [[50,50]] 
head = 0
tail = 0
dir = "Right" 

apple_pos = []
score = 0

key_queue = [] # process key presses in queue to prevent glitches 
# without this, the snake does not respond to rapid key presses and 
# might accidentally eat itself without the player realising 

# Functions

# draw() and erase() control snake graphics to create illusion of movement
def draw(window: tk.Canvas, pos: int):
    window.create_rectangle(snake[pos][0], snake[pos][1],
                            snake[pos][0]+50, snake[pos][1]+50,
                            fill="#00ffae", outline="#00ffae")
def erase(window: tk.Canvas, pos: int):
    window.create_rectangle(snake[pos][0], snake[pos][1],
                            snake[pos][0]+50, snake[pos][1]+50,
                            fill="#00aeff", outline="#00aeff")

def move_snake(window : tk.Canvas):
    '''moves the snake (self explanatory)'''
    global head, tail, dir, score
    x, y = snake[head][0], snake[head][1]
    if dir == "Up": snake.append([x, y-50])
    if dir == "Down": snake.append([x, y+50])
    if dir == "Left": snake.append([x-50, y])
    if dir == "Right": snake.append([x+50, y])
    
    # check collisions 
    game_over_conditions = [
        snake[head+1] in snake[tail:head+1],
        snake[head+1][0] < 0 or snake[head+1][1] < 0,
        snake[head+1][0] >= WIDTH or snake[head+1][1] >= HEIGHT,
    ]
    if any(game_over_conditions): raise TclError()

    # move snake 
    head += 1
    draw(window, head)
    # check for apples
    if apple_pos != snake[head]: 
        erase(window, tail)
        tail += 1
    else:
        apple(window)
        score += 1
    window.update()

def update_dir(event):
    '''Control direction of snake with keypresses'''
    global dir
    accepted = [event.keysym == "Up" and dir != "Down",
                event.keysym == "Down" and dir != "Up",
                event.keysym == "Left" and dir != "Right",
                event.keysym == "Right" and dir != "Left"]
    if any(accepted): dir = event.keysym

def apple(window: tk.Canvas):
    '''Creates a new apple randomly'''
    global snake, apple_pos
    while 1:
        x = 50 * random.randint(1, int(WIDTH/50)-1)
        y = 50 * random.randint(1, int(HEIGHT/50)-1)
        if [x, y] in snake[tail:head+1]: continue
        else: 
            apple_pos = [x,y]
            update_apple(window)
            window.update()
            break

def update_apple(window: tk.Canvas):
    '''Prevents apple from being accidentally erased'''
    window.create_rectangle(apple_pos[0], apple_pos[1], 
                            apple_pos[0]+50, apple_pos[1]+50, 
                            fill = "#ff0000")
    window.update()

# Main loop
if __name__ == '__main__':

    # Create game screen
    root = tk.Tk()
    root.config(height=800, width=800)
    root.title("Snake Game")

    window = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="#00aeff")
    
    # Initialise snake and apple
    draw(window, head)
    apple(window)
    window.pack()

    # Handle key presses effectively 
    def on_press(event): key_queue.append(event)
    window.bind_all("<Key>", on_press)    

    # Main game loop
    while True:
        try:
            if key_queue: update_dir(key_queue.pop(0))
            move_snake(window)
            update_apple(window)
            t = 0.1 + 0.2/(0.5*score + 1) # speed up game as score increases
            time.sleep(t)
        except TclError: # end the game
            print(f"Game Over.\nScore: {score}\n\nThanks for playing!")
            break 
        except KeyboardInterrupt:
            print(f"Uh-oh, the game ended!")
        except:
            print("Oops, looks like there was an error!")
            break