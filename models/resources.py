import os

RECORD_FILE = os.path.join(os.path.expanduser("~"), ".roadrush_record.txt")

class RecordSystem:
    """Persistent high score tracker for Endless mode."""
    def __init__(self):
        self.best_distance = self._load()

    def _load(self):
        try:
            with open(RECORD_FILE, "r") as f:
                return float(f.read().strip())
        except Exception:
            return 0.0

    def _save(self):
        try:
            with open(RECORD_FILE, "w") as f:
                f.write(str(self.best_distance))
        except Exception:
            pass

    def check_and_update(self, distance):
        """Returns True if a new record was set."""
        if distance > self.best_distance:
            self.best_distance = distance
            self._save()
            return True
        return False

class HealthSystem:
    MAX_HEALTH = 3
    def __init__(self):
        self.current = self.MAX_HEALTH

    def take_damage(self):
        self.current = max(0, self.current - 1)

    def is_dead(self):
        return self.current <= 0

class ScoreSystem:
    def __init__(self, mode):
        self.mode = mode
        self.coins = 0
        self.stars = 0
        self.distance = 0.0
        self.just_earned_star = False
        if mode == 3:
            self.COINS_PER_STAR = 30
            self.STARS_TO_WIN = 99999
        elif mode == 2:
            self.COINS_PER_STAR = 10
            self.STARS_TO_WIN = 5
        else:
            self.COINS_PER_STAR = 10
            self.STARS_TO_WIN = 3 

    def add_coin(self):
        self.coins += 1
        if self.coins >= self.COINS_PER_STAR:
            self.coins -= self.COINS_PER_STAR
            self.stars += 1
            self.just_earned_star = True
            return True
        return False
        
    def add_distance(self, speed):
        self.distance += speed * 0.1

    def check_victory(self):
        if self.mode == 3: return False
        return self.stars >= self.STARS_TO_WIN