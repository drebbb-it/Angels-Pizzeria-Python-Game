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

# Loading background
loading_bg = pygame.image.load("loadingrat_bg.png")
loading_bg = pygame.transform.scale(loading_bg, (WIDTH, HEIGHT))

# Game states
state = "menu"
user_text = ""
timer_start = None

# Play button rectangle (menu button)
play_button = pygame.Rect(WIDTH//2 - 170, HEIGHT//2 + 200, 340, 100)

clock = pygame.time.Clock()

# LOADING SCREEN VARIABLES
sprite_sheet = None
frames = []
frame_index = 0
char_x = 0
char_y = 0
SCALED_WIDTH = 0
SCALED_HEIGHT = 0
loading_start_time = 0
loading_time = 10000  # Exactly 10 seconds

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

# Initialize loading screen assets
def init_loading_screen():
    global sprite_sheet, frames, SCALED_WIDTH, SCALED_HEIGHT, char_x, char_y, frame_index
    sprite_sheet = pygame.image.load("running rat.png").convert_alpha()
    
    FRAME_WIDTH = 32
    FRAME_HEIGHT = 32
    TOTAL_FRAMES = 123
    
    sheet_width = sprite_sheet.get_width()
    sheet_height = sprite_sheet.get_height()
    
    cols = sheet_width // FRAME_WIDTH
    rows = sheet_height // FRAME_HEIGHT
    num_frames = cols * rows
    
    if TOTAL_FRAMES > num_frames:
        TOTAL_FRAMES = num_frames
    
    SCALE = 8
    SCALED_WIDTH = int(FRAME_WIDTH * SCALE)
    SCALED_HEIGHT = int(FRAME_HEIGHT * SCALE)
    
    frames.clear()
    for i in range(TOTAL_FRAMES):
        x = (i % cols) * FRAME_WIDTH
        y = (i // cols) * FRAME_HEIGHT
        frame = sprite_sheet.subsurface((x, y, FRAME_WIDTH, FRAME_HEIGHT))
        frame = pygame.transform.scale(frame, (SCALED_WIDTH, SCALED_HEIGHT))
        frames.append(frame)
    
    char_x = -SCALED_WIDTH  # Start off left
    char_y = HEIGHT - SCALED_HEIGHT - 150
    frame_index = 0

while True:

    # BACKGROUND PER SCREEN
    if state == "menu":
        screen.blit(menu_bg, (0, 0))
    elif state == "register":
        screen.blit(register_bg, (0, 0))
    elif state == "hello":
        screen.blit(hello_bg, (0, 0))
    elif state == "loading":
        screen.blit(loading_bg, (0, 0))
    elif state == "home":  # New home state
        screen.fill((100, 150, 200))  # Temporary blue background

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
                hello_x = 520
                hello_y = 420
                hello_play_button = pygame.Rect(hello_x, hello_y + 170, 360, 110)
                if hello_play_button.collidepoint(event.pos):
                    state = "loading"
                    init_loading_screen()
                    loading_start_time = pygame.time.get_ticks()

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

    # HELLO SCREEN DRAWING
    elif state == "hello":
        hello_x = 520
        hello_y = 420
        hello_text = font.render(f"Hello, {user_text}!", True, BLACK)
        screen.blit(hello_text, (hello_x, hello_y))
        hello_play_button = pygame.Rect(hello_x, hello_y + 170, 360, 110)
        pygame.draw.rect(screen, YELLOW, hello_play_button, border_radius=20)
        pygame.draw.rect(screen, BLACK, hello_play_button, 5, border_radius=20)
        play_text = font.render("PLAY", True, WHITE)
        screen.blit(play_text, play_text.get_rect(center=hello_play_button.center))

    # LOADING SCREEN DRAWING - ✅ MODERATE SPEED!
    elif state == "loading":
        clock.tick(60)
        
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - loading_start_time
        
        # ✅ MODERATE SPEED (slower but not too slow)
        frame_index += len(frames) * 3.5 / (loading_time / (1000 / 60))  # 1.75x animation speed
        frame_index = frame_index % len(frames)
        char_x += 16  # Moderate movement (was 20, now 16px/frame)
        
        # ✅ EXIT TO HOME SCREEN after exactly 10 seconds
        if elapsed_time >= loading_time:
            state = "home"
            print("🐀 LOADING COMPLETE! → HOME SCREEN (", elapsed_time/1000, "s)")
            continue
        
        # Draw rat
        if char_x >= -SCALED_WIDTH and char_x <= WIDTH:
            current_frame = frames[int(frame_index)]
            screen.blit(current_frame, (char_x, char_y))

    # HOME SCREEN DRAWING
    elif state == "home":
        home_title = title_font.render("HOME SCREEN", True, WHITE)
        screen.blit(home_title, (WIDTH//2 - home_title.get_width()//2, HEIGHT//2 - 100))
        print("🏠 HOME SCREEN - Add your content here!")

    pygame.display.update()