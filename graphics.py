import pygame
import resourcegame

def draw_labirint(screen, coord_player_x, coord_player_y, coords):
    coord_coeff = [
        [(0,0), (0,0), (0,0), (0,0), (0,0)],
        [(0,0), (0,0), (0,0), (0,0), (0,0)],
        [(0,0), (0,0), (0,0), (0,0), (0,0)],
        [(0,0), (0,0), (0,0), (0,0), (0,0)],
        [(0,0), (0,0), (0,0), (0,0), (0,0)],
    ]

    center_point = (2,2)

    for y in range(5):
        for x in range(5):
            coord_coeff[y][x] = (x - center_point[0], y - center_point[1])

    labirint = [
        [(94, 94, 94), (94, 94, 94), (94, 94, 94), (94, 94, 94), (94, 94, 94)],
        [(94, 94, 94), (94, 94, 94), (94, 94, 94), (94, 94, 94), (94, 94, 94)],
        [(94, 94, 94), (94, 94, 94), (0, 255, 0), (94, 94, 94), (94, 94, 94)],
        [(94, 94, 94), (94, 94, 94), (94, 94, 94), (94, 94, 94), (94, 94, 94)],
        [(94, 94, 94), (94, 94, 94), (94, 94, 94), (94, 94, 94), (94, 94, 94)],
    ]

    for y in range(5):
        for x in range(5):
            (new_coord_x, new_coord_y) = (coord_player_x + coord_coeff[y][x][0], coord_player_y + coord_coeff[y][x][1])
            code_cell = coords.get((new_coord_x, new_coord_y))

            text = ''

            if (code_cell != None):
                labirint[y][x] = get_color_cell(code_cell)
                text = get_cell_text(code_cell)

            draw_cell(screen, x, y, labirint[y][x], text)
            
def draw_player(screen):
    draw_cell(screen, 2, 2, (0,255,0), '')

def draw_cell(screen, coord_x, coord_y, color, text):
    if coord_x < 0 or coord_x > 5 or coord_y < 0 or coord_y > 5:
        raise ValueError('выход за пределы лабиринта')
    
    start_x = coord_x * resourcegame.CELL_SIZE
    start_y = coord_y * resourcegame.CELL_SIZE
    
    border_width = 1
    border_color = (0,0,0)

    inner_rect = [
        start_x + border_width, 
        start_y + border_width,
        resourcegame.CELL_SIZE - 2 * border_width, 
        resourcegame.CELL_SIZE - 2 * border_width
    ]
    pygame.draw.rect(screen, color, inner_rect)
    
    outer_rect = [start_x, start_y, resourcegame.CELL_SIZE, resourcegame.CELL_SIZE]
    pygame.draw.rect(screen, border_color, outer_rect, border_width)

    font = pygame.font.SysFont('Arial', 12)
    text_surface = font.render(str(text), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(start_x + resourcegame.CELL_SIZE//2, start_y + resourcegame.CELL_SIZE//2))
    screen.blit(text_surface, text_rect)

def get_color_cell(code_cell_type):
    type_cell = {
        -1: (127, 127, 125),
        0: (255,255,255),
        1: (127, 127, 125),
        2: (255, 0, 0),
    }
    if (type_cell.get(code_cell_type) != None):
        return type_cell[code_cell_type]
    #door
    if (9 < code_cell_type < 100):
        return (66, 48, 1)
    #key
    if (999 < code_cell_type):
        return (222, 255, 5)
    
    return (7, 231, 247)

def get_cell_text(code_cell_type):
    if (-1 == code_cell_type):
        return 'область с радиацией'
    if (code_cell_type == 0):
        return ''
    if (code_cell_type == 1):
        return 'поврежденная стена'
    if (code_cell_type == 2):
        return 'прочная стена'
    if (9 < code_cell_type < 100):
        return f'Дверь {code_cell_type}'
    if (100 <= code_cell_type <= 999):
        return f'Телепорт {code_cell_type}'
    if (999 < code_cell_type):
        return f'ключ {code_cell_type}'
