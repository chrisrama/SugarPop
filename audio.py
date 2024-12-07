import pygame as pg
from settings import RES
import pymunk 


class Sound:
    def __init__(self) -> None:
        pg.init()
        pg.mixer.init()


        self.sound_dict = {
                "complete_level": pg.mixer.Sound('./sound/finish_level.wav'),
                "explosion": pg.mixer.Sound('./sound/bucket_explode.wav'),
                "start_game": pg.mixer.Sound('./sound/start_game.wav'),
                "hit_bucket": pg.mixer.Sound('./sound/hit_bucket.wav')
            }   

        self.channels = {
            "explosion": pg.mixer.Channel(0),
            "bucket_hit": pg.mixer.Channel(1),
            "level_complete": pg.mixer.Channel(2)
        }
    # playing the sound of using mixer 
    def play_sound(self, sound_key, volume=1.0):
        try:
            channel = pg.mixer.find_channel()
            if channel:
                channel.play(self.sound_dict[sound_key])
                channel.set_volume(volume)
        except KeyError:
            print(f"Sound '{sound_key}' not found.")
# playing the sound once the bucket explode
    def play_explosion(self):
        self.play_sound("explosion",2.0)
# playing the sound once the level complete
    def play_level_complete(self):
        self.play_sound("complete_level")

# playing the sound once the sugar grain hit the bucket 
    def play_bucket_hit(self):
       # self.Hit_chanel.play(self.Hit_bucket,num)
        self.play_sound("hit_bucket", 1.0)
# play a sound once the game start    
    def play_start_game(self):
        self.play_sound("start_game")

# did not used this as i used instead a flag 
    def stop_specific_sound(self, sound_key):
        if sound_key in self.channels:
            self.channels[sound_key].stop() 

        

