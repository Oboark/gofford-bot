"""
Emojify but in Python
https://github.com/Fustran/Emojify
"""

num_text = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']

def to_emoji(s):
    "Converts text to emoji, among other things"

    s = s.lower()
    emoji_string = []
    for char in s:
        if char == " ":
            emoji_string.append("    ")
        elif char.isdigit():
            emoji_string.append(num_text[int(char)] + ' ')
        elif char.isalpha(): 
            emoji_string.append(":regional_indicator_" + char + ": ")
        elif char == '#':
            emoji_string.append(":hash: ")
        elif char == '*':
            emoji_string.append(":asterisk: ")
        elif char == '?':
            emoji_string.append(":question: ")
        elif char == '+':
            emoji_string.append(":heavy_plus_sign: ")
        elif char == '-':
            emoji_string.append(":heavy_minus_sign: ")
        elif char == '<':
            emoji_string.append(":arrow_backward: ")
        elif char == '>':
            emoji_string.append(":arrow_forward: ")
        elif char == '^':
            emoji_string.append(":arrow_up_small: ")
        elif char == '$':
            emoji_string.append(":heavy_dollar_sign: ")
        elif char == '!':
            emoji_string.append(":exclamation: ")
    
    emoji_string = "".join(emoji_string)
    if len(emoji_string) >= 2000:
        return "***TOO MANY CHARACTERS :rage:!!!***"
    else:
        return "".join(emoji_string)