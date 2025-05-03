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
    
    
    