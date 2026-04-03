import pygame 
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angel's Pizzeria")

# Fonts (BIGGER)
title_font = pygame.font.SysFont("arialblack", 140)
font = pygame.font.SysFont("opensans", 90)
small_font = pygame.font.SysFont("arial", 70)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (236, 213, 64)

# Background Images
menu_bg = pygame.image.load("menu_bg.png")
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

register_bg = pygame.image.load("register_bg.png")
register_bg = pygame.transform.scale(register_bg, (WIDTH, HEIGHT))

hello_bg = pygame.image.load("hello_bg.png")
hello_bg = pygame.transform.scale(hello_bg, (WIDTH, HEIGHT))

# Game states
state = "menu"
user_text = ""
timer_start = None

# Play button rectangle (menu button)
play_button = pygame.Rect(WIDTH//2 - 170, HEIGHT//2 + 200, 340, 100)

clock = pygame.time.Clock()

# Function to draw title with outline/border
def draw_text_outline(text, font, text_color, outline_color, x, y):
    outline_range = 4

    for dx in range(-outline_range, outline_range + 1):
        for dy in range(-outline_range, outline_range + 1):
            if dx != 0 or dy != 0:
                outline_text = font.render(text, True, outline_color)
                screen.blit(outline_text, (x + dx, y + dy))

    main_text = font.render(text, True, text_color)
    screen.blit(main_text, (x, y))


while True:

    # BACKGROUND PER SCREEN
    if state == "menu":
        screen.blit(menu_bg, (0, 0))

    elif state == "register":
        screen.blit(register_bg, (0, 0))

    elif state == "hello":
        screen.blit(hello_bg, (0, 0))  # ✅ FIXED: show hello popup background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # MENU EVENTS
        if state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    state = "register"

        # REGISTER EVENTS
        elif state == "register":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.strip() != "":
                        state = "hello"

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

                else:
                    if len(user_text) < 15:
                        user_text += event.unicode

        # HELLO EVENTS
        elif state == "hello":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hello_play_button.collidepoint(event.pos):  # ✅ uses correct button
                    state = "loading"
                    timer_start = pygame.time.get_ticks()

    # -------- DRAWING PART --------

    # MENU SCREEN DRAWING
    if state == "menu":
        title_text = "Angel's Pizzeria"

        title_surface = title_font.render(title_text, True, WHITE)
        title_x = WIDTH//2 - title_surface.get_width()//2
        title_y = 160

        draw_text_outline(title_text, title_font, WHITE, BLACK, title_x, title_y)

        pygame.draw.rect(screen, YELLOW, play_button, border_radius=20)
        pygame.draw.rect(screen, BLACK, play_button, 5, border_radius=20)

        play_text = font.render("PLAY", True, WHITE)
        screen.blit(play_text, play_text.get_rect(center=play_button.center))

    # REGISTER SCREEN DRAWING
    elif state == "register":
        title_text = "Enter Your Name"

        title_surface = font.render(title_text, True, WHITE)
        title_x = WIDTH//2 - title_surface.get_width()//2
        title_y = 180

        draw_text_outline(title_text, font, WHITE, BLACK, title_x, title_y)

        input_box = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 + 80, 700, 100)
        pygame.draw.rect(screen, WHITE, input_box, border_radius=20)
        pygame.draw.rect(screen, BLACK, input_box, 5, border_radius=20)

        name_surface = small_font.render(user_text, True, BLACK)
        screen.blit(name_surface, (input_box.x + 25, input_box.y + 20))

        info = small_font.render("Press ENTER to continue", True, WHITE)
        info_rect = info.get_rect(center=(WIDTH//2, HEIGHT//2 + 220))
        screen.blit(info, info_rect)

    # HELLO SCREEN DRAWING (POPUP FLOATING SCREEN)
    elif state == "hello":

        # ✅ LEFT-CENTER position (because logo is on right)
        hello_x = 520
        hello_y = 420

        hello_text = font.render(f"Hello, {user_text}!", True, BLACK)
        screen.blit(hello_text, (hello_x, hello_y))

        # ✅ Button placed under hello text (left-center)
        hello_play_button = pygame.Rect(hello_x, hello_y + 170, 360, 110)

        pygame.draw.rect(screen, YELLOW, hello_play_button, border_radius=20)
        pygame.draw.rect(screen, BLACK, hello_play_button, 5, border_radius=20)

        play_text = font.render("PLAY", True, WHITE)
        screen.blit(play_text, play_text.get_rect(center=hello_play_button.center))

    pygame.display.update()
    clock.tick(60)