import pygame


class Color:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (180, 180, 180)
    dark_grey = (144, 144, 144)


class Block:
    border_thickness = 3
    width = 100
    height = 100
    border_color = Color.black
    bg_color = Color.white
    sel_color = Color.grey
    text_color = Color.red

    def __init__(self, pos_x=0, pos_y=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos = (pos_x, pos_y)
        self.status = True  # The status only tells whether the block is operable or not
        self.text = ''
        self.text_size = 40

    def display_bg(self, win):
        t = Block.border_thickness
        pygame.draw.rect(win, Block.border_color,
                         (self.pos_x, self.pos_y, Block.width, Block.height))
        pygame.draw.rect(win, Block.bg_color,
                         (self.pos_x + t, self.pos_y + t, Block.width - 2 * t, Block.height - 2 * t))

    def display(self, win, select=False):
        t = Block.border_thickness
        self.display_bg(win)
        if self.status and select:
            pygame.draw.rect(win, Block.sel_color,
                             (self.pos_x + t, self.pos_y + t, Block.width - 2 * t, Block.height - 2 * t))
        if not self.status:
            font = pygame.font.SysFont('Helvetica', self.text_size)
            text = font.render(self.text, 1, self.text_color)
            win.blit(text, (
                self.pos_x + (self.width / 2 - text.get_width() / 2),
                self.pos_y + (self.height / 2 - text.get_height() / 2)))

    def update_text(self, string):
        self.text = string
        self.status = False


class Button:
    border_thickness = 3
    border_color = Color.black
    def __init__(self, pos_x, pos_y, width, height, text = ''):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.bg_color = Color.dark_grey
        self.sel_bg_color = Color.blue
        self.text = text
        self.text_color = Color.black
        self.text_size = int(height*3/5)

    def is_on(self, pos):
        t = Button.border_thickness
        if pos[0] < self.pos_x + t or pos[0] > self.pos_x + self.width - t:
            return False
        if pos[1] < self.pos_y + t or pos[1] > self.pos_y + self.height - t:
            return False
        return True

    def display(self, win, sel = False):
        t = Button.border_thickness
        pygame.draw.rect(win, Button.border_color,
                         (self.pos_x, self.pos_y, self.width, self.height))
        color = self.bg_color
        if sel:
            color = self.sel_bg_color
        pygame.draw.rect(win, color,
                             (self.pos_x + t, self.pos_y + t, self.width - 2*t, self.height - 2*t))
        font = pygame.font.SysFont('Helvetica', self.text_size)
        text = font.render(self.text, 1, self.text_color)
        win.blit(text, (
                self.pos_x + (self.width / 2 - text.get_width() / 2),
                self.pos_y + (self.height / 2 - text.get_height() / 2)))
        
        
        
# A function to get time in (h:)mm:ss given seconds
def get_time(time):  # time is given in seconds
    time = int(time)
    ret_string = ''
    h = time // 3600
    time = time % 3600
    if h > 0:
        ret_string += str(h) + ':'
    m = time // 60
    if m < 10:
        ret_string += '0'
    ret_string += str(m) + ':'
    time = time % 60
    if time < 10:
        ret_string += '0'
    ret_string += str(time)
    return ret_string
