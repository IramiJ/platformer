import pygame
def load_animation(path,dur,entity):
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in dur:
        animation_frame_id = animation_name + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert_alpha()
        animation_image.set_colorkey((0,0,0))
        entity.animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n +=1 
    return animation_frame_data
def draw_constants(display):
    coin_count = pygame.image.load('assets/constants/coins.png').convert()
    display.blit(coin_count, (0,0))