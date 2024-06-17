import pygame
pygame.init()


# set up display window and program variables
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # set window to height and width
pygame.display.set_caption("Ben's Pong Game")  # set caption title for window
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 10


# class to define the paddles used to keep the ball in play
class Paddle:
    COLOR = WHITE  # class attribute to define paddle color
    VEL = 4  # the velocity paddles move when arrow keys are pressed

    # constructor
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x  # x coordinate for paddle. Store original value in separate variable for resetting
        self.y = self.original_y = y  # y coordinate for paddle
        self.width = width
        self.height = height

    # function that draws the paddle on the window as a rectangle
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    # function for moving the paddles
    def move(self, up=True):
        if up:  # if 'up' key is pressed
            self.y -= self.VEL
        else:
            self.y += self.VEL

    # function to reset paddle to original location
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


# class defining the ball
class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x  # also stores original center x as separate variable
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL  # ball will move to right at max velocity at start of game
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius,)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    # function to reset the ball if someone scores
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1  # if someone scores, ball restarts in opposite direction to give their opponent recover time


# define a function to do the drawing for the app
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)  # background color for window

    # draw scores
    left_score_text = SCORE_FONT.render(f'{left_score}', 1, WHITE)
    right_score_text = SCORE_FONT.render(f'{right_score}', 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))  # draw at halfway coordinates
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:  # loop to draw all paddles
        paddle.draw(win)

    # draw a dashed line in middle of screen as 10 rectangles, each 10px in height
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:  # check if 'i' is an even number
            continue  # immediately skip this iteration and not draw a rectangle
        else:
            pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)  # draw ball to window

    pygame.display.update()  # required to actually update window with new drawings


# function for handling paddle movement
def handle_paddle_movement(keys, left_paddle, right_paddle):
    # move left paddle up and down if 'w' and 's' keys are used
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:  # AND statement doesn't allow paddle to go off-screen
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    # move right paddle if arrow keys are used
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


# main loop for program to display window
def main():
    run = True
    clock = pygame.time.Clock()  # Establish a clock so game runs at same frame rate on every device

    # creates left and right paddles centered in the middle (x coordinate is always the top-left corner of rectangle)
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)  # draw in middle of screen. Use double division results integer

    # create score counters
    left_score = 0
    right_score = 0

    # define main program loop
    while run:
        clock.tick(FPS)  # while loop can only run at a max of 60 FPS

        # continuously update the window with drawings every frame
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():  # get events like mouse clicks, keyboard inputs, closing window
            if event.type == pygame.QUIT:  # check if red button in top-right corner is pressed
                run = False
                break

        keys = pygame.key.get_pressed()  # gets keys pressed by user
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # update if someone scores
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # check if anyone has won the game. Display winner. Restart a new game after 5 seconds of winning
        won = False
        win_text = ''
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()  # update display with winning text
            pygame.time.delay(5000)  # delay game restart by 5 seconds
            ball.reset()
            right_paddle.reset()
            left_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()  # quit and close program once main loop has concluded


# function to handle ball collisions
def handle_collision(ball, left_paddle, right_paddle):
    # check if ball collides with floor or ceiling
    if ball.y + ball.radius >= HEIGHT:  # calculate if ball collides with floor
        ball.y_vel *= -1  # reverse the ball's direction at its current velocity
    elif ball.y + ball.radius <= 0:  # calculate if ball hits the ceiling
        ball.y_vel *= -1

    # check if ball collides with either paddle
    if ball.x_vel < 0:  # only check for left paddle if ball is moving left
        # calculate if ball is within range of the left paddle
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:  # check if ball's center y is in range
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:  # check if ball's center x is in range
                ball.x_vel *= -1  # reverse x direction
                middle_y = left_paddle.y + left_paddle.height / 2  # determine middle point of paddle
                difference_in_y = middle_y - ball.y  # determine displacement between paddle and ball's center points
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_velocity = difference_in_y / reduction_factor
                ball.y_vel = y_velocity * -1
    else:  # checks for right paddle collision
        # calculate if ball is in range of right paddle
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2  # determine middle point of paddle
                difference_in_y = middle_y - ball.y  # determine displacement between paddle and ball's center points
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_velocity = difference_in_y / reduction_factor
                ball.y_vel = y_velocity * -1


if __name__ == '__main__':  # ensures only this module can run the main() method
    main()
