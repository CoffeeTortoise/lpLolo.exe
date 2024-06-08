import pygame as pg
pg.init()
ct_wndInfo = pg.display.Info()
ct_wndRawSize = (ct_wndInfo.current_w, ct_wndInfo.current_h)
ct_fps1, ct_fps2, ct_frT, ct_len0, ct_len1 = 30, 60, .1, 24, 48
ct_size = ct_wndRawSize[1]/ct_len0 if ct_wndRawSize[1] < ct_wndRawSize[0] else ct_wndRawSize[0]/ct_len1
ct_wndSize, ct_title = (ct_size*ct_len1, ct_size*ct_len0), 'The Penguin\'s revenge'
ct_fnt_size = int(ct_size)
ct_ico_path, ct_fnt_path = 'Assets/Face_pixian_ai.bmp', 'Assets/Fonts/cirillic_font.ttf'
ct_beg_path, ct_lev_path = 'Assets/Brain/Beginner.txt', 'Assets/Brain/Level.txt'
ct_prog_path, ct_que_path = 'Assets/Brain/Progress.txt', 'Assets/Brain/Queue.txt'
ct_ru_path, ct_stag_path = 'Assets/Brain/RU.txt', 'Assets/Brain/Stage.txt'
ct_mouse_img = 'Assets/Mouse_pixian_ai.png'
ct_mouse_snd = 'Assets/Music/Action/HammerSteel.ogg'
ct_red, ct_green, ct_blue = (255, 0, 0), (0, 255, 0), (0, 0, 255)
ct_black, ct_grey, ct_white = (0, 0, 0), (128, 128, 128), (255, 255, 255)
ct_sulfur, ct_cinnabar = (237, 255, 33), (255, 77, 0)
ct_scarlett, ct_amethyst = (252, 40, 71), (153, 102, 204)
ct_carmine, ct_sunrise = (150, 0, 24), (255, 207, 72)
ct_papyrus, ct_yellow = (242, 239, 220), (255, 219, 139)
ct_warning, ct_orchid = (229, 190, 1), (230, 168, 215)
ct_rosy, ct_malachite = (255, 20, 147), (11, 218, 81)
