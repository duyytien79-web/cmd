import pygame
import sys
import os
import json
import random
from datetime import datetime

# =========================
# INIT
# =========================
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker - Final Project Edition")
CLOCK = pygame.time.Clock()
FPS = 60

# =========================
# SAFE FONT (fix lỗi ô vuông)
# =========================
def get_safe_font(size, bold=False):
    candidates = [
        "arial",
        "segoeui",
        "tahoma",
        "verdana",
        "calibri",
        "timesnewroman",
        "cambria"
    ]
    for name in candidates:
        try:
            font = pygame.font.SysFont(name, size, bold=bold)
            if font:
                return font
        except:
            pass
    return pygame.font.Font(None, size)

FONT_XL = get_safe_font(56, True)
FONT_L = get_safe_font(34, True)
FONT_M = get_safe_font(26, True)
FONT_S = get_safe_font(20, False)
FONT_XS = get_safe_font(16, False)

# =========================
# FONT RIÊNG CHO TIẾNG VIỆT (CHỈ DÙNG CHO HOW TO PLAY)
# =========================
def get_vietnamese_font(size, bold=False):
    font_candidates = []

    # Ưu tiên Tahoma vì hỗ trợ tiếng Việt rất ổn trên Windows
    if bold:
        font_candidates = [
            r"C:\Windows\Fonts\tahomabd.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\seguisb.ttf",   # Segoe UI Semibold (nếu có)
            r"C:\Windows\Fonts\segoeuib.ttf",  # Segoe UI Bold (nếu có)
            r"C:\Windows\Fonts\verdanab.ttf",
        ]
    else:
        font_candidates = [
            r"C:\Windows\Fonts\tahoma.ttf",
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\verdana.ttf",
        ]

    for path in font_candidates:
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except:
                pass

    # fallback cuối cùng
    return pygame.font.Font(None, size)

FONT_VN_TITLE = get_vietnamese_font(34, True)
FONT_VN_TEXT = get_vietnamese_font(20, False)

# =========================
# COLORS
# =========================
BG_TOP = (10, 16, 32)
BG_BOTTOM = (25, 45, 75)

WHITE = (245, 245, 245)
BLACK = (15, 15, 15)
GRAY = (120, 130, 150)
LIGHT_GRAY = (185, 195, 210)

CYAN = (0, 220, 255)
BLUE = (40, 110, 255)
DARK_BLUE = (25, 45, 85)
NAVY = (18, 28, 48)

GREEN = (40, 220, 120)
RED = (235, 70, 70)
ORANGE = (255, 145, 50)
YELLOW = (255, 220, 60)
PURPLE = (170, 90, 255)
PINK = (255, 100, 180)
GOLD = (255, 210, 70)

BRICK_COLORS = [
    (90, 200, 255),
    (255, 120, 120),
    (255, 180, 70),
    (130, 255, 130),
    (220, 140, 255),
    (255, 220, 100),
]

# =========================
# FILES
# =========================
SETTINGS_FILE = "brick_settings.json"
HISTORY_FILE = "brick_history.json"

# =========================
# GAME AREA
# =========================
PLAY_LEFT = 40
PLAY_RIGHT = WIDTH - 40
PLAY_TOP = 130
PLAY_BOTTOM = HEIGHT - 40
PLAY_WIDTH = PLAY_RIGHT - PLAY_LEFT
PLAY_HEIGHT = PLAY_BOTTOM - PLAY_TOP

# =========================
# SETTINGS / HISTORY
# =========================
default_settings = {
    "music_on": True,
    "sound_on": True,
    "ai_mode": False,
    "best_score": 0,
    "current_level": 1,
    "unlocked_level": 1,
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in default_settings.items():
                    if k not in data:
                        data[k] = v
                return data
        except:
            return default_settings.copy()
    return default_settings.copy()

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-20:], f, indent=2, ensure_ascii=False)

settings = load_settings()
history_data = load_history()

# =========================
# LEVELS (10 LEVELS)
# 0 = empty
# 1 = normal brick
# 2 = strong brick (2 hits)
# 3 = unbreakable block
# =========================
LEVELS = [
    [
        "000111111000",
        "001111111100",
        "011111111110",
        "001111111100",
    ],
    [
        "001111111100",
        "011122221110",
        "111111111111",
        "001111111100",
    ],
    [
        "011111111110",
        "112222222211",
        "111111111111",
        "011100001110",
        "001111111100",
    ],
    [
        "111111111111",
        "100000000001",
        "122222222221",
        "111111111111",
        "011111111110",
    ],
    [
        "111111111111",
        "122222222221",
        "122000000221",
        "123222222221",
        "111111111311",
    ],
    [
        "111111111111",
        "211111111112",
        "221122221122",
        "111200002111",
        "222111111222",
        "111111111111",
    ],
    [
        "111122221111",
        "122211112221",
        "221100001122",
        "111233332111",
        "122211112221",
        "111122221111",
    ],
    [
        "222222222222",
        "211111111112",
        "213333333312",
        "213111111312",
        "213100001312",
        "213333333312",
        "211111111112",
    ],
    [
        "222222222222",
        "232332233232",
        "221111111122",
        "231222222132",
        "221211112122",
        "231222222132",
        "221111111122",
        "232332233232",
    ],
    [
        "222222222222",
        "223333333322",
        "231222222132",
        "231211112132",
        "231213312132",
        "231211112132",
        "231222222132",
        "233333333332",
        "222222222222",
    ],
]

# =========================
# LEVEL SPEED CONFIG
# =========================
LEVEL_CONFIG = {
    1: {"speed_x": 4.0, "speed_y": -5.0, "paddle_w": 150},
    2: {"speed_x": 4.5, "speed_y": -5.5, "paddle_w": 145},
    3: {"speed_x": 5.0, "speed_y": -5.8, "paddle_w": 140},
    4: {"speed_x": 5.4, "speed_y": -6.1, "paddle_w": 135},
    5: {"speed_x": 5.8, "speed_y": -6.4, "paddle_w": 130},
    6: {"speed_x": 6.2, "speed_y": -6.8, "paddle_w": 125},
    7: {"speed_x": 6.8, "speed_y": -7.2, "paddle_w": 120},
    8: {"speed_x": 7.4, "speed_y": -7.8, "paddle_w": 115},
    9: {"speed_x": 8.0, "speed_y": -8.4, "paddle_w": 110},
    10: {"speed_x": 8.6, "speed_y": -9.0, "paddle_w": 105},
}

