import pygame

class SoundManager:
    def __init__(self):
        self.enabled = pygame.mixer.get_init() is not None
        self._sounds = {}
        self.current_bgm_path = None

    def load(self, name, path):
        if not self.enabled:
            return
        try:
            snd = pygame.mixer.Sound(path)
            self._sounds[name] = snd
        except Exception:
            pass  # file missing → silence

    def play(self, name):
        snd = self._sounds.get(name)
        if snd:
            snd.play()

    def play_music(self, path, loops=-1):
        if not self.enabled:
            return
        if self.current_bgm_path == path:
            return
            
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(loops)
            self.current_bgm_path = path
        except Exception:
            pass

    def stop_music(self):
        if self.enabled:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
