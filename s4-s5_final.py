#the levels logic: the level2, level3, level4, level5 is darkened until the player finishes the previous level. When the player clicks on a level, if they have completed the previous level, it will show the condition screen for that level. If they have not completed the previous level, it will show a warning message. After the player accepts the condition screen, it will show a message screen with the instructions for that level. But the rest will stay the same. The only problem is the user is able to play the darkened level even after not finishing the previous level.
#make the level 1 already available to play, and the player can only play the next level if they have completed the previous level. 
#make the not yet finished levels darkened and unclickable, and if the player clicks on them, it will show a warning message.
#But the logic for the customer screen and the rest of the game will stay the same. The only problem is that the player can still click on the darkened levels and play them even if they have not finished the previous level. Please fix this issue and make sure that the player can only play the next level if they have completed the previous level, and that the not yet finished levels are darkened and unclickable, and that if the player clicks on them, it will show a warning message. Also, make sure that level 1 is already available to play when the player reaches the home screen.

import pygame 
import sys
import random
import math
from collections import Counter

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Music/angels_pizzeriamusic.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Screen
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angel's Pizzeria")

# Fonts 
title_font = pygame.font.SysFont("arialblack", 140)
font = pygame.font.SysFont("opensans", 90)
order_font = pygame.font.SysFont("opensans", 25)
small_font = pygame.font.SysFont("arial", 70)
condition_font = pygame.font.SysFont("courier new", 18)
info_font = pygame.font.SysFont("arial", 18)
button_font = pygame.font.SysFont("arial", 28)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (236, 213, 64)
DARK_GREY = (80, 80, 80)
RED = (255, 100, 100)
SEMI_TRANSPARENT = (20, 20, 20, 180)

# Background Images
try:
    menu_bg = pygame.image.load("background_screen/menu_bg.png")
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

    register_bg = pygame.image.load("background_screen/register_bg.png")
    register_bg = pygame.transform.scale(register_bg, (WIDTH, HEIGHT))

    hello_bg = pygame.image.load("background_screen/hello_bg.png")
    hello_bg = pygame.transform.scale(hello_bg, (WIDTH, HEIGHT))

    loading_bg = pygame.image.load("background_screen/loadingrat_bg.png")
    loading_bg = pygame.transform.scale(loading_bg, (WIDTH, HEIGHT))

    level_bg = pygame.image.load("background_screen/level_bg.png")
    level_bg = pygame.transform.scale(level_bg, (WIDTH, HEIGHT))

    msg_bg = pygame.image.load("background_screen/msg_screen.png")
    msg_bg = pygame.transform.scale(msg_bg, (WIDTH, HEIGHT))

    notif_bg = pygame.image.load("background_screen/notif_screen.png")
    notif_bg = pygame.transform.scale(notif_bg, (WIDTH, HEIGHT))

    main_kitchen_bg = pygame.image.load("background_screen/main_kitchen.png")
    main_kitchen_bg = pygame.transform.scale(main_kitchen_bg, (WIDTH, HEIGHT))

    oven_bg = pygame.image.load("Ingredients/oven_pizzascreen.png")
    oven_bg = pygame.transform.scale(oven_bg, (WIDTH, HEIGHT))

    cheese_pizza_base = pygame.image.load("Ingredients/cheese_pizza.png")
    
    customer_images = {}
    customer_images["c1"] = pygame.image.load("customers/c1.png")
    customer_images["c2"] = pygame.image.load("customers/c2.png")
    customer_images["c3"] = pygame.image.load("customers/c3.png")
    customer_images["c4"] = pygame.image.load("customers/c4.png")
    customer_images["c5"] = pygame.image.load("customers/c5.png")
    # Add boss if image exists, otherwise fallback to a surface
    try:
        customer_images["boss"] = pygame.image.load("customers/boss.png")
    except:
        customer_images["boss"] = pygame.Surface((WIDTH, HEIGHT))
        customer_images["boss"].fill((50, 0, 0))
    
    # Scale customer images to screen size
    for key in customer_images:
        customer_images[key] = pygame.transform.scale(customer_images[key], (WIDTH, HEIGHT))

    condition_images = [pygame.image.load(f"conditions/condition{i}.png").convert_alpha() for i in range(1, 6)]
    customer_symbol = pygame.image.load("conditions/custumer_symbol.png").convert_alpha()
    time_symbol = pygame.image.load("conditions/time_symbol.png").convert_alpha()
    accept_btn = pygame.image.load("buttons_images/accept_btn.png").convert_alpha()
    exit_btn = pygame.image.load("buttons_images/ex_btn.png").convert_alpha()
    back_btn = pygame.image.load("buttons_images/back_btn.png").convert_alpha()

    play_btn_img = pygame.image.load("buttons_images/play_btn.png")

    level_images = []
    level_images.append(pygame.image.load("conditions/level1.png").convert_alpha())
    level_images.append(pygame.image.load("conditions/level2.png").convert_alpha())
    level_images.append(pygame.image.load("conditions/level3.png").convert_alpha())
    level_images.append(pygame.image.load("conditions/level4.png").convert_alpha())
    level_images.append(pygame.image.load("conditions/level5.png").convert_alpha())

    # Load ingredient images
    ingredient_images = {}
    ingredient_images["pepperoni"] = pygame.image.load("Ingredients/pepperoni_drag.png").convert_alpha()
    ingredient_images["bell pepper"] = pygame.image.load("Ingredients/bellpepper_drag.png").convert_alpha()
    ingredient_images["cheese"] = pygame.image.load("Ingredients/cheese_pizza.png").convert_alpha()
    ingredient_images["bacon"] = pygame.image.load("Ingredients/bacon_drag.png").convert_alpha()
    ingredient_images["beef"] = pygame.image.load("Ingredients/beef_drag.png").convert_alpha()
    ingredient_images["pineapple"] = pygame.image.load("Ingredients/pineapple_drag.png").convert_alpha()
    ingredient_images["mushroom"] = pygame.image.load("Ingredients/mushroom_drag.png").convert_alpha()
    # For olives, use mushroom as fallback if not available
    try:
        ingredient_images["olives"] = pygame.image.load("Ingredients/olives_drag.png").convert_alpha()
    except:
        ingredient_images["olives"] = ingredient_images["mushroom"]

