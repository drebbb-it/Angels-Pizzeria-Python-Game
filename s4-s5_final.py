import pygame 
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angel's Pizzeria")

# Fonts 
title_font = pygame.font.SysFont("arialblack", 140)
font = pygame.font.SysFont("opensans", 90)
small_font = pygame.font.SysFont("arial", 70)
condition_font = pygame.font.SysFont("courier new", 18)
info_font = pygame.font.SysFont("arial", 18)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (236, 213, 64)
DARK_GREY = (80, 80, 80)
RED = (255, 100, 100)
SEMI_TRANSPARENT = (20, 20, 20, 180)

# Background Images
# (Assuming these files exist in your directory)
try:
    menu_bg = pygame.image.load("background_screen/menu_bg.png")
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

    register_bg = pygame.image.load("background_screen/register_bg.png")
    register_bg = pygame.transform.scale(register_bg, (WIDTH, HEIGHT))

    # **FIXED: hello_bg was using register_bg**
    hello_bg = pygame.image.load("background_screen/hello_bg.png")
    hello_bg = pygame.transform.scale(hello_bg, (WIDTH, HEIGHT))

    loading_bg = pygame.image.load("background_screen/loadingrat_bg.png")
    loading_bg = pygame.transform.scale(loading_bg, (WIDTH, HEIGHT))

    level_bg = pygame.image.load("background_screen/level_bg.png")
    level_bg = pygame.transform.scale(level_bg, (WIDTH, HEIGHT))

    tablet_bg = pygame.image.load("background_screen/tablet.png")
    tablet_bg = pygame.transform.scale(tablet_bg, (WIDTH, HEIGHT))
    condition_images = [pygame.image.load(f"conditions/condition{i}.png").convert_alpha() for i in range(1, 6)]
    customer_symbol = pygame.image.load("conditions/custumer_symbol.png").convert_alpha()
    time_symbol = pygame.image.load("conditions/time_symbol.png").convert_alpha()
    accept_btn = pygame.image.load("buttons_images/accept_btn.png").convert_alpha()
    exit_btn = pygame.image.load("buttons_images/ex_btn.png").convert_alpha()
    back_btn = pygame.image.load("buttons_images/back_btn.png").convert_alpha()

    # Play button image
    play_btn_img = pygame.image.load("buttons_images/play_btn.png")

    # Load level images
    level_images = []
    level_images.append(pygame.image.load("conditions/level1.png").convert_alpha())
    level_images.append(pygame.image.load("conditions/level2.png").convert_alpha())
    level_images.append(pygame.image.load("conditions/level3.png").convert_alpha())
    level_images.append(pygame.image.load("conditions/level4.png").convert_alpha())
    level_images.append(pygame.image.load("conditions/level5.png").convert_alpha())
except pygame.error as e:
    print(f"Error loading image: {e}")
    # Creating dummy surfaces for preview purposes if assets are missing
    menu_bg = register_bg = hello_bg = loading_bg = level_bg = tablet_bg = pygame.Surface((WIDTH, HEIGHT))
    condition_images = [pygame.Surface((800, 500)) for _ in range(5)]
    customer_symbol = time_symbol = pygame.Surface((100, 100))
    accept_btn = pygame.Surface((280, 85))
    exit_btn = pygame.Surface((120, 80))
    back_btn = pygame.Surface((120, 80))  # Assuming similar size to exit_btn
    play_btn_img = pygame.Surface((340, 100))
    level_images = [pygame.Surface((211, 130)) for _ in range(5)]
    for img in level_images:
        img.fill(YELLOW)

# Scale level images - SMALL COMPACT BUTTONS HIGHER UP
LEVEL_WIDTH = int(WIDTH * 0.11)   # 211px
LEVEL_HEIGHT = 130                # 130px

# --- ADJUSTED Y OFFSET ---
LEVEL_Y_OFFSET = 350              

LEVEL_SPACING = 30                # Tight gaps
LEVEL_X_START = (WIDTH - (5 * LEVEL_WIDTH + 4 * LEVEL_SPACING)) // 2
level_scaled = []
for img in level_images:
    scaled_img = pygame.transform.scale(img, (LEVEL_WIDTH, LEVEL_HEIGHT))
    level_scaled.append(scaled_img)

