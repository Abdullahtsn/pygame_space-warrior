import pygame as py
import sys
import os
import random
#import math




if getattr(sys,'frozen', False):        
    os.chdir(sys._MEIPASS)
else:                       
    os.chdir('.')


py.init()
py.mixer.init()


class GameWindow:
    def __init__(self):
        self.running = True
        self.scaled()
        self.screen = py.display.set_mode((1280*self.scale, 720*self.scale), py.NOFRAME)     
        self.clock = py.time.Clock()
        self.x = self.screen.get_width()
        self.y = self.screen.get_height()
        self.pageFlags()    
        self.menu = True                            #giriş ekranının menü olarak ayarlanması için.                            
        self.menu_background = py.transform.scale(py.image.load(os.path.join('image','9.jpg')).convert_alpha(),(1280*self.scale, 720*self.scale))
        self.game_background = py.transform.scale(py.image.load(os.path.join('image','16.jpg')).convert_alpha(),(1280*self.scale, 720*self.scale))
        self.hangar_background = py.transform.scale(py.image.load(os.path.join('image','13.jpg')).convert_alpha(),(1280*self.scale, 720*self.scale))
        self.guide_background = py.transform.scale(py.image.load(os.path.join('image','5.jpg')).convert_alpha(),(1280*self.scale, 720*self.scale))
        self.communication_background = py.transform.scale(py.image.load(os.path.join('image','14.jpg')).convert_alpha(),(1280*self.scale, 720*self.scale))
        self.gameover_background = py.transform.scale(py.image.load(os.path.join('image','7.jpg')).convert_alpha(),(1280*self.scale, 720*self.scale))
        self.bgrect = self.menu_background.get_rect()
        self.stateFlags()
        self.save_game_values()

    def pageFlags(self):
        self.windowbar = True
        self.menu = False
        
        self.start = False
        self.hangar = False
        self.guide = False
        self.communication = False
        self.gameOver = False
        self.pause = False
        self.replay = False

        self.player_ship_explosioned = False
        
        self.left_button_pressed = False
        self.right_button_pressed = False
        self.up_button_pressed = False
        self.down_button_pressed = False

        self.music_loop_paused = False
        self.music_loop_stoped = False
        
    def stateFlags(self):
        self.timer_start_and_player_ship_create = True
        self.score = 0
        self.level = 1
        self.time = 0
        self.player_ship_collision = 0
        self.enemy_missile_destroyed = 0
        self.meteor_destroyed = 0
        self.enemy_ship_destroyed = 0

    def save_game_values(self):
        self.end_time = self.time
        self.end_score = self.score
        self.end_level = self.level
        self.end_player_ship_collision = self.player_ship_collision
        self.end_enemy_missile_destroyed = self.enemy_missile_destroyed
        self.end_meteor_destroyed = self.meteor_destroyed
        self.end_enemy_ship_destroyed = self.enemy_ship_destroyed
        
    def scaled(self):
        a = py.display.get_desktop_sizes()
        y , z = a[0]
        if y == 1280 and z == 720 or y == 1366 and z == 768 or y == 1280 and z == 1024 or y == 1600 and z == 1200:
            self.scale = 1
        elif y == 1920 and z == 1080 or y == 1920 and z == 1200:
            self.scale = 1.5
        elif y == 2560 and z == 1440 or y == 2560 and z == 1600 or y == 3440 and z == 1440:
            self.scale = 2
        elif y == 3840 and z == 2160:
            self.scale = 3
        elif y == 5120 and z == 2880:
            self.scale = 4
        elif y == 7680 and z == 4320:
            self.scale = 6
        
game = GameWindow()


class WindowBarButtonCreate:
    def __init__(self,x,yol,yol2 = None) :
        self.x = x
        self.icon_size = (30*game.scale, 30*game.scale)
        if yol2 == None:
            self.image = py.transform.scale(py.image.load(os.path.join('icon',yol)).convert_alpha(),self.icon_size)
        else:
            self.image = [py.transform.scale(py.image.load(os.path.join('icon',yol)).convert_alpha(),self.icon_size),
                        py.transform.scale(py.image.load(os.path.join('icon',yol2)).convert_alpha(),self.icon_size)]
        self.rect = py.rect.Rect(x, 5*game.scale, self.icon_size[0], self.icon_size[1])


class WindowBar:
    def __init__(self):
        self.icon_size = (30*game.scale, 30*game.scale)
        self.windowbar_zone = py.draw.rect(game.screen,(70,89,69),(0, 0, game.x ,self.icon_size[1]+10*game.scale))
        self.menu = WindowBarButtonCreate(5*game.scale, 'menu.png')
        self.music = WindowBarButtonCreate(40*game.scale, 'music.png', 'music2.png')
        self.sound = WindowBarButtonCreate(75*game.scale, 'sound.png', 'sound2.png')
        self.close = WindowBarButtonCreate(game.x - self.icon_size[0]-5*game.scale, 'close.png')

        self.clicked = False
        self.musicflag = True
        self.soundflag = True

    def draw_and_click(self,event,mouse):
        #DRAW
        game.screen.blit(self.menu.image,(self.menu.rect))
        if self.musicflag:
            game.screen.blit(self.music.image[0], (self.music.rect))
        else:
            game.screen.blit(self.music.image[1], (self.music.rect))
        if self.soundflag:
            game.screen.blit(self.sound.image[0],(self.sound.rect))
        else:
            game.screen.blit(self.sound.image[1],(self.sound.rect))
        game.screen.blit(self.close.image,(self.close.rect))
        
        #CLİCK
        if self.windowbar_zone.collidepoint(mouse) and event.type == py.MOUSEBUTTONDOWN and event.button == 1 and not self.clicked:
            if self.menu.rect.collidepoint(mouse):
                if game.gameOver:                       #oyun sonu ekranında menüye tıklanırsa oyun sonu müziğinin durması için buraya yazdık. oyunun diğer bölümlerinde menüye tıklanınca durmamasını sağlıyor buraya bu şekilde yazınca.
                    if sound.game_over_played():        #sesin çalınıp çalınmadığını gösteren fonksiyon. çalınıyorsa durduruyoruz.
                        sound.game_over_stop()
                    else:
                        pass
                        
                game.pageFlags()
                game.menu = True
                
            elif self.music.rect.collidepoint(mouse):
                if self.musicflag == True:
                    self.musicflag = False
                elif self.musicflag == False:
                    self.musicflag = True
                sound.volume_settings()
            elif self.sound.rect.collidepoint(mouse):
                if self.soundflag == True:
                    self.soundflag = False
                elif self.soundflag == False:
                    self.soundflag = True
                sound.volume_settings()
            elif self.close.rect.collidepoint(mouse):
                game.running = False
            self.clicked = True
            sound.buton_play()
        elif event.type == py.MOUSEBUTTONUP and self.clicked:
            self.clicked = False    

windowBar = WindowBar()


class MenuButtonCreate:
    def __init__(self, text, y):
        self.y = y
        self.button_size = (180*game.scale, 50*game.scale)
        self.image = py.transform.scale(py.image.load(os.path.join('image','button.png')).convert_alpha(), self.button_size)
        self.font = py.font.Font(os.path.join('font','43.otf'), int(12*game.scale))
        self.render = self.font.render(text,True,(227,245,244))
        self.font_rect = self.render.get_rect()
        self.font_frame_rect = py.rect.Rect((game.x/2) - (self.button_size[0]/2), y, self.button_size[0], self.button_size[1])
        self.font_rect = py.rect.Rect(self.font_frame_rect.centerx - self.font_rect.width/2, self.font_frame_rect.centery - self.font_rect.height/2 - 2*game.scale , self.font_rect[2], self.font_rect[3])     
      
class Menu:
    def __init__(self):
        self.clicked = False
        self.start = MenuButtonCreate('START', 200*game.scale)
        self.hangar = MenuButtonCreate('HANGAR', 300*game.scale)
        self.guide = MenuButtonCreate('GUIDE', 400*game.scale)
        self.communication = MenuButtonCreate('COMMUNICATİON', 500*game.scale)

    def blits(self,buton):    
        game.screen.blit(buton.image,(buton.font_frame_rect))
        game.screen.blit(buton.render,(buton.font_rect))

    def draw_and_click(self,event,mouse):
        #DRAW
        self.blits(self.start)
        self.blits(self.hangar)
        self.blits(self.guide)
        self.blits(self.communication)

        #CLİCK
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1 and not self.clicked:
            if self.start.font_frame_rect.collidepoint(mouse):
                sound.buton_play()
                game.pageFlags()
                game.windowbar = False
                game.start = True
            elif self.hangar.font_frame_rect.collidepoint(mouse):
                sound.buton_play()
                game.pageFlags()
                game.hangar = True
            elif self.guide.font_frame_rect.collidepoint(mouse):
                sound.buton_play()
                game.pageFlags()
                game.guide = True
            elif self.communication.font_frame_rect.collidepoint(mouse):
                sound.buton_play()
                game.pageFlags()
                game.communication = True
            self.clicked = True
            
        elif event.type == py.MOUSEBUTTONUP and self.clicked:
            self.clicked = False
            

menu = Menu()


class Ships(py.sprite.Sprite):

    player_ships = [
    {'ships' : 1,
     'health' : 3500,
     'damage' : 1750,
     'speed' : 240,
     'armor' : 21,
     'h' : 62, 
     'w' : 66,
     'image_path': ['1','1B']},
    {'ships' : 2,
     'health' : 6500,
     'damage' : 1250,
     'speed' : 120,
     'armor' : 35,
     'h' : 66, 
     'w' : 100,
     'image_path': ['2','2B']},
    {'ships' : 3,
     'health' : 8500,
     'damage' : 900,
     'speed' : 110,
     'armor' : 45,
     'h' : 90, 
     'w' : 124,
     'image_path': ['3','3B']},
    {'ships' : 4,
     'health' : 6000,
     'damage' : 1500,
     'speed' : 180,
     'armor' : 25,
     'h' : 60, 
     'w' : 92,
     'image_path': ['4','4B']},
    {'ships' : 5,
     'health' : 4500,
     'damage' : 1900,
     'speed' : 270,
     'armor' : 13,
     'h' : 50, 
     'w' : 86,
     'image_path': ['5','5B']},
    {'ships' : 6,
     'health' : 5500,
     'damage' : 1200,
     'speed' : 180,
     'armor' : 20,
     'h' : 86, 
     'w' : 52,
     'image_path': ['6','6B']},
    {'ships' : 7,
     'health' : 6750,
     'damage' : 1100,
     'speed' : 210,
     'armor' : 27,
     'h' : 70, 
     'w' : 128,
     'image_path': ['7','7B']},
    {'ships' : 8,
     'health' : 3000,
     'damage' : 2000,
     'speed' : 300,
     'armor' : 13,
     'h' : 90, 
     'w' : 116,
     'image_path': ['8','8B']},    
    {'ships' : 9,
     'health' : 10000,
     'damage' : 500,
     'speed' : 90,
     'armor' : 70,
     'h' : 116, 
     'w' : 168,
     'image_path': ['9','9B']},    
    {'ships' : 10,
     'health' : 5000,
     'damage' : 700,
     'speed' : 300,
     'armor' : 51,
     'h' : 58, 
     'w' : 54,
     'image_path': ['10','10B']},
    {'ships' : 11,
     'health' : 7750,
     'damage' : 1000,
     'speed' : 270,
     'armor' : 17,
     'h' : 200, 
     'w' : 113,
     'image_path': ['11','11B']},
    {'ships' : 12,
     'health' : 6675,
     'damage' : 1340,
     'speed' : 150,
     'armor' : 33,
     'h' : 170, 
     'w' : 60,
     'image_path': ['12','12B']},
    {'ships' : 13,
     'health' : 7250,
     'damage' : 750,
     'speed' : 120,
     'armor' : 42,
     'h' : 84, 
     'w' : 52,
     'image_path': ['13','13B']}]

    def __init__(self, health, damage, speed, armor, w, h, image):
        super().__init__()
        self.health = health
        self.damage = damage
        self.speed = speed       #burada dtyi fonksiyona veremediğimiz için hızlarının hesaplandığı yerde speed ile çarparak vericez
        self.armor = armor
        self.w = w
        self.h = h
        self.image = image
        self.copy_image = image.copy()
        self.copy_image.set_alpha(150)          #set alphanın dönüş değeri olmadığı için önce resmi bi değişkene kopyaladık sonra onun alfa değerini ayarladıktan sonra başka bi değişkene eşitledik.
        self.transparent_image = self.copy_image
        self.rect = self.image.get_rect()
        self.collision = False           #çarpışma için gemiyi saydam yapıcak yer
        
        self.rect.x = 30*game.scale         #rect.x ve rect.y oyun başlarken ekranın sol ortadan başlaması için ayarlandı. bunlar olmasa sol üst köşe (0,0) koordinatlarında başlıyordu.
        self.rect.y = game.y/2 - 50
        self.space = 20*game.scale              #sınırlara tam yaklaşmadan durması için
        self.missile_fire = True                   #ateşleme için space ile birlikte bu bayrağıda koşula ekledik.
    
    def update(self,dt):      #dtleri buraya göndermemin sebebi gemilerin hızlarının burda hespalanması.
        if game.left_button_pressed:
            if hangar.ship_select.rect.x > 0 + self.space:
                hangar.ship_select.rect.x -= (hangar.ship_select.speed * game.scale * dt)  
        if game.right_button_pressed:
            if hangar.ship_select.rect.x < game.x - hangar.ship_select.rect.w - self.space:
                hangar.ship_select.rect.x += (hangar.ship_select.speed * game.scale * dt)  
        if game.up_button_pressed:
            if hangar.ship_select.rect.y > 0 + self.space:
                hangar.ship_select.rect.y -= (hangar.ship_select.speed * game.scale * dt) 
        if game.down_button_pressed:
            if hangar.ship_select.rect.y < game.y - hangar.ship_select.rect.h - self.space:
                hangar.ship_select.rect.y += (hangar.ship_select.speed * game.scale * dt) 
        
    def transparent_draw(self):
        game.screen.blit(self.transparent_image,(self.rect))
        

