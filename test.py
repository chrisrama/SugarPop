import pygame as pg

class SoundManager:
    def __init__(self):
        pg.mixer.init()
        self.sugar_drop_sound = pg.mixer.Sound("./sound/finish_level.wav")
        self.explosion_sound = pg.mixer.Sound("path/to/explosion_sound.wav")
        
        
        # Initialize volume
        self.volume = 1.0  # 1.0 is max volume, 0.0 is mute
        self.set_volume(self.volume)
        
        # Initialize channels
        self.sugar_drop_channel = pg.mixer.Channel(0)
        self.explosion_channel = pg.mixer.Channel(1)
        self.other_channel = pg.mixer.Channel(2)  # For other sounds

    def set_volume(self, volume):
        """Set the volume for all sounds."""
        self.volume = volume
        pg.mixer.music.set_volume(self.volume)
        self.sugar_drop_sound.set_volume(self.volume)
        self.explosion_sound.set_volume(self.volume)
        # Set volume for other sounds here

    def play_sugar_drop(self):
        if not self.sugar_drop_channel.get_busy(): # optional 
            self.sugar_drop_channel.play(self.sugar_drop_sound)


    def play_explosion(self):
        if not self.explosion_channel.get_busy():
            self.explosion_channel.play(self.explosion_sound)

    def play_level(self, sound):
        if not self.other_channel.get_busy():
            self.other_channel.play(sound)

    def adjust_volume(self, delta):
        """Adjust volume by delta amount."""
        new_volume = max(0.0, min(1.0, self.volume + delta))
        self.set_volume(new_volume)
# bucket 
 if not sugar_grain.sound_played:  # Only play sound if not already played 
    self.Sound.play_sugar_drop()
    sugar_grain.sound_played = True # indicate the sound has been played