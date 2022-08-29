import pygame
import sys
import random

# setting up general stuff
pygame.init()


# create the main window
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

WINDOW = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption("Pong")


# Game Constants
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont("freesansbold", 50)

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

BALL_WIDTH = 12
MAX_VELOCITY = 5

WINNING_SCORE = 11

# Classes
class Paddle:
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == "up":
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY


class Ball:
    COLOR = WHITE

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.x_vel = MAX_VELOCITY
        self.y_vel = 0

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.width))

    def move(self):
        self.y += self.y_vel
        self.x += self.x_vel


class ScoreBoard:
    def __init__(self, left_score, right_score):
        self.left_score = left_score
        self.right_score = right_score
        self.left_score_text = FONT.render(f"{self.left_score}", 1, WHITE)
        self.right_score_text = FONT.render(f"{self.right_score}", 1, WHITE)

    def draw(self, window):
        quarter_screen_width = SCREEN_WIDTH // 4
        window.blit(
            self.right_score_text,
            [quarter_screen_width - self.right_score_text.get_width() // 2, 20],
        )
        window.blit(
            self.left_score_text,
            [(3 * quarter_screen_width) - self.left_score_text.get_width() // 2, 20],
        )

    def update_text(self):
        self.left_score_text = FONT.render(f"{self.left_score}", 1, WHITE)
        self.right_score_text = FONT.render(f"{self.right_score}", 1, WHITE)


# Functions
def handle_paddle_movement(keys, left_paddle, right_paddle):

    # up movement for left paddle

    # moves paddle up if not at top of screen
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(direction="up")
    # if paddle at top of screen, don't move it more
    elif keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY < 0:
        left_paddle.y = 2

    # down movement for left paddle

    # moves paddle down if not at bottom of screen
    if (
        keys[pygame.K_s]
        and (left_paddle.y + left_paddle.height + left_paddle.VELOCITY) <= SCREEN_HEIGHT
    ):
        left_paddle.move(direction="down")
    # if paddle is at bottom of screen don't move it anymore
    elif (
        keys[pygame.K_s]
        and (left_paddle.y + left_paddle.height + left_paddle.VELOCITY) > SCREEN_HEIGHT
    ):
        left_paddle.y = (SCREEN_HEIGHT - left_paddle.height) - 2

    # up movement for right paddle

    # moves paddle up if not at top of screen
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(direction="up")
    # if paddle at top of screen, don't move it more
    elif keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY < 0:
        right_paddle.y = 2

    # down movement for right paddle

    # moves paddle down if not at bottom of screen
    if (
        keys[pygame.K_DOWN]
        and (right_paddle.y + right_paddle.height + right_paddle.VELOCITY)
        <= SCREEN_HEIGHT
    ):
        right_paddle.move(direction="down")
    # if paddle is at bottom of screen don't move it anymore
    elif (
        keys[pygame.K_DOWN]
        and (right_paddle.y + right_paddle.height + right_paddle.VELOCITY)
        > SCREEN_HEIGHT
    ):
        right_paddle.y = (SCREEN_HEIGHT - right_paddle.height) - 2


def collision(the_ball, left_paddle, right_paddle, the_scoreboard):

    # handle ball collision with the ceiling
    if the_ball.y <= 0:
        the_ball.y_vel *= -1
    # handle ball collision with the floor
    elif the_ball.y + the_ball.width >= SCREEN_HEIGHT:
        the_ball.y_vel *= -1

    # handle ball passing the paddle on the left (scoring)
    if the_ball.x <= 0:
        left_scored = True
        score(the_ball, the_scoreboard, left_scored)

    # handle the ball passing the paddle on the right (scoring)
    elif the_ball.x >= SCREEN_WIDTH:
        left_scored = False
        score(the_ball, the_scoreboard, left_scored)

    # handle ball collision with the left paddle
    if the_ball.x_vel < 0:  # ball is moving toward the left
        if (
            the_ball.y >= left_paddle.y and the_ball.y <= left_paddle.y + PADDLE_HEIGHT
        ) and (the_ball.x <= left_paddle.x + PADDLE_WIDTH):
            the_ball.x_vel = calculate_new_x_velocity(the_ball)
            the_ball.y_vel = calculate_new_y_velocity(the_ball, left_paddle)

    # handle ball collision with the right paddle
    else:  # ball is moving toward the right
        if (
            the_ball.y >= right_paddle.y
            and the_ball.y <= right_paddle.y + PADDLE_HEIGHT
        ) and (the_ball.x >= right_paddle.x):
            the_ball.x_vel = calculate_new_x_velocity(the_ball)
            the_ball.y_vel = calculate_new_y_velocity(the_ball, right_paddle)


def calculate_new_x_velocity(the_ball):
    if the_ball.x_vel > 0:
        return 0 - MAX_VELOCITY
    else:
        return MAX_VELOCITY


def calculate_new_y_velocity(the_ball, the_paddle):
    paddle_midpoint = the_paddle.y + (PADDLE_HEIGHT / 2)
    ball_midpoint = the_ball.y + (BALL_WIDTH / 2)

    # percentage as 0-1 float of how far off the ball hit the paddle 
    # away from the center of the paddle
    new_y_vel = (ball_midpoint - paddle_midpoint) / (PADDLE_HEIGHT / 2) 

    new_y_vel *= MAX_VELOCITY
    return new_y_vel


def score(the_ball, the_scoreboard, left_scored):

    if left_scored:
        the_scoreboard.left_score += 1
    else:
        the_scoreboard.right_score += 1

    the_scoreboard.update_text()

    # game has been won and the check_win() func call in the main loop
    # will take care of the rest
    if (
        the_scoreboard.left_score >= WINNING_SCORE
        or the_scoreboard.right_score >= WINNING_SCORE
    ):
        pass
    else:
        # reset the ball's position to the center of the screen
        the_ball.x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
        the_ball.y = SCREEN_HEIGHT // 2 - BALL_WIDTH // 2
        # give the ball a random velocity in the x and y direction
        # ball's x_vel has special function b/c it can't be zero
        # or else the ball would never move so that it could score
        # or be hit by a paddle
        the_ball.x_vel = get_non_zero_random(0 - MAX_VELOCITY, MAX_VELOCITY)
        the_ball.y_vel = random.randint(0 - MAX_VELOCITY, MAX_VELOCITY)


def get_non_zero_random(bottom, top):

    while True:
        value = random.randint(bottom, top)
        if value != 0:
            break

    return value


def check_win(the_ball, left_paddle, right_paddle, the_scoreboard, window):
    if (
        the_scoreboard.left_score >= WINNING_SCORE
        or the_scoreboard.right_score >= WINNING_SCORE
    ):

        quarter_screen_width = SCREEN_WIDTH // 4

        # left won
        if the_scoreboard.left_score >= WINNING_SCORE:

            # create messages to be displayed when left wins
            left_message = FONT.render("Winner!", 1, WHITE)
            right_message = FONT.render("Loser.", 1, WHITE)
            window.blit(
                left_message,
                [
                    quarter_screen_width - left_message.get_width() // 2,
                    SCREEN_HEIGHT // 2,
                ],
            )
            window.blit(
                right_message,
                [
                    3 * quarter_screen_width - right_message.get_width() // 2,
                    SCREEN_HEIGHT // 2,
                ],
            )
        else:
            # create messages to be displayed when right wins
            left_message = FONT.render("Winner!", 1, WHITE)
            right_message = FONT.render("Loser.", 1, WHITE)
            window.blit(
                left_message,
                [
                    quarter_screen_width - left_message.get_width() // 2,
                    SCREEN_HEIGHT // 2,
                ],
            )
            window.blit(
                right_message,
                [
                    3 * quarter_screen_width - right_message.get_width() // 2,
                    SCREEN_HEIGHT // 2,
                ],
            )

        # display those messages and wait 5 seconds
        pygame.display.update()
        pygame.time.delay(5000)

        # resetting to start values
        the_scoreboard.left_score = 0
        the_scoreboard.right_score = 0
        the_ball.x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
        the_ball.y = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
        the_ball.x_vel = MAX_VELOCITY
        the_ball.y_vel = 0
        left_paddle.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        right_paddle.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

        the_scoreboard.update_text()


# Drawings
def draw(window, paddles, the_ball, the_scoreboard):
    window.fill(BLACK)

    the_scoreboard.draw(window)

    for paddle in paddles:
        paddle.draw(window)

    the_ball.draw(window)

    for y in range(10, SCREEN_HEIGHT, 20):
        if y % 2 == 1:
            continue
        else:
            pygame.draw.line(
                window, WHITE, [SCREEN_WIDTH // 2, y], [SCREEN_WIDTH // 2, y + 10], 10
            )

    pygame.display.update()


# Event Loop
def main():

    run = True
    clock = pygame.time.Clock()

    # put game objects in the scene
    left_paddle = Paddle(
        10, (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT
    )
    right_paddle = Paddle(
        (SCREEN_WIDTH - 10 - PADDLE_WIDTH),
        (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2),
        PADDLE_WIDTH,
        PADDLE_HEIGHT,
    )
    the_ball = Ball(
        (SCREEN_WIDTH // 2 - BALL_WIDTH // 2),
        (SCREEN_HEIGHT // 2 - BALL_WIDTH // 2),
        BALL_WIDTH,
    )
    the_scoreboard = ScoreBoard(0, 0)

    while run:

        clock.tick(FPS)
        draw(WINDOW, [left_paddle, right_paddle], the_ball, the_scoreboard)

        # loops over each event happening in each frame
        # if that user quits in that frame, close the app
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        the_ball.move()
        collision(the_ball, left_paddle, right_paddle, the_scoreboard)
        check_win(the_ball, left_paddle, right_paddle, the_scoreboard, WINDOW)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