player_group = py.sprite.Group()


'''
#normalde bu şekilde her bir gemi için ayrı ayrı oluşturup hangarda sırayla bunlar üzerinde geiziniyordum ama bellekte yer kaplıyordu. 
#performan açısından kullanıcı seçtikten sonra oluşturmak daha mantıklı geldi o yüzden bunlar kaldırıldı. sınıf kısmında sözlüğe ayarlandı değerler.
ship_1 = Ships(3500, 1750, 240, 21, 62, 66, '1')
ship_2 = Ships(6500, 1250, 120, 35, 66, 100, '2')
ship_3 = Ships(8500, 900, 110, 45, 90, 124, '3')
ship_4 = Ships(6000, 1500, 180, 25, 60, 92, '4')
ship_5 = Ships(4500, 1900, 270, 13, 50, 86, '5')
ship_6 = Ships(5500, 1200, 180, 20, 86, 52, '6')
ship_7 = Ships(6750, 1100, 210, 27, 70, 128, '7')
ship_8 = Ships(3000, 2000, 300, 10, 90, 116, '8')    
ship_9 = Ships(10000, 500, 90, 60, 116, 168, '9')    
ship_10 = Ships(5000, 700, 300, 51, 58, 54, '10')
ship_11 = Ships(7750, 1000, 270, 17, 200, 113, '11')
ship_12 = Ships(6675, 1340, 150, 33, 170, 60, '12')
ship_13 = Ships(7250, 750, 120, 42, 84, 52, '13')
'''

class Missile(py.sprite.Sprite):
    size = (86*game.scale, 24*game.scale)
    image = py.transform.scale(py.image.load(os.path.join('rocket','missile.png')).convert_alpha(), size)
    def __init__(self,dt):
        super().__init__()
        self.image = Missile.image
        self.rect = self.image.get_rect()
        self.speed = (360*game.scale) * dt
        self.fire()                         #mermi ilk oluşturulurken konumunu ayarlama.

    def fire(self):
        self.rect.x = hangar.ship_select.rect.midright[0] - self.rect.width/2
        self.rect.y = hangar.ship_select.rect.midright[1] - Missile.size[1] / 2
    
    def update(self):
        if self.rect.midleft[0] < game.x :
            self.rect.x += self.speed
        else:
            self.kill()

missile_group = py.sprite.Group()


class Meteor(py.sprite.Sprite):
    meteor_point = 20        #meteor imhası puanı
    image = [py.transform.scale(py.image.load(os.path.join('enemies','meteor','1.png')).convert_alpha(), (50*game.scale, 50*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','meteor','2.png')).convert_alpha(), (50*game.scale, 44*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','meteor','3.png')).convert_alpha(), (50*game.scale, 50*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','meteor','4.png')).convert_alpha(), (50*game.scale, 22*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','meteor','5.png')).convert_alpha(), (50*game.scale, 44*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','meteor','6.png')).convert_alpha(), (50*game.scale, 48*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','meteor','7.png')).convert_alpha(), (50*game.scale, 50*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','meteor','8.png')).convert_alpha(), (50*game.scale, 50*game.scale))]
    def __init__(self,dt):
        super().__init__()
        self.image = random.choice(Meteor.image)
        self.rect = self.image.get_rect()
        self.speed = (random.randint(80,280)*game.scale) * dt
        self.rect.x = game.x
        self.rect.y = random.randint(self.rect.height , game.y - self.rect.height)
        self.point = 10
        self.damage = 500

    def update(self):
        if self.rect.midright[0] > 0:
            self.rect.x -= self.speed
        else:
            self.kill()

meteor_group = py.sprite.Group()       

        
class EnemyShip(py.sprite.Sprite):
    image = [py.transform.scale(py.image.load(os.path.join('enemies','ship','1.png')).convert_alpha(), (46*game.scale, 50*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','ship','2.png')).convert_alpha(), (74*game.scale, 46*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','ship','3.png')).convert_alpha(), (38*game.scale, 50*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','ship','4.png')).convert_alpha(), (40*game.scale, 54*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','ship','5.png')).convert_alpha(), (42*game.scale, 68*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','ship','6.png')).convert_alpha(), (42*game.scale, 50*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','ship','7.png')).convert_alpha(), (40*game.scale, 56*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','ship','8.png')).convert_alpha(), (54*game.scale, 64*game.scale)),
             py.transform.scale(py.image.load(os.path.join('enemies','ship','9.png')).convert_alpha(), (76*game.scale, 86*game.scale))] 
    enemy_ship_dict = {
        'level1' : {
            'health' : 4000,
            'damage' : 750,
            'speed' : 20*game.scale,
            'missile' : 8000,
            'point' : 100
            } ,
        'level2' : {
            'health' : 4750,
            'damage' : 1150,
            'speed' : 20*game.scale,
            'missile' : 7100,
            'point' : 150
            } ,
        'level3' : {
            'health' : 5345,
            'damage' : 1462,
            'speed' : 30*game.scale,
            'missile' : 6300,
            'point' : 200
            } ,
        'level4' : {
            'health' : 5999,
            'damage' : 1760,
            'speed' : 30*game.scale,
            'missile' : 5400,
            'point' : 300
            } ,
        'level5' : {
            'health' : 8957,
            'damage' : 1999,
            'speed' : 30*game.scale,
            'missile' : 4800,
            'point' : 500
            } ,
        'level6' : {
            'health' : 12346,
            'damage' : 2222,
            'speed' : 40*game.scale,
            'missile' : 4000,
            'point' : 1000
            } ,
        'level7' : {
            'health' : 15642,
            'damage' : 2340,
            'speed' : 40*game.scale,
            'missile' : 3500,
            'point' : 3000
            } ,
        'level8' : {
            'health' : 23645,
            'damage' : 3200,
            'speed' : 50*game.scale,
            'missile' : 3000,
            'point' : 5000
            } ,
        'level9' : {
            'health' : 36542,
            'damage' : 4100,
            'speed' : 60*game.scale,
            'missile' : 2000,
            'point' : 7000
            }
        }
    
    
    def __init__(self, image, health, damage, speed, missile_time, point):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = game.x + self.rect.width
        self.rect.y = random.randint(self.rect.height, game.y - self.rect.height)
        self.health = health
        self.damage = damage
        self.speed = speed      #math.ceil(speed)   yukarı tam sayıya yuvarlaması için.
        self.missile_time = missile_time
        self.point = point
        self.again = 0
        self.missile = True
        self.current_time = 0
        if self.speed < 0.52:
            self.speed = 0.52       #hız 0.5 ve altı olunca düşman gemileri hareket etmiyor. bazen ilk seviye düşmanların hızı 0.48de kaldığı için ekran  dışında kalıyor o yüzden böyle olanları yukarda bi değer sabitliyoruz..

    def update(self):
        if self.rect.midright[0] <= game.x :
            if self.again == 0:
                self.direction = random.choice(['left','right','up','down'])
                self.again += 1
            elif self.again > 20:
                self.again = 0
            elif 0 < self.again <= 20:
                self.again += 1
                if self.direction == 'left' and self.rect.x > game.x/2:
                    self.rect.x -= self.speed 
                elif self.direction == 'right' and self.rect.midright[0] < game.x :
                    self.rect.x += self.speed 
                elif self.direction == 'up' and self.rect.top > 0 + self.speed:
                    self.rect.y -= self.speed 
                elif self.direction == 'down' and self.rect.bottom < game.y - self.rect.y:
                    self.rect.y += self.speed 
        else:
            self.rect.x -= self.speed 

        #ENEMY SHIP TIMING MISSILE                  #gemilerin mermi zamanlamasına göre ateşlendiği blok
        last_time = py.time.get_ticks() 
        if last_time - self.current_time > self.missile_time:
            self.current_time = py.time.get_ticks() 
            self.missile_fire()
            print(last_time, self.current_time)

    def missile_fire(self):                         #düşman roketinin oluşturulduğu fonksiyon.
        enemy_ship_missile_group.add(EnemyShipMissile(self.rect.midleft[0], self.rect.midleft[1], self.damage))
        

enemy_ship_group = py.sprite.Group()


class EnemyShipMissile(py.sprite.Sprite):
    missile_point = 5        #rakip füze imhası puanı
    image = py.transform.scale(py.image.load(os.path.join('enemies','ship','missile2.png')).convert_alpha(), (84*game.scale, 24*game.scale))
    def __init__(self, x, y, damage):
        super().__init__()
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = 360*game.scale
        self.image = EnemyShipMissile.image
        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.rect.width/2
        self.rect.y = self.y - (self.rect.height/2)
    
    def update(self, dt):
        if self.rect.midright[0] > 0:
            self.rect.x -= self.speed * dt
        else:
            self.kill()
    
enemy_ship_missile_group = py.sprite.Group()


