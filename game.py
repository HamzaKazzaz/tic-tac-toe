import pygame
import sys
import random

pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

background = pygame.image.load("datastr&algorithm/360_F.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

pygame.mixer.init()
click_sound = pygame.mixer.Sound("datastr&algorithm/mixkit-fast-double-click-on-mouse-275.wav")

tahta = [[" " for _ in range(3)] for _ in range(3)]

def main_menu():
    while True:
        screen.blit(background, (0, 0))
        title = font.render("Tic-Tac-Toe", True, WHITE)
        start_button = pygame.Rect(300, 250, 200, 50)
        settings_button = pygame.Rect(300, 350, 200, 50)

        pygame.draw.rect(screen, GREEN, start_button)
        pygame.draw.rect(screen, GRAY, settings_button)

        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title, title_rect)

        start_text = small_font.render("Başlat", True, BLACK)
        settings_text = small_font.render("Ayarlar", True, BLACK)

        screen.blit(start_text, (start_button.x + 70, start_button.y + 15))
        screen.blit(settings_text, (settings_button.x + 65, settings_button.y + 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    click_sound.play()
                    game_loop()
                elif settings_button.collidepoint(event.pos):
                    click_sound.play()
                    settings_menu()

        pygame.display.update()
        clock.tick(FPS)

def settings_menu():
    ses_acik = True
    dil = "Türkçe"

    while True:
        screen.blit(background, (0, 0))
        title = font.render("Ayarlar", True, WHITE)
        ses_button = pygame.Rect(300, 200, 200, 50)
        dil_button = pygame.Rect(300, 300, 200, 50)
        back_button = pygame.Rect(300, 400, 200, 50)

        pygame.draw.rect(screen, GRAY, ses_button)
        pygame.draw.rect(screen, GRAY, dil_button)
        pygame.draw.rect(screen, RED, back_button)

        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title, title_rect)

        ses_text = small_font.render(f"Ses: {'Açık' if ses_acik else 'Kapalı'}", True, BLACK)
        dil_text = small_font.render(f"Dil: {dil}", True, BLACK)
        back_text = small_font.render("Geri", True, BLACK)

        screen.blit(ses_text, (ses_button.x + 50, ses_button.y + 15))
        screen.blit(dil_text, (dil_button.x + 50, dil_button.y + 15))
        screen.blit(back_text, (back_button.x + 80, back_button.y + 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ses_button.collidepoint(event.pos):
                    click_sound.play()
                    ses_acik = not ses_acik
                    pygame.mixer.music.set_volume(1 if ses_acik else 0)
                elif dil_button.collidepoint(event.pos):
                    click_sound.play()
                    dil = "İngilizce" if dil == "Türkçe" else "Türkçe"
                elif back_button.collidepoint(event.pos):
                    click_sound.play()
                    return

        pygame.display.update()
        clock.tick(FPS)

def game_loop():
    player = "X"
    game_over = False

    while True:
        screen.fill(WHITE)
        draw_board()
        draw_figures()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // (HEIGHT // 3)
                clicked_col = mouseX // (WIDTH // 3)

                if tahta[clicked_row][clicked_col] == " ":
                    tahta[clicked_row][clicked_col] = player
                    if check_winner(player):
                        game_over = True
                    player = "O" if player == "X" else "X"

        if player == "O" and not game_over:
            ai_move()
            if check_winner("O"):
                game_over = True
            player = "X"

        if game_over:
            winner = check_winner("X") or check_winner("O")
            if winner:
                show_winner(winner)
            pygame.time.wait(2000)
            reset_board()
            return  

        pygame.display.update()
        clock.tick(FPS)

def ai_move():
    best_score = -float('inf')
    best_move = None
    for row in range(3):
        for col in range(3):
            if tahta[row][col] == " ":
                tahta[row][col] = "O"
                score = minimax(tahta, 0, False)
                tahta[row][col] = " "
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        tahta[best_move[0]][best_move[1]] = "O"

def minimax(board, depth, is_maximizing):
    if check_winner("O"):
        return 1
    elif check_winner("X"):
        return -1
    elif not any(" " in row for row in board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score

def draw_board():
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (i * (WIDTH // 3), 0), (i * (WIDTH // 3), HEIGHT), 2)
        pygame.draw.line(screen, BLACK, (0, i * (HEIGHT // 3)), (WIDTH, i * (HEIGHT // 3)), 2)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if tahta[row][col] == "X":
                pygame.draw.line(screen, BLACK, (col * (WIDTH // 3) + 50, row * (HEIGHT // 3) + 50),
                                ((col + 1) * (WIDTH // 3) - 50, (row + 1) * (HEIGHT // 3) - 50), 2)
                pygame.draw.line(screen, BLACK, ((col + 1) * (WIDTH // 3) - 50, row * (HEIGHT // 3) + 50),
                                (col * (WIDTH // 3) + 50, (row + 1) * (HEIGHT // 3) - 50), 2)
            elif tahta[row][col] == "O":
                pygame.draw.circle(screen, BLACK, (col * (WIDTH // 3) + (WIDTH // 6), row * (HEIGHT // 3) + (HEIGHT // 6)), 50, 2)

def check_winner(player):
    for row in range(3):
        if tahta[row][0] == tahta[row][1] == tahta[row][2] == player:
            return True
    for col in range(3):
        if tahta[0][col] == tahta[1][col] == tahta[2][col] == player:
            return True
    if tahta[0][0] == tahta[1][1] == tahta[2][2] == player:
        return True
    if tahta[0][2] == tahta[1][1] == tahta[2][0] == player:
        return True
    return False

def show_winner(player):
    text = font.render(f"{player} Kazandı!", True, RED)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(2000)  
    reset_board()
    main_menu()  

def reset_board():
    global tahta
    tahta = [[" " for _ in range(3)] for _ in range(3)]

main_menu()
