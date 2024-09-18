import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 定义常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (255, 255, 153)
TILE_SIZE = 50
ROWS, COLS = 6, 6
FPS = 30

# 创建窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("KEEP THE SAME")

# 加载字体
font = pygame.font.Font(None, 64)

# 创建开始按钮
start_button = pygame.Rect(300, 400, 200, 100)

# 难度选择按钮
easy_button = pygame.Rect(300, 200, 200, 100)
medium_button = pygame.Rect(300, 350, 200, 100)
hard_button = pygame.Rect(300, 500, 200, 100)

# 开始界面
def start_screen():
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button.collidepoint(x, y):
                    running = False
                    difficulty_screen()  # 进入难度选择界面

        # 绘制背景和控件
        screen.fill(BG_COLOR)
        title_text = font.render("KEEP THE SAME", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, BLACK, start_button)
        start_text = font.render("START", True, WHITE)
        start_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_rect)

        pygame.display.flip()
#难度选择
def difficulty_screen():
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if easy_button.collidepoint(x, y):
                    running = False
                    game_screen(60)  # 简单难度
                elif medium_button.collidepoint(x, y):
                    running = False
                    game_screen(40)  # 中等难度
                elif hard_button.collidepoint(x, y):
                    running = False
                    game_screen(20)  # 困难难度

        # 绘制难度选择界面
        screen.fill(BG_COLOR)
        title_text = font.render("Difficulty Selection", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # 绘制按钮
        pygame.draw.rect(screen, BLACK, easy_button)
        easy_text = font.render("Easy", True, WHITE)
        easy_rect = easy_text.get_rect(center=easy_button.center)
        screen.blit(easy_text, easy_rect)

        pygame.draw.rect(screen, BLACK, medium_button)
        medium_text = font.render("Medium", True, WHITE)
        medium_rect = medium_text.get_rect(center=medium_button.center)
        screen.blit(medium_text, medium_rect)

        pygame.draw.rect(screen, BLACK, hard_button)
        hard_text = font.render("Hard", True, WHITE)
        hard_rect = hard_text.get_rect(center=hard_button.center)
        screen.blit(hard_text, hard_rect)

        pygame.display.flip()

def game_screen(countdown_time):
    # 创建窗口
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("KEEP THE SAME")

    # 加载图案图片
    patterns = [pygame.image.load(f"image/p{i}.png") for i in range(1, 6)]
    patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

    # 确保每种图片的数量是3的倍数
    board = []
    for _ in range(ROWS * COLS // 3):
        pattern = random.choice(patterns)
        board.extend([pattern] * 3)  # 每种图片添加3次
    random.shuffle(board)  # 打乱顺序
    board = [board[i:i + COLS] for i in range(0, len(board), COLS)]  # 生成游戏板

    selected = []

    # 初始化倒计时
    remaining_time = countdown_time
    start_ticks = pygame.time.get_ticks()  # 获取游戏开始时的时间

    def draw_board():
        spacing = 40  # 图片之间的间隔大小
        total_width = COLS * TILE_SIZE + (COLS - 1) * spacing
        total_height = ROWS * TILE_SIZE + (ROWS - 1) * spacing
        start_x = (screen.get_width() - total_width) // 2
        start_y = (screen.get_height() - total_height) // 2

        for row in range(ROWS):
            for col in range(COLS):
                tile = board[row][col]
                if tile is not None:
                    x = start_x + col * (TILE_SIZE + spacing)
                    y = start_y + row * (TILE_SIZE + spacing)
                    screen.blit(tile, (x, y))

    def check_match():
        if len(selected) == 3:
            r1, c1 = selected[0]
            r2, c2 = selected[1]
            r3, c3 = selected[2]
            if (board[r1][c1] == board[r2][c2] == board[r3][c3] and
                (r1, c1) != (r2, c2) and (r1, c1) != (r3, c3) and (r2, c2) != (r3, c3)):
                board[r1][c1] = None
                board[r2][c2] = None
                board[r3][c3] = None
            selected.clear()

    # 主游戏循环
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(FPS)

        # 计算剩余时间
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # 计算经过的秒数
        remaining_time = countdown_time - seconds  # 剩余时间

        if remaining_time <= 0:
            remaining_time = 0
            # 倒计时结束，显示失败界面
            game_over(failed=True)  # 结束游戏并显示失败界面
            return  # 退出游戏循环

        # 检查是否胜利
        if all(tile is None for row in board for tile in row):
            victory_screen()  # 显示胜利界面
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = -1
                col = -1

                if 150 <= y <= 200:
                    row = 0
                if 240 <= y <= 290:
                    row = 1
                if 330 <= y <= 380:
                    row = 2
                if 420 <= y <= 470:
                    row = 3
                if 510 <= y <= 560:
                    row = 4
                if 600 <= y <= 650:
                    row = 5
                if 150 <= x <= 200:
                    col = 0
                if 240 <= x <= 290:
                    col = 1
                if 330 <= x <= 380:
                    col = 2
                if 420 <= x <= 470:
                    col = 3
                if 510 <= x <= 560:
                    col = 4
                if 600 <= x <= 650:
                    col = 5
                if row > -1 and col > -1:
                    if board[row][col] is not None:
                        selected.append((row, col))

                    if len(selected) == 3:
                        check_match()

        screen.fill(BG_COLOR)
        draw_board()

        # 显示倒计时
        countdown_text = font.render(f"Time Remaining: {remaining_time}", True, BLACK)
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - 200, 20))

        pygame.display.flip()

def victory_screen():
    # 胜利界面
    running = True
    back_button = pygame.Rect(300, 500, 200, 100)  # 返回按钮

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button.collidepoint(x, y):
                    running = False
                    difficulty_screen()  # 返回难度选择界面

        screen.fill(BG_COLOR)
        victory_text = font.render("Congratulations! You Win!", True, BLACK)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(victory_text, victory_rect)

        # 绘制返回按钮
        pygame.draw.rect(screen, BLACK, back_button)
        back_text = font.render("Return", True, WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)

        pygame.display.flip()
def game_over(failed=False):
    # 游戏结束界面
    running = True
    back_button = pygame.Rect(300, 500, 200, 100)  # 返回难度选择按钮

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button.collidepoint(x, y):
                    running = False
                    difficulty_screen()  # 返回难度选择界面

        screen.fill(BG_COLOR)
        if failed:
            game_over_text = font.render("Game over!You lose!", True, BLACK)
        else:
            game_over_text = font.render("Game over!You lose!", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        restart_text = font.render(" ", True, BLACK)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        screen.blit(restart_text, restart_rect)

        # 绘制返回按钮
        pygame.draw.rect(screen, BLACK, back_button)
        back_text = font.render("Return", True, WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)

        pygame.display.flip()






# 启动主菜单
start_screen()
