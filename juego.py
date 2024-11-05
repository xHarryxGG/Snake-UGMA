import pygame
import sys 
import random

pygame.init()

SW, SH = 500, 500

BLOCK_SIZE = 50
FONT = pygame.font.Font(None, BLOCK_SIZE*2)  # Cambié a una fuente predeterminada

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake Alpha - UGMA")
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
    
    def update(self):
        global apple
        
        for square in self.body:
            if self.head.colliderect(square):
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
        
        if self.dead:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            apple = Apple()
        
        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

class Apple:
    def __init__(self):
        self.x = random.randint(0, (SW // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.y = random.randint(0, (SH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def update(self):
        apple_image = pygame.image.load('img/apple.png')
        apple_image = pygame.transform.scale(apple_image, (BLOCK_SIZE, BLOCK_SIZE))
        screen.blit(apple_image, self.rect)

def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

score = FONT.render("0", True, "white")
score_rect = score.get_rect(center=(SW/2, SH/10))

snake = Snake()
apple = Apple()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and snake.ydir == 0:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP and snake.ydir == 0:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT and snake.xdir == 0:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT and snake.xdir == 0:
                snake.ydir = 0
                snake.xdir = -1

    snake.update()
    
    screen.fill('black')
    drawGrid()
    apple.update()
    score = FONT.render(f"{len(snake.body)}", True, "white")

    head_image = pygame.image.load('img/snakeHead.png')
    head_image = pygame.transform.scale(head_image, (BLOCK_SIZE * 2, BLOCK_SIZE * 2))

    if snake.xdir == -1:  # Si la serpiente se mueve hacia la derecha
        head_image_rotated = pygame.transform.rotate(head_image, 270)  # Rota la imagen 270 grados (hacia la derecha)
    elif snake.xdir == 1:  # Si la serpiente se mueve hacia la izquierda
        head_image_rotated = pygame.transform.rotate(head_image, 90)  # Rota la imagen 90 grados (hacia la izquierda)
    elif snake.ydir == -1:  # Si la serpiente se mueve hacia abajo
        head_image_rotated = pygame.transform.rotate(head_image, 180)  # Rota la imagen 180 grados (hacia abajo)
    elif snake.ydir == 1:  # Si la serpiente se mueve hacia arriba
        head_image_rotated = head_image  # No rota la imagen (hacia arriba)

    head_image_rect = head_image_rotated.get_rect(center=snake.head.center)  # Obtiene el rectángulo que rodea la imagen rotada y lo centra en la cabeza de la serpiente
    screen.blit(head_image_rotated, head_image_rect)  # Dibuja la imagen rotada en la pantalla

    for square in snake.body:
        pygame.draw.rect(screen, "#A0C432", square)

    screen.blit(score, score_rect)

    score_num = len(snake.body)
    
    eat_sound = pygame.mixer.Sound('audio/eating-sound-effect.mp3')
    mondongo_sound = pygame.mixer.Sound('audio/mondongo.mp3')

    if snake.head.colliderect(apple.rect):
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()

        if score_num == 9:
            mondongo_sound.play()
            image = pygame.image.load('img/mondongo.jpg')  # Carga la imagen
            image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))  # Ajusta el tamaño de la imagen al tamaño de la pantalla
            screen.blit(image, (0, 0))  # Dibuja la imagen en la pantalla
            pygame.display.update()  # Actualiza la pantalla
            pygame.time.wait(1000)  # Espera 1 segundo
        else:
            eat_sound.play()

    pygame.display.update()
    clock.tick(10)  # Aumenta el valor para una mayor suavidad
