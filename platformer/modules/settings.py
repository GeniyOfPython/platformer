import pygame
import os

pygame.init()

win_height = 800
win_width = 850

# 5. Створити функцію create_path, що знаходить абсолютний шлях до файлу.
# Застосовуємо модуль os.path та його методи abspath(), join()
def create_path():
    path_abs = os.path.abspath(__file__ + "/..")
    path_abs = path_abs.split("\\") 
    del path_abs[-1]
    path_abs = "\\".join(path_abs)
    return path_abs


class Settings:
    def __init__(self, x = None, y = None, width = None, height = None, name_image = None, color = None):
    # 7. Задати 7 властивостей:
        self.X = x
        self.Y = y
        self.WIDTH = width
        self.HEIGHT = height
        self.NAME_IMAGE = name_image
        self.IMAGE = None
        self.RECT = pygame.Rect(self.X, self.Y, self.WIDTH, self.HEIGHT) 
        self.COLOR = color
        if self.NAME_IMAGE:
            self.load_image()

    # 8. Створити метод завантаження зображення до властивості IMAGE
    def load_image(self, direction= False):
        # - створи змінну path, яка зберігає абсолютний шлях до файлу зображення, застосовуємо функцію create_path
        path_image = create_path()
        # - завантажити зображення до всластивості IMAGE
        path_image = os.path.join(path_image, self.NAME_IMAGE)
        # - трансформувати збережене в IMAGE зображення до розмірів,
        self.IMAGE = pygame.image.load(path_image)
        # що збережені у властивостях WIDTH, HEIGHT. Та зберегти повторно у властивості IMAGE.
        self.IMAGE = pygame.transform.scale(self.IMAGE, (self.WIDTH, self.HEIGHT))
        # повертаємо зображення спрайта по горизонталі 
        self.IMAGE = pygame.transform.flip(self.IMAGE,direction,False)

    def blit_sprite(self,win):
        # - застосовуємо метод blit() модуля pygame
        win.blit(self.IMAGE, (self.X,self.Y))
    
    def draw_rect(self, win):
        pygame.draw.rect(win, self.COLOR, self.RECT)