# 2048 - Puzzle Game
from sprites import *
import random

class Game:
    def __init__(self):
        # initialize game window, ect
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((SIZE, SIZE))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = FONT_NAME
        self.move = True
        self.direction = 'Null'
        self.generate = False
        self.gen_num = 0

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.sprite_col = [pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group()]
        self.sprite_row = [pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group()]
        self.gen_cell()
        self.gen_cell()
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # check move
            if event.type == pg.KEYDOWN:
                if self.move:
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        self.gen_num = 1
                        self.direction = 'Up'
                        for cell in self.all_sprites:
                            cell.fuse = True
                            cell.vel.y = -CELL_VEL
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        self.gen_num = 1
                        self.direction = 'Down'
                        for cell in self.all_sprites:
                            cell.fuse = True
                            cell.vel.y = CELL_VEL
                    if event.key == pg.K_LEFT or event.key == pg.K_a:
                        self.gen_num = 1
                        self.direction = 'Left'
                        for cell in self.all_sprites:
                            cell.fuse = True
                            cell.vel.x = -CELL_VEL
                    if event.key == pg.K_RIGHT or event.key == pg.K_d:
                        self.gen_num = 1
                        self.direction = 'Right'
                        for cell in self.all_sprites:
                            cell.fuse = True
                            cell.vel.x = CELL_VEL

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # if can move or not
        for cell in self.all_sprites:
            if cell.vel.x or cell.vel.y:
                self.move = False
            else:
                self.move = True
        # move up
        if self.direction == 'Up':
            self.move_up()
        # move down
        if self.direction == 'Down':
            self.move_down()
        # move left
        if self.direction == 'Left':
            self.move_left()
        # move right
        if self.direction == 'Right':
            self.move_right()
        # generate cell
        count = 0
        for cell in self.all_sprites:
            if cell.vel.x or cell.vel.y:
                count += 1
        if count == 0:
            if self.generate and self.gen_num:
                self.gen_cell()
                self.generate = False
                self.gen_num -= 1
        # die!
        count = 0
        for cell in self.all_sprites:
            if cell.vel.x or cell.vel.y:
                count += 1
        if count == 0:
            cell_num = 0
            for cell in self.all_sprites:
                cell_num += 1
            pos_dict = {}
            for i in range(5):
                for j in range(5):
                    pos_dict[str((i, j))] = 0
            for cell in self.all_sprites:
                pos_dict[str((cell.cx, cell.cy))] = cell.value
            will_die = True
            for i in range(4):
                for j in range(4):
                    if pos_dict[str((i, j))] == pos_dict[str((i+1, j))] or pos_dict[str((i, j))] == pos_dict[str((i, j+1))]:
                        will_die = False
            if cell_num == 16 and will_die:
                self.playing = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        #game splash/start screen
        self.screen.fill(WHITE)
        self.draw_text('2048', int(SIZE/10), BLACK, int(SIZE/2), int(SIZE/3))
        self.draw_text('Press any key to start', int(SIZE/20), BLACK, int(SIZE/2), int(SIZE*4/5))
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.draw_text('GAME OVER', int(SIZE/10), BLACK, int(SIZE/2), int(SIZE/3))
        self.draw_text('Press space to try again', int(SIZE/20), BLACK, int(SIZE/2), int(SIZE*4/5))
        pg.display.flip()
        self.wait_for_enter()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def wait_for_enter(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False

    def move_up(self):
        for cell in self.sprite_row[0]:
            if cell.rect.top < 0:
                cell.vel.y = 0
                cell.rect.y += 1
        for cell in self.sprite_row[1]:
            if cell.rect.top < CELL_SIZE:
                hit = pg.sprite.spritecollide(cell, self.sprite_row[0], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.top <= 0:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.y = 0
                        cell.rect.y += 1
                else:
                    self.sprite_row[0].add(cell)
                    self.sprite_row[1].remove(cell)
                    self.generate = True
        for cell in self.sprite_row[2]:
            if cell.rect.top < CELL_SIZE*2:
                hit = pg.sprite.spritecollide(cell, self.sprite_row[1], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.top <= CELL_SIZE:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.y = 0
                        cell.rect.y += 1
                else:
                    self.sprite_row[1].add(cell)
                    self.sprite_row[2].remove(cell)
                    self.generate = True
        for cell in self.sprite_row[3]:
            if cell.rect.top < CELL_SIZE*3:
                hit = pg.sprite.spritecollide(cell, self.sprite_row[2], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.top <= CELL_SIZE*2:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.y = 0
                        cell.rect.y += 1
                else:
                    self.sprite_row[2].add(cell)
                    self.sprite_row[3].remove(cell)
                    self.generate = True

    def move_down(self):
        for cell in self.sprite_row[3]:
            if cell.rect.bottom > CELL_SIZE*4:
                cell.vel.y = 0
                cell.rect.y -= 1
        for cell in self.sprite_row[2]:
            if cell.rect.bottom > CELL_SIZE*3:
                hit = pg.sprite.spritecollide(cell, self.sprite_row[3], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.bottom >= CELL_SIZE*4:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.y = 0
                        cell.rect.y -= 1
                else:
                    self.sprite_row[3].add(cell)
                    self.sprite_row[2].remove(cell)
                    self.generate = True
        for cell in self.sprite_row[1]:
            if cell.rect.bottom > CELL_SIZE*2:
                hit = pg.sprite.spritecollide(cell, self.sprite_row[2], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.bottom >= CELL_SIZE*3:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.y = 0
                        cell.rect.y -= 1
                else:
                    self.sprite_row[2].add(cell)
                    self.sprite_row[1].remove(cell)
                    self.generate = True
        for cell in self.sprite_row[0]:
            if cell.rect.bottom > CELL_SIZE:
                hit = pg.sprite.spritecollide(cell, self.sprite_row[1], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.bottom >= CELL_SIZE*2:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.y = 0
                        cell.rect.y -= 1
                else:
                    self.sprite_row[1].add(cell)
                    self.sprite_row[0].remove(cell)
                    self.generate = True

    def move_left(self):
        for cell in self.sprite_col[0]:
            if cell.rect.left < 0:
                cell.vel.x = 0
                cell.rect.x += 1
        for cell in self.sprite_col[1]:
            if cell.rect.left < CELL_SIZE:
                hit = pg.sprite.spritecollide(cell, self.sprite_col[0], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.left <= 0:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.x = 0
                        cell.rect.x += 1
                else:
                    self.sprite_col[0].add(cell)
                    self.sprite_col[1].remove(cell)
                    self.generate = True
        for cell in self.sprite_col[2]:
            if cell.rect.left < CELL_SIZE*2:
                hit = pg.sprite.spritecollide(cell, self.sprite_col[1], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.left <= CELL_SIZE:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.x = 0
                        cell.rect.x += 1
                else:
                    self.sprite_col[1].add(cell)
                    self.sprite_col[2].remove(cell)
                    self.generate = True
        for cell in self.sprite_col[3]:
            if cell.rect.left < CELL_SIZE*3:
                hit = pg.sprite.spritecollide(cell, self.sprite_col[2], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.left <= CELL_SIZE*2:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.x = 0
                        cell.rect.x += 1
                else:
                    self.sprite_col[2].add(cell)
                    self.sprite_col[3].remove(cell)
                    self.generate = True

    def move_right(self):
        for cell in self.sprite_col[3]:
            if cell.rect.right > CELL_SIZE*4:
                cell.vel.x = 0
                cell.rect.x -= 1
        for cell in self.sprite_col[2]:
            if cell.rect.right > CELL_SIZE*3:
                hit = pg.sprite.spritecollide(cell, self.sprite_col[3], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.right >= CELL_SIZE*4:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.x = 0
                        cell.rect.x -= 1
                else:
                    self.sprite_col[3].add(cell)
                    self.sprite_col[2].remove(cell)
                    self.generate = True
        for cell in self.sprite_col[1]:
            if cell.rect.right > CELL_SIZE*2:
                hit = pg.sprite.spritecollide(cell, self.sprite_col[2], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.right >= CELL_SIZE*3:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.x = 0
                        cell.rect.x -= 1
                else:
                    self.sprite_col[2].add(cell)
                    self.sprite_col[1].remove(cell)
                    self.generate = True
        for cell in self.sprite_col[0]:
            if cell.rect.right > CELL_SIZE:
                hit = pg.sprite.spritecollide(cell, self.sprite_col[1], False)
                if hit:
                    if cell.value == hit[0].value and hit[0].fuse:
                        cx = hit[0].cx
                        cy = hit[0].cy
                        value = hit[0].value*2
                        if cell.rect.right >= CELL_SIZE*2:
                            cell.kill()
                            hit[0].kill()
                            new_cell = Cell(cx, cy, value)
                            new_cell.fuse = False
                            self.all_sprites.add(new_cell)
                            self.sprite_col[cx].add(new_cell)
                            self.sprite_row[cy].add(new_cell)
                            self.generate = True
                    else:
                        cell.vel.x = 0
                        cell.rect.x -= 1
                else:
                    self.sprite_col[1].add(cell)
                    self.sprite_col[0].remove(cell)
                    self.generate = True

    def gen_cell(self):
        pos_dict = {}
        for i in range(4):
            for j in range(4):
                pos_dict[str((i, j))] = 0
        for cell in self.all_sprites:
            pos_dict[str((cell.cx, cell.cy))] += 1
        flag = 0
        for pos in pos_dict:
            if pos_dict[pos] > 1:
                flag = 1
                cx = int(str(pos[1]))
                cy = int(str(pos[4]))
                for cell in self.all_sprites:
                    if cell.cx == cx and cell.cy == cy:
                        value = cell.value
                        cell.kill()
        if flag:
            new_cell = Cell(cx, cy, value)
            self.all_sprites.add(new_cell)
            self.sprite_col[cx].add(new_cell)
            self.sprite_row[cy].add(new_cell)
        gen_pos = []
        for i in range(4):
            for j in range(4):
                gen_pos.append((i, j))
        for cell in self.all_sprites:
            gen_pos.remove((cell.cx, cell.cy))
        if gen_pos:
            cell_pos = random.choice(gen_pos)
            cell_value = 4 if random.random() <= 0.1 else 2
            gen_cell = Cell(cell_pos[0], cell_pos[1], cell_value)
            self.all_sprites.add(gen_cell)
            self.sprite_col[cell_pos[0]].add(gen_cell)
            self.sprite_row[cell_pos[1]].add(gen_cell)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()