class Timing:
    def __init__(self):
        self.missile_time = py.USEREVENT +1        #oyuncu gemisi roket ateşlemesi için event oluşturma
        self.meteor_time = py.USEREVENT +2
        self.enemy_ship_time = py.USEREVENT +3
        self.level_time = py.USEREVENT +4
        self.transparent_time = py.USEREVENT +5     #gemi bişeye çarpınca saydam olması için zamanlayıcı
        self.info_time = py.USEREVENT +6
        
        self.paused_times = 0
        self.elapsed_times = py.time.get_ticks()
        self.elapsed_missile_time = py.time.get_ticks()        
        self.elapsed_meteor_time = py.time.get_ticks()
        self.elapsed_enemy_ship_time = py.time.get_ticks()
        self.elapsed_level_time = py.time.get_ticks()
        self.elapsed_transparent_time = py.time.get_ticks()
        self.elapsed_info_time = py.time.get_ticks()
        self.remaining_missile_time = 0        
        self.remaining_meteor_time = 0
        self.remaining_enemy_ship_time = 0
        self.remaining_level_time = 0
        self.remaining_transparent_time = 0
        self.remaining_info_time = 0

        self.info_select_time = 1000
        self.missile_select_time = 400
        self.transparent_select_time = 500
        self.meteor_select_time = None
        self.enemy_ship_select_time = None
        self.level_select_time = 30000              #burda none yapıp aşağıdaki gibi ilk değer için fonksiyon çalıştırsam zaten ilk seviyede olduğu için direk ikinci seviyeye geçecekti. 
                                                    #o yüzden zaten birinci seviyede olduğu için orda beklenilmesi gereken zamanı fonksiyona gitmeden burda ayarlıyorum.zaman dolunca fonksiyona gidip, yeni seviye için zamanlamayı ayarlayıp bir yukarı seviyeye yükselticek

        self.level_meteor_time()
        self.level_enemy_ship_time()
        
        self.stats = EnemyShip.enemy_ship_dict

        self.health_scale = 10
        self.damage_scale = 10
        self.speed_scale = 2
        self.armor_scale = 2
        self.stable_health = 2000
        self.stable_time = 60000

    def timer_start(self):
        py.time.set_timer(self.meteor_time, self.meteor_select_time)
        py.time.set_timer(self.enemy_ship_time, self.enemy_ship_select_time)
        py.time.set_timer(self.level_time, self.level_select_time)
        py.time.set_timer(self.info_time, self.info_select_time)
        self.elapsed_meteor_time = py.time.get_ticks()
        self.elapsed_enemy_ship_time = py.time.get_ticks()
        self.elapsed_level_time = py.time.get_ticks()
        self.elapsed_info_time = py.time.get_ticks()
        
    def level_meteor_time(self):
        if game.level == 1:
            self.meteor_select_time = random.randint(1500, 2300)
        elif game.level == 2:
            self.meteor_select_time = random.randint(1200, 2000)
        elif game.level == 3:
            self.meteor_select_time = random.randint(1000, 1700)
        elif game.level == 4:
            self.meteor_select_time = random.randint(1000, 1500)
        elif game.level == 5:
            self.meteor_select_time = random.randint(1000, 1400)
        elif game.level == 6:
            self.meteor_select_time = random.randint(600, 1200)
        elif game.level == 7:
            self.meteor_select_time = random.randint(500, 1000)
        elif game.level == 8:
            self.meteor_select_time = random.randint(400, 800)
        elif game.level == 9:
            self.meteor_select_time = random.randint(300, 600)
        py.time.set_timer(self.meteor_time, self.meteor_select_time)
        self.elapsed_meteor_time = py.time.get_ticks()
    
    def level_enemy_ship_time(self):
        if game.level == 1:
            self.enemy_ship_select_time = random.randint(7000, 10000)
        elif game.level == 2:
            self.enemy_ship_select_time = random.randint(5000, 9000)
        elif game.level == 3:
            self.enemy_ship_select_time = random.randint(5000, 8000)
        elif game.level == 4:
            self.enemy_ship_select_time = random.randint(4200, 7500)
        elif game.level == 5:
            self.enemy_ship_select_time = random.randint(3800, 7000)
        elif game.level == 6:
            self.enemy_ship_select_time = random.randint(3500, 6600)
        elif game.level == 7:
            self.enemy_ship_select_time = random.randint(3000, 6000)
        elif game.level == 8:
            self.enemy_ship_select_time = random.randint(2800, 5000)
        elif game.level == 9:
            self.enemy_ship_select_time = random.randint(2000, 4000)
        py.time.set_timer(self.enemy_ship_time, self.enemy_ship_select_time)
        self.elapsed_enemy_ship_time = py.time.get_ticks()

    
    #@staticmethod                   #static methot; sınıfın örneğini oluşturmak zorunda kalmadan sınıftan bağımsız olarak kullanılabilen fonksiyon oluşturmamızı sağlıyor.
    def create_enemy_ship(self, dt):            #düşman gemileri burda oluşturulurken hızlar başlangıç olarak ayarlanıyor. böylece hareket halindeyken gereksiz matematik işlemlerinden kurtulup tek değişkenle işlem yapılıyor.
        if game.level == 1:                     #eğer düşman gemilerindeki değerlerde değişiklik yapmak istersen enemyship classındaki dictte yap. ordaki sözlükten güncelleniyor değerler.
            enemy_ship_group.add(EnemyShip(EnemyShip.image[0], self.stats['level1']['health'], self.stats['level1']['damage'], self.stats['level1']['speed'] * dt, self.stats['level1']['missile'], self.stats['level1']['point']))
        elif game.level == 2:
            enemy_ship_group.add(EnemyShip(EnemyShip.image[1], self.stats['level2']['health'], self.stats['level2']['damage'], self.stats['level2']['speed'] * dt, self.stats['level2']['missile'], self.stats['level2']['point']))
        elif game.level == 3 :    
            enemy_ship_group.add(EnemyShip(EnemyShip.image[2], self.stats['level3']['health'], self.stats['level3']['damage'], self.stats['level3']['speed'] * dt, self.stats['level3']['missile'], self.stats['level3']['point']))
        elif game.level == 4 :    
            enemy_ship_group.add(EnemyShip(EnemyShip.image[3], self.stats['level4']['health'], self.stats['level4']['damage'], self.stats['level4']['speed'] * dt, self.stats['level4']['missile'], self.stats['level4']['point']))
        elif game.level == 5 :    
            enemy_ship_group.add(EnemyShip(EnemyShip.image[4], self.stats['level5']['health'], self.stats['level5']['damage'], self.stats['level5']['speed'] * dt, self.stats['level5']['missile'], self.stats['level5']['point']))
        elif game.level == 6 :    
            enemy_ship_group.add(EnemyShip(EnemyShip.image[5], self.stats['level6']['health'], self.stats['level6']['damage'], self.stats['level6']['speed'] * dt, self.stats['level6']['missile'], self.stats['level6']['point']))
        elif game.level == 7 :    
            enemy_ship_group.add(EnemyShip(EnemyShip.image[6], self.stats['level7']['health'], self.stats['level7']['damage'], self.stats['level7']['speed'] * dt, self.stats['level7']['missile'], self.stats['level7']['point']))
        elif game.level == 8 :    
            enemy_ship_group.add(EnemyShip(EnemyShip.image[7], self.stats['level8']['health'], self.stats['level8']['damage'], self.stats['level8']['speed'] * dt, self.stats['level8']['missile'], self.stats['level8']['point']))
        elif game.level == 9 :   
            enemy_ship_group.add(EnemyShip(EnemyShip.image[8], self.stats['level9']['health'], self.stats['level9']['damage'], self.stats['level9']['speed'] * dt, self.stats['level9']['missile'], self.stats['level9']['point']))

        self.dt = dt
    

    def next_level_time(self):
        if game.level == 1:
            self.level_select_time = 30000
        elif game.level == 2:
            self.level_select_time = 30000
        elif game.level == 3:
            self.level_select_time = 40000
        elif game.level == 4:
            self.level_select_time = 40000
        elif game.level == 5:
            self.level_select_time = 60000
        elif game.level == 6:
            self.level_select_time = 60000
        elif game.level == 7:
            self.level_select_time = 60000
        elif game.level == 8:
            self.level_select_time = 60000
        elif game.level == 9:
            self.level_select_time = self.stable_time

        py.time.set_timer(self.level_time, self.level_select_time)
        self.elapsed_level_time = py.time.get_ticks()

        if game.level < 9:
            game.level += 1
            self.ship_up_level()                            #atlanılan seviyeye göre nitelik artırımı.
        else:
            self.ship_fixed_level_health()                   
        
    def ship_up_level(self):                    #her seviyede geminin niteliklerinin yükseliceği fonksiyon
        hangar.ship_select.health += round(hangar.ship_select.health /100 * self.health_scale)
        hangar.ship_select.damage += round(hangar.ship_select.damage /100 * self.damage_scale)
        hangar.ship_select.speed += round(hangar.ship_select.speed /100 * self.speed_scale)
        hangar.ship_select.armor += round(hangar.ship_select.armor /100 * self.armor_scale)

    def ship_fixed_level_health(self):          #9.seviyeden sonra belli aralıklarla sabit can kazanımı.
        hangar.ship_select.health += (self.stable_health + (round(hangar.ship_select.health /100 * (self.health_scale *2))))

    def player_missile_fire(self):
        py.time.set_timer(self.missile_time, self.missile_select_time)  
        self.elapsed_missile_time = py.time.get_ticks()

    def ship_collision_transparent(self):
        hangar.ship_select.collision = True
        py.time.set_timer(self.transparent_time, self.transparent_select_time)
        self.elapsed_transparent_time = py.time.get_ticks()

    def calculate_times(self):
        self.elapsed_times = py.time.get_ticks() 
        
        self.remaining_missile_time = self.elapsed_times - self.elapsed_missile_time
        self.remaining_transparent_time = self.elapsed_times - self.elapsed_transparent_time
        self.remaining_meteor_time = self.meteor_select_time - (self.elapsed_times - self.elapsed_meteor_time)
        self.remaining_enemy_ship_time = self.enemy_ship_select_time - (self.elapsed_times - self.elapsed_enemy_ship_time)
        self.remaining_level_time = self.level_select_time - (self.elapsed_times - self.elapsed_level_time) 
        self.remaining_info_time = self.info_select_time - (self.elapsed_times - self.elapsed_info_time)

     
        if self.remaining_missile_time > self.missile_select_time:              #oyuncu gemisi mermi atışları ve gemiye çarpan nesneler olduğunda geminin saydam yapılması sürekli kendini tekrarlamadığı için kendini kuramayıp değeri sürekli artıyor.
            self.remaining_missile_time = self.missile_select_time              #bu yüzden bunları en fazla kendilerine eş değer olcak şekilde ayladık. sadece  bu ikisini. diğerleri kendi kendini kuruyor.
        if self.remaining_transparent_time > self.transparent_select_time:
            self.remaining_transparent_time = self.transparent_select_time
        
        print(self.remaining_info_time)
        
    def remaining_times(self):  
        
        py.time.set_timer(self.missile_time, self.remaining_missile_time)
        py.time.set_timer(self.transparent_time, self.remaining_transparent_time)
        py.time.set_timer(self.level_time, self.remaining_level_time)
        py.time.set_timer(self.meteor_time, self.remaining_meteor_time)
        py.time.set_timer(self.enemy_ship_time, self.remaining_enemy_ship_time)
        py.time.set_timer(self.info_time, self.remaining_info_time)
        
        self.paused_times = py.time.get_ticks() - self.elapsed_times        
        self.elapsed_missile_time += self.paused_times                  #bu kısımda set timer ile zamanlayıcıları başlatınca elapset ile damga koymamamın sebebi puase ile zaman durunca onlarıda dahil ediyordu .
        self.elapsed_transparent_time += self.paused_times              #o yüzden bu duraklatılan zamanı hesaplayıp elapsetteki zaman damgalarına ekleyerek sadece oyun içerisinde geçirilen zamana göre remaining hesaplanıp ona göre zamanlayıcı kuruluyor.
        self.elapsed_meteor_time += self.paused_times
        self.elapsed_enemy_ship_time += self.paused_times
        self.elapsed_level_time += self.paused_times
        self.elapsed_info_time += self.paused_times
    
    def time_enemy_missiles(self):
        for enemy in enemy_ship_group:
            enemy.current_time += self.paused_times

    def time_spent_in_game(self):
        py.time.set_timer(self.info_time, self.info_select_time)
        self.elapsed_info_time = py.time.get_ticks()

        
timing = Timing()