# Game progress - Changed from current_level_unlocked to levels_completed
levels_completed = -1  # -1 = no levels completed, 0 = level 1 completed, 4 = all levels completed

# Selected level for tablet screen
selected_level = None

# Game states
state = "menu"
user_text = ""
condition_state = None  # "condition1", "condition2", etc.
warning_active = False
warning_timer = 0

play_button = pygame.Rect(WIDTH//2 - 170, HEIGHT//2 + 200, 340, 100)  # **FIXED: Added width and height**
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
loading_time = 8500

# Level condition data - CUSTOMIZE THESE
level_data = {
    1: {"customers": "3 customers", "time": "30 seconds", "instruction": "Serve 3 customers in 30 seconds!\nYou might unlock a kitchen tool after finishing this level."},
    2: {"customers": "3 customers", "time": "45 seconds", "instruction": "Serve 3 customers in 45 seconds!\nYou might unlock a kitchen tool after finishing this level."},
    3: {"customers": "5 customers", "time": "55 seconds", "instruction": "Serve 5 customers in 55 seconds!\nYou might unlock a kitchen tool after finishing this level."},
    4: {"customers": "5 customers", "time": "65 seconds", "instruction": "Serve 5 customers in 65 seconds!\nYou might unlock a kitchen tool after finishing this level."},
    5: {"customers": "1 customer", "time": "60 seconds", "instruction": "Ultimate Challenge!\nServe the Boss!"}
}

def draw_text_outline(text, font, text_color, outline_color, x, y):
    outline_range = 4
    for dx in range(-outline_range, outline_range + 1):
        for dy in range(-outline_range, outline_range + 1):
            if dx != 0 or dy != 0:
                outline_text = font.render(text, True, outline_color)
                screen.blit(outline_text, (x + dx, y + dy))
    main_text = font.render(text, True, text_color)
    screen.blit(main_text, (x, y))

def draw_condition_screen(level_num):
    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(SEMI_TRANSPARENT)
    screen.blit(overlay, (0, 0))
    
    # Condition background image
    cond_img = pygame.transform.scale(condition_images[level_num-1], (800, 500))
    screen.blit(cond_img, (WIDTH//2 - 400, HEIGHT//2 - 250))
    
    # Level instruction text - SIMPLE COURIER NEW, NO OUTLINE
    data = level_data[level_num]
    lines = data["instruction"].split('\n')
    y_pos = HEIGHT//2 - 80
    for line in lines:
        text_surf = condition_font.render(line, True, BLACK)
        text_rect = text_surf.get_rect(center=(WIDTH//2, y_pos))
        screen.blit(text_surf, text_rect)  # SIMPLE BLIT, NO OUTLINE
        y_pos += 35  # Reduced spacing for smaller font
    
    # Customer and Time symbols (HORIZONTAL)
    info_y = HEIGHT//2 + 30
    
    # Customer
    cust_sym = pygame.transform.scale(customer_symbol, (100, 100))
    screen.blit(cust_sym, (WIDTH//2 - 180, info_y - 15))
    cust_text = info_font.render(data["customers"], True, BLACK)
    screen.blit(cust_text, (WIDTH//2 - 80, info_y + 25))
    
    # Time
    time_sym = pygame.transform.scale(time_symbol, (70, 70))
    screen.blit(time_sym, (WIDTH//2 + 10, info_y))
    time_text = info_font.render(data["time"], True, BLACK)
    screen.blit(time_text, (WIDTH//2 + 100, info_y + 25))

    # Buttons
    accept_scaled = pygame.transform.scale(accept_btn, (280, 85))
    accept_rect = pygame.Rect(WIDTH//2 - 140, HEIGHT//2 + 120, 280, 85)
    screen.blit(accept_scaled, accept_rect)    
    
    cond_x = WIDTH//2 - 400
    cond_y = HEIGHT//2 - 250
    exit_btn_width = 120
    exit_btn_height = 80
    right_margin = 3

    exit_rect = pygame.Rect(cond_x + 800 - exit_btn_width - right_margin, cond_y + 20, exit_btn_width, exit_btn_height)
    exit_scaled = pygame.transform.scale(exit_btn, (exit_btn_width, exit_btn_height))
    screen.blit(exit_scaled, exit_rect)

    return accept_rect, exit_rect

def draw_warning():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(SEMI_TRANSPARENT)
    screen.blit(overlay, (0, 0))
    
    warning_text = "Complete previous level first!"
    text_surf = font.render(warning_text, True, RED)
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
    draw_text_outline(warning_text, font, RED, WHITE, text_rect.x, text_rect.y)

def init_loading_screen():
    global sprite_sheet, frames, SCALED_WIDTH, SCALED_HEIGHT, char_x, char_y, frame_index
    try:
        sprite_sheet = pygame.image.load("conditions/running_rat.png").convert_alpha()
        
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
    except pygame.error:
        # Fallback if image doesn't exist
        SCALED_WIDTH, SCALED_HEIGHT = 256, 256
        dummy = pygame.Surface((SCALED_WIDTH, SCALED_HEIGHT))
        dummy.fill(YELLOW)
        frames = [dummy]

    char_x = -SCALED_WIDTH
    char_y = HEIGHT - SCALED_HEIGHT - 150
    frame_index = 0

while True:
    # BACKGROUND
    if state == "menu":
        screen.blit(menu_bg, (0, 0))
    elif state == "register":
        screen.blit(register_bg, (0, 0))
    elif state == "hello":
        screen.blit(hello_bg, (0, 0))
    elif state == "loading":
        screen.blit(loading_bg, (0, 0))
    elif state == "home":
        screen.blit(level_bg, (0, 0))
    elif state == "tablet":
        screen.blit(tablet_bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                state = "register"

        elif state == "register" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_text.strip() != "":
                    state = "hello"
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                # NEW LOGIC: Only allow letters and spaces using .isalpha()
                if len(user_text) < 15 and (event.unicode.isalpha() or event.unicode == ' '):
                    user_text += event.unicode

        elif state == "hello" and event.type == pygame.MOUSEBUTTONDOWN:
            hello_x, hello_y = 520, 420
            hello_play_button = pygame.Rect(hello_x, hello_y + 170, 340, 100)
            if hello_play_button.collidepoint(event.pos):
                state = "loading"
                init_loading_screen()
                loading_start_time = pygame.time.get_ticks()

        elif state == "home" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle condition screen buttons
            if condition_state:
                level_num = int(condition_state[-1])
                accept_rect, exit_rect = draw_condition_screen(level_num)
                if accept_rect.collidepoint(mouse_pos):
                    print(f"ACCEPT CHALLENGE - Showing tablet for Level {level_num}!")
                    selected_level = level_num
                    state = "tablet"
                    condition_state = None
                elif exit_rect.collidepoint(mouse_pos):
                    print(f"EXIT - Back to level selection")
                    condition_state = None
                continue
            
            # Dismiss warning on click
            if warning_active:
                warning_active = False
                continue
            
            # **NEW LEVEL SELECTION LOGIC**
            # Any level <= levels_completed + 1 is playable (completed levels + current level)
            for i in range(5):
                level_rect = pygame.Rect(
                    LEVEL_X_START + i * (LEVEL_WIDTH + LEVEL_SPACING),
                    HEIGHT - LEVEL_HEIGHT - LEVEL_Y_OFFSET,
                    LEVEL_WIDTH,
                    LEVEL_HEIGHT
                )
                if level_rect.collidepoint(mouse_pos):
                    # Check if level is playable
                    if i <= levels_completed + 1:  # Can play completed levels + current level
                        condition_state = f"condition{i+1}"
                        print(f"Opening condition screen for Level {i+1}")
                    else:
                        warning_active = True
                        warning_timer = pygame.time.get_ticks()
                        print(f"Level {i+1} LOCKED! Complete Level {levels_completed+1} first")

        elif state == "tablet" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            back_rect = pygame.Rect(20, 20, 150, 100)  # Updated size
            if back_rect.collidepoint(mouse_pos):
                # Go back to condition screen
                condition_state = f"condition{selected_level}"
                state = "home"
                print(f"Back to condition screen for Level {selected_level}")
            else:
                # Any other click starts the level
                print(f"Starting Level {selected_level}!")
                # For demo: "complete" the level and unlock next one
                if levels_completed < selected_level - 1:
                    levels_completed = selected_level - 1
                state = "home"
                selected_level = None

    # DRAWING
    if state == "menu":
        title_text = "Angel's Pizzeria"
        title_surface = title_font.render(title_text, True, WHITE)
        title_x = WIDTH//2 - title_surface.get_width()//2
        title_y = 160
        draw_text_outline(title_text, title_font, WHITE, BLACK, title_x, title_y)
        play_btn_scaled = pygame.transform.scale(play_btn_img, (340, 100))
        screen.blit(play_btn_scaled, (play_button.x, play_button.y))

    elif state == "register":
        title_text = "Enter Your Name"
        title_surface = font.render(title_text, True, WHITE)
        title_x = WIDTH//2 - title_surface.get_width()//2
        title_y = 180
        draw_text_outline(title_text, font, WHITE, BLACK, title_x, title_y)
        input_box = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 + 180, 700, 100)
        pygame.draw.rect(screen, WHITE, input_box, border_radius=20)
        pygame.draw.rect(screen, BLACK, input_box, 5, border_radius=20)
        name_surface = small_font.render(user_text, True, BLACK)
        screen.blit(name_surface, (input_box.x + 25, input_box.y + 20))
        info = small_font.render("Press ENTER to continue", True, WHITE)
        info_rect = info.get_rect(center=(WIDTH//2, HEIGHT//2 + 320))
        screen.blit(info, info_rect)

    elif state == "hello":
        hello_x, hello_y = 520, 420
        hello_text = font.render(f"Hello, {user_text}!", True, BLACK)
        screen.blit(hello_text, (hello_x, hello_y))
        hello_play_button = pygame.Rect(hello_x, hello_y + 170, 340, 100)
        play_btn_scaled = pygame.transform.scale(play_btn_img, (340, 100))
        screen.blit(play_btn_scaled, (hello_play_button.x, hello_play_button.y))

    elif state == "loading":
        clock.tick(60)
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - loading_start_time
        
        frame_index += len(frames) * 5.0 / (loading_time / (1000 / 60))
        frame_index = frame_index % len(frames)
        char_x += 22
        
        if elapsed_time >= loading_time:
            state = "home"
            print("🐀 LOADING COMPLETE!")
            continue
        
        if char_x >= -SCALED_WIDTH and char_x <= WIDTH:
            current_frame = frames[int(frame_index)]
            screen.blit(current_frame, (char_x, char_y))

    elif state == "home":
        # **UPDATED LEVEL DRAWING LOGIC**
        # Show all levels as normal if all completed, otherwise only darken truly locked levels
        for i in range(5):
            level_x = LEVEL_X_START + i * (LEVEL_WIDTH + LEVEL_SPACING)
            level_y = HEIGHT - LEVEL_HEIGHT - LEVEL_Y_OFFSET
            
            # Only darken levels that are truly locked (beyond current progress)
            if levels_completed >= 4:  # All levels completed - show all normally
                screen.blit(level_scaled[i], (level_x, level_y))
            elif i > levels_completed + 1:  # Level is locked (beyond current progress)
                temp_surface = level_scaled[i].copy()
                temp_surface.fill(DARK_GREY, special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(temp_surface, (level_x, level_y))
            else:  # Playable level (completed or current)
                screen.blit(level_scaled[i], (level_x, level_y))
        
        # Draw overlays
        if condition_state:
            level_num = int(condition_state[-1])
            draw_condition_screen(level_num)
        
        if warning_active:
            elapsed = pygame.time.get_ticks() - warning_timer
            if elapsed < 2000:  # 2 seconds
                draw_warning()
    elif state == "tablet":
        # Draw back button in top left with background for visibility
        back_btn_scaled = pygame.transform.scale(back_btn, (150, 100))  # Made bigger
        back_rect = pygame.Rect(20, 20, 150, 100)
        # Draw a more visible background to make button stand out
        bg_surface = pygame.Surface((160, 110), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 200))  # Semi-transparent white background
        pygame.draw.rect(bg_surface, (0, 0, 0), (0, 0, 160, 110), 3, border_radius=10)  # Black border
        screen.blit(bg_surface, (15, 15))
        screen.blit(back_btn_scaled, back_rect)
        
        # Add text label for clarity
        back_text = small_font.render("BACK", True, BLACK)
        screen.blit(back_text, (back_rect.centerx - back_text.get_width()//2, back_rect.bottom + 5))

    pygame.display.update()
    clock.tick(60)