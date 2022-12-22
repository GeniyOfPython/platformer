import pygame
import os
import modules.settings as settings
import modules.area as area

pygame.init()

win_height = 800
win_width = 850

# 6. Створити клас Sprite, в методі init задати 5 параметрів зі значенням за замовчуванням None
class Sprite(settings.Settings):
    def __init__(self, **kwargs):        
        # крок з яким буде рухатись спрайт 
        super().__init__(**kwargs)
        self.STEP = 3
        # швідкість зміни костюмів спрайта
        self.SPEED_ANIMATION = 0
        # властивість, що відповідає за номер костюма, для анімації бігу 
        self.COUNT_IMG = 5
        # флаг, що вказує напрямок руху спрайта
        self.DIRECTION = "R"
        # свойство, которое задаёт значение гравитации
        self.GRAVITY = 6
        # Флаг, который определяет, может ли наш спрайт двигаться в право
        self.CAN_MOVE_RIGHT = True
        # Флаг, который определяет, может ли наш спрайт двигаться в лево
        self.CAN_MOVE_LEFT = False
        # Флаг, который определяет, в прыжке ли находиться наш спрайт
        self.PLAYER_JUMP = False
        # Свойство, которое определяет, сколько повторов основного цикла было совершено
        self.COUNT_JUMP = 0
        #Флаг, благодаря которому мы определяем, нажата ли стрелочка вверх и находиться ли наш спрайт в состоянии прыжка
        self.PRESSED = False 
    # Метод руху спрайта вліво та вправо 
    def move_sprite(self):
        # отримуємо кортеж всіх ключів кнопок 
        event = pygame.key.get_pressed()
        # умова, що відповідає за рух спрайта у праву сторону        
        if event[pygame.K_RIGHT] and self.X + self.WIDTH <= win_width:
            self.DIRECTION = 'R' # задаємо напрямок руху
            if self.CAN_MOVE_RIGHT:
                self.X += self.STEP
                self.RECT.x = self.RECT.x + self.STEP
            self.animation() # метод класу, що виконує анімацію бігу спрайту
        # умова, що вілповідає за рух спрайта у ліву сторону
        elif event[pygame.K_LEFT] and self.X + 10 >= 0:            
            self.DIRECTION = 'L'
            if self.CAN_MOVE_LEFT:
                self.X -= self.STEP
                self.RECT.x = self.RECT.x - self.STEP
            self.animation()
        # умова, що відповідає за спокійний стан спрайта - спарайт стоїть на місці
        else:
            self.NAME_IMAGE = "images/player/1.png"
            self.direction()
    # Создаём функцию, которая определяет, столкнулся ли спрайт со стенкой справа, если да, то спрайт не может продолжать движение вправо
    def can_move_right(self, list_rect):        
        for block in list_rect:
            if self.DIRECTION == "R":
                # нижняя точка y cпрайта
                if self.RECT.y + self.RECT.height - 10 < block.y + block.height and self.RECT.y + self.RECT.height - 10 > block.y:
                    #если правая верхняя точка спрайта больше левой верхней точки спрайта, и если происходит колизия ректов спрайта и блока, то:
                    if self.RECT.x + self.RECT.width > block.x and self.RECT.colliderect(block):
                        self.CAN_MOVE_RIGHT = False
                        self.X -= 3
                        self.RECT.x -= 3
                        break
                    else:
                        self.CAN_MOVE_RIGHT = True
                else:
                    self.CAN_MOVE_RIGHT = True
    # Создаём функцию, которая определяет, столкнулся ли спрайт со стенкой слева, если да, то спрайт не может продолжать движение влево
    def can_move_left(self, list_rect):
        for block in list_rect:
            if self.DIRECTION == "L":
                # нижняя точка y cпрайта
                if self.RECT.y + self.RECT.height - 10 < block.y + block.height and self.RECT.y + self.RECT.height - 10 > block.y:
                    #если левая верхняя точка спрайта меньше правой верхней точки спрайта, и если происходит колизия ректов спрайта и блока, то:
                    if self.RECT.x < block.x + block.width and self.RECT.colliderect(block):
                        self.CAN_MOVE_LEFT = False
                        self.X += 3
                        self.RECT.x += 3
                        break
                    else:
                        self.CAN_MOVE_LEFT = True
                else:
                    self.CAN_MOVE_LEFT = True
    # Метод, що виконує анімацію спрайта під час руху вправо та вліво
    def animation(self):
        self.SPEED_ANIMATION += 1
        # Якщо залішок від ділення  значення self.SPEED_ANIMATION на 5 буде = 0, то буде задаватись новий номер зображення 
        if self.SPEED_ANIMATION % 5 == 0:
            if self.COUNT_IMG == 11:
                self.COUNT_IMG = 5
            self.NAME_IMAGE = f"images/player/{self.COUNT_IMG}.png"
            self.direction() # задаємо напрямок по горизонталі зображення 
            self.COUNT_IMG += 1 # задаємо наступний номер зображення
    # Метод, що задає напрямок для спрайта по горизонталі
    def direction(self):
        if self.DIRECTION == 'R':
            self.load_image()
        elif self.DIRECTION == 'L':
            self.load_image(direction=True)
    # Создаём функцию, которая отвечает за гравитацию (падение спрайта в низ)
    def gravity(self, list_rect):
        # 1. collidelist
        # 2. colliderect
        index = self.RECT.collidelist(list_rect)
        if not self.RECT.colliderect(list_rect[index]) and not self.PRESSED: 
            if self.Y < win_height - self.HEIGHT:
                self.Y += self.GRAVITY
                self.RECT.y = self.RECT.y + self.GRAVITY
                self.NAME_IMAGE = "images/player/6.png"
                self.direction() # задаємо напрямок по горизонталі зображення
    # Создаём функцию, которая позволяет спрайту совершить прыжок
    def jump(self, list_rect):
        event = pygame.key.get_pressed() 
        # Если нажата стрелочка вверх и спрайт не находится в состоянии прыжка, то флаг PRESSED становиться True
        if event[pygame.K_UP] and self.PLAYER_JUMP == False:
            self.PRESSED = True 
        #Если нажата стрелочка вверх и спрайт не находится в состоянии прыжка, то количество повторов основного цикла +1
        # если количество повторов основного цикла поделить на 2 и небудет никакого остатка
        # и количество повторов основного цикла меньше 35, то спрайт перемещается на 10 пикселей вверх (и его рект)
        if self.PRESSED:
            if self.COUNT_JUMP % 2 == 0 and self.COUNT_JUMP < 35:
                self.Y -= 10
                self.RECT.y -= 10 
            self.COUNT_JUMP += 1
        # Если количество повторов основного цикла больше или равно 35, то игрок находится в состоянии прыжка,
        # количество повторов осн. цикла = 0, флаг PRESSED = False
        if self.COUNT_JUMP >= 35:
            self.PLAYER_JUMP = True
            self.COUNT_JUMP = 0
            self.PRESSED = False
        # Если рект спрайта касается ректа платформы, то спрайт выходит из состояния прыжка, и он снова может прыгать
        index = self.RECT.collidelist(list_rect)
        if self.RECT.colliderect(list_rect[index]):
            self.PLAYER_JUMP = False
                
sprite = Sprite(
        width = 50,
        height = 75,
        x = 300,
        y = 100,
        name_image = "images/player/1.png",
        color= (255, 0, 0)
    )

sprite.RECT.width = 40
# sprite.RECT.height = 120
sprite.RECT.x = sprite.X + sprite.WIDTH // 2 - sprite.RECT.width // 2
# sprite.RECT.y = sprite.Y + sprite.HEIGHT // 2 - sprite.RECT.height // 2 
