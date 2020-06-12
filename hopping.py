import pygame
pygame.init() 

white = (255, 255, 255) 
X = 400
Y = 400
screen = pygame.display.set_mode((X, Y)) 
screen.fill(white) 

# pygame.display.set_caption('Image') 
# done = False

# image = pygame.image.load('/Users/yashakaushal/Documents/My Docs/Backup/Docs/01__1437639063_31640.jpg') 

# while not done:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             done = True
#     screen.blit(image,(100,100))
#     pygame.display.flip()

class button():
    def __init__(self,color,x,y,height,width,text=''):
        self.color = color
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text
    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen,outline, (self.x-2, self.y-2, self.width+4, self.height+4),0)
        if (self.text != ''):
            font = pygame.font.SysFont('comicsans',60, bold =1)
            text = font.render(self.text, 1,(0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2) ))
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

def redrawWindow():
    screen.fill(white)
    greenButton.draw(screen, (0,0,0))

run = True
greenButton = button((0,255,0), 150, 225, 250, 100, 'Click Me :D')

while run:
    redrawWindow()
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type==pygame.QUIT:
            run = False    
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if greenButton.isOver(pos):
                print ('clicked the button')
        if event.type == pygame.MOUSEMOTION:
            if greenButton.isOver(pos):
                greenButton.color = (255, 0, 0)
            else:
                greenButton.color = (0, 255, 0)


