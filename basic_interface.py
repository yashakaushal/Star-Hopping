import pygame
from PIL import Image
import io
import matplotlib.pyplot as plt,mpld3
from mpld3 import plugins

pygame.init() 
white = (255, 255, 255) 
X = 1000
Y = 600
img = pygame.image.load('/Users/yashakaushal/Documents/summer_project/Star-Hopping/test1.png') 
img = pygame.transform.scale(img,(800,600))

SCREEN_WIDTH = img.get_rect().size[0] 
SCREEN_HEIGHT = img.get_rect().size[1]
zoom_event = False
scale_up = 1.2
scale_down = 0.8
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption('Image') 
done = False
screen.fill(white) 

class GameState:
    def __init__(self):
        self.tab = 1
        self.zoom = 1
        self.world_offset_x = 0
        self.world_offset_y = 0
        self.update_screen = True
        self.legacy_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

game_state = GameState()

def world_2_screen(world_x, world_y):
    screen_x = (world_x - game_state.world_offset_x) * game_state.zoom
    screen_y = (world_y - game_state.world_offset_y) * game_state.zoom
    return [screen_x, screen_y]


def screen_2_world(screen_x, screen_y):
    world_x = (screen_x / game_state.zoom) + game_state.world_offset_x
    world_y = (screen_y / game_state.zoom) + game_state.world_offset_y
    return [world_x, world_y]


while not done:
    screen.blit(img,(0,0))
    pygame.display.flip()
    pygame.display.update()  
    # Mouse screen coords
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done = True
            pygame.quit() 
        if event.type == pygame.MOUSEBUTTONDOWN:  # if any mouse button is pressed
            if pygame.mouse.get_pressed()[0]:        # check if left mouse button is pressed
                pos = pygame.mouse.get_pos()        # get the x,y position of the cursor
                print(pos)
            if event.type == pygame.KEYDOWN:
                 # X and Y before the zoom
                mouseworld_x_before, mouseworld_y_before = screen_2_world(mouse_x, mouse_y)
            
	        # ZOOM IN/OUT
                if event.key == pygame.K_KP_EQUALS and game_state.zoom < 10:
                    game_state.zoom *= scale_up
                elif event.key == pygame.K_KP_MINUS and game_state.zoom > 0.5:
                    game_state.zoom *= scale_down
            
        	# X and Y after the zoom
                mouseworld_x_after, mouseworld_y_after = screen_2_world(mouse_x, mouse_y)

	        # Do the difference between before and after, and add it to the offset

                game_state.world_offset_x += mouseworld_x_before - mouseworld_x_after
                game_state.world_offset_y += mouseworld_y_before - mouseworld_y_after       

    if game_state.tab == 1:
        if game_state.update_screen:
            # Updates the legacy screen if something has changed in the image data
            game_state.legacy_screen.blit(img, (0, 0))
            game_state.update_screen = False

        # Sets variables for the section of the legacy screen to be zoomed
        world_left, world_top = screen_2_world(0, 0)
        world_right, world_bottom = SCREEN_WIDTH/game_state.zoom, SCREEN_HEIGHT/game_state.zoom

        # Makes a temp surface with the dimensions of a smaller section of the legacy screen (for zooming).
        new_screen = pygame.Surface((world_right, world_bottom))
        # Blits the smaller section of the legacy screen to the temp screen
        new_screen.blit(game_state.legacy_screen, (0, 0), (world_left, world_top, world_right, world_bottom))
        # Blits the final cut-out to the main screen, and scales the image to fit with the screen height and width
        screen.fill((255, 255, 255))
        screen.blit(pygame.transform.scale(new_screen, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
   
print('Bye!')
