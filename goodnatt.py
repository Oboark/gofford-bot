"""
Generates a bunch of wholesome emojis
https://github.com/Oboark/goodnatt-tradition
"""

import random

#Default emoji list we feed to the function
emoji_list = [  
                "gay_pride_flag", "rainbow", "kiss_ww","couple_ww", "family_wwbb", "family_wwgg", 
                "sparkling_heart", "heart", "blue_heart", "purple_heart", "ok_woman", "star2",
                "peach", "shaved_ice", "unicorn", "bee", "dragon", "four_leaf_clover", "hibiscus", "maple_leaf",
                "sunflower", "white_flower", "wilted_rose", "fallen_leaf", "cherry_blossom", "tulip", "blossom",
                "blossom", "cherry_blossom", "hibiscus", "sun_with_face", "two_hearts", "two_women_holding_hands"
            ]

def goodnatt(emojis=emoji_list, n_emojis=10):
    'Generates a sequence of n_emoji length with emojis list of emoji names'
    goodnatt_s = []

    for i in range(n_emojis):
        choice = random.uniform(0, 1)
        if choice <= 0.7:
            goodnatt_s.append(random.choice(emojis))
        elif choice <= 0.85:
            goodnatt_s.append("gay_pride_flag")
        else:
            goodnatt_s.append("sparkling_heart")

    return ':' + '::'.join(goodnatt_s) + ':'
