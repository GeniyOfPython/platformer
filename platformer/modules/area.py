import pygame
import os
import modules.settings as settings

win_height = 800
win_width = 850

area_w = 200
area_h = 50

list_area = [
    "0000",
    "0000",
    "0000",
    "0000",
    "1000",
    "1000",
    "0101",
    "0101",
    "0011"
]

list_create_area = []
list_rect = []
class Area(settings.Settings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
def create_area(level):
    x = 0
    y = 0
    for string in list_area:
        for el in string:
            if el == "1":
                area = Area(
                    x= x,
                    y= y,
                    width= area_w,
                    height= area_h,
                    color= (255, 165, 0)
                )
                list_create_area.append(area)
                list_rect.append(area.RECT)

            x += area_w
        x = 0
        y += area_h

create_area(list_area)





      

