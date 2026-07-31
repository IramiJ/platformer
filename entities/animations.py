import pygame
from pathlib import Path
from core.settings import REFERENCE_TICKS_PER_SECOND
from core.paths import assets_path
ANIMATION_TICKS_PER_SECOND = REFERENCE_TICKS_PER_SECOND

def load_animation(path: str, dur: int, entity):
    path = Path(path)
    animation_name = path.name
    animation_frame_data = []
    for number, duration in enumerate(dur):
        animation_frame_id = f"{animation_name}{number}"
        img_loc = path / f"{animation_frame_id}.png"
        animation_image = pygame.image.load(str(img_loc)).convert_alpha()
        animation_image.set_colorkey((0, 0, 0))
        entity.animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(duration):
            animation_frame_data.append(animation_frame_id)
    return animation_frame_data


def draw_constants(display):
    coin_count = pygame.image.load(assets_path("constants/coins.png")).convert()
    coin_count.set_colorkey((0, 0, 0))
    display.blit(coin_count, (0, 0))
