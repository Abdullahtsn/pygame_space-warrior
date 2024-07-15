import pygame as py
import sys
import os
import random



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
        self.screen = py.display.set_mode((1280*self.scale, 720*self.scale), py.NOFRAME) #'''*self.scale ve py.noframeyi ekle'''
        self.clock = py.time.Clock()
        self.x = self.screen.get_width()
        self.y = self.screen.get_height()
        self.pageFlags()    
        self.menu = True                                                       #giriş ekranının menü olarak ayarlanması için.
        self.stateFlags()

    def pageFlags(self):
        self.menu = False
        self.aloneLobby = False
        self.joinLobby = False
        self.createLobby = False
        self.guide = False
        self.settings = False
        self.communication = False
        self.gameActive = False
        self.gameOver = False
        self.lobbyactived = False

     
        

    def stateFlags(self):
        pass
    
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
    def __init__(self,yol,x,icon_size) :
        self.x = x
        self.icon_size = icon_size
        self.image = py.transform.scale(py.image.load(os.path.join('icon',yol)).convert_alpha(),self.icon_size)
        self.image_rect = py.rect.Rect(self.x,0,self.icon_size[0],self.icon_size[1])
        
    



class WindowBar:
    def __init__(self):
        self.frame = py.rect.Rect(0,0,game.x,44)
        self.icon_size = (40,40)
        self.clicked = False
        self.homepage = WindowBarButtonCreate('homepage.png',10,self.icon_size)

        self.musicflag = True
        self.music = WindowBarButtonCreate('music.png', 90 ,self.icon_size)
        self.mutemusic = WindowBarButtonCreate('mutemusic.png', 90 ,self.icon_size)
        self.settings = WindowBarButtonCreate('settings.png', 170 ,self.icon_size)


        '''#lobi kapalıysa ; 
        self.alonelobby = WindowBarButtonCreate('alonelobby.png', 120 ,self.icon_size)
        self.searclobby = WindowBarButtonCreate('searchlobby.png', 180 ,self.icon_size)
        self.createlobby = WindowBarButtonCreate('createlobby.png', 240 ,self.icon_size)

        #lobi açıksa; duruma göre bunlardan biri görünücek.
        self.aloneflag = False
        self.searcflag = False
        self.createflag = False
        self.alonestate = WindowBarButtonCreate('alonestate.png', 120 ,self.icon_size)
        self.acceptstate = WindowBarButtonCreate('acceptstate.png', 120 ,self.icon_size)
        self.multiplestate = WindowBarButtonCreate('multiplestate.png', 120 ,self.icon_size)
        self.closelobby = WindowBarButtonCreate('closelobby.png', 180 ,self.icon_size)
        self.minus = WindowBarButtonCreate('minus.png',self.frame.width -130 ,self.icon_size)'''

        self.windowbarflag = True
        self.minusw = WindowBarButtonCreate('minusw.png',self.frame.width/2 - 20 ,self.icon_size)
        self.plusw = WindowBarButtonCreate('plusw.png',self.frame.width/2 -20 ,self.icon_size)

        
        
        self.guide = WindowBarButtonCreate('guide.png',self.frame.width -130 ,self.icon_size)
        
        self.close = WindowBarButtonCreate('close.png',self.frame.width -50 ,self.icon_size)

    def draw(self):
        if self.windowbarflag:
            self.z = py.draw.rect(game.screen,(231, 240, 220),self.frame)
            game.screen.blit(self.homepage.image, (self.homepage.image_rect))

            if self.musicflag:
                game.screen.blit(self.music.image, (self.music.image_rect))
            else:
                game.screen.blit(self.mutemusic.image, (self.mutemusic.image_rect))

            '''if not game.lobbyactived:
                game.screen.blit(self.alonelobby.image, (self.alonelobby.image_rect))
                game.screen.blit(self.searclobby.image, (self.searclobby.image_rect))
                game.screen.blit(self.createlobby.image, (self.createlobby.image_rect))
            else:
                if self.aloneflag:
                    game.screen.blit(self.alonestate.image, (self.alonestate.image_rect))
                elif self.searcflag:
                    game.screen.blit(self.acceptstate.image, (self.acceptstate.image_rect))
                elif self.createflag:
                    game.screen.blit(self.multiplestate.image, (self.multiplestate.image_rect))
                game.screen.blit(self.closelobby.image(self.closelobby.image_rect))
                game.screen.blit(self.minus.image, (self.minus.image_rect))'''

            game.screen.blit(self.minusw.image, (self.minusw.image_rect))
            game.screen.blit(self.settings.image, (self.settings.image_rect))
            game.screen.blit(self.guide.image, (self.guide.image_rect))
            
            game.screen.blit(self.close.image, (self.close.image_rect))

        else:
            game.screen.blit(self.plusw.image, (self.plusw.image_rect))
    
    def click(self,event):
        if self.windowbarflag:
            if event.type == py.MOUSEBUTTONDOWN and self.z.collidepoint(py.mouse.get_pos()) and not self.clicked:
                if self.plusw.image_rect.collidepoint(py.mouse.get_pos()):
                    self.windowbarflag = False
                elif self.homepage.image_rect.collidepoint(py.mouse.get_pos()):
                    game.pageFlags()
                    game.menu = True
                elif self.music.image_rect.collidepoint(py.mouse.get_pos()):
                    if self.musicflag:
                        self.musicflag = False
                    else:
                        self.musicflag = True
                elif self.settings.image_rect.collidepoint(py.mouse.get_pos()):
                    game.pageFlags()
                    game.settings = True
                elif self.guide.image_rect.collidepoint(py.mouse.get_pos()):
                    game.pageFlags()
                    game.guide = True
                elif self.close.image_rect.collidepoint(py.mouse.get_pos()):
                    game.running = False
                self.clicked = True
                
        elif not self.windowbarflag:
            if event.type == py.MOUSEBUTTONDOWN and self.minusw.image_rect.collidepoint(py.mouse.get_pos()) and not self.clicked:
                self.windowbarflag = True
                self.clicked = True
        if event.type == py.MOUSEBUTTONUP  and self.clicked:
            self.clicked = False
            print('ergrtyrjkkılkuıo')

            
        




        



    

