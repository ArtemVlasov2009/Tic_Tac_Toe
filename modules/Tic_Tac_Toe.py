import pygame as pg
import sys

pg.init()
game = False
def is_point_in_square(pos: tuple[int,int], square: list[tuple[int,int]]):
    x1, y1 = square[0]
    x2, y2 = square[1]
    x3, y3 = square[2]
    x4, y4 = square[3]
    return (min(x1, x2, x3, x4) <= pos[0] <= max(x1, x2, x3, x4)) and (min(y1, y2, y3, y4) <= pos[1] <= max(y1, y2, y3, y4))


SizeScreen = (450, 500)

SizeScreen_center = (SizeScreen[0] // 2, SizeScreen[1] // 2)

bg_color = (42, 83, 144)
sc = pg.display.set_mode(SizeScreen)
sc.fill(bg_color) 

pg.display.set_caption("Tic Tac Toe")

WHITE = (255, 255, 255)
green = (0, 150, 0)

background = pg.image.load('images/1.png')
reset = pg.image.load('images/RESET.png')
draw = pg.image.load('images/3.png')


bg_x, bg_y = background.get_size()

def update_screen():
    sc.blit(background, ((SizeScreen[0] - bg_x), (SizeScreen[1] - bg_y)))
    sc.blit(reset,(135, 430))
    

update_screen()

bg_color = (42, 83, 144)

pg.display.update()

current_figure = 'X'

def border(pos: tuple[int, int], size: tuple[int, int]) -> list:
    return [pos,(pos[0]+size[0], pos[1]+size[1]),(pos[0], pos[1]+size[1]),(pos[0]+size[0], pos[1])]

class Cell:
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        self.positions  = pos

        self.center_pos = (pos[0]+size[0]//2, pos[1]+size[1]//2)
        self.status = None

        self.points = border(pos, size)

    def check(self, mouse: tuple[int, int]):
        return is_point_in_square(mouse, self.points)
    
    def render_x(self):
        pass
        pg.draw.line(sc, WHITE, (self.center_pos[0]-40, self.center_pos[1]-40), (self.center_pos[0]+40, self.center_pos[1]+40), 12)
        pg.draw.line(sc, WHITE, (self.center_pos[0]+40, self.center_pos[1]-40), (self.center_pos[0]-40, self.center_pos[1]+40), 12)

    def render_o(self):
        pass
        pg.draw.circle(sc, WHITE, self.center_pos, 50, 10)

    def get_figure(self):
        return self.status
    
    def set_figure(self, value):
        self.status = value


class button:
    def __init__(self, pos, size):
        self.points = border(pos, size)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and is_point_in_square(event.pos, self.points):
            return True
        return False

slots: "list[tuple[Cell,Cell,Cell]]" = [
    [Cell((56,  66 ), (104, 100)), Cell((174, 66 ), (104, 100)), Cell((290, 66 ), (104, 100))],
    [Cell((56,  188), (104, 100)), Cell((174, 188), (104, 100)), Cell((290, 188), (104, 100))],
    [Cell((56,  304), (104, 100)), Cell((174, 304), (104, 100)), Cell((290, 304), (104, 100))]]

def check_win(board):
# Проверяем горизонтальные линии
    for i in range(3):
        if board[i][0].get_figure() == board[i][1].get_figure() == board[i][2].get_figure() and board[i][0].get_figure() is not None:
            pg.draw.line(sc, green, (80, i*100 + 135), (390, i*100 + 135), 15)
            return board[i][0].get_figure() 


# Проверяем вертикальные линии
    for i in range(3):
        if board[0][i].get_figure() == board[1][i].get_figure() == board[2][i].get_figure() and board[0][i].get_figure() is not None:
            pg.draw.line(sc, green, (i*100 + 120, 80), (i*100 + 120, 400), 15)
            return board[0][i].get_figure()

    # Проверяем диагонали
    if board[0][0].get_figure() == board[1][1].get_figure() == board[2][2].get_figure()and board[0][0].get_figure() is not None:
        pg.draw.line(sc, green, (80, 100), (350, 350), 15)
        return board[0][0].get_figure()

    if board[0][2].get_figure() == board[1][1].get_figure() == board[2][0].get_figure() and board[0][2].get_figure() is not None:
        pg.draw.line(sc, green, (70, 390), (360, 70), 15)
        return board[0][2].get_figure()
    
    
    




highlight_color = (255, 0, 0)

reset_button = button((135, 429), size=(179,36))

while True:
    check_win(slots)
    pg.display.update()

    for i in pg.event.get():
        if i.type == pg.QUIT: sys.exit()


        if i.type == pg.MOUSEBUTTONDOWN:   
            if i.button == 1:
                
                if reset_button.is_clicked(i):
                    update_screen()
                    for x in slots:
                        for cell in x:
                            cell.set_figure(None)

                box: Cell | None = None

                for x in slots:
                    for cell in x:
                        if cell.check(i.pos):
                            box = cell

                if box is None or box.get_figure():
                    continue

                position_figure = box.center_pos
                box.set_figure(current_figure)

                match current_figure:
                    case "X":
                        box.render_x()
                        current_figure = '0'
                    case "0":
                        box.render_o()
                        current_figure = 'X'

        if i.type == pg.KEYDOWN:
            match i.key:
                case pg.K_x:
                    current_figure = 'X'
                case pg.K_o:
                    current_figure = '0'

    pg.time.delay(20)