# =========================
# UTIL DRAW
# =========================
def draw_gradient_background():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        pygame.draw.line(SCREEN, (r, g, b), (0, y), (WIDTH, y))

def draw_panel(rect, color=(18, 28, 48), border=CYAN, radius=18):
    pygame.draw.rect(SCREEN, color, rect, border_radius=radius)
    pygame.draw.rect(SCREEN, border, rect, 2, border_radius=radius)

def draw_text(text, font, color, x, y, center=False):
    surf = font.render(str(text), True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    SCREEN.blit(surf, rect)

def draw_button(rect, text, color, text_color=WHITE, hovered=False):
    fill = (
        min(255, color[0] + 25),
        min(255, color[1] + 25),
        min(255, color[2] + 25),
    ) if hovered else color

    pygame.draw.rect(SCREEN, fill, rect, border_radius=14)
    pygame.draw.rect(SCREEN, WHITE, rect, 2, border_radius=14)
    draw_text(text, FONT_M, text_color, rect.centerx, rect.centery, center=True)

# =========================
# SOUND (Tạo âm thanh đơn giản bằng frequency)
# =========================
def play_sound(name="hit"):
    if not settings["sound_on"]:
        return
    try:
        # Tạo âm thanh đơn giản
        freq_map = {
            "paddle": 880,   # La (A)
            "brick": 1050,   # Do (C)
            "wall": 700,     # Sol (G)
            "hit": 1200,     # Đô cao
            "powerup": 1320, # Mi (E)
        }
        
        freq = freq_map.get(name, 880)
        duration_ms = 100
        sample_rate = 22050
        duration_samples = int(sample_rate * duration_ms / 1000)
        
        # Tạo waveform đơn giản (sin wave)
        import math
        frames = []
        for i in range(duration_samples):
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * freq * i / sample_rate))
            sample = max(-32768, min(32767, sample))
            frames.append(sample.to_bytes(2, 'little', signed=True))
        
        sound_data = b''.join(frames)
        sound = pygame.mixer.Sound(buffer=sound_data)
        sound.set_volume(0.3)
        sound.play()
    except Exception as e:
        # Im lặng nếu có lỗi
        pass

