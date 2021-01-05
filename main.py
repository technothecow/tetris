import random
import sys
import pygame
import mysql.connector
from cryptography import fernet


class Constants:
    class Database:
        HOST = 'sql7.freemysqlhosting.net'
        USER = 'sql7384872'
        PASSWORD = 'j3S7PXimi6'
        DATABASE = 'sql7384872'

    I, J, L, O, S, T, Z = 1, 2, 3, 4, 5, 6, 7
    MAIN_MENU, SETTINGS, START_SCREEN, SHOP, PAUSE, INGAME, LEVEL_SELECT, PROFILE = 1, 2, 3, 4, 5, 6, 7, 8
    ENDSCREEN, AUTHORISATION = 9, 10
    SIDE_LENGTH = 32
    HD = (1280, 720)
    FULL_HD = (1920, 1080)
    MY_SCREEN = (1300, 700)  # (1366, 768)
    WINDOW_SIZE = MY_SCREEN
    FRAME_TOPLEFT = (50, 20)
    BOARD_TOPLEFT = (FRAME_TOPLEFT[0] + 99, FRAME_TOPLEFT[1] + 7)
    BOARD_SIZE = (10, 20)
    MAX_VOLUME = 0.5
    FALL_TIME = 1000
    FONT_SIZE = 30
    SCORE_FRAME_TOPLEFT = (700, 300)
    SCORE_TOPLEFT = (SCORE_FRAME_TOPLEFT[0] + 283, SCORE_FRAME_TOPLEFT[1] + 22)
    CURRENT_LEVEL_TOPLEFT = (SCORE_FRAME_TOPLEFT[0] + 283, SCORE_FRAME_TOPLEFT[1] + 72)
    TOTAL_LINES_TOPLEFT = (SCORE_FRAME_TOPLEFT[0] + 283, SCORE_FRAME_TOPLEFT[1] + 112)
    LINES_TILL_NEXT_LEVEL_TOPLEFT = (SCORE_FRAME_TOPLEFT[0] + 283, SCORE_FRAME_TOPLEFT[1] + 152)
    BLOCK_FALL_TIMER = 3000
    BLOCK_QUEUE_TOPLEFT = (FRAME_TOPLEFT[0] + 436, FRAME_TOPLEFT[1] + 34)
    HOLDED_BLOCK_TOPLEFT = (FRAME_TOPLEFT[0] + 19, FRAME_TOPLEFT[1] + 54)
    FPS = 30

    MAIL_SYMBOL_LIMIT = 30

    MUSIC_MAIN_MENU = 'music/menu_theme.mp3'

    PACK_DEFAULT = 'default'

    MARATHON, WORLDRECORD = 0, 1
    WIN, LOSE, NEUTRAL = 0, 1, 2

    KEY = b'3P8EAvmBQTK9Oz_WQdpMlzGB9agTwxmNOp7IdDJCm08='
    FERNET = fernet.Fernet(KEY)


pygame.mixer.pre_init()
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(Constants.WINDOW_SIZE)  # , pygame.FULLSCREEN)


