import pygame
import sys
import random
import math


# Game configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20

GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Base speed; can be scaled by difficulty
BASE_FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Forest palette
FOREST_TOP = (6, 26, 20)
FOREST_MID = (10, 45, 28)
FOREST_BOTTOM = (36, 26, 18)
TREE_DARK = (9, 25, 16)
TREE_LEAVES = (20, 70, 35)
MIST = (120, 200, 160)

SNAKE_HEAD = (170, 240, 120)
SNAKE_BODY = (90, 190, 90)
SNAKE_BELLY = (40, 110, 60)
SNAKE_OUTLINE = (15, 40, 20)

APPLE_RED = (215, 60, 60)
APPLE_HIGHLIGHT = (250, 210, 210)
APPLE_LEAF = (40, 130, 60)
APPLE_STEM = (90, 55, 30)

GRID_COLOR = (20, 45, 30)
HUD_BG = (8, 16, 12)
HUD_LINE = (25, 55, 35)
ACCENT = (195, 230, 140)
GRAY = (160, 160, 160)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # moving right
        self.grow_pending = 0

    def head(self):
        return self.positions[0]

    def change_direction(self, new_direction):
        # Prevent reversing directly into yourself
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def move(self):
        cur_x, cur_y = self.head()
        dx, dy = self.direction
        new_head = ((cur_x + dx) % GRID_WIDTH, (cur_y + dy) % GRID_HEIGHT)

        # Check self-collision
        if new_head in self.positions[1:]:
            return False

        self.positions.insert(0, new_head)

        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()

        return True

    def grow(self, amount=1):
        self.grow_pending += amount


class Food:
    def __init__(self, snake_positions):
        self.position = self.random_position(snake_positions)

    def random_position(self, snake_positions):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_positions:
                return pos

    def respawn(self, snake_positions):
        self.position = self.random_position(snake_positions)


def draw_background(surface, tick):
    """Forest-style layered background with subtle animation."""
    # Vertical gradient sky / canopy / ground
    for y in range(WINDOW_HEIGHT):
        t = y / WINDOW_HEIGHT
        if t < 0.45:
            # Blend top to mid
            blend = t / 0.45
            r = int(FOREST_TOP[0] * (1 - blend) + FOREST_MID[0] * blend)
            g = int(FOREST_TOP[1] * (1 - blend) + FOREST_MID[1] * blend)
            b = int(FOREST_TOP[2] * (1 - blend) + FOREST_MID[2] * blend)
        else:
            # Blend mid to bottom
            blend = (t - 0.45) / 0.55
            r = int(FOREST_MID[0] * (1 - blend) + FOREST_BOTTOM[0] * blend)
            g = int(FOREST_MID[1] * (1 - blend) + FOREST_BOTTOM[1] * blend)
            b = int(FOREST_MID[2] * (1 - blend) + FOREST_BOTTOM[2] * blend)
        pygame.draw.line(surface, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    # Distant tree silhouettes
    sway = math.sin(tick * 0.01)
    for i, x in enumerate(range(-60, WINDOW_WIDTH + 60, 120)):
        offset = int(sway * (4 + (i % 3)))
        base_x = x + offset
        trunk_width = 22
        trunk_height = 160
        trunk_bottom = WINDOW_HEIGHT - 40
        pygame.draw.rect(
            surface,
            TREE_DARK,
            (base_x, trunk_bottom - trunk_height, trunk_width, trunk_height),
        )
        # Canopy
        cx = base_x + trunk_width // 2
        top_y = trunk_bottom - trunk_height - 20
        pygame.draw.polygon(
            surface,
            TREE_LEAVES,
            [(cx, top_y), (base_x - 25, trunk_bottom - 40), (base_x + trunk_width + 25, trunk_bottom - 40)],
        )

    # Low mist layer near the ground
    mist_surface = pygame.Surface((WINDOW_WIDTH, 120), pygame.SRCALPHA)
    alpha = 55 + int(20 * math.sin(tick * 0.02))
    pygame.draw.rect(
        mist_surface,
        (MIST[0], MIST[1], MIST[2], alpha),
        (0, 40, WINDOW_WIDTH, 80),
    )
    surface.blit(mist_surface, (0, WINDOW_HEIGHT - 140))


def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))


