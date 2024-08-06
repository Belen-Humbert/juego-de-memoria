import pygame
import sys
import random
import time

pygame.init()

# Configuración de la ventana
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Juego de Memoria')

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)  
YELLOW = (255, 255, 0)  


FONT = pygame.font.Font('assets/fonts/press_start_2p.ttf', 36)
INSTRUCTION_FONT = pygame.font.Font('assets/fonts/ComicCup.otf', 30)

# Configuración del juego
CARD_SIZE = 100
CARD_SPACING = 10
GRID_SIZE = 4
SYMBOLS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] * 2
TIME_LIMIT = 60  # Tiempo límite en segundos

# Carga música de fondo
pygame.mixer.music.load('assets/sounds/sound1.wav')
pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen
pygame.mixer.music.play(-1)  # Reproduce la música en bucle

class Card:
    def __init__(self, x, y, symbol):
        self.rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
        self.symbol = symbol
        self.revealed = False
        self.matched = False

def create_board():
    cards = []
    symbols = SYMBOLS.copy()
    random.shuffle(symbols)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * (CARD_SIZE + CARD_SPACING) + CARD_SPACING
            y = i * (CARD_SIZE + CARD_SPACING) + CARD_SPACING
            cards.append(Card(x, y, symbols.pop()))
    return cards

def draw_board(cards):
    screen.fill(BLACK)
    for card in cards:
        if card.revealed:
            if card.matched:
                pygame.draw.rect(screen, GREEN, card.rect)
            else:
                pygame.draw.rect(screen, WHITE, card.rect)
            text = FONT.render(card.symbol, True, BLACK)
            text_rect = text.get_rect(center=card.rect.center)
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, GRAY, card.rect)
    pygame.display.flip()

def draw_menu():
    screen.fill(BLACK)
    title = FONT.render("Juego de Memoria", True, WHITE)
    start_text = FONT.render("Jugar", True, RED)
    instructions_text = FONT.render("Instrucciones", True, YELLOW)

    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    instructions_rect = instructions_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(title, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(instructions_text, instructions_rect)

    pygame.display.flip()

def draw_instructions():
    screen.fill(BLACK)
    instructions = [
        "Instrucciones del Juego:",
        "1. Empareja todas las cartas.",
        "2. Haz clic en las cartas para revelarlas.",
        "3. Si dos cartas coinciden, permanecen reveladas.",
        "4. Si no coinciden, se ocultan nuevamente.",
        "5. Gana el juego al emparejar todas las cartas."
    ]
    y_offset = HEIGHT // 4
    for line in instructions:
        text = INSTRUCTION_FONT.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 50

    back_text = INSTRUCTION_FONT.render("Volver al menú", True, WHITE)
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    screen.blit(back_text, back_rect)

    pygame.display.flip()

def draw_timer(start_time):
    elapsed_time = time.time() - start_time
    remaining_time = max(0, TIME_LIMIT - int(elapsed_time))
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    timer_text = FONT.render(f"Tiempo: {minutes:02d}:{seconds:02d}", True, WHITE)
    
    # Calcula la posición del cronómetro
    text_rect = timer_text.get_rect()
    text_rect.right = WIDTH - 10
    text_rect.bottom = HEIGHT - 10
    
    screen.blit(timer_text, text_rect)

def enemy_action(cards, revealed_cards):
    pygame.time.wait(60)  # Tiempo que el enemigo espera antes de ocultar cartas
    for card in revealed_cards:
        if not card.matched:
            card.revealed = False

def main():
    in_menu = True
    show_instructions = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if in_menu:
                    if WIDTH // 2 - 50 <= mouse_pos[0] <= WIDTH // 2 + 50:
                        if HEIGHT // 2 - 80 <= mouse_pos[1] <= HEIGHT // 2 - 20:
                            in_menu = False
                            start_time = time.time()  # Guardar el tiempo de inicio
                        elif HEIGHT // 2 + 20 <= mouse_pos[1] <= HEIGHT // 2 + 80:
                            show_instructions = True
                    if show_instructions and HEIGHT - 140 <= mouse_pos[1] <= HEIGHT - 60:
                        show_instructions = False
                        in_menu = True
                else:
                    if show_instructions and HEIGHT - 140 <= mouse_pos[1] <= HEIGHT - 60:
                        show_instructions = False
                        in_menu = True

        if in_menu:
            draw_menu()
        elif show_instructions:
            draw_instructions()
        else:
            cards = create_board()
            selected_cards = []
            matches = 0
            clock = pygame.time.Clock()
            start_time = time.time()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for card in cards:
                            if card.rect.collidepoint(event.pos) and not card.revealed and not card.matched:
                                card.revealed = True
                                selected_cards.append(card)
                                if len(selected_cards) == 2:
                                    if selected_cards[0].symbol == selected_cards[1].symbol:
                                        matches += 1
                                        selected_cards[0].matched = True
                                        selected_cards[1].matched = True
                                    else:
                                        enemy_action(cards, selected_cards)
                                    selected_cards = []

                # Actualiza la pantalla
                screen.fill(BLACK)
                draw_board(cards)
                draw_timer(start_time)

                elapsed_time = time.time() - start_time
                if elapsed_time > TIME_LIMIT:
                    screen.fill(BLACK)
                    lose_text = FONT.render("¡Tiempo agotado!", True, WHITE)
                    screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, HEIGHT // 2 - lose_text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    in_menu = True
                    break

                if matches == len(SYMBOLS) // 2:
                    screen.fill(BLACK)
                    win_text = FONT.render("¡Has ganado!", True, WHITE)
                    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    in_menu = True
                    break

                pygame.display.flip()  
                clock.tick(30)

if __name__ == "__main__":
    main()