class Board:
    audio_single = pygame.mixer.Sound('audio/single.wav')
    audio_double = pygame.mixer.Sound('audio/double.wav')
    audio_triple = pygame.mixer.Sound('audio/triple.wav')
    audio_tetris = pygame.mixer.Sound('audio/tetris.wav')

    surface_frame = pygame.image.load('res/frame.png').convert_alpha()

    def __init__(self, side_length, topleft):

        self.sprite_single_I = pygame.sprite.Sprite()
        self.surface_single_I = pack.singleI
        self.sprite_single_I.image = pygame.transform.scale(self.surface_single_I,
                                                            (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

        self.sprite_single_J = pygame.sprite.Sprite()
        self.surface_single_J = pack.singleJ
        self.sprite_single_J.image = pygame.transform.scale(self.surface_single_J,
                                                            (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

        self.sprite_single_L = pygame.sprite.Sprite()
        self.surface_single_L = pack.singleL
        self.sprite_single_L.image = pygame.transform.scale(self.surface_single_L,
                                                            (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

        self.sprite_single_O = pygame.sprite.Sprite()
        self.surface_single_O = pack.singleO
        self.sprite_single_O.image = pygame.transform.scale(self.surface_single_O,
                                                            (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

        self.sprite_single_S = pygame.sprite.Sprite()
        self.surface_single_S = pack.singleS
        self.sprite_single_S.image = pygame.transform.scale(self.surface_single_S,
                                                            (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

        self.sprite_single_T = pygame.sprite.Sprite()
        self.surface_single_T = pack.singleT
        self.sprite_single_T.image = pygame.transform.scale(self.surface_single_T,
                                                            (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

        self.sprite_single_Z = pygame.sprite.Sprite()
        self.surface_single_Z = pack.singleZ
        self.sprite_single_Z.image = pygame.transform.scale(self.surface_single_Z,
                                                            (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))

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
        screen.blit(self.surface_frame, Constants.FRAME_TOPLEFT)
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
        game.blocks += 1
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
            self.audio_single.set_volume(settings.AUDIO_VOLUME)
            self.audio_single.play()
            game.singles += 1
        elif len(lines) == 2:
            self.audio_double.set_volume(settings.AUDIO_VOLUME)
            self.audio_double.play()
            game.doubles += 1
        elif len(lines) == 3:
            self.audio_triple.set_volume(settings.AUDIO_VOLUME)
            self.audio_triple.play()
            game.triples += 1
        elif len(lines) == 4:
            self.audio_tetris.set_volume(settings.AUDIO_VOLUME)
            self.audio_tetris.play()
            game.tetrises += 1

        for line in lines:
            i = line
            while i > 0:
                self.board[i] = self.board[i - 1].copy()
                i -= 1

        if pygame.time.get_ticks() - self.last_time_destroyed < 5000:
            self.combo_counter += 1
            if self.combo_counter > game.max_combo:
                game.max_combo = self.combo_counter
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

        game.add_cleared_lines(len(lines))

    def check_lose(self):
        if len(set(self.board[0])) != 1:
            game.gameover = True

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
    audio_move = pygame.mixer.Sound('audio/move.wav')
    audio_rotate = pygame.mixer.Sound('audio/rotate.wav')
    audio_hard_drop = pygame.mixer.Sound('audio/hard_drop.wav')
    audio_soft_drop = pygame.mixer.Sound('audio/soft_drop.wav')
    audio_rotate_2 = pygame.mixer.Sound('audio/rotate_2.wav')
    audio_fall = pygame.mixer.Sound('audio/fall.wav')

    def __init__(self):
        self.sprite_I = pygame.sprite.Sprite()
        self.surface_I = pack.I
        self.sprite_I.image = pygame.transform.scale(self.surface_I, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH * 4))

        self.sprite_J = pygame.sprite.Sprite()
        self.surface_J = pack.J
        self.sprite_J.image = pygame.transform.scale(self.surface_J,
                                                     (Constants.SIDE_LENGTH * 3, Constants.SIDE_LENGTH * 2))

        self.sprite_L = pygame.sprite.Sprite()
        self.surface_L = pack.L
        self.sprite_L.image = pygame.transform.scale(self.surface_L,
                                                     (Constants.SIDE_LENGTH * 3, Constants.SIDE_LENGTH * 2))

        self.sprite_O = pygame.sprite.Sprite()
        self.surface_O = pack.O
        self.sprite_O.image = pygame.transform.scale(self.surface_O,
                                                     (Constants.SIDE_LENGTH * 2, Constants.SIDE_LENGTH * 2))

        self.sprite_S = pygame.sprite.Sprite()
        self.surface_S = pack.S
        self.sprite_S.image = pygame.transform.scale(self.surface_S,
                                                     (Constants.SIDE_LENGTH * 3, Constants.SIDE_LENGTH * 2))

        self.sprite_T = pygame.sprite.Sprite()
        self.surface_T = pack.T
        self.sprite_T.image = pygame.transform.scale(self.surface_T,
                                                     (Constants.SIDE_LENGTH * 3, Constants.SIDE_LENGTH * 2))

        self.sprite_Z = pygame.sprite.Sprite()
        self.surface_Z = pack.Z
        self.sprite_Z.image = pygame.transform.scale(self.surface_Z,
                                                     (Constants.SIDE_LENGTH * 3, Constants.SIDE_LENGTH * 2))

        self.audio_move.set_volume(settings.AUDIO_VOLUME)
        self.audio_rotate.set_volume(settings.AUDIO_VOLUME)
        self.audio_hard_drop.set_volume(settings.AUDIO_VOLUME)
        self.audio_soft_drop.set_volume(settings.AUDIO_VOLUME)
        self.audio_rotate_2.set_volume(settings.AUDIO_VOLUME)
        self.audio_fall.set_volume(settings.AUDIO_VOLUME)

        self.status = 0
        self.position = [4, 0]
        self.timer_set = False

    def draw(self):
        screen.blit(self.get_sprite(), (Constants.BOARD_TOPLEFT[0] + Constants.SIDE_LENGTH * self.position[0],
                                        Constants.BOARD_TOPLEFT[1] + Constants.SIDE_LENGTH * self.position[1]))

        temp = self.get_sprite().copy()
        temp.set_alpha(50)
        temp_position = self.position.copy()
        while temp_position[1] + self.get_height() < Constants.BOARD_SIZE[1] and \
                game.board.check_under(temp_position, self.get_under()):
            temp_position[1] += 1
        screen.blit(temp, (Constants.BOARD_TOPLEFT[0] + Constants.SIDE_LENGTH * temp_position[0],
                           Constants.BOARD_TOPLEFT[1] + Constants.SIDE_LENGTH * temp_position[1]))

    def get_under(self):
        return [0]

    def get_sprite(self):
        return self.sprite_I.image

    def move_right(self):
        if self.position[0] < Constants.BOARD_SIZE[0]:
            self.position[0] += 1
        self.audio_move.set_volume(settings.AUDIO_VOLUME)
        self.audio_move.play()

    def rotate(self):
        pass

    def fall(self):
        if self.check_bottom():
            self.position[1] += 1
        else:
            if not self.timer_set:
                self.timer_set = True
                game.BLOCK_ANCHOR.start(Constants.BLOCK_FALL_TIMER)

    def hard_drop(self, sound):
        while self.check_bottom():
            self.position[1] += 1
            game.score += 2
        if sound:
            self.audio_hard_drop.set_volume(settings.AUDIO_VOLUME)
            self.audio_hard_drop.play()
        else:
            self.audio_fall.set_volume(settings.AUDIO_VOLUME)
            self.audio_fall.play()
        self.anchor()
        return self.position, self.get_length(), self.get_height()

    def anchor(self):
        game.board.anchor_block(self.position, self.get_pattern())
        game.next_block()

    def check_bottom(self):
        pass

    def get_pattern(self):
        return list()

    def move_left(self):
        if self.position[0] > 0 and game.board.check_left(self.position, self.get_left_pattern()):
            self.position[0] -= 1
            self.audio_move.set_volume(settings.AUDIO_VOLUME)
            self.audio_move.play()

    def get_left_pattern(self):
        return list()

    def check_rotation(self):
        if not game.board.check_collide(self.position, self.get_pattern()):
            self.position[1] += 1
            if not game.board.check_collide(self.position, self.get_pattern()):
                while not game.board.check_collide(self.position, self.get_pattern()) and self.position[1] > 0:
                    self.position[1] -= 1
            else:
                game.tspins += 1
                game.add_score(100 * game.current_level)
                self.audio_rotate_2.set_volume(settings.AUDIO_VOLUME)
                self.audio_rotate_2.play()
                self.audio_rotate_2.set_volume(settings.AUDIO_VOLUME)
                return
        self.audio_rotate.set_volume(settings.AUDIO_VOLUME)
        self.audio_rotate.play()

    def get_length(self):
        return len(self.get_pattern()[0])

    def get_height(self):
        return len(self.get_pattern())


class BlockI(Block):
    def __init__(self):
        super().__init__()
        self.position = [3, 0]
        self.sprite = self.sprite_I
        self.status = 1

    def get_self(self):
        if self:
            return BlockI()

    def get_sprite_for_frame(self):
        return pygame.transform.scale(self.get_sprite(), (18 * 4, 18))

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
        self.audio_move.set_volume(settings.AUDIO_VOLUME)
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
        if self.position[1] >= Constants.BOARD_SIZE[1] - self.get_height():
            return False
        if sum(game.board.get_line(self.position, self.get_length(), self.get_height())) == 0:
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

    def get_under(self):
        if self.status == 0:
            return [4]
        elif self.status == 1:
            return [1, 1, 1, 1]


class BlockJ(Block):
    def __init__(self):
        super().__init__()
        self.position = [4, 0]
        self.sprite = self.sprite_J

    def get_self(self):
        if self:
            return BlockJ()

    def get_sprite_for_frame(self):
        return pygame.transform.scale(self.get_sprite(), (18 * 3, 18 * 2))

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
        self.audio_move.set_volume(settings.AUDIO_VOLUME)
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

    def get_self(self):
        if self:
            return BlockL()

    def get_sprite_for_frame(self):
        return pygame.transform.scale(self.get_sprite(), (18 * 3, 18 * 2))

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
        self.audio_move.set_volume(settings.AUDIO_VOLUME)
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

    def get_self(self):
        if self:
            return BlockO()

    def get_sprite_for_frame(self):
        return pygame.transform.scale(self.get_sprite(), (18 * 2, 18 * 2))

    def rotate(self):
        self.audio_rotate.set_volume(settings.AUDIO_VOLUME)
        self.audio_rotate.play()

    def move_right(self):
        if self.position[0] < Constants.BOARD_SIZE[0] - 2 and game.board.check_right(self.position,
                                                                                     self.get_right_pattern()):
            self.position[0] += 1
        self.audio_move.set_volume(settings.AUDIO_VOLUME)
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

    def get_under(self):
        if self.status == 0:
            return [2, 2]


class BlockS(Block):
    def __init__(self):
        super().__init__()
        self.position = [4, 0]
        self.sprite = self.sprite_S

    def get_self(self):
        if self:
            return BlockS()

    def get_sprite_for_frame(self):
        return pygame.transform.scale(self.get_sprite(), (18 * 3, 18 * 2))

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
        self.audio_move.set_volume(settings.AUDIO_VOLUME)
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

    def get_self(self):
        if self:
            return BlockT()

    def get_sprite_for_frame(self):
        return pygame.transform.scale(self.get_sprite(), (18 * 3, 18 * 2))

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

        self.audio_move.set_volume(settings.AUDIO_VOLUME)
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

    def get_self(self):
        if self:
            return BlockZ()

    def get_sprite_for_frame(self):
        return pygame.transform.scale(self.get_sprite(), (18 * 3, 18 * 2))

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
        self.audio_move.set_volume(settings.AUDIO_VOLUME)
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

        self.counter = 0

    def get_type(self):
        return self.block.get_self()

    def update(self):
        self.counter += 1
        self.counter %= 2
        if self.counter == 0:
            if self.move_right:
                self.block.move_right()
            elif self.move_left:
                self.block.move_left()
            elif self.move_down:
                if self.block.position[1] + len(self.block.get_pattern()) < Constants.BOARD_SIZE[1] \
                        and self.block.check_bottom():
                    game.add_score(1)
                    self.block.fall()
                    self.audio_fall.set_volume(settings.AUDIO_VOLUME)
                    self.audio_fall.play()

    def set_block(self, block):
        self.block = block
        game.BLOCK_ANCHOR.stop()


class Game:
    audio_level_up = pygame.mixer.Sound('audio/game_level_up.wav')
    audio_level_up1 = pygame.mixer.Sound('audio/level_up1.wav')
    audio_level_up2 = pygame.mixer.Sound('audio/level_up2.wav')

    surface_scoreboard = pygame.image.load('res/scoreboard.png').convert_alpha()

    audio_ready = pygame.mixer.Sound('audio/ready.wav')
    audio_count = pygame.mixer.Sound('audio/count.wav')
    audio_go = pygame.mixer.Sound('audio/go.wav')
    audio_game_start = pygame.mixer.Sound('audio/game_start.wav')

    def __init__(self):
        self.gameover = False

        pygame.mixer.music.stop()

        self.score, self.combo = 0, 0
        self.singles, self.doubles, self.triples, self.tetrises, self.blocks = 0, 0, 0, 0, 0
        self.max_combo, self.lines_cleared, self.lines_cleared_from_last_level, self.tspins = 0, 0, 0, 0

        self.board = Board(Constants.SIDE_LENGTH, Constants.BOARD_TOPLEFT)

        self.font = pygame.font.Font('fonts/Orbitron-Bold.ttf', Constants.FONT_SIZE)

        self.start_time = pygame.time.get_ticks()

        self.block_queue = BlockQueue()
        self.current_block = CurrentBlock()
        self.BLOCK_ANCHOR = Timer()

        self.holded = False
        pygame.time.set_timer(FALL_BLOCK_EVENT, Constants.FALL_TIME)

        self.countdown_count = list()
        for i in range(5):
            self.countdown_count.append(True)

    def render_and_update(self):
        if self.current_block.block is None:
            self.next_block()

        self.current_block.update()

        self.board.draw_board()
        self.current_block.block.draw()
        self.board.check_lose()
        self.block_queue.render()

        particles.update()
        particles.draw(screen)

    def get_current_time(self):
        return pygame.time.get_ticks() - self.start_time

    def is_countdown(self):
        return self.get_current_time() < 4700

    def countdown(self):
        game.board.draw_board()
        if 0 <= self.get_current_time() < 50 and self.countdown_count[0]:
            self.audio_ready.set_volume(settings.AUDIO_VOLUME)
            self.audio_ready.play()
            self.countdown_count[0] = False
        elif 1000 <= self.get_current_time() < 1050 and self.countdown_count[1]:
            self.audio_count.set_volume(settings.AUDIO_VOLUME)
            self.audio_count.play()
            self.countdown_count[1] = False
        elif 2000 <= self.get_current_time() < 2050 and self.countdown_count[2]:
            self.audio_count.play()
            self.countdown_count[2] = False
        elif 3000 <= self.get_current_time() < 3050 and self.countdown_count[3]:
            self.audio_count.play()
            self.countdown_count[3] = False
        elif 4000 <= self.get_current_time() < 4050 and self.countdown_count[4]:
            self.audio_go.set_volume(settings.AUDIO_VOLUME)
            self.audio_go.play()
            self.countdown_count[4] = False
        elif 4500 <= self.get_current_time() < 4550:
            self.audio_game_start.set_volume(settings.AUDIO_VOLUME)
            self.audio_game_start.play()
        elif 4600 <= self.get_current_time() < 4650:
            self.load_music()

        text = None

        if 0 <= self.get_current_time() < 1000:
            text = 'READY'
        elif 1000 <= self.get_current_time() < 2000:
            text = '3'
        elif 2000 <= self.get_current_time() < 3000:
            text = '2'
        elif 3000 <= self.get_current_time() < 4000:
            text = '1'
        elif 4000 <= self.get_current_time() < 4500:
            text = 'GO'

        surface_text = self.font.render(text, True, (255, 255, 255))
        rect_text = surface_text.get_rect(center=(
            (Constants.BOARD_TOPLEFT[0] + Constants.BOARD_SIZE[0] * Constants.SIDE_LENGTH) // 3 * 2,
            (Constants.BOARD_TOPLEFT[1] + Constants.BOARD_SIZE[1] * Constants.SIDE_LENGTH) // 3))
        screen.blit(surface_text, rect_text)

    def may_hold(self):
        return not self.holded

    def add_score(self, score):
        self.score += score

    def add_cleared_lines(self, lines):
        self.lines_cleared += lines

    def next_block(self):
        self.current_block.set_block(self.block_queue.pop(0))
        self.holded = False


class Marathon(Game):
    def __init__(self, level):
        super().__init__()
        self.current_level = level
        pygame.time.set_timer(FALL_BLOCK_EVENT, Constants.FALL_TIME // level)
        self.mode = Constants.MARATHON
        self.result = False

    def render_and_update(self):
        super().render_and_update()
        self.draw_score()

    def add_cleared_lines(self, lines):
        super().add_cleared_lines(lines)
        self.lines_cleared_from_last_level += lines
        self.check_level()

    def load_music(self):
        if self.current_level <= 10:
            pygame.mixer.music.load(pack.main_theme)
        elif 10 < self.current_level <= 15:
            pygame.mixer.music.load(pack.main_theme_2)
        elif 15 < self.current_level <= 20:
            pygame.mixer.music.load(pack.main_theme_3)
        pygame.mixer.music.play(-1)

    def check_level(self):
        if self.lines_cleared_from_last_level >= 10:
            if self.current_level <= 10:
                self.lines_cleared_from_last_level -= 10
                self.level_up()
                if self.current_level == 11:
                    pygame.mixer.music.load(pack.main_theme_2)
                    pygame.mixer.music.play(-1)
            elif 10 < self.current_level <= 15 and self.lines_cleared_from_last_level >= 20:
                self.lines_cleared_from_last_level -= 20
                self.level_up()
                if self.current_level == 16:
                    pygame.mixer.music.load(pack.main_theme_3)
                    pygame.mixer.music.play(-1)
            elif 15 < self.current_level < 20 and self.lines_cleared_from_last_level >= 30:
                self.lines_cleared_from_last_level -= 30
                self.level_up()

    def level_up(self):
        self.current_level += 1
        if self.current_level == 11:
            self.audio_level_up1.set_volume(settings.AUDIO_VOLUME)
            self.audio_level_up1.play()
        elif self.current_level == 16:
            self.audio_level_up2.set_volume(settings.AUDIO_VOLUME)
            self.audio_level_up2.play()
        else:
            self.audio_level_up.set_volume(settings.AUDIO_VOLUME)
            self.audio_level_up.play()
        pygame.time.set_timer(FALL_BLOCK_EVENT, Constants.FALL_TIME // self.current_level)

    def get_lines_to_next_level(self):
        if self.current_level <= 10:
            return 10 - self.lines_cleared_from_last_level
        elif 10 < self.current_level <= 15:
            return 20 - self.lines_cleared_from_last_level
        elif 15 < self.current_level < 20:
            return 30 - self.lines_cleared_from_last_level
        elif self.current_level == 20:
            return "Infinite"

    def draw_score(self):
        screen.blit(self.surface_scoreboard, Constants.SCORE_FRAME_TOPLEFT)
        surface = self.font.render(str(self.score), True, (0, 0, 0))
        rect = surface.get_rect(topleft=Constants.SCORE_TOPLEFT)
        screen.blit(surface, rect)
        surface = self.font.render(str(self.current_level), True, (0, 0, 0))
        rect = surface.get_rect(topleft=Constants.CURRENT_LEVEL_TOPLEFT)
        screen.blit(surface, rect)
        surface = self.font.render(str(self.lines_cleared), True, (0, 0, 0))
        rect = surface.get_rect(topleft=Constants.TOTAL_LINES_TOPLEFT)
        screen.blit(surface, rect)
        surface = self.font.render(str(self.get_lines_to_next_level()), True, (0, 0, 0))
        rect = surface.get_rect(topleft=Constants.LINES_TILL_NEXT_LEVEL_TOPLEFT)
        screen.blit(surface, rect)


class WorldRecord(Game):
    class Timer:
        def __init__(self):
            self.start_time = pygame.time.get_ticks()

        def get_time(self):
            return pygame.time.get_ticks() - self.start_time

    def __init__(self):
        super().__init__()
        self.timer = None
        self.time_font = pygame.font.Font('fonts/Orbitron-Bold.ttf', Constants.WINDOW_SIZE[1] // 20)
        self.desk_surface = pygame.surface.Surface(
            (Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 10 * 2))
        self.desk_rect = self.desk_surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 10 * 6,
                                                            Constants.WINDOW_SIZE[1] // 10 * 5))
        self.desk_surface.set_alpha(100)
        self.desk_surface.fill((102, 204, 204))
        self.mode = Constants.WORLDRECORD
        self.current_level = 15
        self.result = False

    def countdown(self):
        super().countdown()
        self.timer = self.Timer()

    def render_and_update(self):
        self.check_win()
        super().render_and_update()
        screen.blit(self.desk_surface, self.desk_rect)
        surface_time_left = self.time_font.render(get_time(self.timer.get_time(), True), True, (255, 255, 255))
        rect_time_left = surface_time_left.get_rect(center=(Constants.WINDOW_SIZE[0] // 10 * 6,
                                                            Constants.WINDOW_SIZE[1] // 20 * 9))
        surface_lines_left = self.time_font.render('Lines left: ' + str(self.get_lines_left()), True, (255, 255, 255))
        rect_lines_left = surface_lines_left.get_rect(center=(Constants.WINDOW_SIZE[0] // 10 * 6,
                                                              Constants.WINDOW_SIZE[1] // 20 * 11))
        screen.blit(surface_time_left, rect_time_left)
        screen.blit(surface_lines_left, rect_lines_left)

    def get_lines_left(self):
        return 100 - self.lines_cleared

    def check_win(self):
        if self.lines_cleared >= 100:
            self.gameover = True
            self.result = True

    def load_music(self):
        if self:
            pygame.mixer.music.load(pack.main_theme_3)
            pygame.mixer.music.play(-1)


def get_random_block():
    return random.choice([BlockI(), BlockJ(), BlockL(), BlockO(), BlockS(), BlockT(), BlockZ()])


class BlockQueue:
    audio_hold = pygame.mixer.Sound('audio/hold.wav')

    def __init__(self):
        self.queue = list()
        for i in range(6):
            self.queue.append(get_random_block())
        self.holded = None

    def hold(self):
        game.BLOCK_ANCHOR.stop()
        self.holded, game.current_block.block = game.current_block.get_type(), self.holded
        game.holded = True
        self.audio_hold.set_volume(settings.AUDIO_VOLUME)
        self.audio_hold.play()

    def pop(self, index):
        self.queue.append(get_random_block())
        return self.queue.pop(index)

    def render(self):
        for i in range(len(self.queue)):
            screen.blit(self.queue[i].get_sprite_for_frame(),
                        (Constants.BLOCK_QUEUE_TOPLEFT[0], Constants.BLOCK_QUEUE_TOPLEFT[1] + i * 55))
        if self.holded:
            screen.blit(self.holded.get_sprite_for_frame(), Constants.HOLDED_BLOCK_TOPLEFT)


class Background:
    def __init__(self):
        self.frames = list()
        self.load_frames()
        self.current_frame = 0

    def load_frames(self):
        for i in range(1, 122):
            if i < 10:
                i = '00' + str(i)
            elif i < 100:
                i = '0' + str(i)
            else:
                i = str(i)
            temp = pygame.image.load(f'res/background/Untitled {i}.jpg').convert()
            temp = pygame.transform.scale(temp, Constants.WINDOW_SIZE)
            self.frames.append(temp)

    def render(self):
        self.current_frame += 1
        self.current_frame %= 120
        screen.blit(self.frames[self.current_frame], (0, 0))


class StartScreen:
    surface_tetris_logo = pygame.image.load('res/tetris_logo_remaster.png').convert_alpha()
    surface_tetris_logo = pygame.transform.scale(surface_tetris_logo, (Constants.WINDOW_SIZE[0] // 20 * 7,
                                                                       Constants.WINDOW_SIZE[1] // 20 * 4))
    rect_tetris_logo = surface_tetris_logo.get_rect(
        center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 20 * 5))
    font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', 40)
    surface_text = font.render('Press F to continue', True, (255, 255, 255))
    rect_text = surface_text.get_rect(center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 4 * 3))

    def __init__(self):
        self.text_fading_mode = 0

    def get_surface_text(self):
        current_alpha = self.surface_text.get_alpha()
        if self.text_fading_mode == 0:
            self.surface_text.set_alpha(current_alpha + 10)
        elif self.text_fading_mode == 1:
            self.surface_text.set_alpha(current_alpha - 10)

        if current_alpha == 0:
            self.text_fading_mode = 0
        elif current_alpha == 255:
            self.text_fading_mode = 1

        return self.surface_text


class LevelSelection:
    audio_swap = pygame.mixer.Sound('audio/level_selection_swap.wav')
    audio_select = pygame.mixer.Sound('audio/level_selection_confirm.wav')
    surface_window = pygame.image.load('res/select_level.png')
    rect_window = surface_window.get_rect(center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 2))
    topleft_x, topleft_y = rect_window.topleft

    def __init__(self):
        self.selected_level = 0
        self.rect_buttons = [pygame.rect.Rect((self.topleft_x + 16 + (9 + 40) * i, self.topleft_y + 51), (40, 40)) for i
                             in range(10)]
        self.rect_buttons += [pygame.rect.Rect((self.topleft_x + 16 + (9 + 40) * i, self.topleft_y + 112), (40, 40)) for
                              i in
                              range(10)]
        self.rect_start_button = pygame.rect.Rect((self.topleft_x + 207, self.topleft_y + 167), (100, 28))

    def render(self):
        screen.blit(self.surface_window, self.rect_window)
        pygame.draw.ellipse(screen, 'black', self.rect_buttons[self.selected_level], 1)

    def check_pos(self, pos):
        for i in range(len(self.rect_buttons)):
            if self.rect_buttons[i].collidepoint(pos):
                if self.selected_level != i:
                    self.selected_level = i
                    self.audio_swap.set_volume(settings.AUDIO_VOLUME)
                    self.audio_swap.play()
                return
        if self.rect_start_button.collidepoint(pos):
            self.audio_select.set_volume(settings.AUDIO_VOLUME)
            self.audio_select.play()
            return True
        return False

    def get_selected_level(self):
        return self.selected_level + 1


class HardDropParticle(pygame.sprite.Sprite):
    image = pygame.image.load('res/beam.png').convert_alpha()

    def __init__(self, pos, length, height):
        super().__init__(particles)
        self.image = pygame.transform.scale(self.image,
                                            (Constants.SIDE_LENGTH * length, (pos[1] + height) * Constants.SIDE_LENGTH))
        self.rect = pygame.rect.Rect((Constants.BOARD_TOPLEFT[0] + pos[0] * Constants.SIDE_LENGTH,
                                      Constants.BOARD_TOPLEFT[1]),
                                     (Constants.SIDE_LENGTH * length, (pos[1] + height) * Constants.SIDE_LENGTH))
        self.start_time = pygame.time.get_ticks()

    def get_current_time(self):
        return pygame.time.get_ticks() - self.start_time

    def update(self):
        self.image.set_alpha(70 - self.get_current_time() // 5)
        if self.image.get_alpha() == 0:
            self.kill()
            del self


class MainMenu:
    surface_light = pygame.image.load('res/light.png').convert_alpha()
    audio_click = pygame.mixer.Sound('audio/main_menu_select.wav')

    def __init__(self, u):
        self.user = u
        self.buttons = list()
        self.surfaces = list()
        self.selected_button = None
        self.transition = True
        self.transcript = {0: Constants.PROFILE, 1: Constants.LEVEL_SELECT, 2: Constants.SHOP, 3: Constants.SETTINGS,
                           4: -1}
        self.confirm_exit = False
        self.surface_tetris_logo = StartScreen.surface_tetris_logo
        self.rect_tetris_logo = StartScreen.rect_tetris_logo
        self.font_buttons = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', 60)
        self.load_buttons()

    def is_transition(self):
        return self.transition

    def do_transition(self):
        if self.rect_tetris_logo.centery > Constants.WINDOW_SIZE[1] // 5:
            self.rect_tetris_logo.centery -= 3
        else:
            self.transition = False

    def load_buttons(self):
        surface_profile = pygame.surface.Surface((Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 10))
        rect_profile = surface_profile.get_rect(topright=(Constants.WINDOW_SIZE[0], 0))
        self.buttons.append([surface_profile, rect_profile])
        surface_play = self.font_buttons.render('Play', True, (255, 255, 255))
        rect_play = surface_play.get_rect(center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 10 * 4))
        self.buttons.append([surface_play, rect_play])
        surface_shop = self.font_buttons.render('Shop', True, (255, 255, 255))
        rect_shop = surface_shop.get_rect(center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 10 * 5))
        self.buttons.append([surface_shop, rect_shop])
        surface_settings = self.font_buttons.render('Settings', True, (255, 255, 255))
        rect_settings = surface_settings.get_rect(
            center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 10 * 6))
        self.buttons.append([surface_settings, rect_settings])
        surface_exit = self.font_buttons.render('Exit', True, (255, 255, 255))
        rect_exit = surface_exit.get_rect(center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 10 * 7))
        self.buttons.append([surface_exit, rect_exit])

    def get_covered(self, pos):
        for i in range(1, 5):
            if self.buttons[i][1].collidepoint(pos):
                self.selected_button = i

    def get_clicked(self, pos):
        for i in range(len(self.buttons)):
            if self.buttons[i][1].collidepoint(pos):
                return self.transcript[i]
        return None

    def draw_buttons(self):
        for button in self.buttons:
            screen.blit(button[0], button[1])

    def button_down(self):
        if self.selected_button:
            if self.selected_button < 4:
                self.selected_button += 1

    def button_up(self):
        if self.selected_button:
            if self.selected_button > 1:
                self.selected_button -= 1

    def button_select(self):
        if self.selected_button:
            return self.transcript[self.selected_button]

    def render(self):
        if self.is_transition():
            self.do_transition()
        else:
            if self.selected_button:
                screen.blit(
                    pygame.transform.scale(self.surface_light, (
                        self.buttons[self.selected_button][1].width, self.buttons[self.selected_button][1].height)),
                    self.buttons[self.selected_button][1])
            self.draw_buttons()
        screen.blit(self.surface_tetris_logo, self.rect_tetris_logo)


def get_time(ms, with_ms=False):
    if not with_ms:
        ms = ms // 1000
        return f'{ms // 60 // 60}:{ms // 60 % 60}:{ms % 60}'
    ms = ms // 10
    return f'{ms // 100 // 60}:{ms // 100 % 60}:{ms % 100}'


class EndGameScreen:
    audio_ok = pygame.mixer.Sound('audio/ok.wav')
    audio_gameover = pygame.mixer.Sound('audio/gameover.wav')

    def __init__(self):
        time = game.get_current_time()
        self.stats = [f'Score: {str(game.score)}', f'Lines cleared: {str(game.lines_cleared)}',
                      f'Time played: {get_time(time)}', '', f'Blocks placed: {str(game.blocks)}',
                      f'Max combo: {str(game.max_combo)}', f'T-spins: {str(game.tspins)}',
                      f'Singles: {str(game.singles)}', f'Doubles: {str(game.doubles)}', f'Triples: {str(game.triples)}',
                      f'Tetris lines cleared: {str(game.tetrises)}']

        self.surface_frame = pygame.surface.Surface((500, 600))
        self.rect_frame = self.surface_frame.get_rect(
            center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 2))
        self.surface_frame.fill((86, 233, 204))

        self.text_font = pygame.font.Font('fonts/Orbitron-Bold.ttf', 25)
        self.title_font = pygame.font.Font('fonts/Orbitron-Bold.ttf', 75)
        self.surface_title = self.title_font.render('Game over!', True, (255, 255, 255))
        self.rect_title = self.surface_title.get_rect(midtop=(500 // 2, 0))

        width = Constants.WINDOW_SIZE[0] // 5
        height = Constants.WINDOW_SIZE[1] // 10
        self.button_back_to_menu = Button(self.on_click, Constants.WINDOW_SIZE[0] // 2 - width // 2,
                                          Constants.WINDOW_SIZE[1] // 20 * 16, width, height, 'Main menu',
                                          (102, 204, 204))

        self.start_time = pygame.time.get_ticks()

        self.music_started = False
        pygame.mixer.music.stop()
        self.audio_gameover.set_volume(settings.AUDIO_VOLUME)
        self.audio_gameover.play()

        self.back_to_menu_pressed = False
        self.fadeout_start_time = None
        self.FADEOUT_TIME = 2000

        if game.mode == Constants.MARATHON:
            user.add_marathon_game(game.score, game.lines_cleared, time, game.blocks, game.max_combo,
                                   game.tspins, game.singles, game.doubles, game.triples, game.tetrises)
        elif game.mode == Constants.WORLDRECORD:
            user.add_world_record_game(game.score, game.lines_cleared, time, game.blocks,
                                       game.max_combo, game.tspins, game.singles, game.doubles, game.triples,
                                       game.tetrises)
            user.add_world_record_time(time)

    def render(self):
        if not self.music_started and pygame.time.get_ticks() - self.start_time > 6000:
            self.music_started = True
            pygame.mixer.music.load('music/eliminated.ogg')
            pygame.mixer.music.play(-1)
        screen.blit(self.surface_frame, self.rect_frame)
        self.surface_frame.blit(self.surface_title, self.rect_title)
        for i in range(len(self.stats)):
            surface = self.text_font.render(self.stats[i], True, (255, 255, 255))
            rect = surface.get_rect(midtop=(Constants.WINDOW_SIZE[0] // 2, 150 + 35 * i))
            screen.blit(surface, rect)
        self.button_back_to_menu.render()
        if self.fadeout_start_time is not None:
            self.fadeout()

    def on_click(self):
        if not self.back_to_menu_pressed:
            self.audio_ok.set_volume(settings.AUDIO_VOLUME)
            self.audio_ok.play()
            self.back_to_menu_pressed = True
            self.fadeout_start_time = pygame.time.get_ticks()

    def fadeout(self):
        time = self.get_time()
        surface = pygame.surface.Surface(Constants.WINDOW_SIZE)
        surface.set_alpha(time // (self.FADEOUT_TIME // 255))
        try:
            pygame.mixer.music.set_volume(
                Settings.MUSIC_VOLUME - time * (self.FADEOUT_TIME / Settings.MUSIC_VOLUME))
        except ZeroDivisionError:
            pass
        screen.blit(surface, (0, 0))
        if not time < self.FADEOUT_TIME:
            global program_state
            program_state = Constants.MAIN_MENU
            pygame.mixer.music.load(Constants.MUSIC_MAIN_MENU)
            pygame.mixer.music.set_volume(Settings.MUSIC_VOLUME)
            pygame.mixer.music.play(-1)

    def get_time(self):
        return pygame.time.get_ticks() - self.fadeout_start_time


class Settings:
    try:
        with open('settings', 'r', encoding='utf8') as reader:
            settings = reader.readlines()
        settings = iter(settings)
    except FileNotFoundError:
        with open('settings', 'w', encoding='utf8') as writer:
            settings = '1\n1\n1073741904\n1073741903\n1073741905\n1073741906\n113\n32\n13'
            writer.write(settings)
        settings = iter(settings.split('\n'))

    AUDIO_VOLUME = float(settings.__next__())
    MUSIC_VOLUME = float(settings.__next__())

    MOVE_LEFT_BUTTON = int(settings.__next__())
    MOVE_RIGHT_BUTTON = int(settings.__next__())
    SOFT_DROP_BUTTON = int(settings.__next__())
    ROTATE_LEFT_BUTTON = int(settings.__next__())
    ROTATE_RIGHT_BUTTON = int(settings.__next__())
    HARD_DROP_BUTTON = int(settings.__next__())
    HOLD_BLOCK_BUTTON = int(settings.__next__())

    pygame.mixer.music.set_volume(MUSIC_VOLUME)

    BUTTONS_TO_STRING = {27: 'esc', 1073741882: 'f1', 1073741883: 'f2', 1073741884: 'f3', 1073741885: 'f4',
                         1073741886: 'f5',
                         1073741887: 'f6', 1073741888: 'f7', 1073741889: 'f8', 1073741890: 'f9', 1073741891: 'f10',
                         1073741892: 'f11',
                         1073741893: 'f12', 45: '-', 61: '=', 9: 'tab', 113: 'q', 119: 'w', 101: 'e', 114: 'r',
                         116: 't', 121: 'y',
                         117: 'u', 105: 'i', 111: 'o', 112: 'p', 91: '[', 93: ']', 92: '\\', 97: 'a', 115: 's',
                         100: 'd', 102: 'f',
                         103: 'g', 104: 'h', 106: 'j', 107: 'k', 108: 'l', 59: ';', 39: "'", 122: 'z', 120: 'x',
                         99: 'c', 118: 'v',
                         98: 'b', 110: 'n', 109: 'm', 44: ',', 46: '.', 47: '/', 1073742049: 'shift',
                         1073742048: 'ctrl',
                         1073742050: 'alt', 32: 'space', 1073741906: 'up', 1073741905: 'down', 1073741904: 'left',
                         1073741903: 'right',
                         13: 'enter'}

    def __init__(self):
        self.surface = pygame.surface.Surface((Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 3 * 2))
        self.rect = self.surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 2))
        self.surface.fill((86, 233, 204))
        self.surface.set_alpha(150)
        self.mouseButtonDown = False
        self.title_font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', Constants.WINDOW_SIZE[1] // 10)
        self.text_font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', Constants.WINDOW_SIZE[1] // 30)

        self.settings_title_surface = self.title_font.render('Settings', True, (255, 255, 255))
        self.settings_title_rect = self.settings_title_surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 2,
                                                                                Constants.WINDOW_SIZE[1] // 4 - 10))

        self.music_volume_title_surface = self.text_font.render('Music volume', True, (255, 255, 255))
        self.music_volume_title_rect = self.music_volume_title_surface.get_rect(
            topleft=(Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 10 * 3))

        self.audio_volume_title_surface = self.text_font.render('Audio volume', True, (255, 255, 255))
        self.audio_volume_title_rect = self.audio_volume_title_surface.get_rect(
            bottomleft=(Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 10 * 4))

        self.music_volume_line = AdjustmentLine(Constants.WINDOW_SIZE[0] // 10 * 5,
                                                Constants.WINDOW_SIZE[1] // 20 * 6 + 5,
                                                Constants.WINDOW_SIZE[0] // 10 * 2, 20, self.MUSIC_VOLUME)
        self.audio_volume_line = AdjustmentLine(Constants.WINDOW_SIZE[0] // 10 * 5,
                                                Constants.WINDOW_SIZE[1] // 20 * 7 + 15,
                                                Constants.WINDOW_SIZE[0] // 10 * 2, 20, self.AUDIO_VOLUME)

        self.controls_title_surface = self.title_font.render('Controls', True, (255, 255, 255))
        self.controls_title_rect = self.controls_title_surface.get_rect(
            center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 20 * 9))

        self.move_left_title_surface = self.text_font.render('Move left', True, (255, 255, 255))
        self.move_left_title_rect = self.move_left_title_surface.get_rect(
            topleft=(Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 20 * 10))
        self.move_right_title_surface = self.text_font.render('Move right', True, (255, 255, 255))
        self.move_right_title_rect = self.move_right_title_surface.get_rect(
            topleft=(Constants.WINDOW_SIZE[0] // 10 * 5, Constants.WINDOW_SIZE[1] // 20 * 10))
        self.rotate_left_title_surface = self.text_font.render('Rotate left', True, (255, 255, 255))
        self.rotate_left_title_rect = self.rotate_left_title_surface.get_rect(
            topleft=(Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 20 * 11))
        self.rotate_right_title_surface = self.text_font.render('Rotate right', True, (255, 255, 255))
        self.rotate_right_title_rect = self.rotate_right_title_surface.get_rect(
            topleft=(Constants.WINDOW_SIZE[0] // 10 * 5, Constants.WINDOW_SIZE[1] // 20 * 11))
        self.hard_drop_title_surface = self.text_font.render('Hard drop', True, (255, 255, 255))
        self.hard_drop_title_rect = self.hard_drop_title_surface.get_rect(
            topleft=(Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 20 * 12))
        self.soft_drop_title_surface = self.text_font.render('Soft drop', True, (255, 255, 255))
        self.soft_drop_title_rect = self.soft_drop_title_surface.get_rect(
            topleft=(Constants.WINDOW_SIZE[0] // 10 * 5, Constants.WINDOW_SIZE[1] // 20 * 12))
        self.hold_tetromino_title_surface = self.text_font.render('Hold tetromino', True, (255, 255, 255))
        self.hold_tetromino_title_rect = self.hold_tetromino_title_surface.get_rect(
            topleft=(Constants.WINDOW_SIZE[0] // 10 * 4, Constants.WINDOW_SIZE[1] // 20 * 13))

        self.move_left_button = ControlsKey(self.BUTTONS_TO_STRING[self.MOVE_LEFT_BUTTON],
                                            Constants.WINDOW_SIZE[0] // 10 * 4, Constants.WINDOW_SIZE[1] // 20 * 10,
                                            Constants.WINDOW_SIZE[1] // 20 - 10)
        self.move_right_button = ControlsKey(self.BUTTONS_TO_STRING[self.MOVE_RIGHT_BUTTON],
                                             Constants.WINDOW_SIZE[0] // 10 * 6, Constants.WINDOW_SIZE[1] // 20 * 10,
                                             Constants.WINDOW_SIZE[1] // 20 - 10)
        self.rotate_left_button = ControlsKey(self.BUTTONS_TO_STRING[self.ROTATE_LEFT_BUTTON],
                                              Constants.WINDOW_SIZE[0] // 10 * 4, Constants.WINDOW_SIZE[1] // 20 * 11,
                                              Constants.WINDOW_SIZE[1] // 20 - 10)
        self.rotate_right_button = ControlsKey(self.BUTTONS_TO_STRING[self.ROTATE_RIGHT_BUTTON],
                                               Constants.WINDOW_SIZE[0] // 10 * 6, Constants.WINDOW_SIZE[1] // 20 * 11,
                                               Constants.WINDOW_SIZE[1] // 20 - 10)
        self.hard_drop_button = ControlsKey(self.BUTTONS_TO_STRING[self.HARD_DROP_BUTTON],
                                            Constants.WINDOW_SIZE[0] // 10 * 4, Constants.WINDOW_SIZE[1] // 20 * 12,
                                            Constants.WINDOW_SIZE[1] // 20 - 10)
        self.soft_drop_button = ControlsKey(self.BUTTONS_TO_STRING[self.SOFT_DROP_BUTTON],
                                            Constants.WINDOW_SIZE[0] // 10 * 6, Constants.WINDOW_SIZE[1] // 20 * 12,
                                            Constants.WINDOW_SIZE[1] // 20 - 10)
        self.hold_tetromino_button = ControlsKey(self.BUTTONS_TO_STRING[self.HOLD_BLOCK_BUTTON],
                                                 Constants.WINDOW_SIZE[0] // 20 * 11,
                                                 Constants.WINDOW_SIZE[1] // 20 * 13,
                                                 Constants.WINDOW_SIZE[1] // 20 - 10)

        self.buttons = [self.move_left_button, self.move_right_button, self.rotate_left_button,
                        self.rotate_right_button, self.hard_drop_button, self.soft_drop_button,
                        self.hold_tetromino_button]

        self.button_getter = None
        self.button_selection = False

    def save_settings(self):
        with open('settings', 'w', encoding='utf8') as writer:
            s = f'{self.AUDIO_VOLUME}\n{self.MUSIC_VOLUME}\n{self.MOVE_LEFT_BUTTON}\n{self.MOVE_RIGHT_BUTTON}\n' \
                f'{self.SOFT_DROP_BUTTON}\n{self.ROTATE_LEFT_BUTTON}\n{self.ROTATE_RIGHT_BUTTON}\n' \
                f'{self.HARD_DROP_BUTTON}\n{self.HOLD_BLOCK_BUTTON}'
            writer.write(s)

    def render(self):
        screen.blit(self.surface, self.rect)

        screen.blit(self.settings_title_surface, self.settings_title_rect)
        screen.blit(self.music_volume_title_surface, self.music_volume_title_rect)
        screen.blit(self.audio_volume_title_surface, self.audio_volume_title_rect)

        screen.blit(self.controls_title_surface, self.controls_title_rect)
        screen.blit(self.move_left_title_surface, self.move_left_title_rect)
        screen.blit(self.move_right_title_surface, self.move_right_title_rect)
        screen.blit(self.rotate_left_title_surface, self.rotate_left_title_rect)
        screen.blit(self.rotate_right_title_surface, self.rotate_right_title_rect)
        screen.blit(self.hard_drop_title_surface, self.hard_drop_title_rect)
        screen.blit(self.soft_drop_title_surface, self.soft_drop_title_rect)
        screen.blit(self.hold_tetromino_title_surface, self.hold_tetromino_title_rect)

        for button in self.buttons:
            button.render()

        self.music_volume_line.render()
        self.audio_volume_line.render()

        for button in self.buttons:
            if button.get_button:
                self.button_selection = True
                if self.button_getter is None:
                    button.render_get_button()
                else:
                    if button.button_pressed(self.button_getter):
                        self.button_selection = False
                    self.button_getter = None

    def check_adjustment_lines(self, pos):
        self.music_volume_line.check_click(pos)
        self.audio_volume_line.check_click(pos)
        pygame.mixer.music.set_volume(self.music_volume_line.get_value())
        self.AUDIO_VOLUME = self.audio_volume_line.get_value()
        self.MUSIC_VOLUME = self.music_volume_line.get_value()


class AdjustmentLine:
    def __init__(self, x, y, width, height, default_value, color='white'):
        self.rect = pygame.rect.Rect((x, y), (width, height))
        self.x, self.y, self.width, self.height = x, y, width, height
        self.value = int(default_value * 100)
        self.color = color

        self.line_surface = pygame.surface.Surface((width, height // 4))
        self.line_surface.fill('white')
        self.line_rect = self.line_surface.get_rect(center=(x + width // 2, y + height // 2))

        self.value_per_pixel = width / 100

    def render(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y + self.height // 2), self.height // 4 // 2)
        pygame.draw.circle(screen, self.color, (self.x + self.width, self.y + self.height // 2), self.height // 4 // 2)
        screen.blit(self.line_surface, self.line_rect)
        center = (self.x + int(self.value * self.value_per_pixel), self.y + self.height // 2)
        radius = self.height // 2 - 1
        pygame.draw.circle(screen, self.color, center, radius)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.value = (pos[0] - self.x) // self.value_per_pixel

    def get_value(self):
        return int(self.value) / 100


class ControlsKey:
    surface_empty_key = pygame.image.load('res/keyboard/empty_key.png').convert_alpha()

    def __init__(self, default_key, x, y, height):
        self.key_title = default_key
        self.surface_key = None
        self.x, self.y, self.height = x, y, height
        self.rect = pygame.rect.Rect((x, y), (height, height))
        self.font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', self.height)
        self.title_font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', Constants.WINDOW_SIZE[1] // 10)
        self.transform_button()
        self.get_button = False

    def render(self):
        screen.blit(self.surface_key, self.rect)
        if self.key_title not in ('left', 'right', 'up', 'down'):
            text_surface = self.font.render(self.key_title.upper(), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
            screen.blit(text_surface, text_rect)

    def check_pos(self, pos):
        if self.rect.collidepoint(pos):
            self.get_button = True

    def render_get_button(self):
        surface = pygame.surface.Surface(Constants.WINDOW_SIZE)
        surface.set_alpha(100)
        screen.blit(surface, (0, 0))
        text_surface = self.title_font.render('Press any button to assign', True, (255, 255, 255))
        screen.blit(text_surface,
                    text_surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 2)))

    def button_pressed(self, button):
        if button in settings.BUTTONS_TO_STRING.keys():
            self.get_button = False
            self.key_title = settings.BUTTONS_TO_STRING[button]
            self.transform_button()
            return True
        return False

    def transform_button(self):
        if self.key_title in ('left', 'right', 'up', 'down'):
            self.surface_key = pygame.transform.scale(pygame.image.load(f'res/keyboard/{self.key_title}.png'),
                                                      (self.height, self.height))
        else:
            width = int(self.height * (1.4 ** (len(self.key_title) - 1)))
            self.surface_key = pygame.transform.scale(self.surface_empty_key, (
                width, self.height))
            self.rect = pygame.rect.Rect((self.x, self.y), (
                width, self.height))


class Timer:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        self.time = None

    def start(self, time):
        self.start_time = pygame.time.get_ticks()
        self.time = time

    def is_time(self):
        if self.time is not None:
            if self.start_time + self.time < pygame.time.get_ticks():
                return True
        return False

    def stop(self):
        self.time = None


class SoundGraphicPack:
    def __init__(self, name):
        self.name = name
        self.I, self.J, self.L, self.O, self.S, self.T, self.Z = None, None, None, None, None, None, None
        self.singleI, self.singleJ, self.singleL, self.singleO = None, None, None, None
        self.singleS, self.singleT, self.singleZ = None, None, None

        self.main_theme, self.main_theme_2, self.main_theme_3 = None, None, None
        self.load()

    def load(self):
        self.I = pygame.image.load(f'res/{self.name}/blocks/I.png').convert_alpha()
        self.J = pygame.image.load(f'res/{self.name}/blocks/J.png').convert_alpha()
        self.L = pygame.image.load(f'res/{self.name}/blocks/L.png').convert_alpha()
        self.O = pygame.image.load(f'res/{self.name}/blocks/O.png').convert_alpha()
        self.S = pygame.image.load(f'res/{self.name}/blocks/S.png').convert_alpha()
        self.T = pygame.image.load(f'res/{self.name}/blocks/T.png').convert_alpha()
        self.Z = pygame.image.load(f'res/{self.name}/blocks/Z.png').convert_alpha()

        self.singleI = pygame.image.load(f'res/{self.name}/single/singleI.png').convert_alpha()
        self.singleJ = pygame.image.load(f'res/{self.name}/single/singleJ.png').convert_alpha()
        self.singleL = pygame.image.load(f'res/{self.name}/single/singleL.png').convert_alpha()
        self.singleO = pygame.image.load(f'res/{self.name}/single/singleO.png').convert_alpha()
        self.singleS = pygame.image.load(f'res/{self.name}/single/singleS.png').convert_alpha()
        self.singleT = pygame.image.load(f'res/{self.name}/single/singleT.png').convert_alpha()
        self.singleZ = pygame.image.load(f'res/{self.name}/single/singleZ.png').convert_alpha()

        self.main_theme = f'music/{self.name}/main_theme.ogg'
        self.main_theme_2 = f'music/{self.name}/main_theme_2.ogg'
        self.main_theme_3 = f'music/{self.name}/main_theme_3.ogg'


class Database:
    def __init__(self, db, userr, password, host):
        self.database = mysql.connector.connect(
            host=host,
            user=userr,
            passwd=password,
            database=db
        )
        self.cursor = self.database.cursor()

    def login(self, email, password):
        self.cursor.execute('SELECT password FROM Users WHERE email = %s', (email,))
        resp = list(self.cursor)
        if len(resp) == 0:
            return False
        else:
            if password == Constants.FERNET.decrypt(resp[0][0].encode()).decode():
                self.cursor.execute('SELECT name FROM Users WHERE email = %s', (email,))
                resp = list(self.cursor)
                return resp[0][0]
            else:
                return False

    def register(self, name, email, password):
        try:
            password = Constants.FERNET.encrypt(password.encode())
        except fernet.InvalidToken:
            return False
        if not self.is_username_taken(name) and not self.is_email_taken(email):
            self.execute('INSERT INTO Users (name, email, password, coins) VALUES (%s, %s, %s, 0)',
                         (name, email, password))
            self.execute('INSERT INTO Stats (name) VALUES (%s)', (name,))
            return True
        return False

    def is_username_taken(self, name):
        self.cursor.execute('SELECT * FROM Users WHERE name = %s', (name,))
        return bool(len(list(self.cursor)))

    def is_email_taken(self, email):
        self.cursor.execute('SELECT * FROM Users WHERE email = %s', (email,))
        return bool(len(list(self.cursor)))

    def execute(self, *args):
        self.cursor.execute(*args)
        self.database.commit()

    def get_stats(self, name):
        self.cursor.execute('SELECT * FROM Stats WHERE name = %s', (name,))
        d = dict()
        resp = iter(list(self.cursor)[0][1::])
        d['games_played'] = next(resp)
        d['blocks_dropped'] = next(resp)
        d['best_score'] = next(resp)
        d['playtime'] = next(resp)
        d['rang'] = next(resp)
        d['wins'] = next(resp)
        d['loses'] = next(resp)
        d['experience'] = next(resp)
        d['tetrises'] = next(resp)
        d['world_record_time'] = next(resp)
        return d

    def set_experience(self, name, experience):
        self.execute('UPDATE Stats SET experience = %s WHERE name = %s', (experience, name))

    def set_score(self, name, score):
        self.execute('UPDATE Stats SET best_score = %s WHERE name = %s', (score, name))

    def set_games(self, name, games):
        self.execute('UPDATE Stats SET games_played = %s WHERE name = %s', (games, name))

    def set_playtime(self, name, playtime):
        self.execute('UPDATE Stats SET playtime = %s WHERE name = %s', (playtime, name))

    def set_rang(self, name, rang):
        self.execute('UPDATE Stats SET rang = %s WHERE name = %s', (rang, name))

    def set_wins(self, name, wins):
        self.execute('UPDATE Stats SET wins = %s WHERE name = %s', (wins, name))

    def set_loses(self, name, loses):
        self.execute('UPDATE Stats SET loses = %s WHERE name = %s', (loses, name))

    def set_blocks_dropped(self, name, blocks):
        self.execute('UPDATE Stats SET blocks_dropped = %s WHERE name = %s', (blocks, name))

    def set_tetrises(self, name, tetrises):
        self.execute('UPDATE Stats SET tetrises = %s WHERE name = %s', (tetrises, name))

    def set_world_record_time(self, name, time):
        self.execute('UPDATE Stats SET world_record_time = %s WHERE name = %s', (time, name))

    def add_game(self, score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles, triples,
                 tetrises, gametype, players, result):
        self.execute('INSERT INTO Games (score, lines_cleared, time_played, blocks_placed, max_combo, tspins, '
                     'singles, doubles, triples, tetrises, gametype, players, '
                     'result) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                     (score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles,
                      triples, tetrises, gametype, players, result))


class User:
    def __init__(self, name, db):
        self.name = name
        self.stats = database.get_stats(name)
        self.db = db

    def update(self):
        self.stats = self.db.get_stats(self.name)

    def add_world_record_game(self, score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles,
                              doubles, triples, tetrises):
        self.db.add_game(score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles,
                         triples, tetrises, Constants.WORLDRECORD, self.name, Constants.NEUTRAL)

    def add_marathon_game(self, score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles,
                          triples, tetrises):
        self.db.add_game(score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles,
                         triples, tetrises, Constants.MARATHON, self.name, Constants.NEUTRAL)

    def add_experience(self, experience):
        self.db.set_experince(self.name, self.stats['experience'] + experience)
        self.update()

    def add_game(self, games=1):
        self.db.set_games(self.name, self.stats['games_played'] + games)
        self.update()

    def add_score(self, score):
        if self.stats['best_score'] < score:
            self.db.set_score(self.name, score)
        self.update()

    def add_blocks_dropped(self, blocks):
        self.db.set_blocks_dropped(self.name, self.stats['blocks_dropped'] + blocks)
        self.update()

    def add_playtime(self, time):
        self.db.set_playtime(self.name, self.stats['playtime'] + time)
        self.update()

    def rang_promote(self):
        self.db.set_rang(self.name, self.stats['rang'] + 1)
        self.update()

    def rang_demote(self):
        self.db.set_range(self.name, self.stats['rang'] - 1)
        self.update()

    def set_rang(self, rang):
        self.db.set_rang(self.name, rang)
        self.update()

    def add_win(self, wins=1):
        self.db.set_wins(self.name, self.stats['wins'] + wins)
        self.update()

    def add_lose(self, loses=1):
        self.db.set_loses(self.name, self.stats['loses'] + loses)
        self.update()

    def add_tetrises(self, tetrises):
        self.db.set_tetrises(self.name, self.stats['tetrises'] + tetrises)
        self.update()

    def add_world_record_time(self, time):
        if self.stats['world_record_time'] > time or self.stats['world_record_time'] is None:
            self.db.set_world_record_time(self.name, time)
        self.update()

    def get_stats(self):
        return self.stats


class AuthorisationWindow:
    audio_click = MainMenu.audio_click
    audio_alert = pygame.mixer.Sound('audio/alert.wav')

    AUTHORISATION, ANIMATION_TO_DOT, ANIMATION_FROM_DOT, CONNECTION = 0, 1, 2, 3

    def __init__(self, db: Database):
        self.database = db
        self.size = [Constants.WINDOW_SIZE[0] // 10 * 4, Constants.WINDOW_SIZE[1] // 10 * 4]
        self.frame = pygame.Surface(self.size)
        self.rect = pygame.rect.Rect((Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 10 * 4),
                                     self.size)
        self.center = self.rect.center
        self.alpha = 100
        self.frame.set_alpha(self.alpha)
        self.color = (86, 233, 204)
        self.frame.fill(self.color)
        self.log_in_title_surface = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf',
                                                     Constants.WINDOW_SIZE[1] // 25).render(
            'Log in using Tetris Extra account', True, (255, 255, 255))
        self.log_in_title_rect = self.log_in_title_surface.get_rect(midtop=(Constants.WINDOW_SIZE[0] // 2,
                                                                            Constants.WINDOW_SIZE[1] // 40 * 17))
        self.email_input = LineEdit(Constants.WINDOW_SIZE[0] // 20 * 7,
                                    Constants.WINDOW_SIZE[1] // 10 * 5,
                                    Constants.WINDOW_SIZE[0] // 20 * 6,
                                    Constants.WINDOW_SIZE[1] // 20,
                                    'E-mail', (102, 204, 204), 200, self, False)
        self.password_input = LineEdit(Constants.WINDOW_SIZE[0] // 20 * 7,
                                       Constants.WINDOW_SIZE[1] // 10 * 6,
                                       Constants.WINDOW_SIZE[0] // 20 * 6,
                                       Constants.WINDOW_SIZE[1] // 20,
                                       'Password', (102, 204, 204), 200, self, True)
        self.continue_button = Button(self.on_click, Constants.WINDOW_SIZE[0] // 10 * 4,
                                      Constants.WINDOW_SIZE[1] // 10 * 7, Constants.WINDOW_SIZE[0] // 10 * 2,
                                      Constants.WINDOW_SIZE[1] // 10 // 2, 'Continue', (102, 204, 204))

        try:
            with open('account', 'rb') as reader:
                file = Constants.FERNET.decrypt(reader.read()).decode()
            self.email_input.input_text, self.password_input.input_text = file.split()
        except FileNotFoundError:
            pass
        except fernet.InvalidToken:
            pass

        self.selected_input = None
        self.keys = list()

        self.status = self.AUTHORISATION

        self.speed = 20

        self.error_font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', Constants.WINDOW_SIZE[1] // 40)
        self.wrong_credentials_surface = self.error_font.render('', True, (255, 0, 0))
        self.wrong_credentials_rect = self.wrong_credentials_surface.get_rect(midtop=self.log_in_title_rect.midbottom)

    def on_click(self):
        self.audio_click.play()
        self.status = self.ANIMATION_TO_DOT

    def render(self):
        screen.blit(StartScreen.surface_tetris_logo, StartScreen.rect_tetris_logo)
        screen.blit(self.frame, self.rect)
        if self.status == self.AUTHORISATION:
            self.render_authorisation()
        elif self.status == self.ANIMATION_TO_DOT:
            self.render_animation_to_dot()
        elif self.status == self.CONNECTION:
            res = self.database.login(self.email_input.get_text(), self.password_input.get_text())
            if not res:
                self.status = self.ANIMATION_FROM_DOT
                self.audio_alert.play()
                return
            with open('account', 'wb') as writer:
                writer.write(
                    Constants.FERNET.encrypt(
                        (self.email_input.get_text() + ' ' + self.password_input.get_text()).encode()))
            return User(r, self.database)
        elif self.status == self.ANIMATION_FROM_DOT:
            self.render_animation_from_dot()
        return False

    def render_animation_to_dot(self):
        if self.size[0] == 0 and self.size[1] == 0:
            self.status = self.CONNECTION
        for i in range(2):
            if self.size[i] > 0:
                self.size[i] -= self.speed
                if self.size[i] < 0:
                    self.size[i] = 0

        self.frame = pygame.Surface(self.size)
        self.frame.fill(self.color)
        self.frame.set_alpha(self.alpha)
        self.rect = self.frame.get_rect(center=self.center)
        pygame.draw.rect(screen, 'white', self.rect, 1)

    def render_animation_from_dot(self):
        if self.size[0] == Constants.WINDOW_SIZE[0] // 10 * 4 and self.size[1] == Constants.WINDOW_SIZE[1] // 10 * 4:
            self.status = self.AUTHORISATION
            self.wrong_credentials_surface = self.error_font.render('Wrong email or password', True, (255, 0, 0))
            self.wrong_credentials_rect = self.wrong_credentials_surface.get_rect(
                midtop=self.log_in_title_rect.midbottom)
        for i in range(2):
            if self.size[i] < Constants.WINDOW_SIZE[i] // 10 * 4:
                self.size[i] += self.speed
                if self.size[i] > Constants.WINDOW_SIZE[i] // 10 * 4:
                    self.size[i] = Constants.WINDOW_SIZE[i] // 10 * 4

        self.frame = pygame.Surface(self.size)
        self.frame.fill(self.color)
        self.frame.set_alpha(self.alpha)
        self.rect = self.frame.get_rect(center=self.center)
        pygame.draw.rect(screen, 'white', self.rect, 1)

    def render_authorisation(self):
        screen.blit(self.log_in_title_surface, self.log_in_title_rect)
        screen.blit(self.wrong_credentials_surface, self.wrong_credentials_rect)
        pygame.draw.rect(screen, 'white', self.rect, 1)
        self.email_input.render()
        self.password_input.render()
        self.continue_button.render()


class LineEdit:
    BUTTONS_TO_STRING = {113: 'q', 119: 'w', 101: 'e', 114: 'r', 116: 't', 121: 'y', 117: 'u', 105: 'i', 111: 'o',
                         112: 'p', 97: 'a', 115: 's', 100: 'd', 102: 'f', 103: 'g', 104: 'h', 106: 'j', 107: 'k',
                         108: 'l', 122: 'z', 120: 'x', 99: 'c', 118: 'v', 98: 'b', 110: 'n',
                         109: 'm', 46: '.', 48: '0', 45: '-', 49: '1', 50: '2', 51: '3', 52: '4',
                         53: '5', 54: '6', 55: '7', 56: '8', 57: '9'}

    PLACEHOLDER, HOVER, SELECTED, IDLE = 0, 1, 2, 3

    def __init__(self, x, y, width, height, placeholder, color, alpha, window, hidden):
        self.hidden = hidden
        self.window = window
        self.x, self.y, self.width, self.height = x, y, width, height
        self.rect = pygame.rect.Rect((x, y), (width, height))
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)
        self.surface.set_alpha(alpha)
        self.placeholder = placeholder
        self.color = color
        self.alpha = alpha
        self.font = pygame.font.Font('fonts/Nunito-Light.ttf', int(self.height / 10 * 7))
        self.status = self.IDLE
        self.input_text = ''

    def get_text(self):
        return self.input_text

    def render(self):
        screen.blit(self.surface, self.rect)
        self.check_hover(pygame.mouse.get_pos())
        if True in pygame.mouse.get_pressed(3):
            self.check_click(pygame.mouse.get_pos())
        if self.status == self.SELECTED and self.window.selected_input != hash(self):
            self.status = self.IDLE
        if self.status == self.HOVER:
            self.render_hover()
        elif self.status == self.SELECTED:
            self.render_selected()
        elif self.status == self.IDLE:
            self.render_idle()

    def render_hover(self):
        self.render_idle()
        white_surface = pygame.Surface((self.width, self.height))
        white_surface.fill('white')
        white_surface.set_alpha(50)
        screen.blit(white_surface, self.rect)

    def check_input(self, k):
        if len(self.get_text()) < Constants.MAIL_SYMBOL_LIMIT:
            temp_text = ''
            for i in k:
                if i in self.BUTTONS_TO_STRING:
                    temp_text += self.BUTTONS_TO_STRING[i]
            if pygame.key.get_pressed()[1073742049]:
                temp_text = temp_text.upper().replace('2', '@')
            self.input_text += temp_text
        if pygame.K_BACKSPACE in k:
            self.input_text = self.input_text[:-1]

    def render_selected(self):
        self.check_input(self.window.keys)
        text = self.input_text if not self.hidden else len(self.input_text) * '*'
        text_surface = self.font.render(text if pygame.time.get_ticks() // 1000 % 2 == 0 else text + '|',
                                        True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, 'white', self.rect, 1)

    def render_idle(self):
        placeholder = len(self.input_text) == 0
        text = self.placeholder if placeholder else (self.input_text if not self.hidden else len(self.input_text) * "*")
        text_surface = self.font.render(text, True, (211, 211, 211) if placeholder else 'white')
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.status = self.SELECTED
            self.window.selected_input = hash(self)
        else:
            self.status = self.IDLE

    def check_hover(self, pos):
        if self.rect.collidepoint(pos) and self.status in (self.IDLE, self.HOVER):
            self.status = self.HOVER
        elif self.status == self.HOVER:
            self.status = self.IDLE

    def __hash__(self):
        return self.x * self.y - self.x - self.y


class Button:
    IDLE, HOVER, PRESSED, RELEASED = 0, 1, 2, 3

    def __init__(self, on_click, x, y, width, height, text, color, text_color=(255, 255, 255), font_size=None):
        self.on_click = on_click
        if font_size is None:
            font_size = int(height / 10 * 7)
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)
        self.rect = pygame.rect.Rect((x, y), (width, height))
        font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', font_size)
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.status = self.IDLE

        self.white_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.white_surface.fill('white')
        self.white_surface.set_alpha(100)

        self.black_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.black_surface.set_alpha(100)

    def render(self):
        if self.status == self.RELEASED:
            self.on_click()

        self.check_pos()

        screen.blit(self.surface, self.rect)
        screen.blit(self.text_surface, self.text_rect)

        if self.status == self.HOVER:
            screen.blit(self.white_surface, self.rect)
        elif self.status == self.PRESSED:
            screen.blit(self.black_surface, self.rect)

    def check_pos(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if True in pygame.mouse.get_pressed(3):
                self.status = self.PRESSED
                return
            elif self.status == self.PRESSED:
                self.status = self.RELEASED
                return
            self.status = self.HOVER
            return
        self.status = self.IDLE


class ProfileView:
    def __init__(self, u: User):
        self.stats = u.get_stats()

    def render(self):
        pass


class GameModeSelection:
    pass


def terminate():
    pygame.quit()
    sys.exit()


FALL_BLOCK_EVENT = pygame.event.custom_type()

connecting_to_db = True
while connecting_to_db:
    try:
        database = Database(db=Constants.Database.DATABASE,
                            userr=Constants.Database.USER,
                            password=Constants.Database.PASSWORD,
                            host=Constants.Database.HOST)
    except mysql.connector.errors.DatabaseError as e:
        print(e)
    else:
        connecting_to_db = False

background = Background()
start_screen = StartScreen()
program_state = Constants.START_SCREEN
level_selection, game, menu, gameover, settings, authorisation, user = None, None, None, None, Settings(), None, None
game_mode_selection = None
particles = pygame.sprite.Group()
pack = SoundGraphicPack(Constants.PACK_DEFAULT)

pygame.mixer.music.load(Constants.MUSIC_MAIN_MENU)
pygame.mixer.music.play(-1)

while True:
    background.render()
    if program_state == Constants.START_SCREEN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    program_state = Constants.AUTHORISATION

        screen.blit(StartScreen.surface_tetris_logo, StartScreen.rect_tetris_logo)
        screen.blit(start_screen.get_surface_text(), StartScreen.rect_text)

    elif program_state == Constants.AUTHORISATION:
        if authorisation is None:
            authorisation = AuthorisationWindow(database)
        keys = list()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP:
                keys.append(event.key)
        authorisation.keys = keys.copy()

        r = authorisation.render()
        if r:
            user = r
            program_state = Constants.MAIN_MENU

    elif program_state == Constants.MAIN_MENU:
        if menu is None:
            menu = MainMenu(user)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menu.button_down()
                elif event.key == pygame.K_UP:
                    menu.button_up()
                elif event.key == 13:
                    response = menu.button_select()
                    program_state = response if response is not None else Constants.MAIN_MENU
            elif event.type == pygame.MOUSEMOTION:
                menu.get_covered(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                response = menu.get_clicked(event.pos)
                if response is not None:
                    menu.audio_click.set_volume(settings.AUDIO_VOLUME)
                    menu.audio_click.play()
                    program_state = response if response is not None else Constants.MAIN_MENU

        menu.render()

    elif program_state == Constants.GAME_MODE_SELECTION:
        if game_mode_selection is None:
            game_mode_selection = GameModeSelection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

    elif program_state == Constants.LEVEL_SELECT:
        if level_selection is None:
            level_selection = LevelSelection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level_selection.check_pos(event.pos):
                    # game = Marathon(level_selection.get_selected_level())
                    game = WorldRecord()
                    program_state = Constants.INGAME
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    program_state = Constants.MAIN_MENU

        level_selection.render()

    elif program_state == Constants.INGAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == Settings.MOVE_LEFT_BUTTON:
                    game.current_block.move_left = True
                elif event.key == Settings.MOVE_RIGHT_BUTTON:
                    game.current_block.move_right = True
                elif event.key == Settings.ROTATE_LEFT_BUTTON:
                    game.current_block.block.rotate()
                elif event.key == Settings.HARD_DROP_BUTTON:
                    hard_drop_particle = HardDropParticle(*game.current_block.block.hard_drop(True))
                elif event.key == Settings.SOFT_DROP_BUTTON:
                    game.current_block.move_down = True
                elif event.key == Settings.HOLD_BLOCK_BUTTON and game.may_hold():
                    game.block_queue.hold()
            elif event.type == pygame.KEYUP:
                try:
                    if event.key == Settings.MOVE_LEFT_BUTTON:
                        game.current_block.move_left = False
                    elif event.key == Settings.MOVE_RIGHT_BUTTON:
                        game.current_block.move_right = False
                    elif event.key == Settings.SOFT_DROP_BUTTON:
                        game.current_block.move_down = False
                except AttributeError:
                    print(2)
            elif event.type == FALL_BLOCK_EVENT and not game.gameover:
                try:
                    game.current_block.block.fall()
                except AttributeError:
                    print(3)

        if game.is_countdown():
            game.countdown()
        else:
            if not game.gameover:
                game.render_and_update()
                if game.BLOCK_ANCHOR.is_time():
                    if game.current_block.block.timer_set:
                        game.current_block.block.hard_drop(False)
            else:
                gameover = EndGameScreen()
                program_state = Constants.ENDSCREEN

    elif program_state == Constants.ENDSCREEN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        gameover.render()

    elif program_state == Constants.SETTINGS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if settings.button_selection:
                if event.type == pygame.KEYDOWN:
                    settings.button_getter = event.key
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        settings.save_settings()
                        program_state = Constants.MAIN_MENU
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu.audio_click.set_volume(settings.AUDIO_VOLUME)
                    menu.audio_click.play()
                    settings.mouseButtonDown = True
                    settings.check_adjustment_lines(event.pos)
                    for btn in settings.buttons:
                        btn.check_pos(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    settings.mouseButtonDown = False
                elif settings.mouseButtonDown and event.type == pygame.MOUSEMOTION:
                    settings.check_adjustment_lines(event.pos)

        settings.render()

    elif program_state == -1:
        terminate()

    clock.tick(Constants.FPS)
    pygame.display.update()
