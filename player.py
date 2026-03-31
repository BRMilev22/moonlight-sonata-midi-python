import pygame


class MidiPlayer:

    def __init__(self):
        pygame.mixer.init()

    def play(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    @property
    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def wait(self):
        while self.is_playing:
            pygame.time.delay(200)

    def cleanup(self):
        pygame.mixer.quit()