def draw_snake(surface, snake):
    for i, (x, y) in enumerate(snake.positions):
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        inner_rect = rect.inflate(-6, -6)
        is_head = i == 0

        # Base body segment with outline and belly
        pygame.draw.rect(surface, SNAKE_OUTLINE, rect, border_radius=8)
        pygame.draw.rect(surface, SNAKE_BODY, inner_rect, border_radius=7)

        # Slight belly stripe
        belly_rect = pygame.Rect(
            inner_rect.x,
            inner_rect.y + inner_rect.height // 2,
            inner_rect.width,
            inner_rect.height // 2,
        )
        pygame.draw.rect(surface, SNAKE_BELLY, belly_rect, border_radius=7)

        if is_head:
            # Brighter head overlay
            head_rect = inner_rect.inflate(2, 2)
            pygame.draw.rect(surface, SNAKE_HEAD, head_rect, border_radius=9)

            # Eyes oriented by direction
            dir_x, dir_y = snake.direction
            eye_radius = 3
            offset = 4
            cx = head_rect.centerx
            cy = head_rect.centery

            if dir_x == 1:  # moving right
                eye1 = (head_rect.right - offset, head_rect.top + offset)
                eye2 = (head_rect.right - offset, head_rect.bottom - offset)
            elif dir_x == -1:  # moving left
                eye1 = (head_rect.left + offset, head_rect.top + offset)
                eye2 = (head_rect.left + offset, head_rect.bottom - offset)
            elif dir_y == -1:  # moving up
                eye1 = (head_rect.left + offset, head_rect.top + offset)
                eye2 = (head_rect.right - offset, head_rect.top + offset)
            else:  # moving down
                eye1 = (head_rect.left + offset, head_rect.bottom - offset)
                eye2 = (head_rect.right - offset, head_rect.bottom - offset)

            for eye in (eye1, eye2):
                pygame.draw.circle(surface, WHITE, eye, eye_radius)
                pygame.draw.circle(surface, BLACK, eye, eye_radius - 1)

            # Small tongue in front of head
            tongue_length = 6
            tongue_width = 2
            if dir_x == 1:
                tongue_rect = pygame.Rect(head_rect.right, cy - tongue_width // 2, tongue_length, tongue_width)
            elif dir_x == -1:
                tongue_rect = pygame.Rect(head_rect.left - tongue_length, cy - tongue_width // 2, tongue_length, tongue_width)
            elif dir_y == -1:
                tongue_rect = pygame.Rect(cx - tongue_width // 2, head_rect.top - tongue_length, tongue_width, tongue_length)
            else:
                tongue_rect = pygame.Rect(cx - tongue_width // 2, head_rect.bottom, tongue_width, tongue_length)
            pygame.draw.rect(surface, APPLE_RED, tongue_rect)


def draw_food(surface, food):
    x, y = food.position
    center = (
        x * CELL_SIZE + CELL_SIZE // 2,
        y * CELL_SIZE + CELL_SIZE // 2 + 2,
    )
    radius = CELL_SIZE // 2 - 3

    # Apple body
    pygame.draw.circle(surface, APPLE_RED, center, radius)

    # Highlight
    highlight_center = (center[0] - radius // 3, center[1] - radius // 3)
    pygame.draw.circle(surface, APPLE_HIGHLIGHT, highlight_center, max(1, radius // 4))

    # Stem
    stem_height = 6
    pygame.draw.rect(
        surface,
        APPLE_STEM,
        (
            center[0] - 1,
            center[1] - radius - stem_height + 2,
            3,
            stem_height,
        ),
    )

    # Leaf
    leaf_points = [
        (center[0] + 2, center[1] - radius),
        (center[0] + 10, center[1] - radius - 6),
        (center[0] + 6, center[1] - radius + 2),
    ]
    pygame.draw.polygon(surface, APPLE_LEAF, leaf_points)


def draw_score(surface, font, score):
    panel_height = 32
    pygame.draw.rect(surface, HUD_BG, (0, 0, WINDOW_WIDTH, panel_height))
    pygame.draw.line(surface, HUD_LINE, (0, panel_height), (WINDOW_WIDTH, panel_height), 1)
    text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(text, (12, 6))


def draw_high_score(surface, font, high_score):
    text = font.render(f"Best: {high_score}", True, ACCENT)
    rect = text.get_rect(topright=(WINDOW_WIDTH - 12, 6))
    surface.blit(text, rect)


def main_menu(screen, clock, font_title, font_menu, font_small):
    """Show the initial menu and return selected difficulty FPS multiplier."""
    options = [("Easy", 0.8), ("Normal", 1.0), ("Hard", 1.3)]
    selected = 1
    tick = 0

    while True:
        tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[selected][1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        draw_background(screen, tick)

        # Title
        title_surf = font_title.render("SNAKE", True, WHITE)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 140))
        screen.blit(title_surf, title_rect)

        subtitle = font_small.render("Use ↑/↓ to choose difficulty, ENTER to start", True, ACCENT)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 90))
        screen.blit(subtitle, subtitle_rect)

        # Difficulty options
        base_y = WINDOW_HEIGHT // 2 - 10
        spacing = 40
        for i, (label, _) in enumerate(options):
            is_selected = i == selected
            color = ACCENT if is_selected else WHITE
            prefix = "▶ " if is_selected else "   "
            text_surf = font_menu.render(prefix + label, True, color)
            rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, base_y + i * spacing))
            screen.blit(text_surf, rect)

        # Footer
        footer = font_small.render("ESC to quit", True, GRAY)
        footer_rect = footer.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
        screen.blit(footer, footer_rect)

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(screen, clock, score, high_score, font_big, font_small):
    tick = 0
    while True:
        tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "retry"
                elif event.key == pygame.K_ESCAPE:
                    return "menu"

        draw_background(screen, tick)

        msg = "Game Over"
        msg_surf = font_big.render(msg, True, WHITE)
        msg_rect = msg_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        screen.blit(msg_surf, msg_rect)

        score_text = font_small.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        best_text = font_small.render(f"Best: {high_score}", True, ACCENT)
        best_rect = best_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        screen.blit(best_text, best_rect)

        hint = "ENTER: play again   M: menu   ESC: quit"
        hint_surf = font_small.render(hint, True, WHITE)
        hint_rect = hint_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        screen.blit(hint_surf, hint_rect)

        # Allow quick jump to menu with M
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            return "menu"

        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.init()
    pygame.display.set_caption("Snake Game")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    font_small = pygame.font.SysFont("consolas", 18)
    font_big = pygame.font.SysFont("consolas", 36, bold=True)
    font_title = pygame.font.SysFont("consolas", 64, bold=True)
    font_menu = pygame.font.SysFont("consolas", 28)

    high_score = 0

    # Initial main menu to choose difficulty
    difficulty_multiplier = main_menu(screen, clock, font_title, font_menu, font_small)
    fps = int(BASE_FPS * difficulty_multiplier)

    while True:
        snake = Snake()
        food = Food(snake.positions)
        score = 0
        running = True
        tick = 0

        while running:
            tick += 1
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        snake.change_direction((0, -1))
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        snake.change_direction((0, 1))
                    elif event.key in (pygame.K_a, pygame.K_LEFT):
                        snake.change_direction((-1, 0))
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        snake.change_direction((1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        # Pause to menu
                        choice = game_over_screen(screen, clock, score, high_score, font_big, font_small)
                        if choice == "menu":
                            difficulty_multiplier = main_menu(screen, clock, font_title, font_menu, font_small)
                            fps = int(BASE_FPS * difficulty_multiplier)
                            running = False
                        elif choice == "retry":
                            running = False

            # Move snake
            alive = snake.move()
            if not alive:
                if score > high_score:
                    high_score = score
                choice = game_over_screen(screen, clock, score, high_score, font_big, font_small)
                if choice == "menu":
                    difficulty_multiplier = main_menu(screen, clock, font_title, font_menu, font_small)
                    fps = int(BASE_FPS * difficulty_multiplier)
                running = False
                break

            # Check for food collision
            if snake.head() == food.position:
                score += 1
                snake.grow()
                food.respawn(snake.positions)

            # Draw everything
            draw_background(screen, tick)
            draw_grid(screen)
            draw_snake(screen, snake)
            draw_food(screen, food)
            draw_score(screen, font_small, score)
            draw_high_score(screen, font_small, high_score)

            pygame.display.flip()
            clock.tick(fps)


if __name__ == "__main__":
    main()