class Hangar:
    def __init__(self):
        self.ship_list = Ships.player_ships
        self.current_index = 0
        self.ship_select = None
        self.design = 1
        self.clicked = False
        #self.shipframe_size = (190*game.scale, 250*game.scale)
        #self.shipframe_image = py.transform.scale(py.image.load(os.path.join('image','shipframe.png')).convert_alpha(), self.shipframe_size)
        #self.shipframe_rect = py.rect.Rect( self.frame_rect.x + (self.frame_rect.width/2 - self.shipframe_image.get_width()/2) , self.frame_rect.centery - self.shipframe_image.get_height()/2 - 150*game.scale, self.shipframe_size[0] , self.shipframe_size[1] )
        #self.statsframe_size = (300*game.scale, 160*game.scale)
        #self.statsframe_image = py.transform.scale(py.image.load(os.path.join('image','statsframe.png')).convert_alpha(), self.statsframe_size)
        #self.statsframe_rect = py.rect.Rect(self.shipframe_rect.midbottom[0] - self.statsframe_image.get_width()/2, self.shipframe_rect.midbottom[1] + 100*game.scale, self.statsframe_size[0], self.statsframe_size[1])
        self.frame_size = (470*game.scale, 700*game.scale)
        self.icon_size = (50*game.scale, 50*game.scale)
        self.shipframe_size =  (200*game.scale, 200*game.scale)   
        self.statsframe_size = (220*game.scale, 300*game.scale)

        self.frame_image = py.transform.scale(py.image.load(os.path.join('image','hangarwindow.png')).convert_alpha(), self.frame_size)
        self.frame_image.set_alpha(200)         #resimleri zaten surface olarak yüklediği için direk set alpha diyerek onu saydam şekle getirebiliyoruz.
        self.frame_rect = py.rect.Rect(game.x/2 - self.frame_size[0]/2, game.y/2 - self.frame_size[1]/2, self.frame_size[0], self.frame_size[1])
        self.shipframe_rect = py.rect.Rect( self.frame_rect.x + (self.frame_rect.width/2 - self.shipframe_size[0]/2) , self.frame_rect.centery - self.shipframe_size[1]/2 - 120*game.scale, self.shipframe_size[0] , self.shipframe_size[1] )
        self.next_image = py.transform.scale(py.image.load(os.path.join('icon','next.png')).convert_alpha(), self.icon_size)
        self.next_rect = py.rect.Rect(self.shipframe_rect.midright[0] + 30*game.scale, self.shipframe_rect.midright[1] - self.next_image.get_height()/2,  self.icon_size[0], self.icon_size[1])
        self.back_image = py.transform.scale(py.image.load(os.path.join('icon','back.png')).convert_alpha(), self.icon_size)
        self.back_rect = py.rect.Rect(self.shipframe_rect.midleft[0] - 30*game.scale - self.back_image.get_width(), self.shipframe_rect.midleft[1] - self.next_image.get_height()/2,  self.icon_size[0], self.icon_size[1])
        self.design_image = [py.transform.scale(py.image.load(os.path.join('icon','design.png')).convert_alpha(), self.icon_size),
                         py.transform.scale(py.image.load(os.path.join('icon','design2.png')).convert_alpha(), self.icon_size)]
        self.design_rect = py.rect.Rect(self.shipframe_rect.midtop[0] - self.design_image[0].get_width()/2, self.shipframe_rect.midtop[1] - self.design_image[0].get_height() - 30*game.scale, self.icon_size[0], self.icon_size[1])

        self.statsframe_rect = py.rect.Rect(self.shipframe_rect.midbottom[0] - self.statsframe_size[0]/2, self.shipframe_rect.midbottom[1] + 30*game.scale, self.statsframe_size[0], self.statsframe_size[1])
        self.health_image = py.transform.scale(py.image.load(os.path.join('icon','health.png')).convert_alpha(), (50*game.scale ,50*game.scale))        #simgelerin formları korunsun diye her biri kendine göre ölçeklendi. o yüzden değişkene sabitlenmedi.
        self.health_rect = py.rect.Rect(self.statsframe_rect.topleft[0] +30*game.scale, self.statsframe_rect.topleft[1] +20*game.scale, self.health_image.get_width(), self.health_image.get_height())
        self.damage_image = py.transform.scale(py.image.load(os.path.join('icon','damage.png')).convert_alpha(), (50*game.scale, 50*game.scale))
        self.damage_rect = py.rect.Rect(self.statsframe_rect.topleft[0] +30*game.scale, self.statsframe_rect.topleft[1] +86*game.scale, self.damage_image.get_width(), self.damage_image.get_height())
        self.speed_image = py.transform.scale(py.image.load(os.path.join('icon','speed.png')).convert_alpha(), (50*game.scale, 50*game.scale))
        self.speed_rect = py.rect.Rect(self.statsframe_rect.topleft[0] +30*game.scale, self.statsframe_rect.topleft[1] +160*game.scale, self.speed_image.get_width(), self.speed_image.get_height())
        self.armor_image = py.transform.scale(py.image.load(os.path.join('icon','armor.png')).convert_alpha(), (50*game.scale, 50*game.scale))
        self.armor_rect = py.rect.Rect(self.statsframe_rect.topleft[0] +30*game.scale, self.statsframe_rect.topleft[1] +230*game.scale, self.armor_image.get_width(), self.armor_image.get_height())

        self.font = py.font.Font(os.path.join('font','37.ttf'), int(20*game.scale))
        self.render = self.font.render('546',True,(0,0,0)).get_rect()           #bu satır yazının ortalama genişlik ve yüksekliğinin ölçüsünü alabilmek için yazıldı.

        self.player_ship_select()                                               #hangara tıklanmasa bile varsayılan olarak bir geminin seçili olması için başlangıçta bir kere çalıştırıyoruz.

    def draw_and_click(self,event, mouse):
        #DRAW-FRAME
        game.screen.blit(self.frame_image,(self.frame_rect))
        py.draw.rect(game.screen,(0,0,0),self.shipframe_rect, border_radius= int(30*game.scale))
        py.draw.rect(game.screen,(0,0,0),self.statsframe_rect, border_radius= int(30*game.scale))
        #DRAW-ICON
        if self.design == 1:
            game.screen.blit(self.design_image[0],(self.design_rect))
        else:
            game.screen.blit(self.design_image[1],(self.design_rect))
        game.screen.blit(self.next_image,(self.next_rect))
        game.screen.blit(self.back_image,(self.back_rect))
        game.screen.blit(self.health_image,(self.health_rect))
        game.screen.blit(self.damage_image,(self.damage_rect))
        game.screen.blit(self.speed_image,(self.speed_rect))
        game.screen.blit(self.armor_image,(self.armor_rect))
        #game.screen.blit(self.statsframe_image,(self.statsframe_rect))
        #game.screen.blit(self.shipframe_image,(self.shipframe_rect))

        #CLİCK
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1 and not self.clicked:
            if self.next_rect.collidepoint(mouse):
                if self.current_index < len(self.ship_list) -1:
                    self.current_index += 1
                else:
                    self.current_index = 0
            elif self.back_rect.collidepoint(mouse):
                if self.current_index > 0:
                    self.current_index -= 1
                else:
                    self.current_index = len(self.ship_list) -1
            elif self.design_rect.collidepoint(mouse):
                if self.design == 1:
                    self.design = 2
                else:
                    self.design = 1
            self.clicked = True
            self.player_ship_select()                           #kullanıcı hanhar kısmında her gemi dğeiştiğinde geminin ayarlanması için çalışacak fonksiyon
            sound.buton_play()
        elif event.type == py.MOUSEBUTTONUP and self.clicked:
            self.clicked = False

        #SELECT-SHİP
        self.show_ship_info()

    def player_ship_select(self):
        self.ship_select = self.ship_list[self.current_index]
        if self.design == 1:
            self.ship_select_image = py.transform.scale(py.image.load(os.path.join('ships',f'{self.ship_select['image_path'][0]}.png')).convert_alpha(), (self.ship_select['w']*game.scale, self.ship_select['h']*game.scale))   
        elif self.design == 2:
            self.ship_select_image = py.transform.scale(py.image.load(os.path.join('ships',f'{self.ship_select['image_path'][1]}.png')).convert_alpha(), (self.ship_select['w']*game.scale, self.ship_select['h']*game.scale))  

    def show_ship_info(self):
        game.screen.blit(self.ship_select_image, (self.shipframe_rect.center[0] - self.ship_select['w']*game.scale/2, self.shipframe_rect.center[1] - self.ship_select['h']*game.scale/2 , self.ship_select['h']*game.scale, self.ship_select['h']*game.scale))
        game.screen.blit(self.font.render(str(self.ship_select['health']), True, (67,100,165)), (self.health_rect.midright[0] + 40*game.scale , self.health_rect.midright[1] - self.render.height/2))
        game.screen.blit(self.font.render(str(self.ship_select['damage']), True, (67,100,165)), (self.damage_rect.midright[0] + 40*game.scale , self.damage_rect.midright[1] - self.render.height/2))
        game.screen.blit(self.font.render(str(self.ship_select['speed']), True, (67,100,165)), (self.speed_rect.midright[0] + 40*game.scale , self.speed_rect.midright[1] - self.render.height/2))
        game.screen.blit(self.font.render(str(self.ship_select['armor']), True, (67,100,165)),( self.armor_rect.midright[0] + 40*game.scale , self.armor_rect.midright[1] - self.render.height/2))

hangar = Hangar()

class Info_in_game:
    def __init__(self):
        self.font = self.font = py.font.Font(os.path.join('font','43.otf'), int(8*game.scale))
        self.info_player_frame_rect = py.rect.Rect(0, 0, 106*game.scale, 72*game.scale)
        self.player_text_color = (100,100,250)
        self.info_enemy_frame_rect = py.rect.Rect(game.x - 104*game.scale, game.y - 88*game.scale, 104*game.scale, 88*game.scale)
        self.enemy_text_color = (100,100,250)
        self.info_game_frame_rect = py.rect.Rect(0, game.y - 54*game.scale, 96*game.scale, 54*game.scale)
        self.game_text_color = (100,100,250)

    def info_player_ship(self):          #burda health damage gibi değişkenlerin beyaz görünmesi henüz oyuncu gemisi oluşturulmadığından kaynaklı. oyun içerisinde oluşturulunca sorunsuz çalışıcak.
        self.health_text = self.font.render(f'HEALTH  :  {hangar.ship_select.health}', True, self.player_text_color)
        self.damage_text = self.font.render(f'DAMAGE  :  {hangar.ship_select.damage}', True, self.player_text_color)
        self.speed_text = self.font.render(f'SPEED  :  {hangar.ship_select.speed}', True, self.player_text_color)
        self.armor_text = self.font.render(f'ARMOR  :  {hangar.ship_select.armor}', True, self.player_text_color)
        
        self.player_frame = py.draw.rect(game.screen,(0,0,0), self.info_player_frame_rect, border_bottom_right_radius= int(4*game.scale))
        self.player_frame2 = py.draw.rect(game.screen,self.player_text_color, self.info_player_frame_rect, border_bottom_right_radius= int(4*game.scale),width= int(2*game.scale))
        game.screen.blit(self.health_text,(self.info_player_frame_rect.topleft[0] + 8*game.scale, self.info_player_frame_rect.topleft[1] + 6*game.scale))
        game.screen.blit(self.damage_text,(self.info_player_frame_rect.topleft[0] + 8*game.scale , self.info_player_frame_rect.topleft[1] + 22*game.scale))
        game.screen.blit(self.speed_text,(self.info_player_frame_rect.topleft[0] + 8*game.scale , self.info_player_frame_rect.topleft[1] + 38*game.scale))
        game.screen.blit(self.armor_text,(self.info_player_frame_rect.topleft[0] + 8*game.scale , self.info_player_frame_rect.topleft[1] + 54*game.scale))

    def info_enemy_ship(self):
        self.enemy_frame = py.draw.rect(game.screen,(0,0,0), self.info_enemy_frame_rect, border_top_left_radius= int(4*game.scale))
        self.enemy_frame2 = py.draw.rect(game.screen,self.enemy_text_color, self.info_enemy_frame_rect, border_top_left_radius= int(4*game.scale),width= int(2*game.scale))
        self.enemy_health_title = self.font.render('ENEMY HEALTH', True, self.enemy_text_color)
        a = 6
        game.screen.blit(self.enemy_health_title,(self.info_enemy_frame_rect.topleft[0] + 8*game.scale, self.info_enemy_frame_rect.topleft[1] + a*game.scale))
        for enemy in enemy_ship_group:
            a += 16
            self.enemy_health_text = self.font.render(f'+ {enemy.health}', True, self.enemy_text_color)
            game.screen.blit(self.enemy_health_text,(self.info_enemy_frame_rect.topleft[0] + 8*game.scale, self.info_enemy_frame_rect.topleft[1] + a*game.scale))
            
    def info_game_value(self):
        self.level_text = self.font.render(f'LEVEL  :  {game.level}', True, self.game_text_color)
        self.score_text = self.font.render(f'SCORE  :  {game.score}', True, self.game_text_color)
        self.time_text = self.font.render(f'TİME  :   {game.time}', True, self.game_text_color)
        self.game_frame = py.draw.rect(game.screen,(0,0,0), self.info_game_frame_rect, border_top_right_radius= int(4*game.scale))
        self.game_frame2 = py.draw.rect(game.screen,self.game_text_color, self.info_game_frame_rect, border_top_right_radius= int(4*game.scale),width= int(2*game.scale))
        game.screen.blit(self.level_text,(self.info_game_frame_rect.topleft[0] + 8*game.scale , self.info_game_frame_rect.topleft[1] + 6*game.scale))
        game.screen.blit(self.score_text,(self.info_game_frame_rect.topleft[0] + 8*game.scale , self.info_game_frame_rect.topleft[1] + 22*game.scale))
        game.screen.blit(self.time_text,(self.info_game_frame_rect.topleft[0] + 8*game.scale , self.info_game_frame_rect.topleft[1] + 38*game.scale))

