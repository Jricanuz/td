import pygame as py
from math import sqrt, degrees, atan
from ast import literal_eval
from time import time
py.init()
py.font.init()
width = height = 750
screen = py.display.set_mode((width, height))
py.display.set_caption("Tower Defence")
fps = 60
white = (255, 255, 255)
black = (0, 0, 0)
class circle:
    def __init__(self, screen, cords, radius, image, alpha=127, colorkey=None):
        self.black, self.screen, self.radius, self.cords = (0, 0, 0), screen, radius, cords
        self.image = py.image.load(image)
        self.image = py.transform.scale(self.image, (self.radius*2, self.radius*2))
        self.image.set_alpha(alpha)
        if colorkey != None:
            self.image.set_colorkey(colorkey)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = cords
    def draw(self):
        self.screen.blit(self.image, self.image_rect)
    def collidepos(self, pos_colliding):
        distance = sqrt(pow((self.cords[0]-pos_colliding[0]), 2)+pow((self.cords[1]-pos_colliding[1]), 2))
        if self.radius >= distance:
            return True
        else:
            return False
    def colliderect(self, rect_colliding):
        points = [(rect_colliding.x, rect_colliding.y), (rect_colliding.x, rect_colliding.y+rect_colliding.height), (rect_colliding.x+rect_colliding.width, rect_colliding.y), (rect_colliding.x+rect_colliding.width, rect_colliding.y+rect_colliding.height), rect_colliding.center]
        for point in points:
            distance = sqrt(pow((self.cords[0]-point[0]), 2)+pow((self.cords[1]-point[1]), 2))
            if self.radius >= distance:
                return True
        return False
class Button:
    def __init__(self, screen, cords, size, image, command, argument=None, center=None, angle=0, colorkey=None, special=None):
        self.screen, self.size, self.clicked, self.command, self.argument, self.special, self.image = screen, size, False, command, argument, special, py.image.load(image)
        self.image = py.transform.scale(self.image, (size[0], size[1]))
        self.image = py.transform.rotate(self.image, angle)
        if colorkey != None:
            self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.x = cords[0]
        self.rect.y = cords[1]
        if center != None:
            self.rect.center = center
        self.special = special
        if self.special == "play_pause":
            self.clicked = True
    def draw(self, pos, pressed):
        if pressed[0] == 1 and not self.clicked and self.rect.collidepoint(pos):
            if self.argument != None:
                self.command(self.argument)
            else:
                self.command()
            self.clicked = True
        if pressed[0] == 0:
            self.clicked = False
        self.screen.blit(self.image, self.rect)
