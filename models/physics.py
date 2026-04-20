import pygame

def check_collisions_aabb(sprite, group, ratio=0.75):
    """Checks for AABB overlaps with a slight ratio reduction to make collisions fairer."""
    return pygame.sprite.spritecollideany(sprite, group, pygame.sprite.collide_rect_ratio(ratio))

def check_collisions_circle(sprite, group, dokill=True):
    """Checks for circular overlaps (e.g. for coins)."""
    return pygame.sprite.spritecollide(sprite, group, dokill, pygame.sprite.collide_circle)

def get_colliding_objects(sprite, group):
    """Returns all objects in the group that overlap the sprite's AABB."""
    return [obj for obj in group if obj.rect.colliderect(sprite.rect)]
