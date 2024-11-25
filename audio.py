import pygame as pg

# Initialize the mixer
pg.mixer.init()

Explosion_bucket_sound = pg.mixer.Sound('./sound/bucket_explode.wav')
Level_complete_sound = pg.mixer.Sound('./sound/finish_level.wav')
Bucket_On_target = pg.mixer.Sound('./sound/hit_bucket.wav')
Start_game = pg.mixer.Sound('./sound/start_game.wav')

Explosion_bucket_sound.set_volume(0.8) 

Level_complete_sound.set_volume(1.0)
Level_complete_sound.set_volume(3.0)