class level_map_page:
    def __init__(self, screen, map_1=None, map_2=None, map_3=None, map_4=None):
        self.black, self.white, self.screen, self.map_size, self.base_map_list, self.map_list, on, self.base_difficulty_list, self.difficulty_image_size, self.difficulty_list, dif_on, self.selecting_mode, self.map_for_mode, self.mode_clicked = (0, 0, 0), (255, 255, 255), screen, ((width//3), (height//3)), [map_1, map_2, map_3, map_4], [], 0, ["easy", "medium", "hard"], ((width-width//4), height//5), [], 0, False, None, True
        self.lock_img = py.image.load("lock.png")
        self.lock_img = py.transform.scale(self.lock_img, self.map_size)
        self.lock_rect = self.lock_img.get_rect()
        self.coming_soon_image = py.image.load("coming_soon.png")
        self.coming_soon_image = py.transform.scale(self.coming_soon_image, self.map_size)
        for map in self.base_map_list:
            on += 1
            rect = py.Rect((0, 0), self.map_size)
            if on % 2 == 1: rect.x = (width//7)+(width//100)
            else: rect.x = (width//2)+(width//30)
            if on > 2: rect.y = (height//2)+(height//8)
            else: rect.y = (height//4)
            if map != None:
                name = map[2]
                image = py.image.load(map[0])
                image = py.transform.scale(image, self.map_size)
                locked = map[1]
                self.map_list.append((name, image, rect, locked))
            else:
                self.map_list.append((False, self.coming_soon_image, rect))
        self.counter = 0
        for difficulty in self.base_difficulty_list:
            dif_on += 1
            image = py.image.load(f"{difficulty}_rect.png")
            image = py.transform.scale(image, self.difficulty_image_size)
            rect = image.get_rect()
            rect.center = (width/2, (height/4*dif_on)+height//10)
            self.difficulty_list.append((difficulty, image, rect))
        self.bg = py.image.load("level_select_bg.png")
        self.bg = py.transform.scale(self.bg, (width, height))
        self.bg_rect = self.bg.get_rect()
    def draw(self, pos, pressed):
        self.screen.blit(self.bg, self.bg_rect)
        if self.counter >= fps/3: self.can_start = True
        else: self.can_start = False
        if not self.selecting_mode:
            for map in self.map_list:
                if not map[0] == False:
                    if pressed[0] == 1 and map[2].collidepoint(pos) and not map[3] and self.can_start:
                        self.selecting_mode = True
                        self.map_for_mode = map[0]
                        break
                    if map[3]:
                        self.screen.blit(self.lock_img, map[2])
                    else:
                        self.screen.blit(map[1], map[2])
                else:
                    self.screen.blit(map[1], map[2])
        if not self.can_start: self.counter += 1
        if self.selecting_mode:
            self.draw_mode_selection(pos, pressed)
    def draw_mode_selection(self, pos, pressed):
        global save_vars
        self.screen.blit(self.bg, self.bg_rect)
        if pressed[0] == 0:
            self.mode_clicked = False
        for difficulty in self.difficulty_list:
            self.screen.blit(difficulty[1], difficulty[2])
            if pressed[0] == 1 and difficulty[2].collidepoint(pos) and not self.mode_clicked:
                start_map(self.map_for_mode, difficulty[0])
class charictar_in_menu:
    def __init__(self, image, cost, charictar_class, image_list, range):
        self.image, self.cost, self.charictar_class, self.image_list, self.range = py.image.load(image), cost, charictar_class, image_list, range
class ig_menu:
    global charictars_on_screen, money, health
    def __init__(self, screen, charictars, bg_img):
        self.white, self.screen, self.bg_img, self.charictars, self.charictars_full, self.charictar_size, number_on, self.image_for_mouse, self.placed, self.placing, self.just_placed, self.cost_text_size, self.range_img, self.red_range_img, self.money_size, self.health_img, self.down, self.last_down = (255, 255, 255), screen, py.image.load(bg_img), charictars, [], (width//10, (height//5)-(height//25)), 0, None, True, False, False, width//50, py.image.load("range.png"), py.image.load("red_range.png"), width//25, py.image.load("health.jpg"), False, False
        self.font, self.money_font =  py.font.SysFont("arial", self.cost_text_size), py.font.SysFont("arial", self.money_size)
        self.ig_play_button, self.ig_pause_button = circle(self.screen, (width-width//10, height-height//10), width//20, "play_button_ig.png", alpha=255, colorkey=self.white), circle(self.screen, (width-width//10, height-height//10), width//20, "pause_button_ig.png", alpha=255, colorkey=self.white)
        self.bg_img = py.transform.scale(self.bg_img, (width, height//5+1))
        self.bg_img.set_colorkey(white)
        self.bg_rect = self.bg_img.get_rect()
        self.bg_rect.x, self.bg_rect.y = 0, height-(height//5)-1
        for charictar in self.charictars:
            number_on += 1
            image = charictar.image
            image = py.transform.scale(image, self.charictar_size)
            rect = image.get_rect()
            rect.x = (width//10)*number_on
            rect.y = height-(height//5)+(height//50)
            cost = charictar.cost
            cost_text = self.font.render(f"${cost}", 1, self.white)
            cost_text_rect = cost_text.get_rect()
            cost_text_rect.center = (((width//10)*number_on)+(self.charictar_size[0]//2), height-(height//25))
            charictar_class = charictar.charictar_class
            image_list = charictar.image_list
            range = charictar.range
            self.charictars_full.append((image, rect, cost, charictar_class, image_list, cost_text, cost_text_rect, range))
        self.range_img.set_colorkey(self.white)
        self.range_img.set_alpha(127)
        self.red_range_img.set_colorkey(self.white)
        self.red_range_img.set_alpha(127)
        self.health_img = py.transform.scale(self.health_img, (width//25, height//25))
        self.health_img.set_colorkey(self.white)
        self.health_img_rect = self.health_img.get_rect()
        self.health_img_rect.x, self.health_img_rect.y = width-width//9+width//80, height//55
        self.money_text, self.health_text = self.money_font.render(f"${money}", 1, self.white), self.money_font.render(str(health), 1, self.white)
        self.money_rect, self.health_rect = self.money_text.get_rect(), self.health_text.get_rect()
        self.money_rect.x, self.money_rect.y, self.health_rect.x, self.health_rect.y = width//50, height//75, width-(len(str(health))*width//50)-(width//10), height//75
    def draw(self, paused, pos, pressed):
        index_on = -1
        self.get_first_enemy()
        for charictar in self.charictars_full:
            index_on += 1
            if charictar[1].collidepoint(pos) and pressed[0] == 1 and not self.placing and money >= charictar[2]:
                self.placed = False
                self.placing = True
                self.image_for_mouse = charictar[0]
                self.image_for_mouse = py.transform.scale(self.image_for_mouse, (width//30, height//30))
                self.rect_for_mouse = self.image_for_mouse.get_rect()
                self.rect_for_mouse.center = (pos[0], pos[1])
                self.charictar_index = index_on
        self.screen.blit(self.bg_img, self.bg_rect)
        self.last_down = self.down
        if paused:
            self.ig_pause_button.draw()
            if pressed[0] == 1:
                self.down = True
            if pressed[0] == 0:
                self.down = False
            if not self.down and self.last_down and self.ig_pause_button.collidepos(pos):
                unpause()
        elif not paused:
            self.ig_play_button.draw()
            if pressed[0] == 1:
                self.down = True
            if pressed[0] == 0:
                self.down = False
            if not self.down and self.last_down and self.ig_pause_button.collidepos(pos):
                pause()
        for charictar in self.charictars_full:
            self.screen.blit(charictar[0], charictar[1])
            self.screen.blit(charictar[5], charictar[6])
        if self.image_for_mouse != None:
            self.placeable = self.can_place(charictars_on_screen)
            if pressed[0] == 1 and self.placing and self.placeable:
                self.range_img = py.transform.scale(self.range_img, (self.charictars_full[self.charictar_index][7], self.charictars_full[self.charictar_index][7]))
                self.range_rect = self.range_img.get_rect()
                self.range_rect.center = (pos[0], pos[1])
                self.screen.blit(self.range_img, self.range_rect)
            elif pressed[0] == 1 and self.placing and not self.placeable:
                self.red_range_img = py.transform.scale(self.red_range_img, (self.charictars_full[self.charictar_index][7]*1.2, self.charictars_full[self.charictar_index][7]*1.2))
                self.red_range_rect = self.red_range_img.get_rect()
                self.red_range_rect.center = (pos[0], pos[1])
                self.screen.blit(self.red_range_img, self.red_range_rect)
            if pressed[0] == 1 and self.placing:
                self.rect_for_mouse.center = (pos[0], pos[1])
                self.screen.blit(self.image_for_mouse, self.rect_for_mouse)
            if pressed[0] == 0 and self.placing:
                self.placed = True
                self.placing = False
                self.just_placed = True
            else:
                self.just_placed = False
        self.money_text, self.health_text = self.money_font.render(f"${money}", 1, self.white), self.money_font.render(str(health), 1, self.white)
        self.health_rect.x = width-(len(str(health))*width//50)-(width//10)
        self.screen.blit(self.money_text, self.money_rect)
        self.screen.blit(self.health_text, self.health_rect)
        self.screen.blit(self.health_img, self.health_img_rect)
    def place_charictar(self):
        new_charictar = self.charictars_full[self.charictar_index][3](self.screen, py.mouse.get_pos(), self.charictars_full[self.charictar_index][4], self.charictars_full[self.charictar_index][7])
        return new_charictar
    def can_place(self, charictar_list):
        new_charictar = self.charictars_full[self.charictar_index][3](self.screen, py.mouse.get_pos(), self.charictars_full[self.charictar_index][4], self.charictars_full[self.charictar_index][7])
        yes = True
        if py.mouse.get_pos()[1] > height-(height//5):
            yes = False
        if yes:
            for rect in charictar_list:
                if rect.rect.colliderect(new_charictar.rect):
                    yes = False
                    break
        if yes:
            for rect in map.rect_list:
                if rect.colliderect(new_charictar.rect):
                    yes = False
                    break
        return yes
    def get_cost(self):
        return self.charictars_full[self.charictar_index][2]
    def get_first_enemy(self):
        global enemys, first_enemy
        first_enemy = None
        self.highest_pos = -1
        for enemy in enemys:
            try:
                if enemy.pos_on > self.highest_pos:
                    first_enemy = enemy
                    self.highest_pos = enemy.pos_on
            except AttributeError:
                pass
class triangle_charictar:
    def __init__(self, screen, cords, image_list, range_num, attack_speed=1):
        self.white, self.screen, self.cords, self.size, self.image_list, self.index, self.clicked, self.range_num, self.attack_speed, self.counter = (255, 255, 255), screen, cords, (width//30, height//30), [], 0, False, range_num, 120/attack_speed, 0
        for image in image_list:
            image1 = py.image.load(image)
            image1 = py.transform.scale(image1, self.size)
            image_rect = image1.get_rect()
            image_rect.center = cords
            self.image_list.append((image1, image_rect))
        self.rect = self.image_list[self.index][1]
        self.range = circle(self.screen, self.cords, self.range_num//2, "range.png", colorkey=self.white)
        self.projectile_image_list = load_image_list(["home_button.png"], colorkey=self.white)
    def draw(self, projectiles, paused, pos, pressed):
        collided_pos = self.rect.collidepoint(pos)
        if pressed[0] == 1 and not self.clicked and collided_pos:
            self.clicked = True
        if pressed[0] == 1 and self.clicked and not collided_pos:
            self.clicked = False
        if self.clicked:
           self.range.draw()
        if not paused:
            if self.counter > self.attack_speed:
                if self.find_enemy_in_range():
                    projectiles.append(projectile(self.screen, self.rect.center, self.projectile_image_list, 10, "straight", self.range, colorkey=self.white))
                    self.counter = 0
            self.counter += 1
        self.screen.blit(self.image_list[self.index][0],  self.image_list[self.index][1])
    def find_enemy_in_range(self):
        global enemys
        for enemy in enemys:
            try:
                if self.range.colliderect(enemy.rect):
                    return True
            except AttributeError:
                pass
        return False
class map:
    def __init__(self, data):
        self.rect_list, self.path_list = data[0], data[1]
class floating_text:
    red = (255, 0, 0)
    def __init__(self, screen, text, font="arial", color=red, size=int(width/10), speed=2):
        self.screen, self.font, self.color, self.alpha, self.speed = screen, py.font.SysFont(font, size), color, 255, speed
        self.text = self.font.render(text, 1, self.color)
        self.rect = self.text.get_rect()
        self.rect.center = ((width//2), (height//3))
    def draw(self):
        global floating_texts
        self.text.set_alpha(self.alpha)
        self.alpha -= 2*self.speed
        self.rect.y -= 1*self.speed
        self.screen.blit(self.text, self.rect)
        if self.rect.y < width/9.375:
            floating_texts.remove(self)
class base_enemy:
    green_image, grey_image, hp_bar_width, hp_bar_height = py.image.load("green_rect.png"), py.image.load("grey_rect.png"), width//25*1.4, height//150
    def __init__(self, screen, image_list, hp, size=(width//25*1.4, height//15*1.4), speed=1):
        self.screen, self.image_list, self.width, self.height, self.index, self.pos_on, self.speed, self.starting_hp, self.hp, self.counter, self.image_list = screen, [], size[0], size[1], 0, 0, speed, hp, hp, 0, []
        for image in image_list:
            image = py.transform.scale(image, (self.width, self.height))
            self.image_list.append(image)
        self.rect = self.image_list[0].get_rect()
    def draw(self, paused, map):
        global health, money, enemys
        self.image = self.image_list[self.index]
        self.rect.center = map.path_list[self.pos_on][1]
        if not paused:
            if not self.pos_on == len(map.path_list):
                if not self.pos_on + self.speed >= len(map.path_list):
                    self.pos_on += self.speed
                else:
                    self.pos_on = len(map.path_list)-1
                    enemys.remove(self)
                    health -= 1
                    return
        if self.hp <= 0:
            enemys.remove(self)
            money += 1
            return
        self.screen.blit(self.image, self.rect)
        if self.hp != self.starting_hp:
            self.green_part = self.hp_bar_width*(self.hp/self.starting_hp)
            self.grey_part = self.hp_bar_width-self.green_part
            self.green_image, self.grey_image = py.transform.scale(self.green_image, (self.green_part, self.hp_bar_height)), py.transform.scale(self.grey_image, (self.grey_part, self.hp_bar_height))
            self.screen.blit(self.green_image, (self.rect.x, self.rect.y-height//150))
            self.screen.blit(self.grey_image, (self.rect.x+self.green_part, self.rect.y-height//150))
class settings:
    def __init__(self, screen, image, settings_menu, colorkey=None):
        self.screen = screen
        self.image = py.image.load(image)
        self.image = py.transform.scale(self.image, (width//25, height//25))
        if colorkey != None:
            self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.x = width-width//20
        self.rect.y = height//75
        self.settings_menu = settings_menu
        self.clicked = False
        self.opened = False
    def draw(self, pos, pressed):
        global paused
        if self.opened:
            self.settings_menu.draw(pos, pressed)
        if pressed[0] == 1 and self.clicked == False and self.rect.collidepoint(pos):
            if not self.opened:
                paused = True
            self.opened = True
            self.clicked = True
        if pressed[0] == 0:
            self.clicked = False
        if pressed[0] == 1 and not self.rect.collidepoint(pos) and not self.settings_menu.bg_rect.collidepoint(pos):
            if self.opened:
                paused = False
            self.opened = False
        self.screen.blit(self.image, self.rect)
class settings_menu:
    global save_vars
    def __init__(self, screen, bg_image, colorkey=None):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.screen = screen
        self.bg_image = py.image.load(bg_image)
        self.bg_image = py.transform.scale(self.bg_image, (width//2, height//3))
        if colorkey != None:
            self.bg_image.set_colorkey(colorkey)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.center = (width//2, height//3)
        self.buttons = [Button(self.screen, (width//3, (height//2)-(height//50)), (width//20, height//20), "home_button.png", start_game, colorkey=self.white), Button(self.screen, (width-(width//3)-(width//20), (height//2)-(height//50)), (width//20, height//20), "continue_arrow.png", close_setttings_menu, colorkey=self.black)]
        self.switches = [switch(self.screen, (width/1.648351648351648, height/3.75), change_auto_play, starting_state=save_vars["auto_play"], text="Autoplay")]
    def draw(self, pos, pressed):
        self.screen.blit(self.bg_image, self.bg_rect)
        for button in self.buttons:
            button.draw(pos, pressed)
        for switch in self.switches:
            switch.draw(pos, pressed)
class switch:
    white = (255, 255, 255)
    def __init__(self, screen, cords, command, starting_state=False, size=(width//15, height//30), text=None, text_color=white):
        self.screen = screen
        self.cords = cords
        self.state = starting_state
        self.size = size
        self.command = command
        self.on_image = py.image.load("on_switch.png")
        self.on_image = py.transform.scale(self.on_image, self.size)
        self.off_image = py.image.load("off_switch.png")
        self.off_image = py.transform.scale(self.off_image, self.size)
        if self.state:
            self.image = self.on_image
        else:
            self.image = self.off_image
        self.rect = self.image.get_rect()
        self.rect.x = cords[0]
        self.rect.y = cords[1]
        self.clicked = True
        self.text_size = (self.size[0]+self.size[1])*2
        self.text = text
        if self.text != None:
            self.font = py.font.SysFont("arial", self.text_size//len(text))
            self.text = self.font.render(text, 1, text_color)
            self.text_rect = self.text.get_rect()
            self.text_rect.center = (self.cords[0]+(self.size[0]//2), self.cords[1]-(self.size[1]))
    def draw(self, pos, pressed):
        if self.state:
            self.image = self.on_image
        else:
            self.image = self.off_image
        if pressed[0] == 1 and self.clicked == False and self.rect.collidepoint(pos):
            self.command()
            self.state = not self.state
            self.clicked = True
        if pressed[0] == 0:
            self.clicked = False
        self.screen.blit(self.image, self.rect)
        if self.text != None:
            self.screen.blit(self.text, self.text_rect)
class projectile:
    def __init__(self, screen, cords, image_list, damage, path_type, base_range, size=(width//50, height//50), colorkey=None, speed=10):
        global enemys, projectiles
        self.screen, self.cords, self.image_list, self.width, self.height, self.index, self.damage, self.path_type, self.speed, self.base_range = screen, cords, [], size[0], size[1], 0, damage, path_type, speed, base_range
        self.target = self.get_target()
        for image in image_list:
            image = py.transform.scale(image, (self.width, self.height))
            self.image_list.append(image)
        self.rect = self.image_list[0].get_rect()
        self.rect.center = cords
        self.get_angle()
        self.actual_rect_cords = self.rect.center
    def draw(self, paused):
        global projectiles
        self.image = self.image_list[self.index]
        self.rect.center = self.actual_rect_cords
        self.cords = self.rect.center
        if not paused:
            if self.off_screen():
                projectiles.remove(self)
                return
            if self.check_hit():
                self.enemy_hit.hp -= self.damage
                projectiles.remove(self)
                return
            if self.path_type == "straight":
                self.forward(self.speed)
            elif self.path_type == "homing":
                self.get_angle()
                self.forward(self.speed)
        self.screen.blit(self.image, self.rect)
        #py.draw.polygon(self.screen, (0, 0, 0), [self.A, self.B, self.C])
    def check_hit(self):
        for enemy in enemys:
            try:
                if self.rect.colliderect(enemy.rect):
                    self.enemy_hit = enemy
                    return True
            except AttributeError:
                pass
        return False
    def off_screen(self):
        if not 0 < self.actual_rect_cords[0] < width or not 0 < self.actual_rect_cords[1] < height:
            return True
    def forward(self, steps):
        global angle_directory
        self.actual_rect_cords = (self.actual_rect_cords[0]+(angle_directory[self.angle][0]*steps), self.actual_rect_cords[1]+(angle_directory[self.angle][1]*steps))
    def get_quad(self):
        if self.target.rect.center[0] <= self.cords[0] and self.target.rect.center[1] <= self.cords[1]:
            return 2
        if self.target.rect.center[0] <= self.cords[0] and self.target.rect.center[1] >= self.cords[1]:
            return 3
        if self.target.rect.center[0] >= self.cords[0] and self.target.rect.center[1] <= self.cords[1]:
            return 1
        if self.target.rect.center[0] >= self.cords[0] and self.target.rect.center[1] >= self.cords[1]:
            return 4
    def get_angle(self):
        global first_enemy, enemys
        if not self.target in enemys:
            self.target = first_enemy
        if self.target != None:
            self.A = self.cords
            self.B = self.target.rect.center
            self.C = (self.target.rect.center[0], self.cords[1])
            self.AC = abs(self.A[0]-self.B[0])
            self.BC = abs(self.A[1]-self.B[1])
            if self.BC != 0 and self.AC != 0:
                self.angle =int(degrees(atan(self.BC/self.AC)))
                quad = self.get_quad()
                if quad == 1: pass
                elif quad == 2: self.angle = 180 - self.angle
                elif quad == 3: self.angle += 180
                elif quad == 4: self.angle = 360 - self.angle
                if self.angle != 0: self.angle -= 1
            else:
                if self.target.rect.center[1] < self.cords[1]:
                    self.angle = 89
                elif self.target.rect.center[0] < self.cords[0]:
                    self.angle = 179
                elif self.target.rect.center[1] > self.cords[1]:
                    self.angle = 269
                else:
                    self.angle = 359
    def get_target(self):
        global enemys
        highest_pos_in_range = -1
        target = None
        for enemy in enemys:
            if enemy.pos_on > highest_pos_in_range and self.base_range.collidepos(enemy.rect.center):
                target = enemy
                highest_pos_in_range = enemy.pos_on
        return target
class round:
    def __init__(self, data):
        self.data = data
        self.counter = 0
        self.done_making = False
        self.done = False
    def run(self):
        global paused, map, enemys, projectiles
        if not paused:
            if self.counter != len(self.data):
                if self.data[self.counter] != "-":
                    spawn_enemy(self.data[self.counter][0], self.data[self.counter][1], self.data[self.counter][2])
                self.counter += 1
            else:
                self.done_making = True
            if self.done_making and len(enemys) == 0 and len(projectiles) == 0:
                self.done = True
class full_game:
    def __init__(self, rounds):
        self.rounds = rounds
        self.number_of_rounds = len(self.rounds)
        self.round_on = 0
        self.did = False
    def run(self):
        global save_vars, paused, projectiles
        if not paused:
            if self.round_on != self.number_of_rounds:
                self.rounds[self.round_on].run()
                if self.rounds[self.round_on].done:
                    if save_vars["auto_play"]:
                        if not self.did:
                            unpause()
                            self.did = True
                    else:
                        if not self.did:
                            pause()
                            self.did = True
                    if not paused:
                        self.round_on += 1
                else:
                    self.did = False
def start_game():
    global screen_on, page_on, settings_wheel, pages, just_opened
    unpause()
    if not just_opened:
        for page in pages:
            page.counter = 0
            page.selecting_mode = False
    else:
        for page in pages:
            page.counter = fps
    settings_wheel.opened = False
    page_on = 1
    screen_on = "map_select"
    just_opened = False
def start_map(map, mode):
    global screen_on, money, starting_money, game_running, menu_ig, starting_health, health, enemys, map_1, charictars_on_screen, projectiles, mode_on
    enemys = []
    charictars_on_screen = []
    projectiles = []
    game_running = False
    menu_ig.game_running = False
    money = starting_money
    health = starting_health
    screen_on = map
    mode_on = mode
def draw_loading_screen():
    white = (255, 255, 255)
    black = (0, 0, 0)
    screen.fill(white)
    font = py.font.SysFont("arial", width//5)
    text = font.render("Loading...", 1, black)
    text_rect = text.get_rect()
    text_rect.center = (width//2, height//2)
    screen.blit(text, text_rect)
    py.display.update()
def draw_start_screen(start_text_1, start_text_1_cords, start_text_2, start_text_2_cords, start_button, floating_texts):
    pos, pressed = py.mouse.get_pos(), py.mouse.get_pressed()
    screen.fill(white)
    screen.blit(start_text_1, start_text_1_cords)
    screen.blit(start_text_2, start_text_2_cords)
    start_button.draw(pos, pressed)
    for text in floating_texts:
        text.draw()
    py.display.update()
def draw_map_select_screen(pages, page_on, right_arrow, left_arrow, floating_texts):
    pos, pressed = py.mouse.get_pos(), py.mouse.get_pressed()
    pages[page_on-1].draw(pos, pressed)
    if len(pages) > page_on:
        right_arrow.draw(pos, pressed)
    if page_on > 1:
        left_arrow.draw(pos, pressed)
    for text in floating_texts:
        text.draw()
    py.display.update()
def draw_map_screen(map_img, map_rect, menu_ig, charictars_on_screen, floating_texts, enemys, settings_wheel, projectiles):
    global paused, map
    pos, pressed = py.mouse.get_pos(), py.mouse.get_pressed()
    screen.blit(map_img, map_rect)
    for enemy in enemys:
        enemy.draw(paused, map)
    for charictar in charictars_on_screen:
        charictar.draw(projectiles, paused, pos, pressed)
    for pro in projectiles:
        pro.draw(paused)
    menu_ig.draw(paused, pos, pressed)
    settings_wheel.draw(pos, pressed)
    for text in floating_texts:
        text.draw()
    py.display.update()
def page_on_add():
    global page_on
    page_on += 1
def page_on_subtract():
    global page_on
    page_on -= 1
def close_setttings_menu():
    global settings_wheel
    settings_wheel.opened = False
def change_auto_play():
    global save_vars
    save_vars["auto_play"] = not save_vars["auto_play"]
def pause():
    global paused
    paused = True
def unpause():
    global paused
    paused = False
def save():
    global save_vars
    with open("td_save.txt", "r+") as f:
        f.truncate(0)
        f.write(str(save_vars))
def spawn_enemy(type, hp, image_list):
    global enemys
    enemys.append(eval(type)(screen, image_list, hp))
def init_save_vars():
    global save_vars
    try:
        with open("td_save.txt", "r") as f:
            lines = f.readlines()
            save_vars = literal_eval(lines[0])
    except IOError:
        with open("td_save.txt", "w") as f:
            pass
        save_vars = {"auto_play": False, "map_1_modes_complete": {"easy": False, "medium": False, "hard": False}, "map_2_modes_complete": {"easy": False, "medium": False, "hard": False}}
def load_image_list(image_list, colorkey=None):
    full_image_list = []
    for image in image_list:
            image = py.image.load(image)
            image.convert()
            if colorkey != None:
                image.set_colorkey(colorkey)
            full_image_list.append(image)
    return full_image_list
def main():
    global screen_on, pages, page_on, game_running, menu_ig, charictars_on_screen, money, starting_money, settings_wheel, health, starting_health, enemys, save_vars, map_1, map_2, projectiles, charictars_on_screen, paused, floating_texts, just_opened, map, angle_directory
    draw_loading_screen()
    init_save_vars()
    just_opened = True
    white = (255, 255, 255)
    running = 1
    clock = py.time.Clock()
    money = 0
    health = 0
    starting_money = 100000
    starting_health = 100
    screen_on = "opening"
    start_font = py.font.SysFont("comicsans", int(width/7.5))
    start_text_1 = start_font.render("Tower", 1, black)
    start_text_2 = start_font.render("Defence", 1, black)
    start_text_1_cords = ((width//4+width//25), (height//10))
    start_text_2_cords = ((width//4+width//50), (height//4))
    start_button_size = (100, 50)
    start_button_cords = (((width//2)-start_button_size[0]//2),(height-(height//3)))
    start_button = Button(screen, start_button_cords, start_button_size, "play_button.png", start_game)
    pages = [level_map_page(screen, ("map_1_bg.png", False, "map_1"), ("map_2_bg.png", False, "map_2"))]
    page_on = 1
    right_arrow = Button(screen, (0, 0), (width//15, height//15), "arrow.png", page_on_add, center=((width-(width//20)), height//2), angle=-90)
    left_arrow = Button(screen, (0, 0), (width//15, height//15), "arrow.png", page_on_subtract, center=((width//20), height//2), angle=90)
    triangle_image_list = ["arrow.png"]
    charictars = [charictar_in_menu("arrow.png", 500, triangle_charictar, triangle_image_list, 500), charictar_in_menu("arrow.png", 5000, triangle_charictar, triangle_image_list, 100)]
    charictars_on_screen = []
    game_running = False
    map_1_bg_img = py.image.load("map_1_bg.png")
    map_1_bg_img = py.transform.scale(map_1_bg_img, (width, height-(height//5)))
    map_1_bg_rect = map_1_bg_img.get_rect()
    map_1 = map(
    ([py.Rect((0, 570), (5, 30)), py.Rect((5, 565), (5, 35)), py.Rect((45, 575), (5, 30)), py.Rect((50, 140), (5, 15)), py.Rect((55, 135), (5, 20)), py.Rect((60, 575), (5, 30)), py.Rect((65, 570), (5, 35)), py.Rect((70, 460), (5, 5)), py.Rect((70, 565), (5, 40)), py.Rect((75, 455), (5, 10)), py.Rect((85, 130), (5, 25)), py.Rect((90, 135), (5, 20)), py.Rect((90, 455), (5, 10)), py.Rect((95, 140), (5, 10)), py.Rect((100, 565), (5, 35)), py.Rect((105, 570), (5, 30)), py.Rect((285, 15), (5, 60)), py.Rect((315, 560), (5, 10)), py.Rect((320, 5), (5, 35)), py.Rect((320, 555), (5, 15)), py.Rect((325, 5), (5, 30)), py.Rect((330, 10), (5, 5)), py.Rect((330, 20), (5, 15)), py.Rect((335, 555), (5, 15)), py.Rect((360, 575), (5, 20)), py.Rect((365, 570), (5, 30)), py.Rect((370, 565), (5, 35)), py.Rect((405, 570), (5, 35)), py.Rect((445, 580), (5, 25)), py.Rect((450, 210), (5, 15)), py.Rect((455, 205), (5, 20)), py.Rect((470, 195), (5, 35)), py.Rect((490, 200), (5, 35)), py.Rect((495, 205), (5, 30)), py.Rect((665, 35), (5, 20)), py.Rect((670, 35), (5, 25)), py.Rect((675, 30), (5, 35)), py.Rect((680, 25), (5, 45)), py.Rect((685, 20), (5, 50)), py.Rect((700, 25), (5, 30)), py.Rect((700, 60), (5, 10)), py.Rect((705, 20), (5, 35)), py.Rect((710, 15), (5, 40)), py.Rect((715, 10), (5, 45)), py.Rect((740, 15), (5, 35)), py.Rect((745, 20), (5, 30)), py.Rect((35, 565), (10, 40)), py.Rect((50, 585), (10, 20)), py.Rect((60, 130), (10, 25)), py.Rect((75, 560), (10, 45)), py.Rect((80, 450), (10, 15)), py.Rect((230, 25), (10, 25)), py.Rect((265, 20), (10, 45)), py.Rect((275, 25), (10, 50)), py.Rect((290, 10), (10, 65)), py.Rect((300, 5), (10, 60)), py.Rect((310, 5), (10, 40)), py.Rect((325, 550), (10, 20)), py.Rect((375, 560), (10, 45)), py.Rect((460, 200), (10, 25)), py.Rect((690, 25), (10, 45)), py.Rect((720, 10), (10, 50)), py.Rect((730, 15), (10, 45)), py.Rect((70, 125), (15, 30)), py.Rect((85, 565), (15, 40)), py.Rect((385, 565), (20, 40)), py.Rect((475, 195), (15, 40)), py.Rect((10, 560), (25, 45)), py.Rect((240, 15), (25, 45)), py.Rect((410, 575), (35, 30)), py.Rect((100, 125), (50, 235)), py.Rect((250, 125), (50, 300)), py.Rect((450, 245), (50, 180)), py.Rect((0, 305), (100, 55)), py.Rect((150, 125), (100, 55)), py.Rect((300, 365), (150, 60)), py.Rect((500, 245), (250, 60))], [(0, (2.5, 327.5)), (1, (5.0, 327.5)), (2, (7.5, 327.5)), (3, (10.0, 327.5)), (4, (12.5, 327.5)), (5, (15.0, 327.5)), (6, (17.5, 327.5)), (7, (20.0, 327.5)), (8, (22.5, 327.5)), (9, (25.0, 327.5)), (10, (27.5, 327.5)), (11, (30.0, 327.5)), (12, (32.5, 327.5)), (13, (35.0, 327.5)), (14, (37.5, 327.5)), (15, (40.0, 327.5)), (16, (42.5, 327.5)), (17, (45.0, 327.5)), (18, (47.5, 327.5)), (19, (50.0, 327.5)), (20, (52.5, 327.5)), (21, (55.0, 327.5)), (22, (57.5, 327.5)), (23, (60.0, 327.5)), (24, (62.5, 327.5)), (25, (65.0, 327.5)), (26, (67.5, 327.5)), (27, (70.0, 327.5)), (28, (72.5, 327.5)), (29, (75.0, 327.5)), (30, (77.5, 327.5)), (31, (80.0, 327.5)), (32, (82.5, 327.5)), (33, (85.0, 327.5)), (34, (87.5, 327.5)), (35, (90.0, 327.5)), (36, (92.5, 327.5)), (37, (95.0, 327.5)), (38, (97.5, 327.5)), (39, (100.0, 327.5)), (40, (102.5, 327.5)), (41, (105.0, 327.5)), (42, (107.5, 327.5)), (43, (110.0, 327.5)), (44, (112.5, 327.5)), (45, (115.0, 327.5)), (46, (117.5, 327.5)), (47, (120.0, 327.5)), (48, (122.5, 327.5)), (49, (125.0, 327.5)), (50, (127.5, 327.5)), (51, (127.5, 325.0)), (52, (127.5, 322.5)), (53, (127.5, 320.0)), (54, (127.5, 317.5)), (55, (127.5, 315.0)), (56, (127.5, 312.5)), (57, (127.5, 310.0)), (58, (127.5, 307.5)), (59, (127.5, 305.0)), (60, (127.5, 302.5)), (61, (127.5, 300.0)), (62, (127.5, 297.5)), (63, (127.5, 295.0)), (64, (127.5, 292.5)), (65, (127.5, 290.0)), (66, (127.5, 287.5)), (67, (127.5, 285.0)), (68, (127.5, 282.5)), (69, (127.5, 280.0)), (70, (127.5, 277.5)), (71, (127.5, 275.0)), (72, (127.5, 272.5)), (73, (127.5, 270.0)), (74, (127.5, 267.5)), (75, (127.5, 265.0)), (76, (127.5, 262.5)), (77, (127.5, 260.0)), (78, (127.5, 257.5)), (79, (127.5, 255.0)), (80, (127.5, 252.5)), (81, (127.5, 250.0)), (82, (127.5, 247.5)), (83, (127.5, 245.0)), (84, (127.5, 242.5)), (85, (127.5, 240.0)), (86, (127.5, 237.5)), (87, (127.5, 235.0)), (88, (127.5, 232.5)), (89, (127.5, 230.0)), (90, (127.5, 227.5)), (91, (127.5, 225.0)), (92, (127.5, 222.5)), (93, (127.5, 220.0)), (94, (127.5, 217.5)), (95, (127.5, 215.0)), (96, (127.5, 212.5)), (97, (127.5, 210.0)), (98, (127.5, 207.5)), (99, (127.5, 205.0)), (100, (127.5, 202.5)), (101, (127.5, 200.0)), (102, (127.5, 197.5)), (103, (127.5, 195.0)), (104, (127.5, 192.5)), (105, (127.5, 190.0)), (106, (127.5, 187.5)), (107, (127.5, 185.0)), (108, (127.5, 182.5)), (109, (127.5, 180.0)), (110, (127.5, 177.5)), (111, (127.5, 175.0)), (112, (127.5, 172.5)), (113, (127.5, 170.0)), (114, (127.5, 167.5)), (115, (127.5, 165.0)), (116, (127.5, 162.5)), (117, (127.5, 160.0)), (118, (127.5, 157.5)), (119, (127.5, 155.0)), (120, (127.5, 152.5)), (121, (127.5, 150.0)), (122, (127.5, 147.5)), (123, (130.0, 147.5)), (124, (132.5, 147.5)), (125, (135.0, 147.5)), (126, (137.5, 147.5)), (127, (140.0, 147.5)), (128, (142.5, 147.5)), (129, (145.0, 147.5)), (130, (147.5, 147.5)), (131, (150.0, 147.5)), (132, (152.5, 147.5)), (133, (155.0, 147.5)), (134, (157.5, 147.5)), (135, (160.0, 147.5)), (136, (162.5, 147.5)), (137, (165.0, 147.5)), (138, (167.5, 147.5)), (139, (170.0, 147.5)), (140, (172.5, 147.5)), (141, (175.0, 147.5)), (142, (177.5, 147.5)), (143, (180.0, 147.5)), (144, (182.5, 147.5)), (145, (185.0, 147.5)), (146, (187.5, 147.5)), (147, (190.0, 147.5)), (148, (192.5, 147.5)), (149, (195.0, 147.5)), (150, (197.5, 147.5)), (151, (200.0, 147.5)), (152, (202.5, 147.5)), (153, (205.0, 147.5)), (154, (207.5, 147.5)), (155, (210.0, 147.5)), (156, (212.5, 147.5)), (157, (215.0, 147.5)), (158, (217.5, 147.5)), (159, (220.0, 147.5)), (160, (222.5, 147.5)), (161, (225.0, 147.5)), (162, (227.5, 147.5)), (163, (230.0, 147.5)), (164, (232.5, 147.5)), (165, (235.0, 147.5)), (166, (237.5, 147.5)), (167, (240.0, 147.5)), (168, (242.5, 147.5)), (169, (245.0, 147.5)), (170, (247.5, 147.5)), (171, (250.0, 147.5)), (172, (252.5, 147.5)), (173, (255.0, 147.5)), (174, (257.5, 147.5)), (175, (260.0, 147.5)), (176, (262.5, 147.5)), (177, (265.0, 147.5)), (178, (267.5, 147.5)), (179, (270.0, 147.5)), (180, (272.5, 147.5)), (181, (272.5, 150.0)), (182, (272.5, 152.5)), (183, (272.5, 155.0)), (184, (272.5, 157.5)), (185, (272.5, 160.0)), (186, (272.5, 162.5)), (187, (272.5, 165.0)), (188, (272.5, 167.5)), (189, (272.5, 170.0)), (190, (272.5, 172.5)), (191, (272.5, 175.0)), (192, (272.5, 177.5)), (193, (272.5, 180.0)), (194, (272.5, 182.5)), (195, (272.5, 185.0)), (196, (272.5, 187.5)), (197, (272.5, 190.0)), (198, (272.5, 192.5)), (199, (272.5, 195.0)), (200, (272.5, 197.5)), (201, (272.5, 200.0)), (202, (272.5, 202.5)), (203, (272.5, 205.0)), (204, (272.5, 207.5)), (205, (272.5, 210.0)), (206, (272.5, 212.5)), (207, (272.5, 215.0)), (208, (272.5, 217.5)), (209, (272.5, 220.0)), (210, (272.5, 222.5)), (211, (272.5, 225.0)), (212, (272.5, 227.5)), (213, (272.5, 230.0)), (214, (272.5, 232.5)), (215, (272.5, 235.0)), (216, (272.5, 237.5)), (217, (272.5, 240.0)), (218, (272.5, 242.5)), (219, (272.5, 245.0)), (220, (272.5, 247.5)), (221, (272.5, 250.0)), (222, (272.5, 252.5)), (223, (272.5, 255.0)), (224, (272.5, 257.5)), (225, (272.5, 260.0)), (226, (272.5, 262.5)), (227, (272.5, 265.0)), (228, (272.5, 267.5)), (229, (272.5, 270.0)), (230, (272.5, 272.5)), (231, (272.5, 275.0)), (232, (272.5, 277.5)), (233, (272.5, 280.0)), (234, (272.5, 282.5)), (235, (272.5, 285.0)), (236, (272.5, 287.5)), (237, (272.5, 290.0)), (238, (272.5, 292.5)), (239, (272.5, 295.0)), (240, (272.5, 297.5)), (241, (272.5, 300.0)), (242, (272.5, 302.5)), (243, (272.5, 305.0)), (244, (272.5, 307.5)), (245, (272.5, 310.0)), (246, (272.5, 312.5)), (247, (272.5, 315.0)), (248, (272.5, 317.5)), (249, (272.5, 320.0)), (250, (272.5, 322.5)), (251, (272.5, 325.0)), (252, (272.5, 327.5)), (253, (272.5, 330.0)), (254, (272.5, 332.5)), (255, (272.5, 335.0)), (256, (272.5, 337.5)), (257, (272.5, 340.0)), (258, (272.5, 342.5)), (259, (272.5, 345.0)), (260, (272.5, 347.5)), (261, (272.5, 350.0)), (262, (272.5, 352.5)), (263, (272.5, 355.0)), (264, (272.5, 357.5)), (265, (272.5, 360.0)), (266, (272.5, 362.5)), (267, (272.5, 365.0)), (268, (272.5, 367.5)), (269, (272.5, 370.0)), (270, (272.5, 372.5)), (271, (272.5, 375.0)), (272, (272.5, 377.5)), (273, (272.5, 380.0)), (274, (272.5, 382.5)), (275, (272.5, 385.0)), (276, (272.5, 387.5)), (277, (275.0, 387.5)), (278, (277.5, 387.5)), (279, (280.0, 387.5)), (280, (282.5, 387.5)), (281, (285.0, 387.5)), (282, (287.5, 387.5)), (283, (290.0, 387.5)), (284, (292.5, 387.5)), (285, (295.0, 387.5)), (286, (297.5, 387.5)), (287, (300.0, 387.5)), (288, (302.5, 387.5)), (289, (305.0, 387.5)), (290, (307.5, 387.5)), (291, (310.0, 387.5)), (292, (312.5, 387.5)), (293, (315.0, 387.5)), (294, (317.5, 387.5)), (295, (320.0, 387.5)), (296, (322.5, 387.5)), (297, (325.0, 387.5)), (298, (327.5, 387.5)), (299, (330.0, 387.5)), (300, (332.5, 387.5)), (301, (335.0, 387.5)), (302, (337.5, 387.5)), (303, (340.0, 387.5)), (304, (342.5, 387.5)), (305, (345.0, 387.5)), (306, (347.5, 387.5)), (307, (350.0, 387.5)), (308, (352.5, 387.5)), (309, (355.0, 387.5)), (310, (357.5, 387.5)), (311, (360.0, 387.5)), (312, (362.5, 387.5)), (313, (365.0, 387.5)), (314, (367.5, 387.5)), (315, (370.0, 387.5)), (316, (372.5, 387.5)), (317, (375.0, 387.5)), (318, (377.5, 387.5)), (319, (380.0, 387.5)), (320, (382.5, 387.5)), (321, (385.0, 387.5)), (322, (387.5, 387.5)), (323, (390.0, 387.5)), (324, (392.5, 387.5)), (325, (395.0, 387.5)), (326, (397.5, 387.5)), (327, (400.0, 387.5)), (328, (402.5, 387.5)), (329, (405.0, 387.5)), (330, (407.5, 387.5)), (331, (410.0, 387.5)), (332, (412.5, 387.5)), (333, (415.0, 387.5)), (334, (417.5, 387.5)), (335, (420.0, 387.5)), (336, (422.5, 387.5)), (337, (425.0, 387.5)), (338, (427.5, 387.5)), (339, (430.0, 387.5)), (340, (432.5, 387.5)), (341, (435.0, 387.5)), (342, (437.5, 387.5)), (343, (440.0, 387.5)), (344, (442.5, 387.5)), (345, (445.0, 387.5)), (346, (447.5, 387.5)), (347, (450.0, 387.5)), (348, (452.5, 387.5)), (349, (455.0, 387.5)), (350, (457.5, 387.5)), (351, (460.0, 387.5)), (352, (462.5, 387.5)), (353, (465.0, 387.5)), (354, (467.5, 387.5)), (355, (470.0, 387.5)), (356, (472.5, 387.5)), (357, (475.0, 387.5)), (358, (477.5, 387.5)), (359, (477.5, 385.0)), (360, (477.5, 382.5)), (361, (477.5, 380.0)), (362, (477.5, 377.5)), (363, (477.5, 375.0)), (364, (477.5, 372.5)), (365, (477.5, 370.0)), (366, (477.5, 367.5)), (367, (477.5, 365.0)), (368, (477.5, 362.5)), (369, (477.5, 360.0)), (370, (477.5, 357.5)), (371, (477.5, 355.0)), (372, (477.5, 352.5)), (373, (477.5, 350.0)), (374, (477.5, 347.5)), (375, (477.5, 345.0)), (376, (477.5, 342.5)), (377, (477.5, 340.0)), (378, (477.5, 337.5)), (379, (477.5, 335.0)), (380, (477.5, 332.5)), (381, (477.5, 330.0)), (382, (477.5, 327.5)), (383, (477.5, 325.0)), (384, (477.5, 322.5)), (385, (477.5, 320.0)), (386, (477.5, 317.5)), (387, (477.5, 315.0)), (388, (477.5, 312.5)), (389, (477.5, 310.0)), (390, (477.5, 307.5)), (391, (477.5, 305.0)), (392, (477.5, 302.5)), (393, (477.5, 300.0)), (394, (477.5, 297.5)), (395, (477.5, 295.0)), (396, (477.5, 292.5)), (397, (477.5, 290.0)), (398, (477.5, 287.5)), (399, (477.5, 285.0)), (400, (477.5, 282.5)), (401, (477.5, 280.0)), (402, (477.5, 277.5)), (403, (477.5, 275.0)), (404, (477.5, 272.5)), (405, (480.0, 272.5)), (406, (482.5, 272.5)), (407, (485.0, 272.5)), (408, (487.5, 272.5)), (409, (490.0, 272.5)), (410, (492.5, 272.5)), (411, (495.0, 272.5)), (412, (497.5, 272.5)), (413, (500.0, 272.5)), (414, (502.5, 272.5)), (415, (505.0, 272.5)), (416, (507.5, 272.5)), (417, (510.0, 272.5)), (418, (512.5, 272.5)), (419, (515.0, 272.5)), (420, (517.5, 272.5)), (421, (520.0, 272.5)), (422, (522.5, 272.5)), (423, (525.0, 272.5)), (424, (527.5, 272.5)), (425, (530.0, 272.5)), (426, (532.5, 272.5)), (427, (535.0, 272.5)), (428, (537.5, 272.5)), (429, (540.0, 272.5)), (430, (542.5, 272.5)), (431, (545.0, 272.5)), (432, (547.5, 272.5)), (433, (550.0, 272.5)), (434, (552.5, 272.5)), (435, (555.0, 272.5)), (436, (557.5, 272.5)), (437, (560.0, 272.5)), (438, (562.5, 272.5)), (439, (565.0, 272.5)), (440, (567.5, 272.5)), (441, (570.0, 272.5)), (442, (572.5, 272.5)), (443, (575.0, 272.5)), (444, (577.5, 272.5)), (445, (580.0, 272.5)), (446, (582.5, 272.5)), (447, (585.0, 272.5)), (448, (587.5, 272.5)), (449, (590.0, 272.5)), (450, (592.5, 272.5)), (451, (595.0, 272.5)), (452, (597.5, 272.5)), (453, (600.0, 272.5)), (454, (602.5, 272.5)), (455, (605.0, 272.5)), (456, (607.5, 272.5)), (457, (610.0, 272.5)), (458, (612.5, 272.5)), (459, (615.0, 272.5)), (460, (617.5, 272.5)), (461, (620.0, 272.5)), (462, (622.5, 272.5)), (463, (625.0, 272.5)), (464, (627.5, 272.5)), (465, (630.0, 272.5)), (466, (632.5, 272.5)), (467, (635.0, 272.5)), (468, (637.5, 272.5)), (469, (640.0, 272.5)), (470, (642.5, 272.5)), (471, (645.0, 272.5)), (472, (647.5, 272.5)), (473, (650.0, 272.5)), (474, (652.5, 272.5)), (475, (655.0, 272.5)), (476, (657.5, 272.5)), (477, (660.0, 272.5)), (478, (662.5, 272.5)), (479, (665.0, 272.5)), (480, (667.5, 272.5)), (481, (670.0, 272.5)), (482, (672.5, 272.5)), (483, (675.0, 272.5)), (484, (677.5, 272.5)), (485, (680.0, 272.5)), (486, (682.5, 272.5)), (487, (685.0, 272.5)), (488, (687.5, 272.5)), (489, (690.0, 272.5)), (490, (692.5, 272.5)), (491, (695.0, 272.5)), (492, (697.5, 272.5)), (493, (700.0, 272.5)), (494, (702.5, 272.5)), (495, (705.0, 272.5)), (496, (707.5, 272.5)), (497, (710.0, 272.5)), (498, (712.5, 272.5)), (499, (715.0, 272.5)), (500, (717.5, 272.5)), (501, (720.0, 272.5)), (502, (722.5, 272.5)), (503, (725.0, 272.5)), (504, (727.5, 272.5)), (505, (730.0, 272.5)), (506, (732.5, 272.5)), (507, (735.0, 272.5)), (508, (737.5, 272.5)), (509, (740.0, 272.5)), (510, (742.5, 272.5)), (511, (745.0, 272.5))])
)
    map_2 = map(
    ([py.Rect((180, 455), (5, 120)), py.Rect((185, 445), (5, 135)), py.Rect((190, 440), (5, 145)), py.Rect((195, 435), (5, 150)), py.Rect((200, 135), (5, 210)), py.Rect((205, 130), (5, 215)), py.Rect((225, 430), (5, 55)), py.Rect((225, 530), (5, 55)), py.Rect((235, 125), (5, 215)), py.Rect((240, 125), (5, 205)), py.Rect((245, 125), (5, 195)), py.Rect((350, 425), (5, 55)), py.Rect((390, 130), (5, 345)), py.Rect((395, 135), (5, 335)), py.Rect((430, 5), (5, 35)), py.Rect((435, 5), (5, 40)), py.Rect((435, 235), (5, 150)), py.Rect((440, 230), (5, 165)), py.Rect((480, 345), (5, 55)), py.Rect((595, 5), (5, 50)), py.Rect((600, 5), (5, 55)), py.Rect((615, 350), (5, 230)), py.Rect((620, 355), (5, 220)), py.Rect((625, 360), (5, 210)), py.Rect((635, 5), (5, 265)), py.Rect((640, 5), (5, 260)), py.Rect((645, 20), (5, 240)), py.Rect((200, 430), (25, 155)), py.Rect((210, 125), (25, 220)), py.Rect((355, 125), (35, 355)), py.Rect((445, 225), (35, 175)), py.Rect((585, 350), (30, 235)), py.Rect((605, 5), (30, 270)), py.Rect((230, 430), (120, 50)), py.Rect((250, 125), (105, 50)), py.Rect((440, 5), (155, 45)), py.Rect((480, 225), (125, 50)), py.Rect((485, 350), (100, 50)), py.Rect((0, 290), (200, 55)), py.Rect((230, 535), (355, 50))], [(0, (2.5, 312.5)), (1, (5.0, 312.5)), (2, (7.5, 312.5)), (3, (10.0, 312.5)), (4, (12.5, 312.5)), (5, (15.0, 312.5)), (6, (17.5, 312.5)), (7, (20.0, 312.5)), (8, (22.5, 312.5)), (9, (25.0, 312.5)), (10, (27.5, 312.5)), (11, (30.0, 312.5)), (12, (32.5, 312.5)), (13, (35.0, 312.5)), (14, (37.5, 312.5)), (15, (40.0, 312.5)), (16, (42.5, 312.5)), (17, (45.0, 312.5)), (18, (47.5, 312.5)), (19, (50.0, 312.5)), (20, (52.5, 312.5)), (21, (55.0, 312.5)), (22, (57.5, 312.5)), (23, (60.0, 312.5)), (24, (62.5, 312.5)), (25, (65.0, 312.5)), (26, (67.5, 312.5)), (27, (70.0, 312.5)), (28, (72.5, 312.5)), (29, (75.0, 312.5)), (30, (77.5, 312.5)), (31, (80.0, 312.5)), (32, (82.5, 312.5)), (33, (85.0, 312.5)), (34, (87.5, 312.5)), (35, (90.0, 312.5)), (36, (92.5, 312.5)), (37, (95.0, 312.5)), (38, (97.5, 312.5)), (39, (100.0, 312.5)), (40, (102.5, 312.5)), (41, (105.0, 312.5)), (42, (107.5, 312.5)), (43, (110.0, 312.5)), (44, (112.5, 312.5)), (45, (115.0, 312.5)), (46, (117.5, 312.5)), (47, (120.0, 312.5)), (48, (122.5, 312.5)), (49, (125.0, 312.5)), (50, (127.5, 312.5)), (51, (130.0, 312.5)), (52, (132.5, 312.5)), (53, (135.0, 312.5)), (54, (137.5, 312.5)), (55, (140.0, 312.5)), (56, (142.5, 312.5)), (57, (145.0, 312.5)), (58, (147.5, 312.5)), (59, (150.0, 312.5)), (60, (152.5, 312.5)), (61, (155.0, 312.5)), (62, (157.5, 312.5)), (63, (160.0, 312.5)), (64, (162.5, 312.5)), (65, (165.0, 312.5)), (66, (167.5, 312.5)), (67, (170.0, 312.5)), (68, (172.5, 312.5)), (69, (175.0, 312.5)), (70, (177.5, 312.5)), (71, (180.0, 312.5)), (72, (182.5, 312.5)), (73, (185.0, 312.5)), (74, (187.5, 312.5)), (75, (190.0, 312.5)), (76, (192.5, 312.5)), (77, (195.0, 312.5)), (78, (197.5, 312.5)), (79, (200.0, 312.5)), (80, (202.5, 312.5)), (81, (205.0, 312.5)), (82, (207.5, 312.5)), (83, (210.0, 312.5)), (84, (212.5, 312.5)), (85, (215.0, 312.5)), (86, (217.5, 312.5)), (87, (220.0, 312.5)), (88, (222.5, 312.5)), (89, (222.5, 310.0)), (90, (222.5, 307.5)), (91, (222.5, 305.0)), (92, (222.5, 302.5)), (93, (222.5, 300.0)), (94, (222.5, 297.5)), (95, (222.5, 295.0)), (96, (222.5, 292.5)), (97, (222.5, 290.0)), (98, (222.5, 287.5)), (99, (222.5, 285.0)), (100, (222.5, 282.5)), (101, (222.5, 280.0)), (102, (222.5, 277.5)), (103, (222.5, 275.0)), (104, (222.5, 272.5)), (105, (222.5, 270.0)), (106, (222.5, 267.5)), (107, (222.5, 265.0)), (108, (222.5, 262.5)), (109, (222.5, 260.0)), (110, (222.5, 257.5)), (111, (222.5, 255.0)), (112, (222.5, 252.5)), (113, (222.5, 250.0)), (114, (222.5, 247.5)), (115, (222.5, 245.0)), (116, (222.5, 242.5)), (117, (222.5, 240.0)), (118, (222.5, 237.5)), (119, (222.5, 235.0)), (120, (222.5, 232.5)), (121, (222.5, 230.0)), (122, (222.5, 227.5)), (123, (222.5, 225.0)), (124, (222.5, 222.5)), (125, (222.5, 220.0)), (126, (222.5, 217.5)), (127, (222.5, 215.0)), (128, (222.5, 212.5)), (129, (222.5, 210.0)), (130, (222.5, 207.5)), (131, (222.5, 205.0)), (132, (222.5, 202.5)), (133, (222.5, 200.0)), (134, (222.5, 197.5)), (135, (222.5, 195.0)), (136, (222.5, 192.5)), (137, (222.5, 190.0)), (138, (222.5, 187.5)), (139, (222.5, 185.0)), (140, (222.5, 182.5)), (141, (222.5, 180.0)), (142, (222.5, 177.5)), (143, (222.5, 175.0)), (144, (222.5, 172.5)), (145, (222.5, 170.0)), (146, (222.5, 167.5)), (147, (222.5, 165.0)), (148, (222.5, 162.5)), (149, (222.5, 160.0)), (150, (222.5, 157.5)), (151, (222.5, 155.0)), (152, (222.5, 152.5)), (153, (222.5, 150.0)), (154, (222.5, 147.5)), (155, (225.0, 147.5)), (156, (227.5, 147.5)), (157, (230.0, 147.5)), (158, (232.5, 147.5)), (159, (235.0, 147.5)), (160, (237.5, 147.5)), (161, (240.0, 147.5)), (162, (242.5, 147.5)), (163, (245.0, 147.5)), (164, (247.5, 147.5)), (165, (250.0, 147.5)), (166, (252.5, 147.5)), (167, (255.0, 147.5)), (168, (257.5, 147.5)), (169, (260.0, 147.5)), (170, (262.5, 147.5)), (171, (265.0, 147.5)), (172, (267.5, 147.5)), (173, (270.0, 147.5)), (174, (272.5, 147.5)), (175, (275.0, 147.5)), (176, (277.5, 147.5)), (177, (280.0, 147.5)), (178, (282.5, 147.5)), (179, (285.0, 147.5)), (180, (287.5, 147.5)), (181, (290.0, 147.5)), (182, (292.5, 147.5)), (183, (295.0, 147.5)), (184, (297.5, 147.5)), (185, (300.0, 147.5)), (186, (302.5, 147.5)), (187, (305.0, 147.5)), (188, (307.5, 147.5)), (189, (310.0, 147.5)), (190, (312.5, 147.5)), (191, (315.0, 147.5)), (192, (317.5, 147.5)), (193, (320.0, 147.5)), (194, (322.5, 147.5)), (195, (325.0, 147.5)), (196, (327.5, 147.5)), (197, (330.0, 147.5)), (198, (332.5, 147.5)), (199, (335.0, 147.5)), (200, (337.5, 147.5)), (201, (340.0, 147.5)), (202, (342.5, 147.5)), (203, (345.0, 147.5)), (204, (347.5, 147.5)), (205, (350.0, 147.5)), (206, (352.5, 147.5)), (207, (355.0, 147.5)), (208, (357.5, 147.5)), (209, (360.0, 147.5)), (210, (362.5, 147.5)), (211, (365.0, 147.5)), (212, (367.5, 147.5)), (213, (370.0, 147.5)), (214, (372.5, 147.5)), (215, (375.0, 147.5)), (216, (377.5, 147.5)), (217, (377.5, 150.0)), (218, (377.5, 152.5)), (219, (377.5, 155.0)), (220, (377.5, 157.5)), (221, (377.5, 160.0)), (222, (377.5, 162.5)), (223, (377.5, 165.0)), (224, (377.5, 167.5)), (225, (377.5, 170.0)), (226, (377.5, 172.5)), (227, (377.5, 175.0)), (228, (377.5, 177.5)), (229, (377.5, 180.0)), (230, (377.5, 182.5)), (231, (377.5, 185.0)), (232, (377.5, 187.5)), (233, (377.5, 190.0)), (234, (377.5, 192.5)), (235, (377.5, 195.0)), (236, (377.5, 197.5)), (237, (377.5, 200.0)), (238, (377.5, 202.5)), (239, (377.5, 205.0)), (240, (377.5, 207.5)), (241, (377.5, 210.0)), (242, (377.5, 212.5)), (243, (377.5, 215.0)), (244, (377.5, 217.5)), (245, (377.5, 220.0)), (246, (377.5, 222.5)), (247, (377.5, 225.0)), (248, (377.5, 227.5)), (249, (377.5, 230.0)), (250, (377.5, 232.5)), (251, (377.5, 235.0)), (252, (377.5, 237.5)), (253, (377.5, 240.0)), (254, (377.5, 242.5)), (255, (377.5, 245.0)), (256, (377.5, 247.5)), (257, (377.5, 250.0)), (258, (377.5, 252.5)), (259, (377.5, 255.0)), (260, (377.5, 257.5)), (261, (377.5, 260.0)), (262, (377.5, 262.5)), (263, (377.5, 265.0)), (264, (377.5, 267.5)), (265, (377.5, 270.0)), (266, (377.5, 272.5)), (267, (377.5, 275.0)), (268, (377.5, 277.5)), (269, (377.5, 280.0)), (270, (377.5, 282.5)), (271, (377.5, 285.0)), (272, (377.5, 287.5)), (273, (377.5, 290.0)), (274, (377.5, 292.5)), (275, (377.5, 295.0)), (276, (377.5, 297.5)), (277, (377.5, 300.0)), (278, (377.5, 302.5)), (279, (377.5, 305.0)), (280, (377.5, 307.5)), (281, (377.5, 310.0)), (282, (377.5, 312.5)), (283, (377.5, 315.0)), (284, (377.5, 317.5)), (285, (377.5, 320.0)), (286, (377.5, 322.5)), (287, (377.5, 325.0)), (288, (377.5, 327.5)), (289, (377.5, 330.0)), (290, (377.5, 332.5)), (291, (377.5, 335.0)), (292, (377.5, 337.5)), (293, (377.5, 340.0)), (294, (377.5, 342.5)), (295, (377.5, 345.0)), (296, (377.5, 347.5)), (297, (377.5, 350.0)), (298, (377.5, 352.5)), (299, (377.5, 355.0)), (300, (377.5, 357.5)), (301, (377.5, 360.0)), (302, (377.5, 362.5)), (303, (377.5, 365.0)), (304, (377.5, 367.5)), (305, (377.5, 370.0)), (306, (377.5, 372.5)), (307, (377.5, 375.0)), (308, (377.5, 377.5)), (309, (377.5, 380.0)), (310, (377.5, 382.5)), (311, (377.5, 385.0)), (312, (377.5, 387.5)), (313, (377.5, 390.0)), (314, (377.5, 392.5)), (315, (377.5, 395.0)), (316, (377.5, 397.5)), (317, (377.5, 400.0)), (318, (377.5, 402.5)), (319, (377.5, 405.0)), (320, (377.5, 407.5)), (321, (377.5, 410.0)), (322, (377.5, 412.5)), (323, (377.5, 415.0)), (324, (377.5, 417.5)), (325, (377.5, 420.0)), (326, (377.5, 422.5)), (327, (377.5, 425.0)), (328, (377.5, 427.5)), (329, (377.5, 430.0)), (330, (377.5, 432.5)), (331, (377.5, 435.0)), (332, (377.5, 437.5)), (333, (377.5, 440.0)), (334, (377.5, 442.5)), (335, (377.5, 445.0)), (336, (377.5, 447.5)), (337, (375.0, 447.5)), (338, (372.5, 447.5)), (339, (370.0, 447.5)), (340, (367.5, 447.5)), (341, (365.0, 447.5)), (342, (362.5, 447.5)), (343, (360.0, 447.5)), (344, (357.5, 447.5)), (345, (355.0, 447.5)), (346, (352.5, 447.5)), (347, (350.0, 447.5)), (348, (347.5, 447.5)), (349, (345.0, 447.5)), (350, (342.5, 447.5)), (351, (340.0, 447.5)), (352, (337.5, 447.5)), (353, (335.0, 447.5)), (354, (332.5, 447.5)), (355, (330.0, 447.5)), (356, (327.5, 447.5)), (357, (325.0, 447.5)), (358, (322.5, 447.5)), (359, (320.0, 447.5)), (360, (317.5, 447.5)), (361, (315.0, 447.5)), (362, (312.5, 447.5)), (363, (310.0, 447.5)), (364, (307.5, 447.5)), (365, (305.0, 447.5)), (366, (302.5, 447.5)), (367, (300.0, 447.5)), (368, (297.5, 447.5)), (369, (295.0, 447.5)), (370, (292.5, 447.5)), (371, (290.0, 447.5)), (372, (287.5, 447.5)), (373, (285.0, 447.5)), (374, (282.5, 447.5)), (375, (280.0, 447.5)), (376, (277.5, 447.5)), (377, (275.0, 447.5)), (378, (272.5, 447.5)), (379, (270.0, 447.5)), (380, (267.5, 447.5)), (381, (265.0, 447.5)), (382, (262.5, 447.5)), (383, (260.0, 447.5)), (384, (257.5, 447.5)), (385, (255.0, 447.5)), (386, (252.5, 447.5)), (387, (250.0, 447.5)), (388, (247.5, 447.5)), (389, (245.0, 447.5)), (390, (242.5, 447.5)), (391, (240.0, 447.5)), (392, (237.5, 447.5)), (393, (235.0, 447.5)), (394, (232.5, 447.5)), (395, (230.0, 447.5)), (396, (227.5, 447.5)), (397, (225.0, 447.5)), (398, (222.5, 447.5)), (399, (220.0, 447.5)), (400, (217.5, 447.5)), (401, (215.0, 447.5)), (402, (212.5, 447.5)), (403, (210.0, 447.5)), (404, (207.5, 447.5)), (405, (207.5, 450.0)), (406, (207.5, 452.5)), (407, (207.5, 455.0)), (408, (207.5, 457.5)), (409, (207.5, 460.0)), (410, (207.5, 462.5)), (411, (207.5, 465.0)), (412, (207.5, 467.5)), (413, (207.5, 470.0)), (414, (207.5, 472.5)), (415, (207.5, 475.0)), (416, (207.5, 477.5)), (417, (207.5, 480.0)), (418, (207.5, 482.5)), (419, (207.5, 485.0)), (420, (207.5, 487.5)), (421, (207.5, 490.0)), (422, (207.5, 492.5)), (423, (207.5, 495.0)), (424, (207.5, 497.5)), (425, (207.5, 500.0)), (426, (207.5, 502.5)), (427, (207.5, 505.0)), (428, (207.5, 507.5)), (429, (207.5, 510.0)), (430, (207.5, 512.5)), (431, (207.5, 515.0)), (432, (207.5, 517.5)), (433, (207.5, 520.0)), (434, (207.5, 522.5)), (435, (207.5, 525.0)), (436, (207.5, 527.5)), (437, (207.5, 530.0)), (438, (207.5, 532.5)), (439, (207.5, 535.0)), (440, (207.5, 537.5)), (441, (207.5, 540.0)), (442, (207.5, 542.5)), (443, (207.5, 545.0)), (444, (207.5, 547.5)), (445, (207.5, 550.0)), (446, (207.5, 552.5)), (447, (210.0, 552.5)), (448, (212.5, 552.5)), (449, (215.0, 552.5)), (450, (217.5, 552.5)), (451, (220.0, 552.5)), (452, (222.5, 552.5)), (453, (225.0, 552.5)), (454, (227.5, 552.5)), (455, (230.0, 552.5)), (456, (232.5, 552.5)), (457, (235.0, 552.5)), (458, (237.5, 552.5)), (459, (240.0, 552.5)), (460, (242.5, 552.5)), (461, (245.0, 552.5)), (462, (247.5, 552.5)), (463, (250.0, 552.5)), (464, (252.5, 552.5)), (465, (255.0, 552.5)), (466, (257.5, 552.5)), (467, (260.0, 552.5)), (468, (262.5, 552.5)), (469, (265.0, 552.5)), (470, (267.5, 552.5)), (471, (270.0, 552.5)), (472, (272.5, 552.5)), (473, (275.0, 552.5)), (474, (277.5, 552.5)), (475, (280.0, 552.5)), (476, (282.5, 552.5)), (477, (285.0, 552.5)), (478, (287.5, 552.5)), (479, (290.0, 552.5)), (480, (292.5, 552.5)), (481, (295.0, 552.5)), (482, (297.5, 552.5)), (483, (300.0, 552.5)), (484, (302.5, 552.5)), (485, (305.0, 552.5)), (486, (307.5, 552.5)), (487, (310.0, 552.5)), (488, (312.5, 552.5)), (489, (315.0, 552.5)), (490, (317.5, 552.5)), (491, (320.0, 552.5)), (492, (322.5, 552.5)), (493, (325.0, 552.5)), (494, (327.5, 552.5)), (495, (330.0, 552.5)), (496, (332.5, 552.5)), (497, (335.0, 552.5)), (498, (337.5, 552.5)), (499, (340.0, 552.5)), (500, (342.5, 552.5)), (501, (345.0, 552.5)), (502, (347.5, 552.5)), (503, (350.0, 552.5)), (504, (352.5, 552.5)), (505, (355.0, 552.5)), (506, (357.5, 552.5)), (507, (360.0, 552.5)), (508, (362.5, 552.5)), (509, (365.0, 552.5)), (510, (367.5, 552.5)), (511, (370.0, 552.5)), (512, (372.5, 552.5)), (513, (375.0, 552.5)), (514, (377.5, 552.5)), (515, (380.0, 552.5)), (516, (382.5, 552.5)), (517, (385.0, 552.5)), (518, (387.5, 552.5)), (519, (390.0, 552.5)), (520, (392.5, 552.5)), (521, (395.0, 552.5)), (522, (397.5, 552.5)), (523, (400.0, 552.5)), (524, (402.5, 552.5)), (525, (405.0, 552.5)), (526, (407.5, 552.5)), (527, (410.0, 552.5)), (528, (412.5, 552.5)), (529, (415.0, 552.5)), (530, (417.5, 552.5)), (531, (420.0, 552.5)), (532, (422.5, 552.5)), (533, (425.0, 552.5)), (534, (427.5, 552.5)), (535, (430.0, 552.5)), (536, (432.5, 552.5)), (537, (435.0, 552.5)), (538, (437.5, 552.5)), (539, (440.0, 552.5)), (540, (442.5, 552.5)), (541, (445.0, 552.5)), (542, (447.5, 552.5)), (543, (450.0, 552.5)), (544, (452.5, 552.5)), (545, (455.0, 552.5)), (546, (457.5, 552.5)), (547, (460.0, 552.5)), (548, (462.5, 552.5)), (549, (465.0, 552.5)), (550, (467.5, 552.5)), (551, (470.0, 552.5)), (552, (472.5, 552.5)), (553, (475.0, 552.5)), (554, (477.5, 552.5)), (555, (480.0, 552.5)), (556, (482.5, 552.5)), (557, (485.0, 552.5)), (558, (487.5, 552.5)), (559, (490.0, 552.5)), (560, (492.5, 552.5)), (561, (495.0, 552.5)), (562, (497.5, 552.5)), (563, (500.0, 552.5)), (564, (502.5, 552.5)), (565, (505.0, 552.5)), (566, (507.5, 552.5)), (567, (510.0, 552.5)), (568, (512.5, 552.5)), (569, (515.0, 552.5)), (570, (517.5, 552.5)), (571, (520.0, 552.5)), (572, (522.5, 552.5)), (573, (525.0, 552.5)), (574, (527.5, 552.5)), (575, (530.0, 552.5)), (576, (532.5, 552.5)), (577, (535.0, 552.5)), (578, (537.5, 552.5)), (579, (540.0, 552.5)), (580, (542.5, 552.5)), (581, (545.0, 552.5)), (582, (547.5, 552.5)), (583, (550.0, 552.5)), (584, (552.5, 552.5)), (585, (555.0, 552.5)), (586, (557.5, 552.5)), (587, (560.0, 552.5)), (588, (562.5, 552.5)), (589, (565.0, 552.5)), (590, (567.5, 552.5)), (591, (570.0, 552.5)), (592, (572.5, 552.5)), (593, (575.0, 552.5)), (594, (577.5, 552.5)), (595, (580.0, 552.5)), (596, (582.5, 552.5)), (597, (585.0, 552.5)), (598, (587.5, 552.5)), (599, (590.0, 552.5)), (600, (592.5, 552.5)), (601, (595.0, 552.5)), (602, (597.5, 552.5)), (603, (600.0, 552.5)), (604, (602.5, 552.5)), (605, (605.0, 552.5)), (606, (607.5, 552.5)), (607, (607.5, 550.0)), (608, (607.5, 547.5)), (609, (607.5, 545.0)), (610, (607.5, 542.5)), (611, (607.5, 540.0)), (612, (607.5, 537.5)), (613, (607.5, 535.0)), (614, (607.5, 532.5)), (615, (607.5, 530.0)), (616, (607.5, 527.5)), (617, (607.5, 525.0)), (618, (607.5, 522.5)), (619, (607.5, 520.0)), (620, (607.5, 517.5)), (621, (607.5, 515.0)), (622, (607.5, 512.5)), (623, (607.5, 510.0)), (624, (607.5, 507.5)), (625, (607.5, 505.0)), (626, (607.5, 502.5)), (627, (607.5, 500.0)), (628, (607.5, 497.5)), (629, (607.5, 495.0)), (630, (607.5, 492.5)), (631, (607.5, 490.0)), (632, (607.5, 487.5)), (633, (607.5, 485.0)), (634, (607.5, 482.5)), (635, (607.5, 480.0)), (636, (607.5, 477.5)), (637, (607.5, 475.0)), (638, (607.5, 472.5)), (639, (607.5, 470.0)), (640, (607.5, 467.5)), (641, (607.5, 465.0)), (642, (607.5, 462.5)), (643, (607.5, 460.0)), (644, (607.5, 457.5)), (645, (607.5, 455.0)), (646, (607.5, 452.5)), (647, (607.5, 450.0)), (648, (607.5, 447.5)), (649, (607.5, 445.0)), (650, (607.5, 442.5)), (651, (607.5, 440.0)), (652, (607.5, 437.5)), (653, (607.5, 435.0)), (654, (607.5, 432.5)), (655, (607.5, 430.0)), (656, (607.5, 427.5)), (657, (607.5, 425.0)), (658, (607.5, 422.5)), (659, (607.5, 420.0)), (660, (607.5, 417.5)), (661, (607.5, 415.0)), (662, (607.5, 412.5)), (663, (607.5, 410.0)), (664, (607.5, 407.5)), (665, (607.5, 405.0)), (666, (607.5, 402.5)), (667, (607.5, 400.0)), (668, (607.5, 397.5)), (669, (607.5, 395.0)), (670, (607.5, 392.5)), (671, (607.5, 390.0)), (672, (607.5, 387.5)), (673, (607.5, 385.0)), (674, (607.5, 382.5)), (675, (607.5, 380.0)), (676, (607.5, 377.5)), (677, (607.5, 375.0)), (678, (607.5, 372.5)), (679, (607.5, 370.0)), (680, (607.5, 367.5)), (681, (605.0, 367.5)), (682, (602.5, 367.5)), (683, (600.0, 367.5)), (684, (597.5, 367.5)), (685, (595.0, 367.5)), (686, (592.5, 367.5)), (687, (590.0, 367.5)), (688, (587.5, 367.5)), (689, (585.0, 367.5)), (690, (582.5, 367.5)), (691, (580.0, 367.5)), (692, (577.5, 367.5)), (693, (575.0, 367.5)), (694, (572.5, 367.5)), (695, (570.0, 367.5)), (696, (567.5, 367.5)), (697, (565.0, 367.5)), (698, (562.5, 367.5)), (699, (560.0, 367.5)), (700, (557.5, 367.5)), (701, (555.0, 367.5)), (702, (552.5, 367.5)), (703, (550.0, 367.5)), (704, (547.5, 367.5)), (705, (545.0, 367.5)), (706, (542.5, 367.5)), (707, (540.0, 367.5)), (708, (537.5, 367.5)), (709, (535.0, 367.5)), (710, (532.5, 367.5)), (711, (530.0, 367.5)), (712, (527.5, 367.5)), (713, (525.0, 367.5)), (714, (522.5, 367.5)), (715, (520.0, 367.5)), (716, (517.5, 367.5)), (717, (515.0, 367.5)), (718, (512.5, 367.5)), (719, (510.0, 367.5)), (720, (507.5, 367.5)), (721, (505.0, 367.5)), (722, (502.5, 367.5)), (723, (500.0, 367.5)), (724, (497.5, 367.5)), (725, (495.0, 367.5)), (726, (492.5, 367.5)), (727, (490.0, 367.5)), (728, (487.5, 367.5)), (729, (485.0, 367.5)), (730, (482.5, 367.5)), (731, (480.0, 367.5)), (732, (477.5, 367.5)), (733, (475.0, 367.5)), (734, (472.5, 367.5)), (735, (470.0, 367.5)), (736, (467.5, 367.5)), (737, (465.0, 367.5)), (738, (462.5, 367.5)), (739, (460.0, 367.5)), (740, (457.5, 367.5)), (741, (457.5, 365.0)), (742, (457.5, 362.5)), (743, (457.5, 360.0)), (744, (457.5, 357.5)), (745, (457.5, 355.0)), (746, (457.5, 352.5)), (747, (457.5, 350.0)), (748, (457.5, 347.5)), (749, (457.5, 345.0)), (750, (457.5, 342.5)), (751, (457.5, 340.0)), (752, (457.5, 337.5)), (753, (457.5, 335.0)), (754, (457.5, 332.5)), (755, (457.5, 330.0)), (756, (457.5, 327.5)), (757, (457.5, 325.0)), (758, (457.5, 322.5)), (759, (457.5, 320.0)), (760, (457.5, 317.5)), (761, (457.5, 315.0)), (762, (457.5, 312.5)), (763, (457.5, 310.0)), (764, (457.5, 307.5)), (765, (457.5, 305.0)), (766, (457.5, 302.5)), (767, (457.5, 300.0)), (768, (457.5, 297.5)), (769, (457.5, 295.0)), (770, (457.5, 292.5)), (771, (457.5, 290.0)), (772, (457.5, 287.5)), (773, (457.5, 285.0)), (774, (457.5, 282.5)), (775, (457.5, 280.0)), (776, (457.5, 277.5)), (777, (457.5, 275.0)), (778, (457.5, 272.5)), (779, (457.5, 270.0)), (780, (457.5, 267.5)), (781, (457.5, 265.0)), (782, (457.5, 262.5)), (783, (457.5, 260.0)), (784, (457.5, 257.5)), (785, (457.5, 255.0)), (786, (457.5, 252.5)), (787, (457.5, 250.0)), (788, (457.5, 247.5)), (789, (457.5, 245.0)), (790, (457.5, 242.5)), (791, (460.0, 242.5)), (792, (462.5, 242.5)), (793, (465.0, 242.5)), (794, (467.5, 242.5)), (795, (470.0, 242.5)), (796, (472.5, 242.5)), (797, (475.0, 242.5)), (798, (477.5, 242.5)), (799, (480.0, 242.5)), (800, (482.5, 242.5)), (801, (485.0, 242.5)), (802, (487.5, 242.5)), (803, (490.0, 242.5)), (804, (492.5, 242.5)), (805, (495.0, 242.5)), (806, (497.5, 242.5)), (807, (500.0, 242.5)), (808, (502.5, 242.5)), (809, (505.0, 242.5)), (810, (507.5, 242.5)), (811, (510.0, 242.5)), (812, (512.5, 242.5)), (813, (515.0, 242.5)), (814, (517.5, 242.5)), (815, (520.0, 242.5)), (816, (522.5, 242.5)), (817, (525.0, 242.5)), (818, (527.5, 242.5)), (819, (530.0, 242.5)), (820, (532.5, 242.5)), (821, (535.0, 242.5)), (822, (537.5, 242.5)), (823, (540.0, 242.5)), (824, (542.5, 242.5)), (825, (545.0, 242.5)), (826, (547.5, 242.5)), (827, (550.0, 242.5)), (828, (552.5, 242.5)), (829, (555.0, 242.5)), (830, (557.5, 242.5)), (831, (560.0, 242.5)), (832, (562.5, 242.5)), (833, (565.0, 242.5)), (834, (567.5, 242.5)), (835, (570.0, 242.5)), (836, (572.5, 242.5)), (837, (575.0, 242.5)), (838, (577.5, 242.5)), (839, (580.0, 242.5)), (840, (582.5, 242.5)), (841, (585.0, 242.5)), (842, (587.5, 242.5)), (843, (590.0, 242.5)), (844, (592.5, 242.5)), (845, (595.0, 242.5)), (846, (597.5, 242.5)), (847, (600.0, 242.5)), (848, (602.5, 242.5)), (849, (605.0, 242.5)), (850, (607.5, 242.5)), (851, (610.0, 242.5)), (852, (612.5, 242.5)), (853, (615.0, 242.5)), (854, (617.5, 242.5)), (855, (620.0, 242.5)), (856, (622.5, 242.5)), (857, (625.0, 242.5)), (858, (627.5, 242.5)), (859, (627.5, 240.0)), (860, (627.5, 237.5)), (861, (627.5, 235.0)), (862, (627.5, 232.5)), (863, (627.5, 230.0)), (864, (627.5, 227.5)), (865, (627.5, 225.0)), (866, (627.5, 222.5)), (867, (627.5, 220.0)), (868, (627.5, 217.5)), (869, (627.5, 215.0)), (870, (627.5, 212.5)), (871, (627.5, 210.0)), (872, (627.5, 207.5)), (873, (627.5, 205.0)), (874, (627.5, 202.5)), (875, (627.5, 200.0)), (876, (627.5, 197.5)), (877, (627.5, 195.0)), (878, (627.5, 192.5)), (879, (627.5, 190.0)), (880, (627.5, 187.5)), (881, (627.5, 185.0)), (882, (627.5, 182.5)), (883, (627.5, 180.0)), (884, (627.5, 177.5)), (885, (627.5, 175.0)), (886, (627.5, 172.5)), (887, (627.5, 170.0)), (888, (627.5, 167.5)), (889, (627.5, 165.0)), (890, (627.5, 162.5)), (891, (627.5, 160.0)), (892, (627.5, 157.5)), (893, (627.5, 155.0)), (894, (627.5, 152.5)), (895, (627.5, 150.0)), (896, (627.5, 147.5)), (897, (627.5, 145.0)), (898, (627.5, 142.5)), (899, (627.5, 140.0)), (900, (627.5, 137.5)), (901, (627.5, 135.0)), (902, (627.5, 132.5)), (903, (627.5, 130.0)), (904, (627.5, 127.5)), (905, (627.5, 125.0)), (906, (627.5, 122.5)), (907, (627.5, 120.0)), (908, (627.5, 117.5)), (909, (627.5, 115.0)), (910, (627.5, 112.5)), (911, (627.5, 110.0)), (912, (627.5, 107.5)), (913, (627.5, 105.0)), (914, (627.5, 102.5)), (915, (627.5, 100.0)), (916, (627.5, 97.5)), (917, (627.5, 95.0)), (918, (627.5, 92.5)), (919, (627.5, 90.0)), (920, (627.5, 87.5)), (921, (627.5, 85.0)), (922, (627.5, 82.5)), (923, (627.5, 80.0)), (924, (627.5, 77.5)), (925, (627.5, 75.0)), (926, (627.5, 72.5)), (927, (627.5, 70.0)), (928, (627.5, 67.5)), (929, (627.5, 65.0)), (930, (627.5, 62.5)), (931, (627.5, 60.0)), (932, (627.5, 57.5)), (933, (627.5, 55.0)), (934, (627.5, 52.5)), (935, (627.5, 50.0)), (936, (627.5, 47.5)), (937, (627.5, 45.0)), (938, (627.5, 42.5)), (939, (627.5, 40.0)), (940, (627.5, 37.5)), (941, (627.5, 35.0)), (942, (627.5, 32.5)), (943, (627.5, 30.0)), (944, (627.5, 27.5)), (945, (627.5, 25.0)), (946, (627.5, 22.5)), (947, (625.0, 22.5)), (948, (622.5, 22.5)), (949, (620.0, 22.5)), (950, (617.5, 22.5)), (951, (615.0, 22.5)), (952, (612.5, 22.5)), (953, (610.0, 22.5)), (954, (607.5, 22.5)), (955, (605.0, 22.5)), (956, (602.5, 22.5)), (957, (600.0, 22.5)), (958, (597.5, 22.5)), (959, (595.0, 22.5)), (960, (592.5, 22.5)), (961, (590.0, 22.5)), (962, (587.5, 22.5)), (963, (585.0, 22.5)), (964, (582.5, 22.5)), (965, (580.0, 22.5)), (966, (577.5, 22.5)), (967, (575.0, 22.5)), (968, (572.5, 22.5)), (969, (570.0, 22.5)), (970, (567.5, 22.5)), (971, (565.0, 22.5)), (972, (562.5, 22.5)), (973, (560.0, 22.5)), (974, (557.5, 22.5)), (975, (555.0, 22.5)), (976, (552.5, 22.5)), (977, (550.0, 22.5)), (978, (547.5, 22.5)), (979, (545.0, 22.5)), (980, (542.5, 22.5)), (981, (540.0, 22.5)), (982, (537.5, 22.5)), (983, (535.0, 22.5)), (984, (532.5, 22.5)), (985, (530.0, 22.5)), (986, (527.5, 22.5)), (987, (525.0, 22.5)), (988, (522.5, 22.5)), (989, (520.0, 22.5)), (990, (517.5, 22.5)), (991, (515.0, 22.5)), (992, (512.5, 22.5)), (993, (510.0, 22.5)), (994, (507.5, 22.5)), (995, (505.0, 22.5)), (996, (502.5, 22.5)), (997, (500.0, 22.5)), (998, (497.5, 22.5)), (999, (495.0, 22.5)), (1000, (492.5, 22.5)), (1001, (490.0, 22.5)), (1002, (487.5, 22.5)), (1003, (485.0, 22.5)), (1004, (482.5, 22.5)), (1005, (480.0, 22.5)), (1006, (477.5, 22.5)), (1007, (475.0, 22.5)), (1008, (472.5, 22.5)), (1009, (470.0, 22.5)), (1010, (467.5, 22.5)), (1011, (467.5, 20.0)), (1012, (467.5, 17.5)), (1013, (467.5, 15.0)), (1014, (467.5, 12.5)), (1015, (467.5, 10.0)), (1016, (467.5, 7.5)), (1017, (467.5, 5.0))]))
    map_2_bg_img = py.image.load("map_2_bg.png")
    map_2_bg_img = py.transform.scale(map_2_bg_img, (width, height-(height//5)))
    map_2_bg_rect = map_2_bg_img.get_rect()
    menu_ig = ig_menu(screen, charictars, "ig_menu_bg.png")
    floating_texts = []
    zombie_image_list = load_image_list(["zombie.png"], colorkey=white)
    enemys = []
    setting_menu = settings_menu(screen, "settings_bg.png", colorkey=white)
    settings_wheel = settings(screen, "settings_wheel.png", setting_menu, colorkey=white)
    projectiles = []
    paused = False
    round_1_data = [('base_enemy', 10, ['zombie.png']), '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', ('base_enemy', 10, ['zombie.png']), '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
'-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', ('base_enemy', 10, ['zombie.png']), '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
'-', '-', '-', '-', '-', '-', '-', '-', ('base_enemy', 10, ['zombie.png']), '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', ('base_enemy', 10, ['zombie.png'])]
    round_1 = round(round_1_data)
    round_2_data = [('base_enemy', 10, ['zombie.png'])]
    round_2 = round(round_2_data)
    full_rounds = full_game([round_1, round_2])
    counter = 0
    angle_directory = {
            0: (0.9998476951563913, -0.01745240643728351), 1: (0.9993908270190958, -0.03489949670250097), 2: (0.9986295347545739, -0.05233595624294383), 3: (0.9975640502598243, -0.0697564737441253), 4: (0.9961946980917455, -0.08715574274765818), 5: (0.9945218953682734, -0.10452846326765348), 6: (0.9925461516413222, -0.12186934340514749), 7: (0.9902680687415706, -0.13917310096006547), 8: (0.987688340595138, -0.1564344650402309), 9: (0.9848077530122084, -0.1736481776669304), 10: (0.9816271834476643, -0.19080899537654486), 11: (0.978147600733806, -0.2079116908177594), 12: (0.9743700647852357, -0.22495105434386506), 13: (0.970295726275997, -0.2419218955996678), 14: (0.9659258262890689, -0.25881904510252085), 15: (0.9612616959383194, -0.27563735581699933), 16: (0.9563047559630361, -0.29237170472273694), 17: (0.9510565162951542, -0.3090169943749476), 18: (0.9455185755993175, -0.32556815445715687), 19: (0.9396926207859091, -0.34202014332566893), 20: (0.9335804264972025, -0.3583679495453005), 21: (0.9271838545667882, -0.37460659341591224), 22: (0.9205048534524412, -0.390731128489274), 23: (0.9135454576426018, -0.4067366430758005), 24: (0.9063077870366508, -0.4226182617406997), 25: (0.8987940462991678, -0.43837114678907774), 26: (0.8910065241883688, -0.45399049973954714), 27: (0.8829475928589279, -0.46947156278589114), 28: (0.8746197071393967, -0.4848096202463374), 29: (0.8660254037844396, -0.5000000000000004), 30: (0.8571673007021132, -0.5150380749100547), 31: (0.8480480961564268, -0.5299192642332055), 32: (0.8386705679454249, -0.5446390350150276), 33: (0.8290375725550426, -0.5591929034707475), 34: (0.8191520442889927, -0.5735764363510468), 35: (0.8090169943749482, -0.5877852522924739), 36: (0.7986355100472937, -0.6018150231520492), 37: (0.7880107536067229, -0.6156614753256592), 38: (0.7771459614569719, -0.6293203910498384), 39: (0.7660444431189791, -0.6427876096865403), 40: (0.754709580222773, -0.6560590289905082), 41: (0.7431448254773952, -0.6691306063588591), 42: (0.7313537016191716, -0.6819983600624995), 43: (0.7193398003386522, -0.6946583704589983), 44: (0.7071067811865486, -0.7071067811865486), 45: (0.6946583704589984, -0.7193398003386522), 46: (0.6819983600624996, -0.7313537016191716), 47: (0.6691306063588593, -0.7431448254773954), 48: (0.6560590289905084, -0.7547095802227732), 49: (0.6427876096865404, -0.7660444431189793), 50: (0.6293203910498385, -0.7771459614569722), 51: (0.6156614753256593, -0.7880107536067233), 52: (0.6018150231520493, -0.7986355100472943), 53: (0.587785252292474, -0.8090169943749489), 54: (0.573576436351047, -0.8191520442889934), 55: (0.5591929034707478, -0.8290375725550433), 56: (0.5446390350150281, -0.8386705679454257), 57: (0.529919264233206, -0.8480480961564276), 58: (0.5150380749100553, -0.857167300702114), 59: (0.5000000000000011, -0.8660254037844404), 60: (0.4848096202463381, -0.8746197071393976), 61: (0.46947156278589186, -0.8829475928589289), 62: (0.45399049973954786, -0.8910065241883698), 63: (0.43837114678907846, -0.8987940462991689), 64: (0.4226182617407005, -0.9063077870366519), 65: (0.40673664307580126, -0.9135454576426029), 66: (0.39073112848927477, -0.9205048534524424), 67: (0.37460659341591307, -0.9271838545667894), 68: (0.35836794954530127, -0.9335804264972037), 69: (0.34202014332566966, -0.9396926207859104), 70: (0.3255681544571576, -0.945518575599319), 71: (0.3090169943749483, -0.9510565162951558), 72: (0.29237170472273755, -0.9563047559630378), 73: (0.27563735581699994, -0.9612616959383211), 74: (0.2588190451025215, -0.9659258262890706), 75: (0.24192189559966848, -0.9702957262759989), 76: (0.2249510543438657, -0.9743700647852377), 77: (0.20791169081776, -0.9781476007338081), 78: (0.19080899537654544, -0.9816271834476665), 79: (0.17364817766693094, -0.9848077530122107), 80: (0.15643446504023142, -0.9876883405951404), 81: (0.13917310096006597, -0.990268068741573), 82: (0.12186934340514795, -0.9925461516413248), 83: (0.10452846326765389, -0.9945218953682761), 84: (0.08715574274765854, -0.9961946980917483), 85: (0.06975647374412564, -0.9975640502598271), 86: (0.052335956242944126, -0.9986295347545767), 87: (0.03489949670250122, -0.9993908270190985), 88: (0.017452406437283713, -0.999847695156394), 89: (1.5265566588595902e-16, -1.0000000000000029), 90: (-0.01745240643728341, -0.9998476951563942), 91: (-0.03489949670250092, -0.9993908270190986), 92: (-0.052335956242943835, -0.9986295347545768), 93: (-0.06975647374412536, -0.9975640502598272), 94: (-0.08715574274765828, -0.9961946980917484), 95: (-0.10452846326765364, -0.9945218953682763), 96: (-0.1218693434051477, -0.9925461516413251), 97: (-0.13917310096006572, -0.9902680687415735), 98: (-0.1564344650402312, -0.9876883405951409), 99: (-0.17364817766693075, -0.9848077530122112), 100: (-0.19080899537654528, -0.9816271834476672), 101: (-0.20791169081775987, -0.9781476007338089), 102: (-0.2249510543438656, -0.9743700647852385), 103: (-0.24192189559966837, -0.9702957262759998), 104: (-0.25881904510252146, -0.9659258262890716), 105: (-0.275637355817, -0.9612616959383222), 106: (-0.2923717047227376, -0.9563047559630389), 107: (-0.30901699437494834, -0.951056516295157), 108: (-0.32556815445715764, -0.9455185755993202), 109: (-0.34202014332566977, -0.9396926207859118), 110: (-0.3583679495453014, -0.9335804264972052), 111: (-0.3746065934159132, -0.9271838545667909), 112: (-0.39073112848927494, -0.9205048534524438), 113: (-0.4067366430758015, -0.9135454576426044), 114: (-0.4226182617407008, -0.9063077870366535), 115: (-0.43837114678907885, -0.8987940462991705), 116: (-0.4539904997395483, -0.8910065241883713), 117: (-0.46947156278589236, -0.8829475928589304), 118: (-0.48480962024633867, -0.8746197071393993), 119: (-0.5000000000000017, -0.8660254037844421), 120: (-0.5150380749100559, -0.8571673007021158), 121: (-0.5299192642332068, -0.8480480961564294), 122: (-0.544639035015029, -0.8386705679454275), 123: (-0.5591929034707488, -0.8290375725550451), 124: (-0.5735764363510482, -0.8191520442889951), 125: (-0.5877852522924752, -0.8090169943749507), 126: (-0.6018150231520505, -0.798635510047296), 127: (-0.6156614753256605, -0.7880107536067252), 128: (-0.6293203910498397, -0.7771459614569741), 129: (-0.6427876096865416, -0.7660444431189812), 130: (-0.6560590289905096, -0.7547095802227751), 131: (-0.6691306063588606, -0.7431448254773974), 132: (-0.6819983600625009, -0.7313537016191736), 133: (-0.6946583704589998, -0.7193398003386542), 134: (-0.7071067811865501, -0.7071067811865506), 135: (-0.7193398003386539, -0.6946583704590003), 136: (-0.7313537016191732, -0.6819983600625015), 137: (-0.743144825477397, -0.6691306063588611), 138: (-0.7547095802227749, -0.6560590289905102), 139: (-0.766044443118981, -0.6427876096865421), 140: (-0.7771459614569739, -0.6293203910498402), 141: (-0.7880107536067251, -0.615661475325661), 142: (-0.7986355100472962, -0.6018150231520509), 143: (-0.8090169943749509, -0.5877852522924757), 144: (-0.8191520442889954, -0.5735764363510487), 145: (-0.8290375725550453, -0.5591929034707495), 146: (-0.8386705679454277, -0.5446390350150297), 147: (-0.8480480961564297, -0.5299192642332076), 148: (-0.8571673007021161, -0.5150380749100568), 149: (-0.8660254037844425, -0.5000000000000026), 150: (-0.8746197071393997, -0.48480962024633956), 151: (-0.882947592858931, -0.46947156278589325), 152: (-0.8910065241883719, -0.4539904997395492), 153: (-0.898794046299171, -0.4383711467890798), 154: (-0.9063077870366542, -0.4226182617407018), 155: (-0.9135454576426051, -0.4067366430758025), 156: (-0.9205048534524446, -0.390731128489276), 157: (-0.9271838545667918, -0.37460659341591424), 158: (-0.9335804264972062, -0.3583679495453024), 159: (-0.9396926207859129, -0.34202014332567077), 160: (-0.9455185755993214, -0.32556815445715864), 161: (-0.9510565162951582, -0.30901699437494934), 162: (-0.9563047559630402, -0.29237170472273855), 163: (-0.9612616959383236, -0.2756373558170009), 164: (-0.9659258262890731, -0.2588190451025224), 165: (-0.9702957262760014, -0.2419218955996693), 166: (-0.9743700647852401, -0.2249510543438665), 167: (-0.9781476007338107, -0.20791169081776079), 168: (-0.9816271834476691, -0.19080899537654616), 169: (-0.9848077530122132, -0.17364817766693164), 170: (-0.987688340595143, -0.1564344650402321), 171: (-0.9902680687415756, -0.13917310096006658), 172: (-0.9925461516413273, -0.12186934340514852), 173: (-0.9945218953682787, -0.10452846326765441), 174: (-0.996194698091751, -0.08715574274765903), 175: (-0.9975640502598297, -0.06975647374412607), 176: (-0.9986295347545794, -0.0523359562429445), 177: (-0.9993908270191012, -0.034899496702501545), 178: (-0.9998476951563967, -0.01745240643728399), 179: (-1.0000000000000056, -3.8163916471489756e-16), 180: (-0.9998476951563968, 0.017452406437283227), 181: (-0.9993908270191013, 0.03489949670250078), 182: (-0.9986295347545795, 0.05233595624294374), 183: (-0.9975640502598299, 0.0697564737441253), 184: (-0.9961946980917511, 0.08715574274765828), 185: (-0.994521895368279, 0.10452846326765368), 186: (-0.9925461516413278, 0.1218693434051478), 187: (-0.9902680687415761, 0.13917310096006585), 188: (-0.9876883405951435, 0.15643446504023137), 189: (-0.9848077530122139, 0.17364817766693097), 190: (-0.9816271834476699, 0.19080899537654555), 191: (-0.9781476007338116, 0.2079116908177602), 192: (-0.9743700647852411, 0.22495105434386597), 193: (-0.9702957262760025, 0.2419218955996688), 194: (-0.9659258262890743, 0.25881904510252196), 195: (-0.9612616959383249, 0.2756373558170005), 196: (-0.9563047559630415, 0.29237170472273816), 197: (-0.9510565162951596, 0.30901699437494895), 198: (-0.9455185755993228, 0.3255681544571583), 199: (-0.9396926207859144, 0.3420201433256705), 200: (-0.9335804264972078, 0.35836794954530216), 201: (-0.9271838545667935, 0.374606593415914), 202: (-0.9205048534524464, 0.3907311284892758), 203: (-0.9135454576426069, 0.40673664307580243), 204: (-0.9063077870366559, 0.4226182617407018), 205: (-0.8987940462991729, 0.43837114678907985), 206: (-0.8910065241883738, 0.45399049973954936), 207: (-0.8829475928589329, 0.46947156278589347), 208: (-0.8746197071394017, 0.48480962024633983), 209: (-0.8660254037844446, 0.5000000000000029), 210: (-0.8571673007021182, 0.5150380749100573), 211: (-0.8480480961564318, 0.5299192642332081), 212: (-0.8386705679454299, 0.5446390350150304), 213: (-0.8290375725550475, 0.5591929034707503), 214: (-0.8191520442889976, 0.5735764363510498), 215: (-0.8090169943749531, 0.587785252292477), 216: (-0.7986355100472985, 0.6018150231520523), 217: (-0.7880107536067276, 0.6156614753256623), 218: (-0.7771459614569765, 0.6293203910498416), 219: (-0.7660444431189836, 0.6427876096865436), 220: (-0.7547095802227775, 0.6560590289905116), 221: (-0.7431448254773997, 0.6691306063588626), 222: (-0.7313537016191759, 0.6819983600625029), 223: (-0.7193398003386565, 0.6946583704590018), 224: (-0.7071067811865528, 0.7071067811865522), 225: (-0.6946583704590025, 0.719339800338656), 226: (-0.6819983600625037, 0.7313537016191755), 227: (-0.6691306063588633, 0.7431448254773994), 228: (-0.6560590289905124, 0.7547095802227772), 229: (-0.6427876096865444, 0.7660444431189833), 230: (-0.6293203910498424, 0.7771459614569762), 231: (-0.6156614753256631, 0.7880107536067275), 232: (-0.6018150231520529, 0.7986355100472985), 233: (-0.5877852522924777, 0.8090169943749532), 234: (-0.5735764363510505, 0.8191520442889977), 235: (-0.5591929034707511, 0.8290375725550476), 236: (-0.5446390350150313, 0.83867056794543), 237: (-0.5299192642332091, 0.8480480961564321), 238: (-0.5150380749100583, 0.8571673007021186), 239: (-0.500000000000004, 0.8660254037844449), 240: (-0.48480962024634094, 0.8746197071394022), 241: (-0.4694715627858946, 0.8829475928589334), 242: (-0.45399049973955047, 0.8910065241883744), 243: (-0.438371146789081, 0.8987940462991737), 244: (-0.42261826174070294, 0.9063077870366568), 245: (-0.4067366430758036, 0.9135454576426077), 246: (-0.39073112848927705, 0.9205048534524473), 247: (-0.37460659341591523, 0.9271838545667944), 248: (-0.3583679495453034, 0.9335804264972088), 249: (-0.3420201433256717, 0.9396926207859155), 250: (-0.32556815445715953, 0.9455185755993241), 251: (-0.30901699437495017, 0.9510565162951609), 252: (-0.2923717047227394, 0.9563047559630429), 253: (-0.2756373558170017, 0.9612616959383263), 254: (-0.2588190451025232, 0.9659258262890759), 255: (-0.24192189559967003, 0.9702957262760041), 256: (-0.22495105434386717, 0.9743700647852429), 257: (-0.2079116908177614, 0.9781476007338135), 258: (-0.19080899537654672, 0.9816271834476719), 259: (-0.17364817766693214, 0.984807753012216), 260: (-0.15643446504023253, 0.9876883405951458), 261: (-0.139173100960067, 0.9902680687415784), 262: (-0.12186934340514889, 0.9925461516413301), 263: (-0.10452846326765475, 0.9945218953682815), 264: (-0.0871557427476593, 0.9961946980917538), 265: (-0.0697564737441263, 0.9975640502598325), 266: (-0.052335956242944695, 0.9986295347545822), 267: (-0.03489949670250169, 0.999390827019104), 268: (-0.017452406437284088, 0.9998476951563995), 269: (-4.3368086899420177e-16, 1.0000000000000082), 270: (0.01745240643728322, 0.9998476951563995), 271: (0.034899496702500823, 0.999390827019104), 272: (0.05233595624294383, 0.9986295347545822), 273: (0.06975647374412544, 0.9975640502598325), 274: (0.08715574274765846, 0.9961946980917538), 275: (0.1045284632676539, 0.9945218953682816), 276: (0.12186934340514806, 0.9925461516413304), 277: (0.13917310096006616, 0.9902680687415787), 278: (0.15643446504023173, 0.9876883405951461), 279: (0.17364817766693136, 0.9848077530122165), 280: (0.19080899537654597, 0.9816271834476724), 281: (0.20791169081776065, 0.9781476007338141), 282: (0.22495105434386645, 0.9743700647852437), 283: (0.24192189559966934, 0.970295726276005), 284: (0.2588190451025225, 0.9659258262890769), 285: (0.2756373558170011, 0.9612616959383274), 286: (0.2923717047227388, 0.9563047559630441), 287: (0.30901699437494967, 0.9510565162951621), 288: (0.3255681544571591, 0.9455185755993253), 289: (0.3420201433256713, 0.9396926207859169), 290: (0.35836794954530304, 0.9335804264972103), 291: (0.37460659341591496, 0.927183854566796), 292: (0.3907311284892768, 0.9205048534524488), 293: (0.40673664307580343, 0.9135454576426093), 294: (0.4226182617407028, 0.9063077870366584), 295: (0.43837114678908096, 0.8987940462991754), 296: (0.4539904997395505, 0.8910065241883762), 297: (0.4694715627858947, 0.8829475928589352), 298: (0.48480962024634106, 0.874619707139404), 299: (0.5000000000000042, 0.8660254037844468), 300: (0.5150380749100586, 0.8571673007021204), 301: (0.5299192642332096, 0.8480480961564341), 302: (0.5446390350150319, 0.838670567945432), 303: (0.5591929034707518, 0.8290375725550496), 304: (0.5735764363510513, 0.8191520442889997), 305: (0.5877852522924785, 0.8090169943749552), 306: (0.6018150231520537, 0.7986355100473006), 307: (0.6156614753256638, 0.7880107536067297), 308: (0.6293203910498432, 0.7771459614569786), 309: (0.6427876096865451, 0.7660444431189857), 310: (0.6560590289905132, 0.7547095802227796), 311: (0.6691306063588642, 0.7431448254774017), 312: (0.6819983600625047, 0.7313537016191779), 313: (0.6946583704590036, 0.7193398003386584), 314: (0.707106781186554, 0.7071067811865547), 315: (0.7193398003386577, 0.6946583704590044), 316: (0.7313537016191772, 0.6819983600625055), 317: (0.7431448254774011, 0.6691306063588651), 318: (0.754709580222779, 0.656059028990514), 319: (0.7660444431189852, 0.6427876096865459), 320: (0.7771459614569782, 0.6293203910498439), 321: (0.7880107536067295, 0.6156614753256646), 322: (0.7986355100473005, 0.6018150231520545), 323: (0.8090169943749552, 0.5877852522924791), 324: (0.8191520442889997, 0.5735764363510519), 325: (0.8290375725550496, 0.5591929034707526), 326: (0.838670567945432, 0.5446390350150327), 327: (0.8480480961564341, 0.5299192642332106), 328: (0.8571673007021205, 0.5150380749100597), 329: (0.866025403784447, 0.5000000000000053), 330: (0.8746197071394043, 0.4848096202463422), 331: (0.8829475928589355, 0.46947156278589586), 332: (0.8910065241883766, 0.4539904997395517), 333: (0.8987940462991758, 0.4383711467890822), 334: (0.9063077870366589, 0.42261826174070405), 335: (0.91354545764261, 0.4067366430758047), 336: (0.9205048534524495, 0.3907311284892781), 337: (0.9271838545667966, 0.37460659341591623), 338: (0.9335804264972111, 0.3583679495453043), 339: (0.9396926207859179, 0.3420201433256726), 340: (0.9455185755993264, 0.3255681544571604), 341: (0.9510565162951632, 0.309016994374951), 342: (0.9563047559630452, 0.29237170472274016), 343: (0.9612616959383287, 0.27563735581700244), 344: (0.9659258262890782, 0.25881904510252385), 345: (0.9702957262760065, 0.24192189559967067), 346: (0.9743700647852453, 0.22495105434386778), 347: (0.9781476007338159, 0.20791169081776195), 348: (0.9816271834476743, 0.19080899537654725), 349: (0.9848077530122185, 0.17364817766693263), 350: (0.9876883405951482, 0.15643446504023298), 351: (0.9902680687415808, 0.13917310096006738), 352: (0.9925461516413325, 0.12186934340514924), 353: (0.994521895368284, 0.10452846326765505), 354: (0.9961946980917562, 0.08715574274765957), 355: (0.997564050259835, 0.06975647374412652), 356: (0.9986295347545846, 0.052335956242944875), 357: (0.9993908270191064, 0.03489949670250183), 358: (0.9998476951564019, 0.017452406437284185), 359: (1.0000000000000107, 4.85722573273506e-16)}
    while running:
        clock.tick(fps)
        #print(int(clock.get_fps()))
        for event in py.event.get():
            if event.type == py.QUIT:
                running = 0
            if event.type == py.MOUSEBUTTONDOWN:
                #print(py.mouse.get_pos())
                pass
        if screen_on == "opening":
            draw_start_screen(start_text_1, start_text_1_cords, start_text_2, start_text_2_cords, start_button, floating_texts)
        elif screen_on == "map_select":
            draw_map_select_screen(pages, page_on, right_arrow, left_arrow, floating_texts)
        elif screen_on == "map_1":
            menu_ig.map = map_1
            map = map_1
            if menu_ig.just_placed and menu_ig.placeable:
                charictars_on_screen.append(menu_ig.place_charictar())
                money -= menu_ig.get_cost()
            elif menu_ig.just_placed and not menu_ig.placeable:
                floating_texts.append(floating_text(screen, "You cannot place that there", size=width//15))
            #full_rounds.run()
            if not paused:
                if counter % 3 == 0:
                    spawn_enemy("base_enemy", 10, zombie_image_list)
                    counter = 0
                counter += 1
            draw_map_screen(map_1_bg_img, map_1_bg_rect, menu_ig, charictars_on_screen, floating_texts, enemys, settings_wheel, projectiles)
        elif screen_on == "map_2":
            menu_ig.map = map_2
            map = map_2
            if menu_ig.just_placed and menu_ig.can_place(charictars_on_screen):
                charictars_on_screen.append(menu_ig.place_charictar())
                money -= menu_ig.get_cost()
            elif menu_ig.just_placed and not menu_ig.can_place(charictars_on_screen):
                floating_texts.append(floating_text(screen, "You cannot place that there", size=width//15))
            full_rounds.run()
            draw_map_screen(map_2_bg_img, map_2_bg_rect, menu_ig, charictars_on_screen, floating_texts, enemys, settings_wheel, projectiles)
    save()
    py.quit()
if __name__ == "__main__":
    main()