windowBar = WindowBar()


class MenuButtonCreate:
    def __init__(self, text, fontType, size, y):
        self.text = text
        self.y = y
        font = py.font.Font(os.path.join('font',fontType), size)
        self.pasive_color = font.render(text, True, (20, 80, 20))
        self.active_color = font.render(text, True, (231, 240, 220)
)
        self.font_rect = self.pasive_color.get_rect()
        self.font_frame_rect = py.rect.Rect(game.x/2 -400, y, 800 , 100)
        self.clicked = False

    def draw(self):
        self.z = py.draw.rect(game.screen,(231, 240, 220), self.font_frame_rect, width=0, border_radius= 20)
        game.screen.blit(self.pasive_color, (self.z.centerx - self.font_rect.w/2, self.z.centery - self.font_rect.h/2))
    
    def hover(self):
        if self.z.collidepoint(py.mouse.get_pos()):
            self.z = py.draw.rect(game.screen,(20, 80, 20), self.font_frame_rect, width=0, border_radius= 20)
            game.screen.blit(self.active_color, (self.z.centerx - self.font_rect.w/2, self.z.centery - self.font_rect.h/2))
            
    def click(self,event):
        if  event.type == py.MOUSEBUTTONDOWN and self.z.collidepoint(py.mouse.get_pos()) and self.clicked is False:  
            self.clicked = True
            game.pageFlags()                    #tüm sayfa bayraklarını sıfırlaması için.
            if self.text == 'ALONE WARRIOR':
                game.aloneLobby = True
                game.lobbyactived = True
            elif self.text == 'JOIN LOBBY':
                game.joinLobby = True
                game.lobbyactived = True
            elif self.text == 'CREATE LOBBY':
                game.createLobby = True
                game.lobbyactived = True
            elif self.text == 'SETTINGS':
                game.settings = True
            elif self.text == 'GUIDE':
                game.guide = True
            elif self.text == 'COMMUNICATION':
                game.communication = True
        elif event.type == py.MOUSEBUTTONUP and self.clicked :
            self.clicked = False
        
          
                

class Menu:
    def __init__(self):
        aloneButton = MenuButtonCreate('ALONE WARRIOR', '15.ttf', 40, y=340)
        joinButton = MenuButtonCreate('JOIN LOBBY', '15.ttf', 40, y=490)  
        createButton = MenuButtonCreate('CREATE LOBBY', '15.ttf', 40, y=640) 
        settingsButton = MenuButtonCreate('SETTINGS', '15.ttf', 40, y=790) 
        guideButton = MenuButtonCreate('GUIDE', '15.ttf', 40, y=940) 
        communicationButton = MenuButtonCreate('COMMUNICATION', '15.ttf', 40, y=1090) 
        self.menu_buton_list = [aloneButton, joinButton, createButton, settingsButton, guideButton, communicationButton]

    def update(self, event):
        for i in self.menu_buton_list:
            i.draw()   
            i.hover()
            i.click(event)

   

menu = Menu()





def gameLoop():
    while game.running:
        for event in py.event.get():
            if event.type == py.QUIT:
                game.running = False
            
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    game.running = False
                    
            if event.type == py.KEYUP:
                pass

        game.screen.fill((0,0,0))


        if game.menu:
            menu.update(event)

        elif game.aloneLobby:
            pass
        
        elif game.joinLobby:
            pass

        elif game.createLobby:
            pass

        elif game.gameActive:
            pass

        elif game.guide:
            pass

        elif game.settings:
            pass

        elif game.communication:
            pass

        elif game.gameOver:
            pass
        else:
            print('dflgkjdfgkjdflkgjdlkfgjdlkfjgdlkj')


        windowBar.draw()
        windowBar.click(event)


        py.display.flip()
        dt = game.clock.tick(60) / 1000



if __name__ == '__main__':
    gameLoop()
py.quit()
sys.exit()



