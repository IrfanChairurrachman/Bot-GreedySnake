# Irfan Chairurrachman
# Indonesia

import pygame, sys, time, random
import numpy as np

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Greedy Best Snake by Irfan Cr')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Show game over message
def message(msg, color):
    my_font = pygame.font.SysFont('times new roman', 25)
    mesg = my_font.render(msg, True, color)
    game_window.blit(mesg, [frame_size_x / 6, frame_size_y / 3])

# Show score
def show_score(choice, color, font, size, score):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)

# Calculate distance between goal and current state
def dist(state, goal):
    dist = abs(goal[0] - state[0]) + abs(goal[1] - state[1])
    return dist

# Greedy Best-First Search algorith function
# parameter: direction, position (state), goal (food), body(snake_body)
def greedy(direc, pos, goal, body):
    # initiate direction and value for every direction
    arah = ['DOWN', 'UP', 'LEFT', 'RIGHT']
    nilai = np.array([[0, 10], [0, -10], [-10, 0], [10, 0]])
    # append every state and distance goal-state in dictionary
    dict_state = {x: pos + i for x, i in zip(arah, nilai)}
    dict_arah = {x: dist(pos + i, goal) for x, i in zip(arah, nilai)}

    # check if candidate direction is in snake body
    # if yes, then delete the candidate direction
    for item in dict_state.items():
        if list(item[1]) in body:
            arah.remove(item[0])
    
    # print candidate state and distance goal on terminal
    for item in arah:
        print(item, end=' = ')
        print(dict_arah[item], end=' -- ')
    print()

    change = direc

    if len(arah) == 0:
        return change
    
    if direc not in arah:
        change = arah[0]

    # looking which state has least value/distance to food
    for item in arah:
        if dict_arah[item] < dict_arah[change]:
            change = item
    
    # return direction to main()
    return change

# Main logic
def main():

    # Difficulty settings
    # Easy      ->  10
    # Medium    ->  25
    # Hard      ->  40
    # Harder    ->  60
    # Impossible->  120
    difficulty = 40

    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()

    # Game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    direction = 'RIGHT'
    change_to = direction

    end = False
    score = 0

    while True:

        # greedy function return to change_to
        change_to = greedy(direction, snake_pos, food_pos, snake_body)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        print(greedy(direction, snake_pos, food_pos, snake_body))
        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # snake can through window
        snake_pos[0] = snake_pos[0] % frame_size_x
        snake_pos[1] = snake_pos[1] % frame_size_y
        
        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pos[0] = pos[0] % frame_size_x
            pos[1] = pos[1] % frame_size_y
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Touching the snake body
        if snake_pos in snake_body[1:]:
            end = True
            # pygame.display.update()
        
        # if snake touch it's own body, show game over
        while end:
            game_window.fill(black)
            message("YOU LOST! press C-Play or Q-Exit", red)
            show_score(0, red, 'times', 20, score)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        time.sleep(1)
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_c:
                        time.sleep(1)
                        main()

        show_score(1, white, 'consolas', 20, score)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)

if __name__ == "__main__":
    main()