except pygame.error as e:
    print(f"Error loading image: {e}")
    menu_bg = register_bg = hello_bg = loading_bg = level_bg = msg_bg = notif_bg = main_kitchen_bg = oven_bg = c1_bg = pygame.Surface((WIDTH, HEIGHT))
    cheese_pizza_base = pygame.Surface((100, 100))
    condition_images = [pygame.Surface((800, 500)) for _ in range(5)]
    customer_symbol = time_symbol = pygame.Surface((100, 100))
    accept_btn = pygame.Surface((280, 85))
    exit_btn = pygame.Surface((120, 80))
    back_btn = pygame.Surface((120, 80))
    play_btn_img = pygame.Surface((340, 100))
    level_images = [pygame.Surface((211, 130)) for _ in range(5)]
    for img in level_images:
        img.fill(YELLOW)
    ingredient_images = {}

LEVEL_WIDTH = int(WIDTH * 0.11)
LEVEL_HEIGHT = 130
LEVEL_Y_OFFSET = 350
LEVEL_SPACING = 30
LEVEL_X_START = (WIDTH - (5 * LEVEL_WIDTH + 4 * LEVEL_SPACING)) // 2
level_scaled = []
for img in level_images:
    scaled_img = pygame.transform.scale(img, (LEVEL_WIDTH, LEVEL_HEIGHT))
    level_scaled.append(scaled_img)

# ✅ FIXED: Level 1 available by default (0 = level 1 completed)
levels_completed = 0 
selected_level = None
level_finished = False
level_start_time = 0
level_duration = 0
level_failed = False
msg_screen_start_time = 0

state = "menu"
user_text = ""
condition_state = None
warning_active = False
warning_timer = 0

