import pygame

class entity():
    def __init__(self,x,y,width,height):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.action = 'idle'
        self.frame = 0
        self.img_id = None
        self.flip = False
        self.img = None
        self.movement = [0,0]
        self.animation_database = {}
    def change_action(self,new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame = 0

class simple_entity():
    def __init__(self,img,loc):
        self.loc = loc
        self.img = pygame.image.load(img).convert()
    def render(self,surf,scroll):
        surf.blit(self.img, (self.loc[0]-scroll[0], self.loc[1]-scroll[1]))
    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], self.img.get_width(), self.img.get_height())
    def collision_test(self, rect):
        r = self.get_rect()
        return r.colliderect(rect)