# =========================
# GAME OBJECTS
# =========================
class Brick:
    def __init__(self, x, y, w, h, hp=1, unbreakable=False, color_idx=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.hp = hp
        self.max_hp = hp
        self.unbreakable = unbreakable
        self.color_idx = color_idx

    def draw(self):
        if self.hp <= 0:
            return

        if self.unbreakable:
            base = (70, 80, 95)
            glow = (140, 150, 170)
        else:
            base = BRICK_COLORS[self.color_idx % len(BRICK_COLORS)]
            glow = (
                min(255, base[0] + 35),
                min(255, base[1] + 35),
                min(255, base[2] + 35),
            )

        pygame.draw.rect(SCREEN, base, self.rect, border_radius=6)
        pygame.draw.rect(SCREEN, glow, self.rect, 2, border_radius=6)

        inner = self.rect.inflate(-8, -8)
        if inner.width > 0 and inner.height > 0:
            pygame.draw.rect(SCREEN, WHITE, inner, 1, border_radius=4)

        if not self.unbreakable and self.max_hp > 1:
            bar_w = self.rect.width - 8
            bar_x = self.rect.x + 4
            bar_y = self.rect.y + self.rect.height - 7
            pygame.draw.rect(SCREEN, (30, 30, 30), (bar_x, bar_y, bar_w, 4), border_radius=2)
            fill = int(bar_w * (self.hp / self.max_hp))
            pygame.draw.rect(SCREEN, GREEN, (bar_x, bar_y, fill, 4), border_radius=2)

class Ball:
    def __init__(self, x, y, vx, vy, radius=9):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.stuck = True

    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def draw(self):
        pygame.draw.circle(SCREEN, WHITE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(SCREEN, CYAN, (int(self.x), int(self.y)), self.radius, 2)

class PowerUp:
    def __init__(self, x, y, kind):
        self.kind = kind
        self.rect = pygame.Rect(x, y, 28, 28)
        self.speed = 3.0

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        color_map = {
            "expand": GREEN,
            "slow": CYAN,
            "life": RED,
            "multi": YELLOW,
        }
        label_map = {
            "expand": "E",
            "slow": "S",
            "life": "L",
            "multi": "M",
        }

        color = color_map.get(self.kind, WHITE)
        label = label_map.get(self.kind, "?")

        pygame.draw.rect(SCREEN, color, self.rect, border_radius=8)
        pygame.draw.rect(SCREEN, WHITE, self.rect, 2, border_radius=8)
        draw_text(label, FONT_XS, BLACK, self.rect.centerx, self.rect.centery, center=True)

# =========================
# GAME STATE
# =========================
MENU = "menu"
LEVEL_SELECT = "level_select"
SETTINGS = "settings"
HOW_TO_PLAY = "how_to_play"
HISTORY = "history"
PLAYING = "playing"
PAUSED = "paused"
LEVEL_CLEAR = "level_clear"
GAME_OVER = "game_over"
FINAL_WIN = "final_win"

game_state = MENU

# =========================
# GAMEPLAY VARS
# =========================
paddle = pygame.Rect(WIDTH // 2 - 70, PLAY_BOTTOM - 18, 140, 14)
paddle_speed = 8

balls = []
bricks = []
powerups = []

score = 0
combo = 0
lives = 3
selected_level = 1

powerup_message = ""
powerup_message_timer = 0

# =========================
# COUNTDOWN SYSTEM (NEW)
# =========================
countdown_active = False
countdown_start_time = 0
countdown_duration = 5000  # 5 giây

def start_countdown():
    global countdown_active, countdown_start_time
    countdown_active = True
    countdown_start_time = pygame.time.get_ticks()

def get_countdown_seconds_left():
    if not countdown_active:
        return 0
    elapsed = pygame.time.get_ticks() - countdown_start_time
    remain_ms = max(0, countdown_duration - elapsed)
    return (remain_ms + 999) // 1000

def update_countdown():
    global countdown_active
    if countdown_active:
        elapsed = pygame.time.get_ticks() - countdown_start_time
        if elapsed >= countdown_duration:
            countdown_active = False
            for ball in balls:
                ball.stuck = False

# =========================
# AI SMOOTH VARS (NEW)
# =========================
ai_target_x = WIDTH // 2
AI_SMOOTH_FACTOR = 0.25
AI_DEAD_ZONE = 6
AI_MAX_SPEED_FACTOR = 1.4
AI_MISS_CHANCE = 0.12  # Cơ hội bỏ rơi (12%)
AI_MISS_DISTANCE = 80  # Bỏ rơi với độ lệch này

# =========================
# LEVEL BUILD
# =========================
def build_level(level_num):
    global bricks, balls, paddle, powerups, combo
    global powerup_message, powerup_message_timer, ai_target_x

    pattern = LEVELS[level_num - 1]
    cols = len(pattern[0])

    top_margin = PLAY_TOP + 18
    side_margin = 18
    gap = 6

    brick_w = (PLAY_WIDTH - side_margin * 2 - gap * (cols - 1)) // cols
    brick_h = 28

    bricks = []

    for r, row in enumerate(pattern):
        for c, ch in enumerate(row):
            x = PLAY_LEFT + side_margin + c * (brick_w + gap)
            y = top_margin + r * (brick_h + gap)

            if ch == "0":
                continue
            elif ch == "1":
                bricks.append(Brick(x, y, brick_w, brick_h, hp=1, unbreakable=False, color_idx=(r + c) % 6))
            elif ch == "2":
                bricks.append(Brick(x, y, brick_w, brick_h, hp=2, unbreakable=False, color_idx=(r + c + 1) % 6))
            elif ch == "3":
                bricks.append(Brick(x, y, brick_w, brick_h, hp=9999, unbreakable=True, color_idx=0))

    cfg = LEVEL_CONFIG[level_num]

    paddle.width = cfg["paddle_w"]
    paddle.height = 14
    paddle.centerx = WIDTH // 2
    paddle.y = PLAY_BOTTOM - 18

    balls = [Ball(paddle.centerx, paddle.top - 10, cfg["speed_x"], cfg["speed_y"])]
    powerups = []
    combo = 0
    powerup_message = ""
    powerup_message_timer = 0

    ai_target_x = paddle.centerx
    start_countdown()

# =========================
# RESET GAME
# =========================
def start_new_game(level_num):
    global selected_level, score, lives, combo, game_state
    selected_level = level_num
    settings["current_level"] = level_num
    save_settings(settings)

    score = 0
    lives = 3
    combo = 0
    build_level(level_num)
    game_state = PLAYING

def start_level_only(level_num):
    global selected_level, combo, lives, game_state
    selected_level = level_num
    settings["current_level"] = level_num
    save_settings(settings)

    combo = 0
    lives = 3
    build_level(level_num)
    game_state = PLAYING

# =========================
# POWERUP
# =========================
def maybe_spawn_powerup(x, y):
    if random.random() < 0.25:
        kind = random.choice(["expand", "slow", "life", "multi"])
        powerups.append(PowerUp(x, y, kind))

def apply_powerup(kind):
    global lives, powerup_message, powerup_message_timer

    if kind == "expand":
        paddle.width = min(220, paddle.width + 35)
        powerup_message = "EXPAND PADDLE ACTIVATED"
    elif kind == "slow":
        for b in balls:
            b.vx *= 0.88
            b.vy *= 0.88
        powerup_message = "SLOW BALL ACTIVATED"
    elif kind == "life":
        lives = min(9, lives + 1)
        powerup_message = "EXTRA LIFE +1"
    elif kind == "multi":
        if balls:
            base = balls[0]
            new1 = Ball(base.x, base.y, -abs(base.vx) if base.vx != 0 else -4, base.vy)
            new2 = Ball(base.x, base.y, abs(base.vx) if base.vx != 0 else 4, base.vy)
            new1.stuck = False
            new2.stuck = False
            balls.append(new1)
            balls.append(new2)
        powerup_message = "MULTI BALL ACTIVATED"

    powerup_message_timer = 120
    play_sound("powerup")

# =========================
# HELPERS
# =========================
def remaining_breakable_bricks():
    return [b for b in bricks if not b.unbreakable and b.hp > 0]

def all_breakable_bricks_cleared():
    return len(remaining_breakable_bricks()) == 0

def record_history(result):
    global history_data
    entry = {
        "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "level": selected_level,
        "score": score,
        "result": result,
        "ai_mode": "ON" if settings["ai_mode"] else "OFF"
    }
    history_data.append(entry)
    save_history(history_data)

# =========================
# AI LOGIC (FIX MƯỢT, KHÔNG RUNG)
# =========================
def predict_ball_landing_x(ball):
    if ball.vy <= 0:
        return ball.x

    test_x = ball.x
    test_y = ball.y
    vx = ball.vx
    vy = ball.vy

    for _ in range(260):
        test_x += vx
        test_y += vy

        if test_x - ball.radius <= PLAY_LEFT:
            test_x = PLAY_LEFT + ball.radius
            vx *= -1
        elif test_x + ball.radius >= PLAY_RIGHT:
            test_x = PLAY_RIGHT - ball.radius
            vx *= -1

        if test_y + ball.radius >= paddle.top:
            return test_x

    return ball.x

def update_ai_paddle():
    global ai_target_x

    if not balls:
        return

    # Ưu tiên bóng trước
    descending = [b for b in balls if b.vy > 0]
    if descending:
        target_ball = max(descending, key=lambda b: b.y)
        landing_x = predict_ball_landing_x(target_ball)
        ball_urgent = target_ball.y > PLAY_TOP + PLAY_HEIGHT * 0.65  # Bóng sắp rơi
    else:
        target_ball = max(balls, key=lambda b: b.y)
        landing_x = target_ball.x
        ball_urgent = False

    desired_target = landing_x

    # Thỉnh thoảng AI bỏ rơi cố tình (chỉ khi bóng không urgent)
    if not ball_urgent and random.random() < AI_MISS_CHANCE:
        miss_offset = random.randint(-AI_MISS_DISTANCE, AI_MISS_DISTANCE)
        desired_target = landing_x + miss_offset
    else:
        # Chỉ ăn vật phẩm khi bóng đã an toàn (gần target hoặc không urgent)
        if not ball_urgent or abs(landing_x - paddle.centerx) < 100:
            candidate_powerups = [p for p in powerups if p.rect.y > PLAY_TOP + PLAY_HEIGHT * 0.30]
            if candidate_powerups:
                nearest = min(candidate_powerups, key=lambda p: abs(paddle.centerx - p.rect.centerx))
                powerup_distance = abs(nearest.rect.centerx - paddle.centerx)
                ball_distance = abs(landing_x - paddle.centerx)
                
                # Ăn vật phẩm chỉ nếu nó gần hơn bóng hoặc bóng đã khá gần
                if powerup_distance < 150 and powerup_distance < ball_distance * 0.8:
                    desired_target = nearest.rect.centerx + random.randint(-30, 30)

        # Error nhỏ để AI chơi tự nhiên
        error_range = max(6, 14 - selected_level)
        desired_target += random.randint(-error_range, error_range)

    # Giới hạn target trong play area
    desired_target = max(PLAY_LEFT + paddle.width // 2, min(PLAY_RIGHT - paddle.width // 2, desired_target))
    
    ai_target_x += (desired_target - ai_target_x) * AI_SMOOTH_FACTOR

    diff = ai_target_x - paddle.centerx
    max_ai_speed = paddle_speed * AI_MAX_SPEED_FACTOR

    # Di chuyển nhanh hơn nếu bóng urgent
    speed_multiplier = 1.65 if ball_urgent else 1.0
    
    if abs(diff) > AI_DEAD_ZONE:
        move = max(-max_ai_speed * speed_multiplier, min(max_ai_speed * speed_multiplier, diff * 0.40))
        paddle.centerx += int(move)
    elif abs(diff) > 0:
        paddle.centerx += int(diff * 0.22)

    if paddle.left < PLAY_LEFT:
        paddle.left = PLAY_LEFT
    if paddle.right > PLAY_RIGHT:
        paddle.right = PLAY_RIGHT

# =========================
# COLLISION HELPERS (FIX XUYÊN / DÍNH)
# =========================
def clamp_ball_speed(ball):
    if abs(ball.vx) < 2:
        ball.vx = 2 if ball.vx >= 0 else -2
    if abs(ball.vy) < 2:
        ball.vy = 2 if ball.vy >= 0 else -2

    max_speed = 11.5
    if ball.vx > max_speed:
        ball.vx = max_speed
    if ball.vx < -max_speed:
        ball.vx = -max_speed
    if ball.vy > max_speed:
        ball.vy = max_speed
    if ball.vy < -max_speed:
        ball.vy = -max_speed

def separate_ball_from_rect(ball, rect):
    ball_rect = ball.rect()

    overlap_left = ball_rect.right - rect.left
    overlap_right = rect.right - ball_rect.left
    overlap_top = ball_rect.bottom - rect.top
    overlap_bottom = rect.bottom - ball_rect.top

    overlaps = [overlap_left, overlap_right, overlap_top, overlap_bottom]
    min_overlap = min(overlaps)

    if min_overlap == overlap_left:
        ball.x = rect.left - ball.radius - 1
        ball.vx = -abs(ball.vx)
        return "x"
    elif min_overlap == overlap_right:
        ball.x = rect.right + ball.radius + 1
        ball.vx = abs(ball.vx)
        return "x"
    elif min_overlap == overlap_top:
        ball.y = rect.top - ball.radius - 1
        ball.vy = -abs(ball.vy)
        return "y"
    else:
        ball.y = rect.bottom + ball.radius + 1
        ball.vy = abs(ball.vy)
        return "y"

# =========================
# BALL COLLISION
# =========================
def resolve_ball_collisions(ball):
    global score, combo

    if ball.x - ball.radius <= PLAY_LEFT:
        ball.x = PLAY_LEFT + ball.radius + 1
        ball.vx = abs(ball.vx)
        play_sound("wall")
    elif ball.x + ball.radius >= PLAY_RIGHT:
        ball.x = PLAY_RIGHT - ball.radius - 1
        ball.vx = -abs(ball.vx)
        play_sound("wall")

    if ball.y - ball.radius <= PLAY_TOP:
        ball.y = PLAY_TOP + ball.radius + 1
        ball.vy = abs(ball.vy)
        play_sound("wall")

    if ball.rect().colliderect(paddle) and ball.vy > 0:
        ball.y = paddle.top - ball.radius - 1

        offset = (ball.x - paddle.centerx) / max(1, (paddle.width / 2))
        ball.vx = offset * 6.8

        if abs(ball.vx) < 2.2:
            ball.vx = 2.2 if ball.vx >= 0 else -2.2

        speed_bonus = min(1.2, selected_level * 0.06)
        ball.vy = -(abs(ball.vy) + speed_bonus)

        combo = 0
        clamp_ball_speed(ball)
        play_sound("paddle")

    for brick in bricks:
        if brick.hp <= 0:
            continue

        if ball.rect().colliderect(brick.rect):
            separate_ball_from_rect(ball, brick.rect)

            if brick.unbreakable:
                clamp_ball_speed(ball)
                play_sound("hit")
                break

            brick.hp -= 1

            if brick.hp <= 0:
                combo += 1
                gained = 10 + combo * 2
                score += gained
                maybe_spawn_powerup(brick.rect.centerx - 14, brick.rect.centery - 14)
            else:
                score += 5

            clamp_ball_speed(ball)
            play_sound("brick")
            break

# =========================
# GAME UPDATE
# =========================
def update_game():
    global lives, game_state, powerup_message_timer, ai_target_x

    keys = pygame.key.get_pressed()

    update_countdown()

    # --- Paddle control ---
    if settings["ai_mode"] and not countdown_active:
        update_ai_paddle()
    else:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            paddle.x += paddle_speed

        if paddle.left < PLAY_LEFT:
            paddle.left = PLAY_LEFT
        if paddle.right > PLAY_RIGHT:
            paddle.right = PLAY_RIGHT

    # --- Ball stuck on paddle ---
    for ball in balls:
        if ball.stuck:
            ball.x = paddle.centerx
            ball.y = paddle.top - ball.radius - 1

    # --- Move balls with sub-step to reduce tunneling ---
    remove_balls = []

    for ball in balls:
        if not ball.stuck:
            clamp_ball_speed(ball)

            steps = max(1, int(max(abs(ball.vx), abs(ball.vy)) // 3))
            step_vx = ball.vx / steps
            step_vy = ball.vy / steps

            for _ in range(steps):
                ball.x += step_vx
                ball.y += step_vy

                resolve_ball_collisions(ball)

                if ball.y - ball.radius > PLAY_BOTTOM:
                    remove_balls.append(ball)
                    break

    # --- Remove lost balls ---
    for b in remove_balls:
        if b in balls:
            balls.remove(b)

    # --- If all balls lost -> lose 1 life ---
    if len(balls) == 0:
        lives -= 1
        if lives < 0:
            lives = 0

        if lives > 0:
            cfg = LEVEL_CONFIG[selected_level]
            vx = cfg["speed_x"] * random.choice([-1, 1])
            vy = cfg["speed_y"]

            paddle.centerx = WIDTH // 2
            if paddle.left < PLAY_LEFT:
                paddle.left = PLAY_LEFT
            if paddle.right > PLAY_RIGHT:
                paddle.right = PLAY_RIGHT

            new_ball = Ball(paddle.centerx, paddle.top - 10, vx, vy)
            balls.append(new_ball)

            ai_target_x = paddle.centerx
            start_countdown()
        else:
            record_history("Game Over")

            if score > settings["best_score"]:
                settings["best_score"] = score
                save_settings(settings)

            game_state = GAME_OVER
            return

    # --- Powerups ---
    for p in powerups[:]:
        p.update()
        if p.rect.colliderect(paddle):
            apply_powerup(p.kind)
            powerups.remove(p)
        elif p.rect.top > PLAY_BOTTOM:
            powerups.remove(p)

    # --- Powerup message timer ---
    if powerup_message_timer > 0:
        powerup_message_timer -= 1

    # --- Level clear ---
    if all_breakable_bricks_cleared():
        if selected_level < 10:
            settings["unlocked_level"] = max(settings["unlocked_level"], selected_level + 1)

        save_settings(settings)

        if score > settings["best_score"]:
            settings["best_score"] = score
            save_settings(settings)

        record_history("Level Clear")

        if selected_level >= 10:
            game_state = FINAL_WIN
        else:
            game_state = LEVEL_CLEAR

# =========================
# DRAW GAME
# =========================
def draw_game_frame():
    outer = pygame.Rect(PLAY_LEFT, PLAY_TOP, PLAY_WIDTH, PLAY_HEIGHT)
    pygame.draw.rect(SCREEN, (15, 25, 45), outer, border_radius=12)
    pygame.draw.rect(SCREEN, CYAN, outer, 3, border_radius=12)

def draw_hud():
    hud_y = 92
    draw_text(f"Score: {score}", FONT_S, WHITE, 35, hud_y)
    draw_text(f"Best Score: {settings['best_score']}", FONT_S, GOLD, 180, hud_y)
    draw_text(f"Lives: {max(0, lives)}", FONT_S, WHITE, 405, hud_y)
    draw_text(f"Level: {selected_level}/10", FONT_S, WHITE, 525, hud_y)
    draw_text(f"Combo: x{combo}", FONT_S, YELLOW, 650, hud_y)

    ai_text = "AI: ON" if settings["ai_mode"] else "AI: OFF"
    ai_color = GREEN if settings["ai_mode"] else RED
    draw_text(ai_text, FONT_S, ai_color, 790, hud_y)

    pause_btn = pygame.Rect(WIDTH - 150, 14, 110, 42)
    hovered = pause_btn.collidepoint(pygame.mouse.get_pos())
    draw_button(pause_btn, "PAUSE", PURPLE, hovered=hovered)
    return pause_btn

def draw_game():
    draw_gradient_background()
    draw_hud()
    draw_game_frame()

    draw_text(
        "LEFT/RIGHT or A/D = Move Paddle | ESC = Pause",
        FONT_XS,
        LIGHT_GRAY,
        PLAY_LEFT + 10,
        PLAY_TOP + PLAY_HEIGHT + 8
    )

    for brick in bricks:
        if brick.hp > 0:
            brick.draw()

    pygame.draw.rect(SCREEN, BLUE, paddle, border_radius=8)
    pygame.draw.rect(SCREEN, WHITE, paddle, 2, border_radius=8)

    for ball in balls:
        ball.draw()

    for p in powerups:
        p.draw()

    if powerup_message_timer > 0:
        msg_rect = pygame.Rect(WIDTH // 2 - 180, 60, 360, 34)
        draw_panel(msg_rect, (25, 50, 80), YELLOW, 12)
        draw_text(powerup_message, FONT_XS, YELLOW, msg_rect.centerx, msg_rect.centery, center=True)

    if countdown_active:
        remain = get_countdown_seconds_left()

        overlay = pygame.Surface((360, 70), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 145))
        SCREEN.blit(overlay, (WIDTH // 2 - 180, HEIGHT // 2 - 35))

        draw_text(f"Starting in {remain}", FONT_L, WHITE, WIDTH // 2, HEIGHT // 2, center=True)

# =========================
# SCREENS
# =========================
def draw_menu():
    draw_gradient_background()

    title_panel = pygame.Rect(170, 60, 660, 180)
    draw_panel(title_panel, NAVY, CYAN, 24)

    draw_text("BRICK BREAKER", FONT_XL, WHITE, WIDTH // 2, 120, center=True)
    draw_text("Game Project Presentation", FONT_S, WHITE, WIDTH // 2, 175, center=True)
    draw_text("Classic Arcade Game with 10 Unlockable Levels", FONT_XS, LIGHT_GRAY, WIDTH // 2, 205, center=True)

    buttons = [
        ("PLAY", pygame.Rect(350, 275, 300, 55), GREEN),
        ("SETTINGS", pygame.Rect(350, 345, 300, 55), BLUE),
        ("HOW TO PLAY", pygame.Rect(350, 415, 300, 55), ORANGE),
        ("HISTORY", pygame.Rect(350, 485, 300, 55), PURPLE),
        ("EXIT", pygame.Rect(350, 555, 300, 55), RED),
    ]

    for text, rect, color in buttons:
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        draw_button(rect, text, color, hovered=hovered)

    return buttons

def draw_level_select():
    draw_gradient_background()

    panel = pygame.Rect(110, 70, 780, 520)
    draw_panel(panel, NAVY, CYAN, 20)

    draw_text("SELECT LEVEL", FONT_L, WHITE, WIDTH // 2, 110, center=True)
    draw_text(f"Unlocked Level: {settings['unlocked_level']}/10", FONT_S, GOLD, WIDTH // 2, 145, center=True)

    btn_w = 120
    btn_h = 80
    gap_x = 28
    gap_y = 35
    cols = 5

    total_w = cols * btn_w + (cols - 1) * gap_x
    start_x = (WIDTH - total_w) // 2
    start_y = 190

    level_buttons = []
    for i in range(10):
        level = i + 1
        row = i // 5
        col = i % 5
        x = start_x + col * (btn_w + gap_x)
        y = start_y + row * (btn_h + gap_y)

        rect = pygame.Rect(x, y, btn_w, btn_h)
        unlocked = level <= settings["unlocked_level"]

        if unlocked:
            color = GREEN if level == settings["current_level"] else BLUE
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            draw_button(rect, f"LEVEL {level}", color, hovered=hovered)
        else:
            pygame.draw.rect(SCREEN, (70, 70, 80), rect, border_radius=14)
            pygame.draw.rect(SCREEN, GRAY, rect, 2, border_radius=14)
            draw_text(f"LOCKED {level}", FONT_S, LIGHT_GRAY, rect.centerx, rect.centery, center=True)

        level_buttons.append((level, rect, unlocked))

    back_btn = pygame.Rect(WIDTH // 2 - 110, 510, 220, 50)
    hovered = back_btn.collidepoint(pygame.mouse.get_pos())
    draw_button(back_btn, "BACK", RED, hovered=hovered)

    return level_buttons, back_btn

def draw_settings():
    draw_gradient_background()

    panel = pygame.Rect(200, 70, 600, 560)
    draw_panel(panel, NAVY, CYAN, 20)

    draw_text("SETTINGS", FONT_L, WHITE, WIDTH // 2, 110, center=True)

    draw_text("Music", FONT_M, WHITE, 290, 180)
    music_on_btn = pygame.Rect(460, 160, 100, 45)
    music_off_btn = pygame.Rect(580, 160, 100, 45)

    draw_button(
        music_on_btn,
        "ON",
        GREEN if settings["music_on"] else GRAY,
        hovered=music_on_btn.collidepoint(pygame.mouse.get_pos())
    )
    draw_button(
        music_off_btn,
        "OFF",
        RED if not settings["music_on"] else GRAY,
        hovered=music_off_btn.collidepoint(pygame.mouse.get_pos())
    )

    draw_text("Sound", FONT_M, WHITE, 290, 255)
    sound_on_btn = pygame.Rect(460, 235, 100, 45)
    sound_off_btn = pygame.Rect(580, 235, 100, 45)

    draw_button(
        sound_on_btn,
        "ON",
        GREEN if settings["sound_on"] else GRAY,
        hovered=sound_on_btn.collidepoint(pygame.mouse.get_pos())
    )
    draw_button(
        sound_off_btn,
        "OFF",
        RED if not settings["sound_on"] else GRAY,
        hovered=sound_off_btn.collidepoint(pygame.mouse.get_pos())
    )

    draw_text("AI Mode", FONT_M, WHITE, 290, 330)
    ai_on_btn = pygame.Rect(460, 310, 100, 45)
    ai_off_btn = pygame.Rect(580, 310, 100, 45)

    draw_button(
        ai_on_btn,
        "ON",
        GREEN if settings["ai_mode"] else GRAY,
        hovered=ai_on_btn.collidepoint(pygame.mouse.get_pos())
    )
    draw_button(
        ai_off_btn,
        "OFF",
        RED if not settings["ai_mode"] else GRAY,
        hovered=ai_off_btn.collidepoint(pygame.mouse.get_pos())
    )

    reset_btn = pygame.Rect(300, 410, 400, 55)
    draw_button(
        reset_btn,
        "RESET LEVEL PROGRESS",
        ORANGE,
        hovered=reset_btn.collidepoint(pygame.mouse.get_pos())
    )

    back_btn = pygame.Rect(WIDTH // 2 - 110, 520, 220, 50)
    draw_button(back_btn, "BACK", RED, hovered=back_btn.collidepoint(pygame.mouse.get_pos()))

    return {
        "music_on": music_on_btn,
        "music_off": music_off_btn,
        "sound_on": sound_on_btn,
        "sound_off": sound_off_btn,
        "ai_on": ai_on_btn,
        "ai_off": ai_off_btn,
        "reset": reset_btn,
        "back": back_btn
    }

def draw_how_to_play():
    draw_gradient_background()

    panel = pygame.Rect(90, 60, 820, 560)
    draw_panel(panel, NAVY, CYAN, 20)

    # Dùng font tiếng Việt riêng để tránh lỗi dấu
    draw_text("CÁCH CHƠI", FONT_VN_TITLE, WHITE, WIDTH // 2, 100, center=True)

    lines = [
        "1. Dùng phím MŨI TÊN TRÁI/PHẢI hoặc A/D để di chuyển thanh đỡ.",
        "2. Mỗi màn chơi sẽ tự động bắt đầu sau khi đếm ngược 5 giây.",
        "3. Phá hết các viên gạch có thể phá để hoàn thành màn chơi.",
        "4. Gạch cứng cần 2 lần chạm để phá. Gạch xám không thể phá hủy.",
        "5. Vật phẩm hỗ trợ:",
        "   E = Mở rộng thanh đỡ | S = Làm chậm bóng",
        "   L = Thêm 1 mạng       | M = Kích hoạt nhiều bóng",
        "6. Bạn có 3 mạng. Nếu tất cả bóng rơi xuống, bạn sẽ mất 1 mạng.",
        "7. Chế độ AI có thể tự động điều khiển thanh đỡ và nhặt vật phẩm.",
        "8. Các level mở khóa lần lượt. Hoàn thành level hiện tại để mở level tiếp theo.",
        "9. Bạn có thể chọn bất kỳ level nào đã mở khóa trong menu CHƠI.",
        "10. Dùng chức năng TẠM DỪNG khi đang chơi để dừng hoặc tiếp tục.",
    ]

    y = 145
    for line in lines:
        draw_text(line, FONT_VN_TEXT, WHITE, 125, y)
        y += 36

    back_btn = pygame.Rect(WIDTH // 2 - 110, 555, 220, 45)

    # Vẽ nút giống style cũ nhưng dùng font tiếng Việt riêng
    hovered = back_btn.collidepoint(pygame.mouse.get_pos())
    btn_color = (255, 90, 90) if hovered else RED

    pygame.draw.rect(SCREEN, WHITE, back_btn, border_radius=14)
    inner_rect = back_btn.inflate(-4, -4)
    pygame.draw.rect(SCREEN, btn_color, inner_rect, border_radius=12)

    # Dùng font tiếng Việt để chữ không lỗi dấu
    draw_text("QUAY LẠI", FONT_VN_TEXT, WHITE, back_btn.centerx, back_btn.centery - 2, center=True)

    return back_btn

def draw_history():
    draw_gradient_background()

    panel = pygame.Rect(80, 55, 840, 590)
    draw_panel(panel, NAVY, CYAN, 20)

    draw_text("PLAY HISTORY", FONT_L, WHITE, WIDTH // 2, 95, center=True)

    header_y = 145
    draw_text("Time", FONT_S, GOLD, 110, header_y)
    draw_text("Level", FONT_S, GOLD, 390, header_y)
    draw_text("Score", FONT_S, GOLD, 490, header_y)
    draw_text("Result", FONT_S, GOLD, 610, header_y)
    draw_text("AI", FONT_S, GOLD, 770, header_y)

    y = 180
    recent = history_data[-10:][::-1]
    if not recent:
        draw_text("No history yet. Play some levels first!", FONT_M, LIGHT_GRAY, WIDTH // 2, 330, center=True)
    else:
        for item in recent:
            draw_text(item.get("time", ""), FONT_XS, WHITE, 110, y)
            draw_text(item.get("level", ""), FONT_XS, WHITE, 395, y)
            draw_text(item.get("score", ""), FONT_XS, WHITE, 495, y)
            draw_text(item.get("result", ""), FONT_XS, WHITE, 610, y)
            ai_col = GREEN if item.get("ai_mode", "OFF") == "ON" else RED
            draw_text(item.get("ai_mode", ""), FONT_XS, ai_col, 775, y)
            y += 38

    back_btn = pygame.Rect(WIDTH // 2 - 110, 585, 220, 40)
    draw_button(back_btn, "BACK", RED, hovered=back_btn.collidepoint(pygame.mouse.get_pos()))
    return back_btn

def draw_pause_screen():
    draw_game()

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    SCREEN.blit(overlay, (0, 0))

    panel = pygame.Rect(290, 220, 420, 220)
    draw_panel(panel, NAVY, CYAN, 20)

    draw_text("GAME PAUSED", FONT_L, WHITE, WIDTH // 2, 270, center=True)

    resume_btn = pygame.Rect(390, 320, 220, 50)
    menu_btn = pygame.Rect(390, 385, 220, 50)

    draw_button(resume_btn, "RESUME", GREEN, hovered=resume_btn.collidepoint(pygame.mouse.get_pos()))
    draw_button(menu_btn, "MAIN MENU", RED, hovered=menu_btn.collidepoint(pygame.mouse.get_pos()))

    return resume_btn, menu_btn

def draw_level_clear():
    draw_gradient_background()

    panel = pygame.Rect(260, 180, 480, 280)
    draw_panel(panel, NAVY, GREEN, 20)

    draw_text("LEVEL CLEARED!", FONT_L, WHITE, WIDTH // 2, 235, center=True)
    draw_text(f"Level {selected_level} completed", FONT_M, GOLD, WIDTH // 2, 285, center=True)
    draw_text(f"Score: {score}", FONT_M, WHITE, WIDTH // 2, 325, center=True)

    next_btn = pygame.Rect(390, 370, 220, 50)
    menu_btn = pygame.Rect(390, 430, 220, 50)

    draw_button(next_btn, "NEXT LEVEL", GREEN, hovered=next_btn.collidepoint(pygame.mouse.get_pos()))
    draw_button(menu_btn, "MAIN MENU", BLUE, hovered=menu_btn.collidepoint(pygame.mouse.get_pos()))

    return next_btn, menu_btn

def draw_game_over():
    draw_gradient_background()

    panel = pygame.Rect(260, 180, 480, 300)
    draw_panel(panel, NAVY, RED, 20)

    draw_text("GAME OVER", FONT_L, WHITE, WIDTH // 2, 235, center=True)
    draw_text(f"Level Reached: {selected_level}", FONT_M, WHITE, WIDTH // 2, 285, center=True)
    draw_text(f"Score: {score}", FONT_M, GOLD, WIDTH // 2, 325, center=True)
    draw_text(f"Best Score: {settings['best_score']}", FONT_M, CYAN, WIDTH // 2, 360, center=True)

    retry_btn = pygame.Rect(390, 405, 220, 50)
    menu_btn = pygame.Rect(390, 465, 220, 50)

    draw_button(retry_btn, "RETRY LEVEL", ORANGE, hovered=retry_btn.collidepoint(pygame.mouse.get_pos()))
    draw_button(menu_btn, "MAIN MENU", BLUE, hovered=menu_btn.collidepoint(pygame.mouse.get_pos()))

    return retry_btn, menu_btn

def draw_final_win():
    draw_gradient_background()

    panel = pygame.Rect(220, 150, 560, 360)
    draw_panel(panel, NAVY, GOLD, 24)

    draw_text("CONGRATULATIONS!", FONT_L, WHITE, WIDTH // 2, 210, center=True)
    draw_text("You completed all 10 levels", FONT_M, GOLD, WIDTH // 2, 255, center=True)
    draw_text(f"Final Score: {score}", FONT_M, WHITE, WIDTH // 2, 305, center=True)
    draw_text(f"Best Score: {settings['best_score']}", FONT_M, CYAN, WIDTH // 2, 345, center=True)
    draw_text(
        f"AI Mode: {'ON' if settings['ai_mode'] else 'OFF'}",
        FONT_M,
        GREEN if settings["ai_mode"] else RED,
        WIDTH // 2,
        385,
        center=True
    )

    menu_btn = pygame.Rect(390, 445, 220, 50)
    draw_button(menu_btn, "MAIN MENU", BLUE, hovered=menu_btn.collidepoint(pygame.mouse.get_pos()))
    return menu_btn

# =========================
# MAIN LOOP
# =========================
running = True

while running:
    CLOCK.tick(FPS)

    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True

        elif event.type == pygame.KEYDOWN:
            if game_state == PLAYING:
                if event.key == pygame.K_ESCAPE:
                    game_state = PAUSED
            elif game_state == PAUSED:
                if event.key == pygame.K_ESCAPE:
                    game_state = PLAYING

    if game_state == PLAYING:
        update_game()

    if game_state == MENU:
        buttons = draw_menu()

        if clicked:
            for text, rect, _ in buttons:
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if text == "PLAY":
                        game_state = LEVEL_SELECT
                    elif text == "SETTINGS":
                        game_state = SETTINGS
                    elif text == "HOW TO PLAY":
                        game_state = HOW_TO_PLAY
                    elif text == "HISTORY":
                        game_state = HISTORY
                    elif text == "EXIT":
                        running = False

    elif game_state == LEVEL_SELECT:
        level_buttons, back_btn = draw_level_select()

        if clicked:
            if back_btn.collidepoint(pygame.mouse.get_pos()):
                game_state = MENU
            else:
                for level, rect, unlocked in level_buttons:
                    if unlocked and rect.collidepoint(pygame.mouse.get_pos()):
                        start_new_game(level)

    elif game_state == SETTINGS:
        btns = draw_settings()

        if clicked:
            if btns["music_on"].collidepoint(pygame.mouse.get_pos()):
                settings["music_on"] = True
                save_settings(settings)
            elif btns["music_off"].collidepoint(pygame.mouse.get_pos()):
                settings["music_on"] = False
                save_settings(settings)
            elif btns["sound_on"].collidepoint(pygame.mouse.get_pos()):
                settings["sound_on"] = True
                save_settings(settings)
            elif btns["sound_off"].collidepoint(pygame.mouse.get_pos()):
                settings["sound_on"] = False
                save_settings(settings)
            elif btns["ai_on"].collidepoint(pygame.mouse.get_pos()):
                settings["ai_mode"] = True
                save_settings(settings)
            elif btns["ai_off"].collidepoint(pygame.mouse.get_pos()):
                settings["ai_mode"] = False
                save_settings(settings)
            elif btns["reset"].collidepoint(pygame.mouse.get_pos()):
                settings["current_level"] = 1
                settings["unlocked_level"] = 1
                save_settings(settings)
            elif btns["back"].collidepoint(pygame.mouse.get_pos()):
                game_state = MENU

    elif game_state == HOW_TO_PLAY:
        back_btn = draw_how_to_play()
        if clicked and back_btn.collidepoint(pygame.mouse.get_pos()):
            game_state = MENU

    elif game_state == HISTORY:
        back_btn = draw_history()
        if clicked and back_btn.collidepoint(pygame.mouse.get_pos()):
            game_state = MENU

    elif game_state == PLAYING:
        draw_game()
        pause_btn = pygame.Rect(WIDTH - 150, 14, 110, 42)

        if clicked and pause_btn.collidepoint(pygame.mouse.get_pos()):
            game_state = PAUSED

    elif game_state == PAUSED:
        resume_btn, menu_btn = draw_pause_screen()

        if clicked:
            if resume_btn.collidepoint(pygame.mouse.get_pos()):
                game_state = PLAYING
            elif menu_btn.collidepoint(pygame.mouse.get_pos()):
                game_state = MENU

    elif game_state == LEVEL_CLEAR:
        next_btn, menu_btn = draw_level_clear()

        if clicked:
            if next_btn.collidepoint(pygame.mouse.get_pos()):
                start_level_only(selected_level + 1)
            elif menu_btn.collidepoint(pygame.mouse.get_pos()):
                game_state = MENU

    elif game_state == GAME_OVER:
        retry_btn, menu_btn = draw_game_over()

        if clicked:
            if retry_btn.collidepoint(pygame.mouse.get_pos()):
                start_level_only(selected_level)
            elif menu_btn.collidepoint(pygame.mouse.get_pos()):
                game_state = MENU

    elif game_state == FINAL_WIN:
        menu_btn = draw_final_win()

        if clicked and menu_btn.collidepoint(pygame.mouse.get_pos()):
            game_state = MENU

    pygame.display.flip()

pygame.quit()
sys.exit()