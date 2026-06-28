"""Local alarm sound playback using pygame's mixer."""
import os

import pygame

import config


class Alarm:
    def __init__(self, sound_path: str = None):
        self.sound_path = sound_path or config.ALARM_SOUND_PATH
        pygame.mixer.init()
        self._sound = None
        if os.path.exists(self.sound_path):
            self._sound = pygame.mixer.Sound(self.sound_path)
        else:
            print(f"[alarm] Sound file not found at '{self.sound_path}'. Alarm will be silent.")

    def play(self):
        if self._sound is not None:
            self._sound.play()

    def is_playing(self) -> bool:
        return pygame.mixer.get_busy()