info_in_game = Info_in_game()
        
        
class PlayEvent:
    def __init__(self):
        self.icon_size = (30*game.scale, 30*game.scale)
        self.frame_rect = py.rect.Rect(game.x - self.icon_size[0] - 220*game.scale ,0 ,self.icon_size[0] + 220*game.scale, 10*game.scale + self.icon_size[1] )        #eğer sonradan buton eklersen buraya bak bu çerçeveyi genişlet. tıklamalar bu çerçevenin içine göre yapılıyor.
        self.gameover = WindowBarButtonCreate(game.x - self.icon_size[0]-215*game.scale, 'gameover.png')
        self.music = WindowBarButtonCreate(game.x - self.icon_size[0]-180*game.scale, 'music.png', 'music2.png')
        self.sound = WindowBarButtonCreate(game.x - self.icon_size[0]-145*game.scale, 'sound.png', 'sound2.png')
        self.info = WindowBarButtonCreate(game.x - self.icon_size[0]-110*game.scale, 'info.png', 'info2.png')
        self.replay = WindowBarButtonCreate(game.x - self.icon_size[0]-75*game.scale, 'replay.png')
        self.play = WindowBarButtonCreate(game.x - self.icon_size[0]-40*game.scale, 'play.png', 'pause.png')
        self.close = WindowBarButtonCreate(game.x - self.icon_size[0]-5*game.scale, 'close.png')
        self.clicked = False
        self.screen_shot = False
        self.info_flag = True
        
    def play_pause_bar(self,event,mouse): 
        game.screen.blit(self.gameover.image,(self.gameover.rect))
        game.screen.blit(self.replay.image,(self.replay.rect))
        game.screen.blit(self.close.image,(self.close.rect))
        if self.info_flag:
            game.screen.blit(self.info.image[0], (self.info.rect))
        else:
            game.screen.blit(self.info.image[1], (self.info.rect))

        if game.pause:
            game.screen.blit(self.play.image[0], (self.play.rect))
        else:
            game.screen.blit(self.play.image[1], (self.play.rect))

        if windowBar.musicflag:
            game.screen.blit(self.music.image[0], (self.music.rect))
        else:
            game.screen.blit(self.music.image[1], (self.music.rect))

        if windowBar.soundflag:
            game.screen.blit(self.sound.image[0],(self.sound.rect))
        else:
            game.screen.blit(self.sound.image[1],(self.sound.rect))
        
        #CLİCK
        if self.frame_rect.collidepoint(mouse) and event.type == py.MOUSEBUTTONDOWN and event.button == 1 and not self.clicked:
            if self.info.rect.collidepoint(mouse):
                if self.info_flag:
                    self.info_flag = False
                elif not self.info_flag:
                    self.info_flag = True
            elif self.gameover.rect.collidepoint(mouse):
                end_game_preparations()
            elif self.music.rect.collidepoint(mouse):
                if windowBar.musicflag == True:
                    windowBar.musicflag = False
                elif windowBar.musicflag == False:
                    windowBar.musicflag = True
                sound.volume_settings()
            elif self.sound.rect.collidepoint(mouse):
                if windowBar.soundflag == True:
                    windowBar.soundflag = False
                elif windowBar.soundflag == False:
                    windowBar.soundflag = True
                sound.volume_settings()

            elif self.replay.rect.collidepoint(mouse):
                game.save_game_values()                         #oyun içi değerler sıfırlanmadan önce oyuncuya bilgi amaçlı değişkenlere aktarıldı fonksiyon.
                hangar.ship_select.kill()
                clear_lists()            #liste ve spriteleri sıfırlama
                reset_times()            #zamanlayıcıları sıfırlama
                reset_player_ship()
                game.pageFlags()
                game.stateFlags()
                game.windowbar = False
                game.start = True
            elif self.play.rect.collidepoint(mouse):
                self.play_pause_function()                      #bunu burda fonksiyon olarak tanımlamamızın sebebi keyslerde p tuşunada koyucaz kullanıcıya kolaylık olsun diye. p ye basılınca buraya ulaşamıycağımız için burdaki işlemleri bi fonksiyona topladık. o fonksiyona istediğimiz yerden ulaşabiliriz.
            elif self.close.rect.collidepoint(mouse):
                game.running = False
            self.clicked = True
            sound.buton_play()
        elif event.type == py.MOUSEBUTTONUP and self.clicked:
            self.clicked = False  
    
    def record_screen_shot(self):                           #durdurmaya basınca o anki ekranı kaydedip onu çizmesi için çalışacak fonksiyon
        self.screen_shot = py.Surface((game.x, game.y))
        self.screen_shot.blit(game.screen,(0,0))

    def play_pause_function(self):
        if game.pause == True:
            game.pause = False
            game.start = True
            self.screen_shot = None                 #resmi tutup bellekte yer kaplamaması için durdurulmuyorken noneye ayarladım.
            timing.remaining_times()
            timing.time_enemy_missiles()
            sound.gameloop_unpause()
        elif game.pause == False:
            game.pause = True
            game.start = False
            self.record_screen_shot()
            timing.calculate_times()
            reset_times()
            sound.gameloop_pause()
    
    
play_pause_event = PlayEvent()


