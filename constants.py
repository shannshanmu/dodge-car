import emoji
import pygame
import sys
import os

if getattr(sys, "frozen", False):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(os.path.abspath(__file__))

display_width = 800
display_height = 700


divider_width = 25
divider_height = 150
divider_space = 25


title_big_text_size = 140
title_time = 2500
corner_small_text_size = 25
instructions_text_size = 80
instructions_time = 5050
countdown_time = 700
countdown_time_together = countdown_time * 4
intro_time_before_countdown = title_time + instructions_time


FasterOneFontPath = basedir + "/assets/fonts/FasterOne.ttf"
NotoColorEmojiFontPath = basedir + "/assets/fonts/NotoColorEmoji.ttf"
two_arrows_width_together = 475
# if two arrows are next to each other in one Text_sprite, this is their total width


""" THESE EMOJIS ARE ABOVE uFFFF as unicodes, so won't work... 😒
# U+1F612 😒
unamused_face = emoji.emojize(":unamused_face:", use_aliases=True)
# U+1F611 😑
expressionless_face = emoji.emojize(":expressionless_face:", use_aliases=True)
# U+1F928 🤨
face_with_raised_eyebrow = emoji.emojize(":face_with_raised_eyebrow:", use_aliases=True)
# U+1F914 🤔
thinking_face = emoji.emojize(":thinking_face:", use_aliases=True)
# red_car taken from other list
red_car = emoji.emojize(":red_car:", use_aliases=True)
# U+1F3CE 🏎
racing_car = emoji.emojize(":racing_car:", use_aliases=True)
"""

# U+2B05 ⬅
left_arrow = emoji.emojize(":left_arrow:", use_aliases=True)
# U+27A1 ➡
right_arrow = emoji.emojize(":right_arrow:", use_aliases=True)
# U+2620 ☠
skull_and_crossbones = emoji.emojize(":skull_and_crossbones:", use_aliases=True)
# U+270B ✋
raised_hand = emoji.emojize(":raised_hand:", use_aliases=True)
# U+270C ✌
victory_hand = emoji.emojize(":victory_hand:", use_aliases=True)
# U+261D ☝
index_pointing_up = emoji.emojize(":index_pointing_up:", use_aliases=True)
# U+2618 ☘
shamrock = emoji.emojize(":shamrock:", use_aliases=True)
# U+2328 ⌨
keyboard = emoji.emojize(":keyboard:", use_aliases=True)
# U+26B0 ⚰
coffin = emoji.emojize(":coffin:", use_aliases=True)
# U+26D4 ⛔
no_entry = emoji.emojize(":no_entry:", use_aliases=True)
# U+26A0 ⚠
warning = emoji.emojize(":warning:", use_aliases=True)
# U+00A9 ©
copyright_emoji = emoji.emojize(":copyright:", use_aliases=True)
# U+23EA ⏪
fast_reverse_button = emoji.emojize(":fast_reverse_button:", use_aliases=True)
# U+2935 ⤵
right_arrow_curving_down = emoji.emojize(":right_arrow_curving_down:", use_aliases=True)
# U+2049 ⁉ :exclamation_question_mark:
exclamation_question_mark = emoji.emojize(":exclamation_question_mark:", use_aliases=True)
# U+2796 ➖ :minus: CAN BE USED AS SPACE BAR REPRESENTATION
minus_or_space = emoji.emojize(":minus:", use_aliases=True)


emojis = [
    left_arrow,
    right_arrow,
    skull_and_crossbones,  # pos 3!!!
    raised_hand,
    victory_hand,
    index_pointing_up,
    shamrock,
    keyboard,
    coffin,
    no_entry,
    warning,
    copyright_emoji,
    fast_reverse_button,
    right_arrow_curving_down,
    minus_or_space,  # pos 14!!!
    exclamation_question_mark,  # pos 15!!!
]

BLUE = (25, 140, 255)
DARK_BLUE = (0, 0, 128)
PINK = (255, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WHITE_SMOKE = (245, 245, 245)
GREY = (128, 128, 128)
DIM_GREY = (105, 105, 105)
