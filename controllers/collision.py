import pygame
from models.physics import check_collisions_aabb, check_collisions_circle, get_colliding_objects

class CollisionSystem:
    def __init__(self, sfx):
        self.sfx = sfx

    def process_interactions(self, player, enemies, blockers, coins_group, health_system, score_system):
        """Processes all collisions and returns a new game state string if needed, or None."""

        hit_enemy   = check_collisions_aabb(player, enemies, 0.75)
        hit_blocker = check_collisions_aabb(player, blockers, 0.75)

        if hit_enemy or hit_blocker:
            if player.take_hit():
                health_system.take_damage()
                self.sfx.play("crash")

                colliding_enemies = get_colliding_objects(player, enemies)
                colliding_blockers = get_colliding_objects(player, blockers)
                for obj in colliding_enemies + colliding_blockers:
                    obj.kill()
                if health_system.is_dead():
                    return "GAMEOVER"

        collected = check_collisions_circle(player, coins_group, dokill=True)
        for _ in collected:
            earned_star = score_system.add_coin()
            self.sfx.play("coin")
            if earned_star:
                self.sfx.play("star")
            if score_system.check_victory():
                return "VICTORY"
                
        return None