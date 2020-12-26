import random
import sys
import pygame


class Constants:
    I, J, L, O, S, T, Z = 1, 2, 3, 4, 5, 6, 7
    SIDE_LENGTH = 30
    WINDOW_SIZE = (700, 650)
    BOARD_TOPLEFT = (50, 20)
    BOARD_SIZE = (10, 20)
    MAX_VOLUME = 0.5
    FALL_TIME = 2000
    FONT_SIZE = 60
    SCORE_TOPLEFT = (400, 30)


class Settings:
    AUDIO_VOLUME = 100
    MUSIC_VOLUME = 100

    MOVE_LEFT_BUTTON = pygame.K_LEFT
    MOVE_RIGHT_BUTTON = pygame.K_RIGHT
    MOVE_DOWN_BUTTON = pygame.K_DOWN
    ROTATE_LEFT_BUTTON = pygame.K_UP
    ROTATE_RIGHT_BUTTON = pygame.K_q
    HARD_DROP_BUTTON = pygame.K_SPACE


pygame.mixer.pre_init()
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(Constants.WINDOW_SIZE)


class Board:
    audio_single = pygame.mixer.Sound('audio/single.wav')
    audio_double = pygame.mixer.Sound('audio/double.wav')
    audio_triple = pygame.mixer.Sound('audio/triple.wav')
    audio_tetris = pygame.mixer.Sound('audio/tetris.wav')

    sprite_single_I = pygame.sprite.Sprite()
    surface_single_I = pygame.image.load('res/single/singleI.png').convert_alpha()
    sprite_single_I.image = pygame.transform.scale(surface_single_I, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

    sprite_single_J = pygame.sprite.Sprite()
    surface_single_J = pygame.image.load('res/single/singleJ.png').convert_alpha()
    sprite_single_J.image = pygame.transform.scale(surface_single_J, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

    sprite_single_L = pygame.sprite.Sprite()
    surface_single_L = pygame.image.load('res/single/singleL.png').convert_alpha()
    sprite_single_L.image = pygame.transform.scale(surface_single_L, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

    sprite_single_O = pygame.sprite.Sprite()
    surface_single_O = pygame.image.load('res/single/singleO.png').convert_alpha()
    sprite_single_O.image = pygame.transform.scale(surface_single_O, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

    sprite_single_S = pygame.sprite.Sprite()
    surface_single_S = pygame.image.load('res/single/singleS.png').convert_alpha()
    sprite_single_S.image = pygame.transform.scale(surface_single_S, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

    sprite_single_T = pygame.sprite.Sprite()
    surface_single_T = pygame.image.load('res/single/singleT.png').convert_alpha()
    sprite_single_T.image = pygame.transform.scale(surface_single_T, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

    sprite_single_Z = pygame.sprite.Sprite()
    surface_single_Z = pygame.image.load('res/single/singleZ.png').convert_alpha()
    sprite_single_Z.image = pygame.transform.scale(surface_single_Z, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

    def __init__(self, side_length, topleft):
        self.board = list()
        self.init_board()
        self.topleft_x, self.topleft_y = topleft
        self.side_length = side_length
        self.last_time_destroyed = 0
        self.combo_counter = 0

    def init_board(self):
        for i in range(Constants.BOARD_SIZE[1]):
            line = list()
            for j in range(Constants.BOARD_SIZE[0]):
                line.append(0)
            self.board.append(line)

    def draw_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, (119, 136, 153),
                                     (self.topleft_x + self.side_length * j, self.topleft_y + self.side_length * i,
                                      self.side_length, self.side_length), 1)
                else:
                    screen.blit(self.get_block(self.board[i][j]),
                                (self.topleft_x + self.side_length * j, self.topleft_y + self.side_length * i))

    def get_block(self, i):
        if i == Constants.I:
            return self.sprite_single_I.image
        elif i == Constants.J:
            return self.sprite_single_J.image
        elif i == Constants.L:
            return self.sprite_single_L.image
        elif i == Constants.O:
            return self.sprite_single_O.image
        elif i == Constants.S:
            return self.sprite_single_S.image
        elif i == Constants.T:
            return self.sprite_single_T.image
        elif i == Constants.Z:
            return self.sprite_single_Z.image

    def get_line(self, position, length, height):
        try:
            return self.board[position[1] + height][position[0]:position[0] + length]
        except IndexError:
            return [1 for _ in range(length)]

    def check_under(self, position, under):
        for i in range(len(under)):
            if self.board[position[1] + under[i]][position[0] + i] != 0:
                return False
        return True

    def anchor_block(self, position, block_pattern):
        for i in range(len(block_pattern)):
            for j in range(len(block_pattern[i])):
                if block_pattern[i][j] != -1:
                    self.board[position[1] + i][position[0] + j] = block_pattern[i][j]
        self.check_lines()

    def check_collide(self, position, pattern):
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                try:
                    if pattern[i][j] != -1:
                        if self.board[position[1] + i][position[0] + j] != 0:
                            return False
                except IndexError:
                    return False
        return True

    def check_lines(self):
        lines = list()
        for i in range(len(self.board)):
            if 0 not in self.board[i]:
                lines.append(i)
        self.destroy_lines(lines)

    def destroy_lines(self, lines):
        if len(lines) == 0:
            return
        elif len(lines) == 1:
            self.audio_single.play()
        elif len(lines) == 2:
            self.audio_double.play()
        elif len(lines) == 3:
            self.audio_triple.play()
        elif len(lines) == 4:
            self.audio_tetris.play()

        for line in lines:
            i = line
            while i > 0:
                self.board[i] = self.board[i - 1].copy()
                i -= 1

        if pygame.time.get_ticks() - self.last_time_destroyed < 5000:
            self.combo_counter += 1
        else:
            self.combo_counter = 0

        if game.combo > 0:
            game.add_score(self.combo_counter * game.current_level + 50 * game.current_level)

        if len(lines) == 1:
            game.add_score(40 * (game.current_level + 1))
        elif len(lines) == 2:
            game.add_score(100 * (game.current_level + 1))
        elif len(lines) == 3:
            game.add_score(300 * (game.current_level + 1))
        elif len(lines) == 4:
            game.add_score(1200 * (game.current_level + 1))

    def check_lose(self):
        if len(set(self.board[0])) != 1:
            game.lose = True

    def check_right(self, position, pattern):
        for i in range(len(pattern)):
            if self.board[position[1] + i][position[0] + pattern[i]] != 0:
                return False
        return True

    def check_left(self, position, pattern):
        for i in range(len(pattern)):
            if self.board[position[1] + i][position[0] - pattern[i] - 1] != 0:
                return False
        return True


class Block:
    group_blocks = pygame.sprite.Group()

    sprite_I = pygame.sprite.Sprite()
    surface_I = pygame.image.load('res/I.png').convert_alpha()
    sprite_I.image = pygame.transform.scale(surface_I, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH * 4))
    sprite_I.rect = sprite_I.image.get_rect()
    group_blocks.add(sprite_I)

    sprite_J = pygame.sprite.Sprite()
    surface_J = pygame.image.load('res/J.png').convert_alpha()
    sprite_J.image = pygame.transform.scale(surface_J, (Constants.SIDE_LENGTH * 3, Constants.SIDE_LENGTH * 2))
    sprite_J.rect = sprite_J.image.get_rect()
    group_blocks.add(sprite_J)

    sprite_L = pygame.sprite.Sprite()
    surface_L = pygame.image.load('res/L.png').convert_alpha()
    sprite_L.image = pygame.transform.scale(surface_L, (Constants.SIDE_LENGTH * 3, Constants.SIDE_LENGTH * 2))
    sprite_L.rect = sprite_L.image.get_rect()
    group_blocks.add(sprite_L)

    sprite_O = pygame.sprite.Sprite()
    surface_O = pygame.image.load('res/O.png').convert_alpha()
    sprite_O.image = pygame.transform.scale(surface_O, (Constants.SIDE_LENGTH * 2, Constants.SIDE_LENGTH * 2))
    sprite_O.rect = sprite_O.image.get_rect()
    group_blocks.add(sprite_O)

    sprite_S = pygame.sprite.Sprite()
    surface_S = pygame.image.load('res/S.png').convert_alpha()
    sprite_S.image = pygame.transform.scale(surface_S, (Constants.SIDE_LENGTH * 3, Constants.SIDE_LENGTH * 2))
    sprite_S.rect = sprite_S.image.get_rect()
    group_blocks.add(sprite_S)

    sprite_T = pygame.sprite.Sprite()
    surface_T = pygame.image.load('res/T.png').convert_alpha()
    sprite_T.image = pygame.transform.scale(surface_T, (Constants.SIDE_LENGTH * 3, Constants.SIDE_LENGTH * 2))
    sprite_T.rect = sprite_T.image.get_rect()
    group_blocks.add(sprite_T)

    sprite_Z = pygame.sprite.Sprite()
    surface_Z = pygame.image.load('res/Z.png').convert_alpha()
    sprite_Z.image = pygame.transform.scale(surface_Z, (Constants.SIDE_LENGTH * 3, Constants.SIDE_LENGTH * 2))
    sprite_Z.rect = sprite_Z.image.get_rect()
    group_blocks.add(sprite_Z)

    audio_move = pygame.mixer.Sound('audio/move.wav')
    audio_rotate = pygame.mixer.Sound('audio/rotate.wav')
    audio_hard_drop = pygame.mixer.Sound('audio/hard_drop.wav')
    audio_soft_drop = pygame.mixer.Sound('audio/soft_drop.wav')
    audio_rotate_2 = pygame.mixer.Sound('audio/rotate_2.wav')
    audio_move.set_volume(Constants.MAX_VOLUME)
    audio_rotate.set_volume(Constants.MAX_VOLUME)
    audio_hard_drop.set_volume(Constants.MAX_VOLUME)
    audio_soft_drop.set_volume(Constants.MAX_VOLUME)
    audio_rotate_2.set_volume(Constants.MAX_VOLUME)

    def __init__(self):
        self.status = 0
        self.position = [4, 0]

    def draw(self):
        screen.blit(self.get_sprite(), (Constants.BOARD_TOPLEFT[0] + Constants.SIDE_LENGTH * self.position[0],
                                        Constants.BOARD_TOPLEFT[1] + Constants.SIDE_LENGTH * self.position[1]))

    def get_sprite(self):
        pass

    def move_right(self):
        if self.position[0] < Constants.BOARD_SIZE[0]:
            self.position[0] += 1
        self.audio_move.play()

    def rotate(self):
        pass

    def fall(self):
        if self.check_bottom():
            self.position[1] += 1

    def hard_drop(self):
        while self.check_bottom():
            self.position[1] += 1
            game.score += 2
        self.audio_hard_drop.play()
        self.anchor()

    def anchor(self):
        game.board.anchor_block(self.position, self.get_pattern())
        game.current_block.block = game.next_block()

    def check_bottom(self):
        pass

    def get_pattern(self):
        return list()

    def move_left(self):
        if self.position[0] > 0 and game.board.check_left(self.position, self.get_left_pattern()):
            self.position[0] -= 1
            self.audio_move.play()

    def get_left_pattern(self):
        return list()

    def check_rotation(self):
        if not game.board.check_collide(self.position, self.get_pattern()):
            self.position[1] += 1
            if not game.board.check_collide(self.position, self.get_pattern()):
                while not game.board.check_collide(self.position, self.get_pattern()):
                    self.position[1] -= 1
            else:
                self.audio_rotate_2.play()
                return
        self.audio_rotate.play()


class BlockI(Block):
    def __init__(self):
        super().__init__()
        self.position = [3, 0]
        self.sprite = self.sprite_I

    def rotate(self):
        if self.status == 0:
            if self.position[0] > Constants.BOARD_SIZE[0] - 4:
                self.position[0] = Constants.BOARD_SIZE[0] - 4
        elif self.status == 1:
            if self.position[0] == Constants.BOARD_SIZE[0] - 4:
                self.position[0] = Constants.BOARD_SIZE[0] - 1
            if self.position[1] > Constants.BOARD_SIZE[1] - 4:
                self.position[1] = Constants.BOARD_SIZE[1] - 4
        self.status += 1
        self.status = self.status % 2
        self.check_rotation()

    def move_right(self):
        if self.status == 1 and self.position[0] >= Constants.BOARD_SIZE[0] - 4:
            return
        elif self.status == 0 and self.position[0] >= Constants.BOARD_SIZE[0] - 1:
            return
        if game.board.check_right(self.position, self.get_right_pattern()):
            self.position[0] += 1
        self.audio_move.play()

    def get_right_pattern(self):
        if self.status == 0:
            return [1,
                    1,
                    1,
                    1]
        elif self.status == 1:
            return [4]

    def get_left_pattern(self):
        if self.status == 0:
            return [0, 0, 0, 0]
        elif self.status == 1:
            return [0]

    def get_sprite(self):
        if self.status == 0:
            return self.sprite.image
        elif self.status == 1:
            return pygame.transform.rotate(self.sprite.image, 90)

    def check_bottom(self):
        if self.status == 0:
            length = 1
            height = 4
        else:
            length = 4
            height = 1
        if self.position[1] >= Constants.BOARD_SIZE[1] - height:
            return False
        if sum(game.board.get_line(self.position, length, height)) == 0:
            return True
        return False

    def get_pattern(self):
        if self.status == 0:
            return [[Constants.I],
                    [Constants.I],
                    [Constants.I],
                    [Constants.I]]
        else:
            return [[Constants.I, Constants.I, Constants.I, Constants.I]]


class BlockJ(Block):
    def __init__(self):
        super().__init__()
        self.position = [4, 0]
        self.sprite = self.sprite_J

    def rotate(self):
        if self.position[0] >= Constants.BOARD_SIZE[0] - 2:
            self.position[0] -= 1
        self.status += 1
        self.status = self.status % 4
        self.check_rotation()

    def move_right(self):
        if self.status in (0, 2) and self.position[0] >= Constants.BOARD_SIZE[0] - 3:
            return
        elif self.status in (1, 3) and self.position[0] >= Constants.BOARD_SIZE[0] - 2:
            return
        if game.board.check_right(self.position, self.get_right_pattern()):
            self.position[0] += 1
        self.audio_move.play()

    def get_right_pattern(self):
        if self.status == 0:
            return [1, 3]
        elif self.status == 1:
            return [2, 2, 2]
        elif self.status == 2:
            return [3, 3]
        elif self.status == 3:
            return [2, 1, 1]

    def get_left_pattern(self):
        if self.status == 0:
            return [0, 0]
        elif self.status == 1:
            return [-1, -1, 0]
        elif self.status == 2:
            return [0, -2]
        elif self.status == 3:
            return [0, 0, 0]

    def get_sprite(self):
        if self.status == 0:
            return self.sprite.image
        elif self.status == 1:
            return pygame.transform.rotate(self.sprite.image, 90)
        elif self.status == 2:
            return pygame.transform.rotate(self.sprite.image, 180)
        elif self.status == 3:
            return pygame.transform.rotate(self.sprite.image, 270)

    def check_bottom(self):
        if self.position[1] + self.get_height() == Constants.BOARD_SIZE[1]:
            return False
        if game.board.check_under(self.position, self.get_under()):
            return True
        return False

    def get_height(self):
        if self.status in (0, 2):
            return 2
        elif self.status in (1, 3):
            return 3

    def get_under(self):
        if self.status == 0:
            return [2, 2, 2]
        elif self.status == 1:
            return [3, 3]
        elif self.status == 2:
            return [1, 1, 2]
        elif self.status == 3:
            return [3, 1]

    def get_pattern(self):
        if self.status == 0:
            return [[Constants.J, -1, -1],
                    [Constants.J, Constants.J, Constants.J]]
        elif self.status == 1:
            return [[-1, Constants.J],
                    [-1, Constants.J],
                    [Constants.J, Constants.J]]
        elif self.status == 2:
            return [[Constants.J, Constants.J, Constants.J],
                    [-1, -1, Constants.J]]
        elif self.status == 3:
            return [[Constants.J, Constants.J],
                    [Constants.J, -1],
                    [Constants.J, -1]]


class BlockL(Block):
    def __init__(self):
        super().__init__()
        self.position = [4, 0]
        self.sprite = self.sprite_L

    def rotate(self):
        if self.position[0] >= Constants.BOARD_SIZE[0] - 2:
            self.position[0] -= 1
        self.status += 1
        self.status = self.status % 4
        self.check_rotation()

    def move_right(self):
        if self.status in (0, 2) and self.position[0] >= Constants.BOARD_SIZE[0] - 3:
            return
        elif self.status in (1, 3) and self.position[0] >= Constants.BOARD_SIZE[0] - 2:
            return
        if game.board.check_right(self.position, self.get_right_pattern()):
            self.position[0] += 1
        self.audio_move.play()

    def get_right_pattern(self):
        if self.status == 0:
            return [3, 3]
        elif self.status == 1:
            return [2, 2, 2]
        elif self.status == 2:
            return [3, 1]
        elif self.status == 3:
            return [1, 1, 2]

    def get_left_pattern(self):
        if self.status == 0:
            return [-2, 0]
        elif self.status == 1:
            return [0, -1, -1]
        elif self.status == 2:
            return [0, 0]
        elif self.status == 3:
            return [0, 0, 0]

    def get_sprite(self):
        if self.status == 0:
            return self.sprite.image
        elif self.status == 1:
            return pygame.transform.rotate(self.sprite.image, 90)
        elif self.status == 2:
            return pygame.transform.rotate(self.sprite.image, 180)
        elif self.status == 3:
            return pygame.transform.rotate(self.sprite.image, 270)

    def check_bottom(self):
        if self.position[1] + self.get_height() == Constants.BOARD_SIZE[1]:
            return False
        if game.board.check_under(self.position, self.get_under()):
            return True
        return False

    def get_height(self):
        if self.status in (0, 2):
            return 2
        elif self.status in (1, 3):
            return 3

    def get_under(self):
        if self.status == 0:
            return [2, 2, 2]
        elif self.status == 1:
            return [1, 3]
        elif self.status == 2:
            return [2, 1, 1]
        elif self.status == 3:
            return [3, 3]

    def get_pattern(self):
        if self.status == 0:
            return [[-1, -1, Constants.L],
                    [Constants.L, Constants.L, Constants.L]]
        elif self.status == 1:
            return [[Constants.L, Constants.L],
                    [-1, Constants.L],
                    [-1, Constants.L]]
        elif self.status == 2:
            return [[Constants.L, Constants.L, Constants.L],
                    [Constants.L, -1, -1]]
        elif self.status == 3:
            return [[Constants.L, -1],
                    [Constants.L, -1],
                    [Constants.L, Constants.L]]


class BlockO(Block):
    def __init__(self):
        super().__init__()
        self.position = [5, 0]
        self.sprite = self.sprite_O

    def rotate(self):
        self.audio_rotate.play()

    def move_right(self):
        if self.position[0] < Constants.BOARD_SIZE[0] - 2 and game.board.check_right(self.position,
                                                                                     self.get_right_pattern()):
            self.position[0] += 1
        self.audio_move.play()

    def get_right_pattern(self):
        if self.status == 0:
            return [2, 2]

    def get_left_pattern(self):
        if self.status == 0:
            return [0, 0]

    def get_sprite(self):
        if self.status == 0:
            return self.sprite.image

    def check_bottom(self):
        length = 2
        height = 2
        if self.position[1] >= Constants.BOARD_SIZE[1] - height:
            return False
        if sum(game.board.get_line(self.position, length, height)) == 0:
            return True
        return False

    def get_pattern(self):
        return [[Constants.O, Constants.O],
                [Constants.O, Constants.O]]


class BlockS(Block):
    def __init__(self):
        super().__init__()
        self.position = [4, 0]
        self.sprite = self.sprite_S

    def rotate(self):
        if self.position[0] >= Constants.BOARD_SIZE[0] - 2:
            self.position[0] -= 1
        self.status += 1
        self.status = self.status % 2
        self.check_rotation()

    def move_right(self):
        if self.status == 0 and self.position[0] >= Constants.BOARD_SIZE[0] - 3:
            return
        elif self.status == 1 and self.position[0] >= Constants.BOARD_SIZE[0] - 2:
            return
        if game.board.check_right(self.position, self.get_right_pattern()):
            self.position[0] += 1
        self.audio_move.play()

    def get_right_pattern(self):
        if self.status == 0:
            return [3, 2]
        elif self.status == 1:
            return [1, 2, 2]

    def get_left_pattern(self):
        if self.status == 0:
            return [-1, 0]
        elif self.status == 1:
            return [0, 0, -1]

    def get_sprite(self):
        if self.status == 0:
            return self.sprite.image
        elif self.status == 1:
            return pygame.transform.rotate(self.sprite.image, 90)

    def check_bottom(self):
        if self.position[1] + self.get_height() == Constants.BOARD_SIZE[1]:
            return False
        if game.board.check_under(self.position, self.get_under()):
            return True
        return False

    def get_height(self):
        if self.status == 0:
            return 2
        elif self.status == 1:
            return 3

    def get_under(self):
        if self.status == 0:
            return [2, 2, 1]
        elif self.status == 1:
            return [2, 3]

    def get_pattern(self):
        if self.status == 0:
            return [[-1, Constants.S, Constants.S],
                    [Constants.S, Constants.S, -1]]
        elif self.status == 1:
            return [[Constants.S, -1],
                    [Constants.S, Constants.S],
                    [-1, Constants.S]]


class BlockT(Block):
    def __init__(self):
        super().__init__()
        self.position = [4, 0]
        self.sprite = self.sprite_T

    def rotate(self):
        if self.position[0] >= Constants.BOARD_SIZE[0] - 2:
            self.position[0] -= 1
        self.status += 1
        self.status = self.status % 4
        self.check_rotation()

    def move_right(self):
        if self.status in (0, 2) and self.position[0] >= Constants.BOARD_SIZE[0] - 3:
            return
        elif self.status in (1, 3) and self.position[0] >= Constants.BOARD_SIZE[0] - 2:
            return
        if game.board.check_right(self.position, self.get_right_pattern()):
            self.position[0] += 1

        self.audio_move.play()

    def get_right_pattern(self):
        if self.status == 0:
            return [2, 3]
        elif self.status == 1:
            return [2, 2, 2]
        elif self.status == 2:
            return [3, 2]
        elif self.status == 3:
            return [1, 2, 1]

    def get_left_pattern(self):
        if self.status == 0:
            return [-1, 0]
        elif self.status == 1:
            return [-1, 0, -1]
        elif self.status == 2:
            return [0, -1]
        elif self.status == 3:
            return [0, 0, 0]

    def get_sprite(self):
        if self.status == 0:
            return self.sprite.image
        elif self.status == 1:
            return pygame.transform.rotate(self.sprite.image, 90)
        elif self.status == 2:
            return pygame.transform.rotate(self.sprite.image, 180)
        elif self.status == 3:
            return pygame.transform.rotate(self.sprite.image, 270)

    def check_bottom(self):
        if self.position[1] + self.get_height() == Constants.BOARD_SIZE[1]:
            return False
        if game.board.check_under(self.position, self.get_under()):
            return True
        return False

    def get_height(self):
        if self.status in (0, 2):
            return 2
        elif self.status in (1, 3):
            return 3

    def get_under(self):
        if self.status == 0:
            return [2, 2, 2]
        elif self.status == 1:
            return [2, 3]
        elif self.status == 2:
            return [1, 2, 1]
        elif self.status == 3:
            return [3, 2]

    def get_pattern(self):
        if self.status == 0:
            return [[-1, Constants.T, -1],
                    [Constants.T, Constants.T, Constants.T]]
        elif self.status == 1:
            return [[-1, Constants.T],
                    [Constants.T, Constants.T],
                    [-1, Constants.T]]
        elif self.status == 2:
            return [[Constants.T, Constants.T, Constants.T],
                    [-1, Constants.T, -1]]
        elif self.status == 3:
            return [[Constants.T, -1],
                    [Constants.T, Constants.T],
                    [Constants.T, -1]]


class BlockZ(Block):
    def __init__(self):
        super().__init__()
        self.position = [4, 0]
        self.sprite = self.sprite_Z

    def rotate(self):
        if self.position[0] >= Constants.BOARD_SIZE[0] - 2:
            self.position[0] -= 1
        self.status += 1
        self.status = self.status % 2
        self.check_rotation()

    def move_right(self):
        if self.status == 0 and self.position[0] >= Constants.BOARD_SIZE[0] - 3:
            return
        elif self.status == 1 and self.position[0] >= Constants.BOARD_SIZE[0] - 2:
            return
        if game.board.check_right(self.position, self.get_right_pattern()):
            self.position[0] += 1
        self.audio_move.play()

    def get_right_pattern(self):
        if self.status == 0:
            return [2, 3]
        elif self.status == 1:
            return [2, 2, 1]

    def get_left_pattern(self):
        if self.status == 0:
            return [0, -1]
        elif self.status == 1:
            return [-1, 0, 0]

    def get_sprite(self):
        if self.status == 0:
            return self.sprite.image
        elif self.status == 1:
            return pygame.transform.rotate(self.sprite.image, 90)

    def check_bottom(self):
        if self.position[1] + self.get_height() == Constants.BOARD_SIZE[1]:
            return False
        if game.board.check_under(self.position, self.get_under()):
            return True
        return False

    def get_height(self):
        if self.status == 0:
            return 2
        elif self.status == 1:
            return 3

    def get_under(self):
        if self.status == 0:
            return [1, 2, 2]
        elif self.status == 1:
            return [3, 2]

    def get_pattern(self):
        if self.status == 0:
            return [[Constants.Z, Constants.Z, -1],
                    [-1, Constants.Z, Constants.Z]]
        elif self.status == 1:
            return [[-1, Constants.Z],
                    [Constants.Z, Constants.Z],
                    [Constants.Z, -1]]


class CurrentBlock:
    audio_fall = pygame.mixer.Sound('audio/soft_drop.wav')

    def __init__(self):
        self.block = None
        self.move_right = False
        self.move_left = False
        self.move_down = False

    def update(self):
        if self.move_right:
            self.block.move_right()
        elif self.move_left:
            self.block.move_left()
        elif self.move_down:
            if self.block.position[1] + len(self.block.get_pattern()) < Constants.BOARD_SIZE[1] \
                    and self.block.check_bottom():
                game.add_score(1)
                self.block.fall()
                self.audio_fall.play()

    def set_block(self, block):
        self.block = block


class Game:
    def __init__(self, level):
        self.score = 0
        self.current_block = CurrentBlock()
        self.board = Board(Constants.SIDE_LENGTH, Constants.BOARD_TOPLEFT)
        self.current_level = level
        pygame.time.set_timer(FALL_BLOCK_EVENT, Constants.FALL_TIME // level)
        self.lose = False
        self.font = pygame.font.Font('fonts/Orbitron-Bold.ttf', Constants.FONT_SIZE)
        self.combo = 0

    def add_score(self, score):
        self.score += score

    def draw_score(self):
        surface = self.font.render(str(self.score), True, (255, 255, 255))
        rect = surface.get_rect(topleft=Constants.SCORE_TOPLEFT)
        screen.blit(surface, rect)

    def next_block(self):
        self.current_block.set_block(
            random.choice([BlockI(), BlockJ(), BlockL(), BlockO(), BlockS(), BlockT(), BlockZ()]))


FALL_BLOCK_EVENT = pygame.USEREVENT

pygame.mixer.music.load('music/main_theme.ogg')
pygame.mixer.music.play(-1)

game = Game(1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == Settings.MOVE_LEFT_BUTTON:
                game.current_block.move_left = True
            elif event.key == Settings.MOVE_RIGHT_BUTTON:
                game.current_block.move_right = True
            elif event.key == Settings.ROTATE_LEFT_BUTTON:
                game.current_block.block.rotate()
            elif event.key == Settings.HARD_DROP_BUTTON:
                game.current_block.block.hard_drop()
            elif event.key == Settings.MOVE_DOWN_BUTTON:
                game.current_block.move_down = True
            elif event.key == 13:
                game.current_block.block = BlockI()
        elif event.type == pygame.KEYUP:
            if event.key == Settings.MOVE_LEFT_BUTTON:
                game.current_block.move_left = False
            elif event.key == Settings.MOVE_RIGHT_BUTTON:
                game.current_block.move_right = False
            elif event.key == Settings.MOVE_DOWN_BUTTON:
                game.current_block.move_down = False
        elif event.type == FALL_BLOCK_EVENT:
            game.current_block.block.fall()

    if not game.lose:
        if game.current_block.block is None:
            game.next_block()

        game.current_block.update()

        screen.fill('black')
        game.board.draw_board()
        game.current_block.block.draw()
        game.board.check_lose()
        game.draw_score()

    clock.tick(15)
    pygame.display.update()
