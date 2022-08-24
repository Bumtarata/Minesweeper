import pygame

def draw_lines_around_rect(mines_game, rect, surf, thickness=6, inside=False, 
invert=False, singlecolored=False):
    """Draw white and grey lines around given rect into given surface. As
    default lines will be drawn outside of the rect with grey lines at top
    and left."""
    settings = mines_game.settings
    
    # Check if colors should be inverted.
    if invert == False and not singlecolored:
        color1 = settings.outline_grey
        color2 = settings.outline_white
    elif invert == True and not singlecolored:
        color1 = settings.outline_white
        color2 = settings.outline_grey
    
    if singlecolored == 'white':
        color1 = settings.outline_white
        color2 = color1
    elif singlecolored == 'grey':
        color1 = settings.outline_grey
        color2 = color1
    elif singlecolored == 'black':
        color1 = (0, 0, 0)
        color2 = color1
    
    if inside == False:
        start = 1
        stop = thickness + 1
    elif inside == True:
        start = 0
        stop = thickness
    
    # Draw lines.
    for a in range(start, stop):
        # Check if lines should be drawn outside rect or inside.
        if inside == False:
            ll_start_pos = (rect.topleft[0] - a, rect.topleft[1] - thickness)
            ll_end_pos = (rect.bottomleft[0] - a, rect.bottomleft[1] + a)
        elif inside == True:
            ll_start_pos = (rect.topleft[0] + a, rect.topleft[1])
            ll_end_pos = (rect.bottomleft[0] + a, rect.bottomleft[1] - a)
        left_line = pygame.draw.line(surf, color1,
            ll_start_pos, ll_end_pos)
    
    for a in range(start, stop):
        if inside == False:
            tl_start_pos = (rect.topleft[0] - thickness, rect.topleft[1] - a)
            tl_end_pos = (rect.topright[0] + a, rect.topright[1] - a)
        elif inside == True:
            tl_start_pos = (rect.topleft[0], rect.topleft[1] + a)
            tl_end_pos = (rect.topright[0] - a, rect.topright[1] + a)
        top_line = pygame.draw.line(surf, color1,
            tl_start_pos, tl_end_pos)
    
    for a in range(start, stop):
        if inside == False:
            rl_start_pos = (rect.bottomright[0] + a, rect.bottomright[1] + thickness)
            rl_end_pos = (rect.topright[0] + a, rect.topright[1] - a)
        elif inside == True:
            rl_start_pos = (rect.bottomright[0] - a, rect.bottomright[1])
            rl_end_pos = (rect.topright[0] - a, rect.topright[1] + a)
        right_line = pygame.draw.line(surf, color2,
            rl_start_pos, rl_end_pos)
    
    for a in range(start, stop):
        if inside == False:
            bl_start_pos = (rect.bottomright[0] + thickness, rect.bottomright[1] + a)
            bl_end_pos = (rect.bottomleft[0] - a, rect.bottomleft[1] + a)
        elif inside == True:
            bl_start_pos = (rect.bottomright[0], rect.bottomright[1] - a)
            bl_end_pos = (rect.bottomleft[0] + a, rect.bottomleft[1] - a)
        bottom_line = pygame.draw.line(surf, color2,
            bl_start_pos, bl_end_pos)