play_button = pygame.Rect(WIDTH//2 - 170, HEIGHT//2 + 200, 340, 100)
clock = pygame.time.Clock()

sprite_sheet = None
frames = []
frame_index = 0
char_x = 0
char_y = 0
SCALED_WIDTH = 0
SCALED_HEIGHT = 0
loading_start_time = 0
loading_time = 8500

def draw_text_outline(text, font, text_color, outline_color, x, y):
    outline_range = 4
    for dx in range(-outline_range, outline_range + 1):
        for dy in range(-outline_range, outline_range + 1):
            if dx != 0 or dy != 0:
                outline_text = font.render(text, True, outline_color)
                screen.blit(outline_text, (x + dx, y + dy))
    main_text = font.render(text, True, text_color)
    screen.blit(main_text, (x, y))


def is_order_complete(order_ingredients=None):
    if order_ingredients is None:
        order_ingredients = current_customer_order_ingredients
    if not order_ingredients:
        return False
    return Counter(ingredient_stack) == Counter(order_ingredients)

def draw_condition_screen(level_num):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(SEMI_TRANSPARENT)
    screen.blit(overlay, (0, 0))

    cond_img = pygame.transform.scale(condition_images[level_num-1], (800, 500))
    screen.blit(cond_img, (WIDTH//2 - 400, HEIGHT//2 - 250))

    data = level_data[level_num]
    lines = data["instruction"].split('\n')
    y_pos = HEIGHT//2 - 80
    for line in lines:
        text_surf = condition_font.render(line, True, BLACK)
        text_rect = text_surf.get_rect(center=(WIDTH//2, y_pos))
        screen.blit(text_surf, text_rect)
        y_pos += 35
    
    info_y = HEIGHT//2 + 30
    cust_sym = pygame.transform.scale(customer_symbol, (100, 100))
    screen.blit(cust_sym, (WIDTH//2 - 180, info_y - 15))
    cust_text = info_font.render(data["customers"], True, BLACK)
    screen.blit(cust_text, (WIDTH//2 - 80, info_y + 25))

    time_sym = pygame.transform.scale(time_symbol, (70, 70))
    screen.blit(time_sym, (WIDTH//2 + 10, info_y))
    time_text = info_font.render(data["time"], True, BLACK)
    screen.blit(time_text, (WIDTH//2 + 100, info_y + 25))

    accept_scaled = pygame.transform.scale(accept_btn, (280, 85))
    accept_rect = pygame.Rect(WIDTH//2 - 140, HEIGHT//2 + 120, 280, 85)
    screen.blit(accept_scaled, accept_rect)
    
    cond_x = WIDTH//2 - 400
    cond_y = HEIGHT//2 - 250
    exit_btn_width = 120
    exit_btn_height = 80
    exit_rect = pygame.Rect(cond_x + 800 - exit_btn_width - 3, cond_y + 20, exit_btn_width, exit_btn_height)
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
        SCALED_WIDTH, SCALED_HEIGHT = 256, 256
        dummy = pygame.Surface((SCALED_WIDTH, SCALED_HEIGHT))
        dummy.fill(YELLOW)
        frames = [dummy]
    char_x = -SCALED_WIDTH
    char_y = HEIGHT - SCALED_HEIGHT - 150
    frame_index = 0

# --- NEW CUSTOMER SCREEN LOGIC ---
customer_queue = []
current_customer_index = 0
customer_timer = 0
CUSTOMER_SCREEN_DURATION = 3000
current_customer_order_ingredients = []
kitchen_info_active = False
kitchen_selected_ingredient = None
ingredient_stack = []
KITCHEN_INGREDIENT_BUTTONS = ["pepperoni", "bell pepper", "cheese", "bacon", "olives", "beef", "pineapple", "mushroom"]
kitchen_button_rects = []

level_data = {
    1: {"customers": "3 customers", "time": "30 seconds", "instruction": "Serve 3 customers in 30 seconds!\nYou might unlock a kitchen tool after finishing this level."},
    2: {"customers": "3 customers", "time": "45 seconds", "instruction": "Serve 3 customers in 45 seconds!\nYou might unlock a kitchen tool after finishing this level."},
    3: {"customers": "5 customers", "time": "55 seconds", "instruction": "Serve 5 customers in 55 seconds!\nYou might unlock a kitchen tool after finishing this level."},
    4: {"customers": "5 customers", "time": "65 seconds", "instruction": "Serve 5 customers in 65 seconds!\nYou might unlock a kitchen tool after finishing this level."},
    5: {"customers": "1 customer", "time": "60 seconds", "instruction": "Ultimate Challenge!\nServe the Boss!"}
}

customer_ingredient_map = {
    1: {
        "c1": ["cheese", "bacon", "mushroom"],
        "c2": ["pepperoni", "cheese"],
        "c3": ["beef", "pineapple"]
    },
    2: {
        "c1": ["pepperoni", "bell pepper", "olives", "mushroom", "cheese", "beef", "bacon"],
        "c2": ["cheese"],
        "c3": ["pepperoni", "olives"],
        "c4": ["beef", "bell pepper", "mushroom", "cheese"],
        "c5": ["cheese", "bell pepper"]
    },
    3: {
        "c1": ["bacon", "pineapple"],
        "c2": ["bacon", "cheese"],
        "c3": ["pepperoni", "olives"],
        "c4": ["pepperoni", "mushroom", "bell pepper"],
        "c5": ["pepperoni", "olives", "mushroom", "cheese", "beef", "pineapple", "bacon"]
    },
    4: {
        "c1": ["bacon", "pineapple"],
        "c2": ["bacon", "cheese"],
        "c3": ["pepperoni", "mushroom", "bell pepper"],
        "c4": ["beef", "pineapple"],
        "c5": ["pepperoni", "cheese", "beef", "pineapple", "bacon", "olives", "mushroom"]
    },
    5: {
        "boss": ["pepperoni", "bell pepper", "olives", "mushroom", "cheese", "beef", "pineapple", "bacon"]
    }
}


def start_level(level_num):
    # ADD 'current_level' to your global variables here:
    global customer_queue, current_customer_index, customer_timer, state, current_level, level_finished, level_start_time, level_duration, level_failed, ingredient_stack
    
    current_level = level_num # <-- Track the level so the UI knows which orders to use
    level_finished = False
    level_failed = False
    level_start_time = 0
    level_duration = int(level_data[level_num]["time"].split()[0]) if level_num in level_data else 60
    ingredient_stack.clear()  # Clear the stack for the new level

    # Create the queue based on level (Your existing code stays exactly the same)
    if level_num == 1:
        customer_queue = ["c1", "c2", "c3"]
    elif level_num == 2:
        customer_queue = random.sample(["c1", "c2", "c3"], 3)
    elif level_num == 3:
        customer_queue = random.sample(["c1", "c2", "c3", "c4", "c5"], 5)
    elif level_num == 4:
        customer_queue = random.sample(["c1", "c2", "c3", "c4", "c5"], 5)
    elif level_num == 5:
        customer_queue = ["boss"]

    current_customer_index = 0
    customer_timer = pygame.time.get_ticks()
    state = "customer_screen"

def show_customer_ui(customer_key):
    global current_level # <-- Bring in the level we saved in start_level

    # 1. Draw the specific background for this customer
    bg = customer_images.get(customer_key, customer_images["c1"])
    screen.blit(bg, (0, 0))

    # 2. Draw the dialogue text
    # A nested dictionary: templates[level_num][customer_key]
    templates = {
        1: {
            "c1": "Hi! I'd like to order 1 pizza with cheese, bacon, and mushroom only.",
            "c2": "Hello! Can I get 1 pizza with just pepperoni and cheese?\nDo not put any vegetables.",
            "c3": "Good day! I want 1 pizza with beef and pineapple only. No cheese.",
        },
        2: {
            "c1":  "Hi there! Give me 1 pizza with everything on it, please, but no pineapple.\nI don't like sweet pizza.",
            "c2": "Hello! I'd like 1 pizza with just plain cheese and nothing else.",
            "c3": "Hi! Make it 1 pizza with pepperoni and olives only.\nPlease do not add cheese.",
        },
        3: {
            "c1": "Good morning! I'll take 1 pizza with beef and bell peppers.",
            "c2": "Hello! Can I order 1 pizza with bacon, beef, and cheese?",
            "c3": "Hi! I want 1 pizza loaded with all meats:\npepperoni, bacon, and beef.\nNo veggies, please!",
            "c4": "Hey! Give me 1 pizza with bell peppers, beef, mushroom, and cheese only.",
            "c5": "Hi! I'd like 1 pizza, please, with just cheese and bell peppers.\nNo meat.",
        },
        4: {
            "c1": "Hello! Order for 1 pizza with bacon and pineapple, please.",
            "c2": "Good evening! I want 1 pizza with bacon and cheese.\nPlease do not add anything else.",
            "c3": "Hi there! Can I get 1 pizza with pepperoni, mushroom, and bell peppers?",
            "c4": "Hello! I'll have 1 pizza with beef and pineapple.\nPlease do not add anything else.",
            "c5": "Hi! Make it 1 pizza with everything except bell peppers, please.",
        },
        5: {
            "boss": "Impressive! Let's see if you can handle my ultimate pizza challenge!"
        }
    }

    global current_customer_order_ingredients
    level_orders = templates.get(current_level, {})
    text = level_orders.get(customer_key, "Unknown order.")
    current_customer_order_ingredients = customer_ingredient_map.get(current_level, {}).get(customer_key, [])

    # --- UPDATED MULTI-LINE RENDERING LOGIC ---
    # Ensure there are actually newlines in your strings in the dictionary above
    lines = text.split('\n') 
    line_height = order_font.get_height() + 8 # Increased spacing slightly for readability
    
    if customer_key == "boss":
        # Based on the uploaded image, the bubble center is further right and slightly lower than regular customers
        X_OFFSET = 100  
        Y_OFFSET = -40  
    else:
        # Standard offsets for levels 1-4
        X_OFFSET = 50   
        Y_OFFSET = -80  

    total_text_height = len(lines) * line_height
    start_y = (HEIGHT // 2 + Y_OFFSET) - (total_text_height // 2)

    for i, line in enumerate(lines):
        line_surf = order_font.render(line, True, BLACK)
        # Calculate centering for each line
        line_rect = line_surf.get_rect(center=(WIDTH // 2 + X_OFFSET, start_y + (i * line_height)))
        draw_text_outline(line, order_font, BLACK, WHITE, line_rect.x, line_rect.y)

# --- MAIN LOOP ---
while True:
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
    elif state == "msg_screen":
        screen.blit(msg_bg, (0, 0))
    elif state == "notif_screen":
        screen.blit(notif_bg, (0, 0))
    elif state == "kitchen_screen":
        screen.blit(main_kitchen_bg, (0, 0))
    elif state == "oven_screen":
        screen.blit(main_kitchen_bg, (0, 0))
    elif state == "customer_screen":
        current_customer_key = customer_queue[current_customer_index]
        screen.blit(customer_images[current_customer_key], (0, 0))
        show_customer_ui(current_customer_key)
        exit_scaled = pygame.transform.scale(exit_btn, (120, 80))
        exit_rect = pygame.Rect(150, 20, 120, 80)
        screen.blit(exit_scaled, exit_rect)

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
            
            # Handle condition screen first (if active)
            if condition_state:
                level_num = int(condition_state[-1])
                accept_rect, exit_rect = draw_condition_screen(level_num)
                if accept_rect.collidepoint(mouse_pos):
                    selected_level = level_num
                    state = "msg_screen"
                    msg_screen_start_time = pygame.time.get_ticks()
                    condition_state = None
                elif exit_rect.collidepoint(mouse_pos):
                    condition_state = None
                continue

            if warning_active:
                warning_active = False
                continue
            
            for i in range(5):
                level_rect = pygame.Rect(
                    LEVEL_X_START + i * (LEVEL_WIDTH + LEVEL_SPACING),
                    HEIGHT - LEVEL_HEIGHT - LEVEL_Y_OFFSET,
                    LEVEL_WIDTH,
                    LEVEL_HEIGHT
                )
                if level_rect.collidepoint(mouse_pos):
                    if i <= levels_completed:
                        condition_state = f"condition{i+1}"
                    else:
                        warning_active = True
                        warning_timer = pygame.time.get_ticks()

        elif state == "msg_screen" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            back_rect = pygame.Rect(20, 20, 150, 100)
            exit_rect = pygame.Rect(40, 20, 120, 80)
            if back_rect.collidepoint(mouse_pos) or exit_rect.collidepoint(mouse_pos):
                state = "home"
                selected_level = None

        elif state == "notif_screen" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            back_rect = pygame.Rect(20, 20, 150, 100)
            exit_rect = pygame.Rect(40, 20, 120, 80)
            if back_rect.collidepoint(mouse_pos) or exit_rect.collidepoint(mouse_pos):
                state = "home"
                selected_level = None
            notif_message_rect = pygame.Rect(1180, 506, 336, 274)
            if notif_message_rect.collidepoint(mouse_pos):
                if selected_level:
                    start_level(selected_level)  # start customer sequence for chosen level

        elif state == "customer_screen" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            exit_rect = pygame.Rect(40, 20, 120, 80)
            if exit_rect.collidepoint(mouse_pos):
                state = "home"
                selected_level = None
                customer_timer = 0
                current_customer_index = 0

        elif state == "kitchen_screen" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_width = 180
            button_height = 65
            button_spacing = 15
            x_start = (WIDTH - (8 * button_width + 7 * button_spacing)) // 2
            y_start = HEIGHT//2 - 320
            remove_button_rect = pygame.Rect(
                x_start + 7 * (button_width + button_spacing),
                y_start + button_height + button_spacing,
                button_width,
                button_height
            )
            return_button_rect = pygame.Rect(
                x_start + 7 * (button_width + button_spacing),
                y_start + button_height + button_spacing + button_height + button_spacing,
                button_width,
                button_height
            )
            # Define oven rectangle under the bell pepper button (index 1)
            oven_rect = pygame.Rect(
                x_start + 1 * (button_width + button_spacing),
                y_start + button_height + 50,  # Below the button with some spacing
                button_width,
                100  # Height of the oven area
            )
            failed_back_rect = pygame.Rect(WIDTH//2 - 75, HEIGHT//2 + 100, 150, 100)
            if level_failed:
                if failed_back_rect.collidepoint(mouse_pos):
                    state = "home"
                    selected_level = None
                    kitchen_info_active = False
                    kitchen_selected_ingredient = None
                    level_failed = False
                continue
            if return_button_rect.collidepoint(mouse_pos) and selected_level is not None and level_finished:
                state = "home"
                selected_level = None
                kitchen_info_active = False
                kitchen_selected_ingredient = None
                ingredient_stack.clear()
            elif oven_rect.collidepoint(mouse_pos):
                state = "oven_screen"
            else:
                kitchen_button_rects = []
                for col in range(8):
                    rect = pygame.Rect(
                        x_start + col * (button_width + button_spacing),
                        y_start,
                        button_width,
                        button_height
                    )
                    kitchen_button_rects.append(rect)

                for index, button_rect in enumerate(kitchen_button_rects):
                    if button_rect.collidepoint(mouse_pos):
                        clicked_ingredient = KITCHEN_INGREDIENT_BUTTONS[index]
                        ingredient_stack.append(clicked_ingredient)
                        kitchen_selected_ingredient = clicked_ingredient
                        kitchen_info_active = True
                        break
                else:
                    if remove_button_rect.collidepoint(mouse_pos):
                        if ingredient_stack:
                            ingredient_stack.pop()
                        kitchen_selected_ingredient = ingredient_stack[-1] if ingredient_stack else None
                        kitchen_info_active = True

        elif state == "oven_screen" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Calculate oven window position and tab area
            oven_width = 800
            oven_height = 600
            oven_x = (WIDTH - oven_width) // 2
            oven_y = (HEIGHT - oven_height) // 2
            tab_height = 120
            oven_window_rect = pygame.Rect(oven_x, oven_y, oven_width, oven_height + tab_height)
            oven_exit_rect = pygame.Rect(WIDTH - 140, 20, 120, 80)

            current_customer_key = customer_queue[current_customer_index] if customer_queue else None
            current_customer_order_ingredients = customer_ingredient_map.get(current_level, {}).get(current_customer_key, [])
            order_ready = is_order_complete(current_customer_order_ingredients)
            order_button_rect = pygame.Rect(oven_x + oven_width - 210, oven_y + oven_height - 140, 170, 60) if order_ready else None

            # If clicking on the done button when ready, move to next customer or finish level
            return_button_rect = pygame.Rect(WIDTH - 220, HEIGHT - 120, 200, 80)
            if order_button_rect and order_button_rect.collidepoint(mouse_pos):
                ingredient_stack.clear()
                kitchen_info_active = False
                kitchen_selected_ingredient = None
                if customer_queue:
                    customer_queue.pop(current_customer_index)
                if customer_queue:
                    current_customer_index = min(current_customer_index, len(customer_queue) - 1)
                    customer_timer = pygame.time.get_ticks()
                    continue
                else:
                    if selected_level is not None:
                        levels_completed = max(levels_completed, selected_level)
                    level_finished = True
                    state = "kitchen_screen"
                    continue
            elif oven_exit_rect.collidepoint(mouse_pos) or not oven_window_rect.collidepoint(mouse_pos):
                state = "kitchen_screen"

    if state == "msg_screen":
        current_time = pygame.time.get_ticks()
        if current_time - msg_screen_start_time > 3000:
            state = "notif_screen"

    if state == "menu":
        title_text = "Angel's Pizzeria"
        title_surface = title_font.render(title_text, True, WHITE)
        title_x = WIDTH//2 - title_surface.get_width()//2
        draw_text_outline(title_text, title_font, WHITE, BLACK, title_x, 160)
        play_btn_scaled = pygame.transform.scale(play_btn_img, (340, 100))
        screen.blit(play_btn_scaled, (play_button.x, play_button.y))

    elif state == "register":
        title_text = "Enter Your Name"
        title_surface = font.render(title_text, True, WHITE)
        title_x = WIDTH//2 - title_surface.get_width()//2
        draw_text_outline(title_text, font, WHITE, BLACK, title_x, 180)
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
        screen.blit(play_btn_scaled, hello_play_button)

    elif state == "loading":
        clock.tick(60)
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - loading_start_time
        frame_index += len(frames) * 5.0 / (loading_time / (1000 / 60))
        frame_index %= len(frames)
        char_x += 22
        if elapsed_time >= loading_time:
            state = "home"
            continue
        if WIDTH + SCALED_WIDTH > char_x >= -SCALED_WIDTH:
            current_frame = frames[int(frame_index)]
            screen.blit(current_frame, (char_x, char_y))

    elif state == "home":
        for i in range(5):
            level_x = LEVEL_X_START + i * (LEVEL_WIDTH + LEVEL_SPACING)
            level_y = HEIGHT - LEVEL_HEIGHT - LEVEL_Y_OFFSET
            if i > levels_completed:
                temp_surface = level_scaled[i].copy()
                temp_surface.fill(DARK_GREY, special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(temp_surface, (level_x, level_y))
            else:
                screen.blit(level_scaled[i], (level_x, level_y))
        if condition_state:
            draw_condition_screen(int(condition_state.replace("condition", "")))
        if warning_active and pygame.time.get_ticks() - warning_timer < 2000:
            draw_warning()

    elif state == "msg_screen":
        back_btn_scaled = pygame.transform.scale(back_btn, (150, 100))
        back_rect = pygame.Rect(20, 20, 150, 100)
        bg_surface = pygame.Surface((160, 110))
        bg_surface.fill((255, 255, 255))
        pygame.draw.rect(bg_surface, (0, 0, 0), (0, 0, 160, 110), 3, border_radius=10)
        screen.blit(bg_surface, (15, 15))
        screen.blit(back_btn_scaled, back_rect)
        back_text = small_font.render("BACK", True, BLACK)
        screen.blit(back_text, (back_rect.centerx - back_text.get_width()//2, back_rect.bottom + 5))

        exit_scaled = pygame.transform.scale(exit_btn, (120, 80))
        exit_rect = pygame.Rect(40, 20, 120, 80)
        screen.blit(exit_scaled, exit_rect)

    elif state == "notif_screen":
        screen.blit(notif_bg, (0, 0))
        back_btn_scaled = pygame.transform.scale(back_btn, (150, 100))
        back_rect = pygame.Rect(20, 20, 150, 100)
        bg_surface = pygame.Surface((160, 110))
        bg_surface.fill((255, 255, 255))
        pygame.draw.rect(bg_surface, (0, 0, 0), (0, 0, 160, 110), 3, border_radius=10)
        screen.blit(bg_surface, (15, 15))
        screen.blit(back_btn_scaled, back_rect)
        back_text = small_font.render("BACK", True, BLACK)
        screen.blit(back_text, (back_rect.centerx - back_text.get_width()//2, back_rect.bottom + 5))

        exit_scaled = pygame.transform.scale(exit_btn, (120, 80))
        exit_rect = pygame.Rect(150, 20, 120, 80)
        screen.blit(exit_scaled, exit_rect)

    elif state == "kitchen_screen":
        # Draw eight ingredient buttons in a single horizontal row above the rat
        button_width = 180
        button_height = 65
        button_spacing = 15
        columns = 8
        x_start = (WIDTH - (columns * button_width + (columns - 1) * button_spacing)) // 2
        y_start = HEIGHT//2 - 320
        kitchen_button_rects = []
        for col in range(columns):
            index = col
            label = KITCHEN_INGREDIENT_BUTTONS[index]
            rect = pygame.Rect(
                x_start + col * (button_width + button_spacing),
                y_start,
                button_width,
                button_height
            )
            kitchen_button_rects.append(rect)
            fill_color = (238, 224, 196)
            border_color = (94, 50, 29)
            text_color = (45, 30, 12)
            if ingredient_stack and ingredient_stack[-1] == label:
                fill_color = (197, 153, 104)
                border_color = (103, 57, 25)
                text_color = (15, 10, 5)
            pygame.draw.rect(screen, fill_color, rect, border_radius=15)
            pygame.draw.rect(screen, border_color, rect, 3, border_radius=15)
            text_surface = button_font.render(label.title(), True, text_color)
            screen.blit(text_surface, (rect.centerx - text_surface.get_width()//2,
                                       rect.centery - text_surface.get_height()//2))

        # Add a remove-last-ingredient button below the mushroom button
        remove_button_rect = pygame.Rect(
            x_start + 7 * (button_width + button_spacing),
            y_start + button_height + button_spacing,
            button_width,
            button_height
        )
        pygame.draw.rect(screen, (200, 64, 64), remove_button_rect, border_radius=15)
        pygame.draw.rect(screen, (120, 30, 30), remove_button_rect, 3, border_radius=15)
        remove_text = button_font.render("Remove", True, WHITE)
        screen.blit(remove_text, (remove_button_rect.centerx - remove_text.get_width()//2,
                                  remove_button_rect.centery - remove_text.get_height()//2))

        # Draw the level countdown timer above the mushroom button
        if selected_level is not None and level_start_time > 0:
            elapsed = pygame.time.get_ticks() - level_start_time
            remaining_seconds = max(0, level_duration - elapsed // 1000)
            if remaining_seconds <= 0:
                level_failed = True

            timer_width = button_width
            timer_height = 56
            timer_rect = pygame.Rect(
                x_start + 7 * (button_width + button_spacing),
                y_start - timer_height - 15,
                timer_width,
                timer_height
            )
            pygame.draw.rect(screen, (210, 188, 138), timer_rect, border_radius=15)
            pygame.draw.rect(screen, (108, 74, 31), timer_rect, 3, border_radius=15)
            timer_text = button_font.render(f"Time: {remaining_seconds}s", True, BLACK)
            screen.blit(timer_text, (timer_rect.centerx - timer_text.get_width()//2,
                                     timer_rect.centery - timer_text.get_height()//2))

        # Create a pretty stack display at the top of buttons
        if ingredient_stack:
            # Format ingredients with proper capitalization
            formatted_ingredients = [ing.title() for ing in ingredient_stack[-8:]]
            stack_label = "Pizza Stack: " + " + ".join(formatted_ingredients)
        else:
            stack_label = "Pizza Stack: Empty"
        
        # Use smaller font for the stack text
        stack_text = button_font.render(stack_label, True, BLACK)
        stack_bg_width = stack_text.get_width() + 30
        stack_bg_height = stack_text.get_height() + 12
        stack_bg_x = WIDTH//2 - stack_bg_width//2
        stack_bg_y = y_start - stack_bg_height - 15  # Place above the ingredient buttons
        
        # Draw background box with rounded corners (smaller)
        stack_bg_rect = pygame.Rect(stack_bg_x, stack_bg_y, stack_bg_width, stack_bg_height)
        pygame.draw.rect(screen, (255, 248, 220), stack_bg_rect, border_radius=10)  # Cream background
        pygame.draw.rect(screen, (139, 69, 19), stack_bg_rect, 2, border_radius=10)  # Brown border
        
        # Center the text in the background box
        stack_rect = stack_text.get_rect(center=(stack_bg_rect.centerx, stack_bg_rect.centery))
        screen.blit(stack_text, stack_rect)

        # Draw return to levels button below remove button
        if selected_level is not None:
            return_button_rect = pygame.Rect(
                x_start + 7 * (button_width + button_spacing),
                y_start + button_height + button_spacing + button_height + button_spacing,
                button_width,
                button_height
            )
            if level_finished:
                pygame.draw.rect(screen, (64, 110, 150), return_button_rect, border_radius=15)
                pygame.draw.rect(screen, (28, 58, 100), return_button_rect, 3, border_radius=15)
                button_text = button_font.render("Back to Levels", True, WHITE)
            else:
                pygame.draw.rect(screen, (120, 120, 120), return_button_rect, border_radius=15)
                pygame.draw.rect(screen, (80, 80, 80), return_button_rect, 3, border_radius=15)
                button_text = button_font.render("Complete level", True, (220, 220, 220))
            screen.blit(button_text, (return_button_rect.centerx - button_text.get_width()//2,
                                      return_button_rect.centery - button_text.get_height()//2))

        if level_failed:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            warning_rect = pygame.Rect(WIDTH//2 - 360, HEIGHT//2 - 140, 720, 220)
            pygame.draw.rect(screen, (245, 245, 245), warning_rect, border_radius=24)
            pygame.draw.rect(screen, (100, 40, 20), warning_rect, 6, border_radius=24)

            warning_text = "Time's Up! Try Again"
            warning_surface = font.render(warning_text, True, (150, 20, 20))
            warning_rect_text = warning_surface.get_rect(center=(WIDTH//2, warning_rect.top + 70))
            screen.blit(warning_surface, warning_rect_text)

            detail_text = "Your pizza order failed. Return to level select."
            detail_surface = order_font.render(detail_text, True, BLACK)
            detail_rect = detail_surface.get_rect(center=(WIDTH//2, warning_rect.top + 120))
            screen.blit(detail_surface, detail_rect)

            back_button_size = (150, 100)
            back_button_rect = pygame.Rect(WIDTH//2 - back_button_size[0]//2, warning_rect.bottom + 20, back_button_size[0], back_button_size[1])
            back_btn_scaled = pygame.transform.scale(back_btn, back_button_size)
            screen.blit(back_btn_scaled, back_button_rect)

    elif state == "oven_screen":
        # Create darkened overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw oven window in center
        oven_width = 800
        oven_height = 600
        oven_x = (WIDTH - oven_width) // 2
        oven_y = (HEIGHT - oven_height) // 2
        
        # Determine which pizza base to use
        has_cheese = "cheese" in ingredient_stack
        pizza_bg = cheese_pizza_base if has_cheese else oven_bg
        pizza_scaled = pygame.transform.scale(pizza_bg, (oven_width, oven_height))
        screen.blit(pizza_scaled, (oven_x, oven_y))
        
        # Draw ingredients in a circle on the pizza (excluding cheese)
        non_cheese_ingredients = [ing for ing in ingredient_stack if ing != "cheese"]
        if non_cheese_ingredients:
            pizza_center_x = oven_x + oven_width // 2
            pizza_center_y = oven_y + oven_height // 2
            ingredient_size = 60
            
            # Add multiple visible copies per clicked ingredient
            display_ingredients = []
            for ingredient in set(non_cheese_ingredients):
                count = non_cheese_ingredients.count(ingredient)
                copies = min(count * 2, 6)
                display_ingredients.extend([ingredient] * copies)

            total_icons = len(display_ingredients)
            for idx, ingredient in enumerate(display_ingredients):
                if ingredient in ingredient_images:
                    # Calculate angle for circular placement
                    angle = (idx / total_icons) * 2 * math.pi if total_icons > 0 else 0
                    radius = 90 + ((idx * 37) % 70)
                    x = pizza_center_x + radius * math.sin(angle)
                    y = pizza_center_y - radius * math.cos(angle)
                    ingredient_img = pygame.transform.scale(ingredient_images[ingredient], (ingredient_size, ingredient_size))
                    screen.blit(ingredient_img, (x - ingredient_size // 2, y - ingredient_size // 2))

        # Draw order tab below the oven
        tab_height = 150
        tab_rect = pygame.Rect(oven_x, oven_y + oven_height, oven_width, tab_height)
        pygame.draw.rect(screen, (245, 245, 245), tab_rect, border_radius=20)
        pygame.draw.rect(screen, (120, 80, 40), tab_rect, 4, border_radius=20)

        current_customer_key = customer_queue[current_customer_index] if customer_queue else None
        current_customer_order_ingredients = customer_ingredient_map.get(current_level, {}).get(current_customer_key, [])
        order_items = [item.title() for item in current_customer_order_ingredients]

        # Wrap order text so it fits inside the order tab without overlapping the button
        max_order_width = oven_width - 240
        order_lines = []
        if order_items:
            current_line = "Order:"
            remaining = order_items.copy()
            while remaining and len(order_lines) < 3:
                ingredient = remaining.pop(0)
                token = (" + " if current_line != "Order:" else " ") + ingredient
                if button_font.size(current_line + token)[0] <= max_order_width:
                    current_line += token
                else:
                    order_lines.append(current_line)
                    current_line = "      " + ingredient
                if not remaining and current_line:
                    order_lines.append(current_line)
            if remaining:
                # append last line with ellipsis if there are more ingredients than fit
                while remaining and button_font.size(current_line + " + " + remaining[0] + " ...")[0] <= max_order_width:
                    current_line += " + " + remaining.pop(0)
                if remaining:
                    current_line = current_line.rstrip() + " ..."
                if len(order_lines) < 3:
                    order_lines.append(current_line)
            if not order_lines:
                order_lines.append(current_line)
            if len(order_lines) > 3:
                order_lines = order_lines[:3]
        else:
            order_lines = ["Order: None"]

        for idx, line in enumerate(order_lines):
            order_surface = button_font.render(line, True, BLACK)
            order_text_rect = order_surface.get_rect(topleft=(oven_x + 25, oven_y + oven_height + 18 + idx * (button_font.get_height() + 4)))
            screen.blit(order_surface, order_text_rect)

        customer_label = f"Customer {current_customer_index + 1}/{len(customer_queue)}"
        customer_surface = order_font.render(customer_label, True, (80, 80, 80))
        customer_rect = customer_surface.get_rect(topleft=(oven_x + 25, oven_y + oven_height + 18 + len(order_lines) * (button_font.get_height() + 4)))
        screen.blit(customer_surface, customer_rect)

        order_ready = is_order_complete(current_customer_order_ingredients)
        if order_ready:
            order_button_rect = pygame.Rect(oven_x + oven_width - 210, oven_y + oven_height - 140, 170, 60)
            pygame.draw.rect(screen, (76, 175, 80), order_button_rect, border_radius=18)
            pygame.draw.rect(screen, (56, 142, 60), order_button_rect, 4, border_radius=18)
            done_text = button_font.render("Order Done", True, WHITE)
            done_rect = done_text.get_rect(center=order_button_rect.center)
            screen.blit(done_text, done_rect)
        else:
            order_button_rect = None
            status_surface = order_font.render("Complete the requested order to finish.", True, (90, 90, 90))
            status_rect = status_surface.get_rect(topleft=(oven_x + 25, oven_y + oven_height + 18 + len(order_lines) * (button_font.get_height() + 4) + customer_surface.get_height() + 4))
            screen.blit(status_surface, status_rect)

        # Draw exit button in top right
        exit_scaled = pygame.transform.scale(exit_btn, (120, 80))
        oven_exit_rect = pygame.Rect(WIDTH - 140, 20, 120, 80)
        screen.blit(exit_scaled, oven_exit_rect)

    elif state == "customer_screen":
        exit_scaled = pygame.transform.scale(exit_btn, (120, 80))
        exit_rect = pygame.Rect(150, 20, 120, 80)
        screen.blit(exit_scaled, exit_rect)

        now = pygame.time.get_ticks()
        # Ensure list is not empty and index is within bounds
        if now - customer_timer > CUSTOMER_SCREEN_DURATION:
            if current_customer_index < len(customer_queue) - 1:
                current_customer_index += 1
                customer_timer = pygame.time.get_ticks()
            else:
                if selected_level is not None:
                    levels_completed = max(levels_completed, selected_level)
                current_customer_index = 0
                state = "kitchen_screen"
                level_start_time = pygame.time.get_ticks()
                level_failed = False
                customer_timer = now

    # Removed the old block that automatically advanced past the entire queue 
    pygame.display.update()
    clock.tick(60)