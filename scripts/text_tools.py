
def draw_text(surf, text, font, col, pos = (0,0), center = None, align = 'left', draw = True):
    img = font.render(text, True, col)
    rect = img.get_rect()
    if align.lower() == 'right': rect.topright = (surf.get_width() - pos[0], pos[1])
    else: rect.topleft = pos
    if center != None: rect.center = center
    if draw:
        surf.blit(img, rect)
    return img, rect

def draw_lines(surf, text_or_lines: str | list, font, col, pos = (0,0), center = None, align = 'left'):
    if type(text_or_lines) != list: lines = text_or_lines.splitlines()
    else: lines = text_or_lines.copy()
    for line in lines:
        rect = draw_text(surf, line, font, col, draw = False)[1]
        if center != None:
            center = (center[0], rect.height + center[1])

        draw_text(surf, line, font, col, pos = pos, center = center, align = align, draw = True)
        pos = (pos[0], pos[1] + (rect.height))
        
    
def draw_text_slowly(surf, text_lis: list[int|str], font, col, pos = (0,0), center = None, align = 'left', draw = True):
    index, text = text_lis
    draw_text(surf, text[:int(index)], font, col, pos, center, align, draw)
    index = min(index+0.15, len(text)+20)
    text_lis[0] = index
    return index == len(text)+20
