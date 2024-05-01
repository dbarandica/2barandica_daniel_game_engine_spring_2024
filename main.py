
# This file was created by: Daniel Barandica
# Code from course code files
# import libraries and modules
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path
# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        self.MENU_ITEMS = ["Shop, Purple, Blue"] #make a shop where you 
        self.coins_collected = 0  # Track the coins collected by the player
        self.background_color = BGCOLOR  # Initialize the background color to default

        self.font = pg.font.Font(None, 36) #any font, with size 36
        self.current_screen = "Shop" #indicates current location, either menu or item
        self.clock = pg.time.Clock() #controlls frame rate

    def draw_shop_screen(self):
        shop_text = self.font.render("Shop!", True, (255, 255, 255)) #makes font color black, can change with RGB numbers, displays greeting
        self.screen.blit(shop_text, (50, 100)) #vertical or horizontal shifts for the greeting, "welcome"

    def handle_shop_click(self):
        # Check if the player has enough coins to buy an item
        if self.coins_collected >= 1:
            # If the player has 1 or more coins, deduct 1 coin and set background to blue
            self.coins_collected -= 1
            self.background_color = BLUE
        elif self.coins_collected >= 2:
            # If the player has 2 or more coins, deduct 2 coins and set background to purple
            self.coins_collected -= 2
            self.background_color = PURPLE

    def draw_shop_screen(self):
        shop_text = self.font.render("Shop!", True, (255, 255, 255))
        shop_rect = shop_text.get_rect()
        shop_rect.topright = (WIDTH - 10, 10)
        self.screen.blit(shop_text, shop_rect)

        # Draw the available items in the shop
        item_text = self.font.render("1 Coin: Blue Background", True, (255, 255, 255))
        item_rect = item_text.get_rect()
        item_rect.topleft = (50, 150)
        self.screen.blit(item_text, item_rect)

        item_text = self.font.render("2 Coins: Purple Background", True, (255, 255, 255))
        item_rect = item_text.get_rect()
        item_rect.topleft = (50, 200)
        self.screen.blit(item_text, item_rect)

         # Check if the mouse is over the shop items
        if item_rect.collidepoint(pg.mouse.get_pos()):
            # If clicked, perform an action (e.g., make a purchase)
            if pg.mouse.get_pressed()[0]:
                self.handle_shop_click()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    # Create run method which runs the whole GAME
    def new(self):
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.superspeeds = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'm':
                    Mob(self,col,row)
                if tile == 'K':
                    SUPERSPEED(self,col,row)


    def run(self):
        # 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
         pg.quit()
         sys.exit()
    def update(self):
        self.all_sprites.update()
    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)
    def draw(self):
            self.screen.fill(self.background_color)
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
            pg.display.flip()
    
    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
                
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press any key to start, if you dare!", 24, WHITE, WIDTH/2 - 32, 2)
        pg.display.flip()
        self.wait_for_key()
            # made loss screen
    

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
# Instantiate the game... 
g = Game()

# use game method run to run
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