class Guide:
    def __init__(self):
        self.alpha_shipframe = py.Surface(py.Rect(0, 0, game.x, game.y).size, py.SRCALPHA)
        self.icon_size = (50*game.scale, 50*game.scale)
        self.black_alpha_value = (0,0,0,208)
        self.title_color = (0,150,0)
        self.text_color = (100,100,250)
        #self.text_color = (67,100,200)
        self.clicked = False
        self.image = None
        self.stats = None
        self.current_index = 0
        self.enemy_image = EnemyShip.image
        self.enemy_stats = [EnemyShip.enemy_ship_dict['level1'],            
                            EnemyShip.enemy_ship_dict['level2'],
                            EnemyShip.enemy_ship_dict['level3'],
                            EnemyShip.enemy_ship_dict['level4'],
                            EnemyShip.enemy_ship_dict['level5'],
                            EnemyShip.enemy_ship_dict['level6'],
                            EnemyShip.enemy_ship_dict['level7'],
                            EnemyShip.enemy_ship_dict['level8'],
                            EnemyShip.enemy_ship_dict['level9']]
        
        
        self.shipframe_rect = py.rect.Rect( 200*game.scale , 80*game.scale , 160*game.scale, 160*game.scale )
        self.statsframe_rect = py.rect.Rect( 160*game.scale , 270*game.scale , 240*game.scale, 184*game.scale )
        self.pointinfoframe_rect = py.rect.Rect( 500*game.scale, 80*game.scale, 200*game.scale, 420*game.scale)
        self.levelinfoframe_rect = py.rect.Rect( 760*game.scale , 80*game.scale , 256*game.scale, 334*game.scale )
        self.keysinfoframe_rect = py.rect.Rect( 160*game.scale , 480*game.scale , 220*game.scale, 214*game.scale )
        self.rulesinfoframe_rect = py.rect.Rect( 460*game.scale, game.y - 190*game.scale, 700*game.scale, 150*game.scale)
        
        
        self.next_image = py.transform.scale(py.image.load(os.path.join('icon','next.png')).convert_alpha(), self.icon_size)
        self.next_rect = py.rect.Rect(self.shipframe_rect.midright[0] + 30*game.scale, self.shipframe_rect.midright[1] - self.next_image.get_height()/2,  self.icon_size[0], self.icon_size[1])
        self.back_image = py.transform.scale(py.image.load(os.path.join('icon','back.png')).convert_alpha(), self.icon_size)
        self.back_rect = py.rect.Rect(self.shipframe_rect.midleft[0] - 30*game.scale - self.back_image.get_width(), self.shipframe_rect.midleft[1] - self.next_image.get_height()/2,  self.icon_size[0], self.icon_size[1])
        
        self.font = py.font.Font(os.path.join('font','37.ttf'), int(20*game.scale))
    
    def draw_rect_transparent_frame(self, ):
        #frameleri yarı saydam çizebilmek için bi surface oluşturup (self.alpha_shipframe) buna bi bayrak ekliyoruz (py.SRCALPHA). yarı saydam olmasını istediğimiz şeyleri önce bu yüzeye çizip, en son bu yüzeyi genel kullandığımız yüzeye aktarıyoruz.
        self.alpha_shipframe.fill((0,0,0,0))
        py.draw.rect(self.alpha_shipframe, self.black_alpha_value, self.shipframe_rect, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_shipframe, self.black_alpha_value, self.statsframe_rect, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_shipframe, self.black_alpha_value, self.keysinfoframe_rect, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_shipframe, self.black_alpha_value, self.levelinfoframe_rect, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_shipframe, self.black_alpha_value, self.pointinfoframe_rect, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_shipframe, self.black_alpha_value, self.rulesinfoframe_rect, border_radius=int(10*game.scale))
        game.screen.blit(self.alpha_shipframe, self.alpha_shipframe.get_rect())

    def draw_and_click(self, event, mouse):
        #DRAW FRAME
        self.draw_rect_transparent_frame()

        #DRAW İCON
        game.screen.blit(self.next_image,(self.next_rect))
        game.screen.blit(self.back_image,(self.back_rect))

        #CLICK 
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1 and not self.clicked:
            if self.next_rect.collidepoint(mouse):
                if self.current_index < len(self.enemy_stats) -1:
                    self.current_index += 1
                else:
                    self.current_index = 0
            elif self.back_rect.collidepoint(mouse):
                if self.current_index > 0:
                    self.current_index -= 1
                else:
                    self.current_index = len(self.enemy_stats) -1
            self.clicked = True
            sound.buton_play()
        elif event.type == py.MOUSEBUTTONUP and self.clicked:
            self.clicked = False
        
        self.show_enemy_image()
        self.show_enemy_stats()
        self.level_info()
        self.score_info()
        self.keys_info()
        self.rules_info()

    def show_enemy_image(self):
        self.image = self.enemy_image[self.current_index]
        game.screen.blit(self.image, (self.shipframe_rect.center[0] - self.image.get_width()/2, self.shipframe_rect.center[1] - self.image.get_height()/2 , self.image.get_width(), self.image.get_height()))

    def show_enemy_stats(self):
        self.stats = self.enemy_stats[self.current_index]
        game.screen.blit(self.font.render(f'ENEMY LEVEL :  {self.current_index +1}', True, self.title_color), (self.statsframe_rect.topleft[0] + 20* game.scale, self.statsframe_rect.topleft[1] + 20* game.scale ))
        game.screen.blit(self.font.render(f'HEALTH :  {self.stats['health']}', True, self.text_color), (self.statsframe_rect.topleft[0] + 20* game.scale, self.statsframe_rect.topleft[1] + 50* game.scale ))
        game.screen.blit(self.font.render(f'DAMAGE :  {self.stats['damage']}', True, self.text_color), (self.statsframe_rect.topleft[0] + 20* game.scale, self.statsframe_rect.topleft[1] + 80* game.scale ))
        game.screen.blit(self.font.render(f'SPEED :   {self.stats['speed']}', True, self.text_color), (self.statsframe_rect.topleft[0] + 20* game.scale, self.statsframe_rect.topleft[1] + 110* game.scale ))
        game.screen.blit(self.font.render(f'MISSILE TIME :  {self.stats['missile']/1000}', True, self.text_color), (self.statsframe_rect.topleft[0] + 20* game.scale, self.statsframe_rect.topleft[1] + 140* game.scale ))
        
    def level_info(self):
        game.screen.blit(self.font.render('LEVEL UP PLAYER STATS', True, self.title_color), (self.levelinfoframe_rect.topleft[0] + 20*game.scale, self.levelinfoframe_rect.topleft[1] + 20*game.scale))
        game.screen.blit(self.font.render(f'( FOR EVERY LEVEL UP )', True, self.text_color), (self.levelinfoframe_rect.topleft[0] + 20*game.scale, self.levelinfoframe_rect.topleft[1] + 50*game.scale))
        game.screen.blit(self.font.render(f'+ %{timing.health_scale} HEALTH', True, self.text_color), (self.levelinfoframe_rect.topleft[0] + 20*game.scale, self.levelinfoframe_rect.topleft[1] + 80*game.scale))
        game.screen.blit(self.font.render(f'+ %{timing.damage_scale} DAMAGE', True, self.text_color), (self.levelinfoframe_rect.topleft[0] + 20*game.scale, self.levelinfoframe_rect.topleft[1] + 110*game.scale))
        game.screen.blit(self.font.render(f'+ %{timing.speed_scale} SPEED', True, self.text_color), (self.levelinfoframe_rect.topleft[0] + 20*game.scale, self.levelinfoframe_rect.topleft[1] + 140*game.scale))
        game.screen.blit(self.font.render(f'+ %{timing.armor_scale} ARMOR', True, self.text_color), (self.levelinfoframe_rect.topleft[0] + 20*game.scale, self.levelinfoframe_rect.topleft[1] + 170*game.scale))
        game.screen.blit(self.font.render('9.LEVEL PLAYER STATS', True, self.title_color), (self.levelinfoframe_rect.topleft[0] + 20*game.scale, self.levelinfoframe_rect.topleft[1] + 200*game.scale))
        game.screen.blit(self.font.render(f'( FOR EVERY {round(timing.stable_time/1000)} SECONDS )', True, self.text_color), (self.levelinfoframe_rect.topleft[0] + 20*game.scale, self.levelinfoframe_rect.topleft[1] + 230*game.scale))
        game.screen.blit(self.font.render(f'+ %{timing.health_scale*2} HEALTH', True, self.text_color), (self.levelinfoframe_rect.topleft[0] + 20*game.scale, self.levelinfoframe_rect.topleft[1] + 260*game.scale))
        game.screen.blit(self.font.render(f'+ {timing.stable_health} HEALTH', True, self.text_color), (self.levelinfoframe_rect.topleft[0] + 20*game.scale, self.levelinfoframe_rect.topleft[1] + 290*game.scale))

    def score_info(self):
        game.screen.blit(self.font.render('ENEMY SHIP POINTS', True, self.title_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 20*game.scale))
        game.screen.blit(self.font.render(f'Level 1 : {self.enemy_stats[0]['point']}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 50*game.scale))
        game.screen.blit(self.font.render(f'Level 2 : {self.enemy_stats[1]['point']}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 80*game.scale))
        game.screen.blit(self.font.render(f'Level 3 : {self.enemy_stats[2]['point']}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 110*game.scale))
        game.screen.blit(self.font.render(f'Level 4 : {self.enemy_stats[3]['point']}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 140*game.scale))
        game.screen.blit(self.font.render(f'Level 5 : {self.enemy_stats[4]['point']}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 170*game.scale))
        game.screen.blit(self.font.render(f'Level 6 : {self.enemy_stats[5]['point']}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 200*game.scale))
        game.screen.blit(self.font.render(f'Level 7 : {self.enemy_stats[6]['point']}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 230*game.scale))
        game.screen.blit(self.font.render(f'Level 8 : {self.enemy_stats[7]['point']}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 260*game.scale))
        game.screen.blit(self.font.render(f'Level 9 : {self.enemy_stats[8]['point']}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 290*game.scale))
        game.screen.blit(self.font.render('OTHER POINTS', True, self.title_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 320*game.scale))
        game.screen.blit(self.font.render(f'Enemy Missile : {EnemyShipMissile.missile_point}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 350*game.scale))
        game.screen.blit(self.font.render(f'Meteor : {Meteor.meteor_point}', True, self.text_color), (self.pointinfoframe_rect.topleft[0] + 20*game.scale, self.pointinfoframe_rect.topleft[1] + 380*game.scale))

    def keys_info(self):
        game.screen.blit(self.font.render('KEYS', True, self.title_color), (self.keysinfoframe_rect.topleft[0] + 20*game.scale, self.keysinfoframe_rect.topleft[1] + 20*game.scale))
        game.screen.blit(self.font.render('W-A-S-D or Arrows', True, self.text_color), (self.keysinfoframe_rect.topleft[0] + 20*game.scale, self.keysinfoframe_rect.topleft[1] + 50*game.scale))
        game.screen.blit(self.font.render('Fire : SPACE', True, self.text_color), (self.keysinfoframe_rect.topleft[0] + 20*game.scale, self.keysinfoframe_rect.topleft[1] + 80*game.scale))
        game.screen.blit(self.font.render('Pause-Play : P', True, self.text_color), (self.keysinfoframe_rect.topleft[0] + 20*game.scale, self.keysinfoframe_rect.topleft[1] + 110*game.scale))
        game.screen.blit(self.font.render('Menu : ESC', True, self.text_color), (self.keysinfoframe_rect.topleft[0] + 20*game.scale, self.keysinfoframe_rect.topleft[1] + 140*game.scale))
        game.screen.blit(self.font.render('Exit : F4', True, self.text_color), (self.keysinfoframe_rect.topleft[0] + 20*game.scale, self.keysinfoframe_rect.topleft[1] + 170*game.scale))
        
        
    def rules_info(self):
        game.screen.blit(self.font.render('OTHER GAME RULES', True, self.title_color), (self.rulesinfoframe_rect.topleft[0] + 20*game.scale, self.rulesinfoframe_rect.topleft[1] + 20*game.scale))
        game.screen.blit(self.font.render('- IF A MISSILE AND A MISSILE OR METEOR COLLIDE, THEY DESTROY EACH OTHER', True, self.text_color), (self.rulesinfoframe_rect.topleft[0] + 20*game.scale, self.rulesinfoframe_rect.topleft[1] + 50*game.scale))
        game.screen.blit(self.font.render('- THERE CAN BE A MAXIMUM OF 4 ENEMY SHIPS AT THE SAME TIME', True, self.text_color), (self.rulesinfoframe_rect.topleft[0] + 20*game.scale, self.rulesinfoframe_rect.topleft[1] + 80*game.scale))
        game.screen.blit(self.font.render('- POINTS WILL NOT BE GIVEN FOR OBJECTS DESTROYED BY HITTING THE SHIP', True, self.text_color), (self.rulesinfoframe_rect.topleft[0] + 20*game.scale, self.rulesinfoframe_rect.topleft[1] + 110*game.scale))
        

guide = Guide()


class Communication:
    def __init__(self):
        self.font = py.font.Font(os.path.join('font','7.ttf'), int(30*game.scale))
        self.gmail = self.font.render('abdullah.tosun.9696@gmail.com',True,(227,245,244))
        self.gmail_rect = py.rect.Rect(game.x/2 - self.gmail.get_width()/2, game.y/2 - self.gmail.get_height()/2 - 40*game.scale, 0, 0)
        self.github = self.font.render('https://github.com/Abdullahtsn',True,(227,245,244))
        self.github_rect = py.rect.Rect(game.x/2 - self.github.get_width()/2, game.y/2 - self.github.get_height()/2 + 40*game.scale, 0, 0)
    def draw(self):
        game.screen.blit(self.gmail,(self.gmail_rect))
        game.screen.blit(self.github,(self.github_rect))

communication = Communication()


class GameOver:
    def __init__(self):
        self.font = py.font.Font(os.path.join('font','37.ttf'), int(22*game.scale))
        self.alpha_surface = py.Surface(py.Rect(0, 0, game.x, game.y).size, py.SRCALPHA)

        self.inner_frame_rect = py.rect.Rect(game.x/2 - 220*game.scale, game.y/2 - 292*game.scale, 440*game.scale, 584*game.scale)

        self.time_frame_rect = py.rect.Rect(self.inner_frame_rect.topleft[0] + 50*game.scale,self.inner_frame_rect.topleft[1] + 50*game.scale, 340*game.scale, 60*game.scale)
        self.level_frame_rect = py.rect.Rect(self.inner_frame_rect.topleft[0] + 50*game.scale,self.inner_frame_rect.topleft[1] + 120*game.scale, 340*game.scale, 60*game.scale)
        self.score_frame_rect = py.rect.Rect(self.inner_frame_rect.topleft[0] + 50*game.scale,self.inner_frame_rect.topleft[1] + 190*game.scale, 340*game.scale, 60*game.scale)
        self.shipcollision_frame_rect = py.rect.Rect(self.inner_frame_rect.topleft[0] + 50*game.scale,self.inner_frame_rect.topleft[1] + 260*game.scale, 340*game.scale, 60*game.scale)
        self.enemymissiledestroyed_frame_rect = py.rect.Rect(self.inner_frame_rect.topleft[0] + 50*game.scale,self.inner_frame_rect.topleft[1] + 330*game.scale, 340*game.scale, 60*game.scale)
        self.meteordestroyed = py.rect.Rect(self.inner_frame_rect.topleft[0] + 50*game.scale,self.inner_frame_rect.topleft[1] + 400*game.scale, 340*game.scale, 60*game.scale)
        self.enemyshipdestroyed = py.rect.Rect(self.inner_frame_rect.topleft[0] + 50*game.scale,self.inner_frame_rect.topleft[1] + 470*game.scale, 340*game.scale, 60*game.scale)

    def draw_transparent_frame(self):
        py.draw.rect(self.alpha_surface,(0,0,0,220),self.inner_frame_rect, border_radius=int(10*game.scale), width= int(10*game.scale))
        py.draw.rect(self.alpha_surface,(0,0,0,220),self.time_frame_rect, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_surface,(0,0,0,220),self.level_frame_rect, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_surface,(0,0,0,220),self.score_frame_rect, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_surface,(0,0,0,220),self.shipcollision_frame_rect, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_surface,(0,0,0,220),self.enemymissiledestroyed_frame_rect, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_surface,(0,0,0,220),self.meteordestroyed, border_radius=int(10*game.scale))
        py.draw.rect(self.alpha_surface,(0,0,0,220),self.enemyshipdestroyed, border_radius=int(10*game.scale))
        game.screen.blit(self.alpha_surface, self.alpha_surface.get_rect())

    def draw(self):
        self.draw_transparent_frame()
        game.screen.blit(self.font.render(f'TIME : {game.end_time}  (SECOND)', True, (230,230,230)),(self.time_frame_rect.topleft[0] +30*game.scale, self.time_frame_rect.topleft[1] +18*game.scale))
        game.screen.blit(self.font.render(f'LEVEL : {game.end_level}', True, (230,230,230)),(self.level_frame_rect.topleft[0] +30*game.scale, self.level_frame_rect.topleft[1] +18*game.scale))
        game.screen.blit(self.font.render(f'SCORE : {game.end_score}', True, (230,230,230)),(self.score_frame_rect.topleft[0] +30*game.scale, self.score_frame_rect.topleft[1] +18*game.scale))
        game.screen.blit(self.font.render(f'IMPACTORS : {game.end_player_ship_collision}', True, (230,230,230)),(self.shipcollision_frame_rect.topleft[0] +30*game.scale, self.shipcollision_frame_rect.topleft[1] +18*game.scale))
        game.screen.blit(self.font.render(f'DESTROYED ENEMY MISSILE : {game.end_enemy_missile_destroyed}', True, (230,230,230)),(self.enemymissiledestroyed_frame_rect.topleft[0] +30*game.scale, self.enemymissiledestroyed_frame_rect.topleft[1] +18*game.scale))
        game.screen.blit(self.font.render(f'DESTROYED METEOR : {game.end_meteor_destroyed}', True, (230,230,230)),(self.meteordestroyed.topleft[0] +30*game.scale, self.meteordestroyed.topleft[1] +18*game.scale))
        game.screen.blit(self.font.render(f'DESTROYED ENEMY SHIP : {game.end_enemy_ship_destroyed}', True, (230,230,230)),(self.enemyshipdestroyed.topleft[0] +30*game.scale, self.enemyshipdestroyed.topleft[1] +18*game.scale))


gameover = GameOver()

class Animations(py.sprite.Sprite):
    explosion = [py.transform.scale(py.image.load(os.path.join('rocket','3.png')).convert_alpha(), (10*game.scale, 10*game.scale)),
                 py.transform.scale(py.image.load(os.path.join('rocket','3.png')).convert_alpha(), (20*game.scale, 20*game.scale)),
                 py.transform.scale(py.image.load(os.path.join('rocket','3.png')).convert_alpha(), (30*game.scale, 30*game.scale)),
                 py.transform.scale(py.image.load(os.path.join('rocket','3.png')).convert_alpha(), (20*game.scale, 20*game.scale)),
                 py.transform.scale(py.image.load(os.path.join('rocket','3.png')).convert_alpha(), (10*game.scale, 10*game.scale)),
                 py.transform.scale(py.image.load(os.path.join('rocket','3.png')).convert_alpha(), (20*game.scale, 20*game.scale)),
                 py.transform.scale(py.image.load(os.path.join('rocket','3.png')).convert_alpha(), (30*game.scale, 30*game.scale)),
                 py.transform.scale(py.image.load(os.path.join('rocket','4.png')).convert_alpha(), (40*game.scale, 40*game.scale)),
                 py.transform.scale(py.image.load(os.path.join('rocket','5.png')).convert_alpha(), (50*game.scale, 50*game.scale)),
                 py.transform.scale(py.image.load(os.path.join('rocket','6.png')).convert_alpha(), (60*game.scale, 60*game.scale)),
                 py.transform.scale(py.image.load(os.path.join('rocket','7.png')).convert_alpha(), (60*game.scale, 60*game.scale))]
    
    def __init__(self, x, y):
        super().__init__()
        self.current_index = 0
        self.image = Animations.explosion[self.current_index]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.frame_time = 60
        self.last_update = py.time.get_ticks()
        self.active = True
        
    def update(self):
        now = py.time.get_ticks()
        if now - self.last_update > self.frame_time:
            self.last_update = now
            self.current_index +=1
            if self.current_index >= len(self.explosion):   #animasyonlar tamamlanınca oluşturulan sprite silincek
                self.active = False
                self.kill()
            else:
                self.image = Animations.explosion[self.current_index]
                self.rect = self.image.get_rect()
                self.rect.centerx = self.x
                self.rect.centery = self.y
                

explosion_animated_group = py.sprite.Group()

class Sound:
    def __init__(self):
        self.buton = py.mixer.Sound(os.path.join('sound','button.mp3'))
        self.missile_missile = py.mixer.Sound(os.path.join('sound','missile_missile.wav'))
        self.missile_meteor = py.mixer.Sound(os.path.join('sound','missile_meteor.mp3'))
        self.missile_enemy = py.mixer.Sound(os.path.join('sound','missile_enemy.wav'))
        self.player_collision = py.mixer.Sound(os.path.join('sound','player_collision.wav'))
        self.enemy_kill = py.mixer.Sound(os.path.join('sound','enemy_kill.wav'))
        self.game_over = py.mixer.Sound(os.path.join('sound','game_over.mp3'))
        self.game_over_control = None       #game over müziğinin çalınıp çalınmadığını kontrol edicek bayrak
        self.music_loop = py.mixer.music.load(os.path.join('sound','gameloop.mp3'))
        self.volume_settings()                  #oluşturulurken seslerin ayarlanması.
        

    def volume_settings(self):
        if windowBar.soundflag:
            self.buton.set_volume(0.15)
            self.missile_missile.set_volume(0.15)
            self.missile_meteor.set_volume(0.15)
            self.missile_enemy.set_volume(0.15)
            self.enemy_kill.set_volume(0.15)
            self.player_collision.set_volume(0.25)
            self.game_over.set_volume(0.15)
        else:
            self.buton.set_volume(0)
            self.missile_missile.set_volume(0)
            self.missile_meteor.set_volume(0)
            self.missile_enemy.set_volume(0)
            self.enemy_kill.set_volume(0)
            self.player_collision.set_volume(0)
            self.game_over.set_volume(0)

        if windowBar.musicflag:
            py.mixer_music.set_volume(0.15)
        else:
            py.mixer_music.set_volume(0)
        
    def buton_play(self):
        self.buton.play()

    def missile_missile_play(self):
        self.missile_missile.play()

    def missile_meteor_play(self):
        self.missile_meteor.play()
    
    def missile_enemy_play(self):
        self.missile_enemy.play()
    
    def player_collision_play(self):
        self.player_collision.play()

    def enemy_kill_play(self):
        self.enemy_kill.play()

    def game_over_play(self):
        self.game_over_control = self.game_over.play()
        
    def game_over_played(self):             #burda fonksiyon sesin çalınıp çalınmadığına göre true veya false gönderiyor. gerekli yerde buna göre kontrol yapılıp çalınıyorsa durduruyoruz.
        if self.game_over_control.get_busy():
            return True
        else:
            return False
        
    def game_over_stop(self):
        self.game_over.stop()
        
    def gameloop_play(self):
        py.mixer_music.play(-1)

    def gameloop_pause(self):       #duraklatma, daha sonra unpause yaparak kaldığı yerden devam edilebiliyor.
        py.mixer_music.pause()

    def gameloop_unpause(self):     #duraklatılan yerden devam etme.
        py.mixer_music.unpause()

    def gameloop_stop(self):        #müziği tamamen durduruyor ve daha sonra devam edilemiyor müziğe baştan başlaması gerekiyor bu yöntem yapıldıktan sonra.
        py.mixer_music.stop()
    
    
sound = Sound()


def clear_lists():
    for sprite in missile_group:
        sprite.kill()
    missile_group.empty()

    for sprite in meteor_group:
        sprite.kill()
    meteor_group.empty()

    for sprite in enemy_ship_group:
        sprite.kill()
    enemy_ship_group.empty()

    for sprite in enemy_ship_missile_group:
        sprite.kill()
    enemy_ship_missile_group.empty()

    for sprite in player_group:
        sprite.kill()
    player_group.empty()

    for sprite in explosion_animated_group:
        sprite.kill()
    explosion_animated_group.empty()


def reset_times():
    py.time.set_timer(timing.missile_time, 0)
    py.time.set_timer(timing.level_time, 0)
    py.time.set_timer(timing.meteor_time, 0)
    py.time.set_timer(timing.enemy_ship_time, 0)
    py.time.set_timer(timing.transparent_time, 0)
    py.time.set_timer(timing.info_time, 0)

def reset_player_ship():
    hangar.ship_select = None
    hangar.player_ship_select()

def end_game_preparations():
    if not game.player_ship_explosioned:            #oyun sonu olduğu için oyun içerisindeki tüm nesnelerin patlama efektine girip ekranda yok edilmesi
        explosion_animated_group.add(Animations(hangar.ship_select.rect.center[0], hangar.ship_select.rect.center[1]))
        hangar.ship_select.kill()
        for enemy in enemy_ship_group:
            explosion_animated_group.add(Animations(enemy.rect.center[0], enemy.rect.center[1]))
            enemy.kill()
        for meteor in meteor_group:
            explosion_animated_group.add(Animations(meteor.rect.center[0], meteor.rect.center[1]))
            meteor.kill()
        for missile in missile_group:
            explosion_animated_group.add(Animations(missile.rect.center[0], missile.rect.center[1]))
            missile.kill()
        for enemy_missile in enemy_ship_missile_group:
            explosion_animated_group.add(Animations(enemy_missile.rect.center[0], enemy_missile.rect.center[1]))
            enemy_missile.kill()

        game.player_ship_explosioned = True
    
    if not explosion_animated_group:                    #devam eden  patlamalar yoksa burdan aşağısı gerçekleşicek. devam eden patlama animasyonları varsa else kısmı gerçekleşicek.
        game.save_game_values()                         #oyun içi değerler sıfırlanmadan önce oyuncuya bilgi amaçlı değişkenlere aktarıldı fonksiyon.
        hangar.ship_select.kill()
        clear_lists()            #liste ve spriteleri sıfırlama
        reset_times()            #zamanlayıcıları sıfırlama
        reset_player_ship()      #oyuncu gemisinin değerlerini sıfırlama
        game.pageFlags()
        game.stateFlags()
        game.gameOver = True
        sound.gameloop_stop()
        sound.game_over_play()  
    else:       
        hangar.ship_select.health = -1          #gameover butonuna tıklanınca oyuncu gemisinin canı olduğu için ikinci tıklamaya gerekiyor. oyun döngüsündede sürekli canı kontrol edip bu fonksiyona gönderdiğimiz için ;
                                                #eğer efektler devam etmiyorsa gerekli sıfırlamaları yapıyoruz, eğer efektler devam ediyorsa geminin canını eksiye düşürüyoruz ki oyun içindeki can kontrolü yapılan blok tekrar buraya yönlendirsin ve animasyonlar bitince sıfırlamaları yapsın diye.
    


def gameLoop():
    while game.running:
        mouse = py.mouse.get_pos()
        for event in py.event.get():
            if event.type == py.QUIT:
                game.running = False
            
            if event.type == py.KEYDOWN:
                if event.key == py.K_F4:
                    game.running = False

                if event.key == py.K_ESCAPE:
                    if game.start:
                        pass
                    else:
                        game.pageFlags()
                        game.menu = True

                if event.key == py.K_p:                           #durdurma kısayolu p tuşu 
                    if game.start or game.pause:
                        play_pause_event.play_pause_function()

                if game.start:
                    if event.key == py.K_LEFT or event.key == py.K_a:
                        game.left_button_pressed = True
                    elif event.key == py.K_RIGHT or event.key == py.K_d:
                        game.right_button_pressed = True
                    elif event.key == py.K_UP or event.key == py.K_w:
                        game.up_button_pressed = True
                    elif event.key == py.K_DOWN or event.key == py.K_s:
                        game.down_button_pressed = True

                    if event.key == py.K_SPACE and hangar.ship_select.missile_fire:
                        missile_group.add(Missile(dt))                                          #oyuncu gemisinin roket atışları burda oluşturulduğu için dtyi burda veriyoruz.
                        timing.player_missile_fire()               #bir kere ateş edilince mili saniye cinsinden kadar beklenildikten sonra missile_fire bayrağını true yapıcak event.
                        hangar.ship_select.missile_fire = False
                    
            if event.type == py.KEYUP:
                if game.start:
                    if event.key == py.K_LEFT or event.key == py.K_a:
                        game.left_button_pressed = False
                    elif event.key == py.K_RIGHT or event.key == py.K_d:
                        game.right_button_pressed = False
                    elif event.key == py.K_UP or event.key == py.K_w:
                        game.up_button_pressed = False
                    elif event.key == py.K_DOWN or event.key == py.K_s:
                        game.down_button_pressed = False


            if game.start:
                ##### USEREVENTLER
                if event.type == timing.missile_time :                               #mermi ateşleme hızını kontrol edicek event yakalayıcı. yukarda bir kere ateş edince bayrağı falseye çevirip süre başlatmıştık.
                    hangar.ship_select.missile_fire = True                                      #burda o süre geçince bayrağı tekrar true yaparak ateş etmesine izin veriyoruz.

                elif event.type == timing.meteor_time:
                    meteor_group.add(Meteor(dt))                                            #meteorlar burda oluşturulduğu için dtyi burda veriyoruz.
                    timing.level_meteor_time()
                    
                elif event.type == timing.enemy_ship_time:
                    if len(enemy_ship_group) < 4 :                                          #düşman gemiler o an için 4 den fazlaysa yenisi oluşturulmıycak olan blok.
                        timing.create_enemy_ship(dt)                                            #düşman gemilerinin oluşturulduğu fonksiyon. dtyi burda verip hız hesaplamasını burda yapıyoruz. hız işlemleri yapılırken matematik işlemlerini en aza indirmek için.
                    timing.level_enemy_ship_time()

                elif event.type == timing.level_time:                   #seviye için belirtilen zamanlama. zaman dolunca seviyeye özel yeni zaman seçilip seviye yükseltilmesi sağlanıyor.
                    timing.next_level_time()                            #seviye yükseldikçe gemi değerlerinin yükselceği fonksiyona da burdaki fonksiyondan gönderiyoruz. hem zamanlama hem seviye atlama hem değerleri artırma burdan yönetiliyor.
                    
                elif event.type == timing.transparent_time:             #oyuncu gemisi herhangi bişeyle çarpınca saydam olcak ve bu bayraklarla belirleniyor. bu bayrakları kontrol eden ve değiştiren zamanlayıcı eventi.
                    hangar.ship_select.collision = False

                elif event.type == timing.info_time:
                    game.time += 1
                    timing.time_spent_in_game()

        game.screen.fill((0,0,0))
        
        if game.menu:
            game.screen.blit(game.menu_background,game.bgrect)
            menu.draw_and_click(event,mouse)
            
        elif game.start:
            if game.timer_start_and_player_ship_create:                        #bu bayrak sadece sıfırlamalar yapıldığında true döndürücek. 
                timing.timer_start()                #zamanlayıcıların oyun içerisinde bir kere başlatılmasını sağlamak için.    
                #burdan aşağıdaki bloğu sürekli çalıştırmamamızın sebebi sürekli sürekli hangarda değiştirdiğinde gemi oluşturmasın diye. sadece starta basıldığında hangarda seçilen geminin değerleriyle bir kere oluşturucak.
                hangar.ship_select = Ships(hangar.ship_select['health'], hangar.ship_select['damage'], hangar.ship_select['speed'], hangar.ship_select['armor'], hangar.ship_select['w'], hangar.ship_select['h'], hangar.ship_select_image)
                player_group.add(hangar.ship_select)
                sound.gameloop_play()
                game.timer_start_and_player_ship_create = False
                
            game.screen.blit(game.game_background,game.bgrect)
            if play_pause_event.info_flag:
                info_in_game.info_player_ship() 
                info_in_game.info_enemy_ship()
                info_in_game.info_game_value()
            else:
                pass

            player_group.update(dt)               #oyuncu gemisinin kontrol fonksiyonu. dtyi gönderebilcek  nesne oluşum aşaması yok diye burda gönderdim.

            if hangar.ship_select.collision is False:    #eğer oyuncu gemisi herhangi bişeyle çarpışmıyorsa opak çiz
                player_group.draw(game.screen)
            elif hangar.ship_select.collision:
                hangar.ship_select.transparent_draw()     #eğer çarpışma varsa saydamlaştır bi süre.
            
            missile_group.update()               #normalde döngüyle o gruptakileri tek fonksiyona göndermek gerekiyordu update fonksiyonunda blitide çağırmamız gerekiyordu.
            missile_group.draw(game.screen)      #ama super init yaptığımız için bunları bizim için otomatik yapıyor. ne döngüye ne blite gerek kalmıyor.

            meteor_group.update()
            meteor_group.draw(game.screen)

            enemy_ship_missile_group.update(dt)              #düşman mermilerine dtyi güncelleme noktasında vermek en mantıklısı, diğer yöntemler düşman gemi hareketlerini bozduğu için böyle yaptım.
            enemy_ship_missile_group.draw(game.screen)

            enemy_ship_group.update()
            enemy_ship_group.draw(game.screen)

            explosion_animated_group.update()
            explosion_animated_group.draw(game.screen)
            
            ##### COLLISION CHECKS #####
            #PLAYER SHİP AND ENEMY MİSSİLE              #oyuncu gemisinin düşman roketlerle çarpışması
            playerShip_and_enemyMissile = py.sprite.spritecollide(hangar.ship_select, enemy_ship_missile_group, False)
            if playerShip_and_enemyMissile:
                for enemy_missile in playerShip_and_enemyMissile:
                    enemy_missile.kill()
                    hangar.ship_select.health -= round(enemy_missile.damage - (enemy_missile.damage/100 * hangar.ship_select.armor))
                    game.player_ship_collision += 1
                    timing.ship_collision_transparent()     #gemiyle çarpışınca gmeiyi saydam yapıcak ve zamanlayıcı başlatıcak fonksiyon
                    sound.player_collision_play()
                    explosion_animated_group.add(Animations(hangar.ship_select.rect.clip(enemy_missile)[0], hangar.ship_select.rect.clip(enemy_missile)[1]))
                      
            #PLAYER SHİP AND METEOR                     #oyuncu gemisinin meteorla çarpışması
            playerShip_and_meteor = py.sprite.spritecollide(hangar.ship_select, meteor_group, False)
            if playerShip_and_meteor:
                for meteor in playerShip_and_meteor:
                    meteor.kill()
                    hangar.ship_select.health -= round(meteor.damage - (meteor.damage/100 * hangar.ship_select.armor))
                    game.player_ship_collision += 1
                    timing.ship_collision_transparent()
                    sound.player_collision_play()
                    #print(hangar.ship_select.rect.clip(meteor))    #bu çarpışan iki nesnenin o anki çarpışmasının koordinatını bulma
                    explosion_animated_group.add(Animations(hangar.ship_select.rect.clip(meteor)[0], hangar.ship_select.rect.clip(meteor)[1]))          #anlık çarpışma noktasını bulup tam o koordinatlar ile oluşturuyoruz patlamayı.(rect.clip yöntemi bu işe yarıyor.)
    
            #PLAYER SHİP AND ENEMY SHİP                 #oyuncu gemisinin düşman gemisiyle çarpışması
            playerShip_and_enemyShip = py.sprite.spritecollide(hangar.ship_select, enemy_ship_group, False)
            if playerShip_and_enemyShip:
                for enemyship in playerShip_and_enemyShip:
                    enemyship.kill()
                    hangar.ship_select.health -= round(enemyship.health - (enemyship.health/100 * hangar.ship_select.armor))
                    game.player_ship_collision += 1
                    timing.ship_collision_transparent()
                    sound.player_collision_play()
                    explosion_animated_group.add(Animations(hangar.ship_select.rect.clip(enemyship)[0], hangar.ship_select.rect.clip(enemyship)[1]))
                
            #PLAYER MİSSİLE AND ENEMY MİSSİLE
            for player_missile in missile_group:        #bu blokta her oyuncunun roketini döngüyle kotrol edip rakip roket grubuyla çarpışmasını kontrol ediyoruz. eğer çarğıpma varsa;
                playerMissile_and_enemyMissile = py.sprite.spritecollide(player_missile, enemy_ship_missile_group, False)
                if playerMissile_and_enemyMissile:
                    for enemy_missile in playerMissile_and_enemyMissile:    #burası oyuncu roketiyle çarpan rakip roketin listesini döndürüyor. bunları for ile dönerek çarpan rakip roketi hem gruptan hem pygameden çıkarıyoruz.
                        enemy_missile.kill()                                #düşman roketi yok etme
                        explosion_animated_group.add(Animations(player_missile.rect.clip(enemy_missile)[0], player_missile.rect.clip(enemy_missile)[1]))
                    player_missile.kill()                                   #oyuncu roketi yok etme
                    sound.missile_missile_play()
                    game.score += EnemyShipMissile.missile_point
                    game.enemy_missile_destroyed += 1

            #PLAYER MİSSİLE AND METEOR
            for player_missile in missile_group:
                playerMissile_and_meteor = py.sprite.spritecollide(player_missile, meteor_group, False)
                if playerMissile_and_meteor:
                    for meteor in playerMissile_and_meteor:
                        meteor.kill()
                        explosion_animated_group.add(Animations(player_missile.rect.clip(meteor)[0], player_missile.rect.clip(meteor)[1]))
                    player_missile.kill()
                    sound.missile_meteor_play()
                    game.score += Meteor.meteor_point
                    game.meteor_destroyed += 1
            
            #PLAYER MİSSİLE AND ENEMY SHİP
            for player_missile in missile_group:         #bu blokta oyuncu roketiyle çarğışan düşman gemilerin hesapları yapılıyor. oyuncu roketi yok edilip. oyununcu gemisinin hasarı düşman gemisinin canından çıkarılır ve 0 altına düşerse düşman gemisi öldürürülür.
                playerMissile_and_enemyShip = py.sprite.spritecollide(player_missile, enemy_ship_group, False)
                if playerMissile_and_enemyShip:
                    for enemyship in playerMissile_and_enemyShip:
                        enemyship.health -= hangar.ship_select.damage
                        explosion_animated_group.add(Animations(player_missile.rect.clip(enemyship)[0], player_missile.rect.clip(enemyship)[1]))
                        sound.missile_enemy_play()
                        if enemyship.health <= 0:
                            game.score += enemyship.point
                            enemyship.kill()
                            sound.enemy_kill_play()
                            game.enemy_ship_destroyed += 1
                    player_missile.kill()
                    
            if hangar.ship_select.health <= 0:              #bu blok oyuncu gemisinin canı 0 ve altına düşerse devam eden patlamaların listesine bakıp patlama spritesi var onları sürdürüp, liste boşalıp hepsi bitince oyunu sonlandırıyor.
                end_game_preparations()
                    
    
            
        elif game.pause:
            game.screen.blit(play_pause_event.screen_shot,(0,0)) 
            
        elif game.hangar:
            game.screen.blit(game.hangar_background,game.bgrect)
            hangar.draw_and_click(event,mouse)

        elif game.guide:
            game.screen.blit(game.guide_background,game.bgrect)
            guide.draw_and_click(event,mouse)

        elif game.communication:
            game.screen.blit(game.communication_background,game.bgrect)
            communication.draw()

        elif game.gameOver:
            game.screen.blit(game.gameover_background,game.bgrect)
            gameover.draw()

        else:
            pass
            
        if game.windowbar:          #oyun dışında genel görev çubuğu, oyun içerisinde bilgi ve oyun içi görev çubuğu çizimi
            windowBar.draw_and_click(event,mouse)
        else:
            play_pause_event.play_pause_bar(event,mouse)

        
        dt = game.clock.tick(60) / 1000 
        py.display.flip()
       


if __name__ == '__main__':
    gameLoop()
    clear_lists()            #liste ve spriteleri sıfırlama
    reset_times()            #zamanlayıcıları sıfırlama
    reset_player_ship()
py.quit()
sys.exit()



