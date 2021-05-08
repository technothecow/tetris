import hashlib
import random
import sys
import pygame
import mysql.connector
from cryptography import fernet
import math
import os
import itertools


class Constants:
    class Database:
        HOST = 'yvu4xahse0smimsc.chr7pe7iynqr.eu-west-1.rds.amazonaws.com'
        USER = 'lax9a7361e4vfouq'
        PASSWORD = 'jsojpq85v0bnu450'
        DATABASE = 'u96vdo4x19syc3cv'

    class Errors:
        WRONG_FERNET_TOKEN, USERNAME_TAKEN = 0, 1

    class Events:
        TSPIN = 0

    I, J, L, O, S, T, Z, GARBAGE = 1, 2, 3, 4, 5, 6, 7, 8
    MAIN_MENU, SETTINGS, START_SCREEN, SHOP, PAUSE, INGAME, LEVEL_SELECT, PROFILE = 1, 2, 3, 4, 5, 6, 7, 8
    ENDSCREEN, AUTHORISATION, GAME_MODE_SELECTION = 9, 10, 11
    SIDE_LENGTH = 32
    HD = (1280, 720)
    FULL_HD = (1920, 1080)
    MY_SCREEN = (1300, 700)
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

    MUSIC_MAIN_MENU = 'music/menu_theme.ogg'

    PACK_DEFAULT = 'default'

    MARATHON, WORLD_RECORD, TRAINING, ONLINE = 0, 1, 2, 3
    WIN, LOSE, NEUTRAL = 0, 1, 2

    KEY = b'3P8EAvmBQTK9Oz_WQdpMlzGB9agTwxmNOp7IdDJCm08='
    FERNET = fernet.Fernet(KEY)


pygame.mixer.pre_init()
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(Constants.WINDOW_SIZE)
tribute = pygame.image.load('res/ErRPQA4VcAAwn5E.jpg')
tribute = pygame.transform.scale(tribute, (Constants.WINDOW_SIZE[0], Constants.WINDOW_SIZE[0]))
screen.blit(tribute, (0, 0))
pygame.display.update()


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

        self.sprite_single_garbage = pygame.sprite.Sprite()
        self.sprite_single_garbage.image = pygame.surface.Surface((Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))
        self.sprite_single_garbage.image.fill((128, 128, 128))

        self.board = list()
        self.init_board()
        self.side_length = side_length
        self.topleft_x, self.topleft_y = topleft
        self.bottomleft_y = self.topleft_y + side_length * (Constants.BOARD_SIZE[1] - 1)

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
                                     (self.topleft_x + self.side_length * j,
                                      self.bottomleft_y - self.side_length * i,
                                      self.side_length, self.side_length), 1)
                else:
                    screen.blit(self.get_block(self.board[i][j]),
                                (self.topleft_x + self.side_length * j, self.bottomleft_y - self.side_length * i))

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
        elif i == Constants.GARBAGE:
            return self.sprite_single_garbage.image

    def check_collision(self, tiles):
        try:
            for tile in tiles:
                if self.board[tile[1]][tile[0]] != 0 or tile[0] < 0 or tile[1] < 0:
                    return False
            return True
        except IndexError:
            return False

    def anchor_block(self, tiles, piece_type):
        game.blocks += 1
        for tile in tiles:
            self.board[tile[1]][tile[0]] = piece_type
        if not self.check_lines():
            game.is_combo = False
            game.combo = 0

    def check_lines(self):
        # calculating lines to delete
        lines = list()
        garbage_lines = list()
        for i in range(len(self.board)):
            if 0 not in self.board[i]:
                if Constants.GARBAGE in self.board[i]:
                    garbage_lines.append(i)
                else:
                    lines.append(i)
        total_lines = lines.copy() + garbage_lines.copy()

        # audio effects for clearance
        if len(total_lines) == 0:
            return False
        elif len(total_lines) == 1:
            self.audio_single.set_volume(settings.AUDIO_VOLUME)
            self.audio_single.play()
            game.singles += 1
        elif len(total_lines) == 2:
            self.audio_double.set_volume(settings.AUDIO_VOLUME)
            self.audio_double.play()
            game.doubles += 1
        elif len(total_lines) == 3:
            self.audio_triple.set_volume(settings.AUDIO_VOLUME)
            self.audio_triple.play()
            game.triples += 1
        elif len(total_lines) == 4:
            self.audio_tetris.set_volume(settings.AUDIO_VOLUME)
            self.audio_tetris.play()
            game.tetrises += 1

        # deleting lines from board itself
        self.destroy_lines(total_lines)

        # adding lines to stats
        game.add_cleared_lines(len(lines))
        game.add_garbage_lines(len(garbage_lines))

        # counting score

        # for combo
        game.is_combo = True
        game.combo += 1
        print('[GAME] Combo counter:', game.combo)
        game.add_score((game.combo - 1) * game.current_level + 50 * game.current_level)

        # for t-spins
        if game.current_block.block.type == Constants.T and Constants.Events.TSPIN in game.current_block.block.events:
            if len(lines) == 1:
                print('TSPIN SINGLE')
                game.add_score(800 * game.current_level)
                if game.back_to_back_counter > 0:
                    game.add_score(400 * game.current_level)
            elif len(lines) == 2:
                print('TSPIN DOUBLE')
                game.add_score(1200 * game.current_level)
                if game.back_to_back_counter > 0:
                    game.add_score(600 * game.current_level)
            elif len(lines) == 3:
                print('TSPIN TRIPLE')
                game.add_score(1600 * game.current_level)
                if game.back_to_back_counter > 0:
                    game.add_score(800 * game.current_level)
            game.back_to_back_counter += 1
            return True

        # for tetris
        if len(lines) == 4:
            if game.back_to_back_counter > 0:
                game.add_score(400 * game.current_level)
            game.add_score(800 * game.current_level)
            game.back_to_back_counter += 1
            return True

        # for other
        if len(lines) == 1:
            game.add_score(100 * game.current_level)
        elif len(lines) == 2:
            game.add_score(300 * game.current_level)
        elif len(lines) == 3:
            game.add_score(500 * game.current_level)

        game.back_to_back_counter = 0
        return True

    def add_garbage_line(self, empty_slot):
        garbage_line = [0 if i == empty_slot else Constants.GARBAGE for i in range(Constants.BOARD_SIZE[0])].copy()
        for i in range(Constants.BOARD_SIZE[1] - 1, 0, -1):
            self.board[i] = self.board[i - 1].copy()
        self.board[0] = garbage_line.copy()

    def destroy_lines(self, lines):
        lines.reverse()
        for line in lines:
            for i in range(line, Constants.BOARD_SIZE[1] - 1):
                self.board[i] = self.board[i + 1].copy()

    def check_lose(self):
        if len(set(self.board[-1])) != 1:
            game.gameover = True


class Block:
    audio_move = pygame.mixer.Sound('audio/move.wav')
    audio_rotate = pygame.mixer.Sound('audio/rotate.wav')
    audio_hard_drop = pygame.mixer.Sound('audio/hard_drop.wav')
    audio_soft_drop = pygame.mixer.Sound('audio/soft_drop.wav')
    audio_wall_kick = pygame.mixer.Sound('audio/wall_kick.wav')
    audio_lock = pygame.mixer.Sound('audio/lock.wav')
    audio_tspin = pygame.mixer.Sound('audio/tspin.wav')

    def __init__(self):
        self.audio_move.set_volume(settings.AUDIO_VOLUME)
        self.audio_rotate.set_volume(settings.AUDIO_VOLUME)
        self.audio_hard_drop.set_volume(settings.AUDIO_VOLUME)
        self.audio_soft_drop.set_volume(settings.AUDIO_VOLUME)
        self.audio_wall_kick.set_volume(settings.AUDIO_VOLUME)
        self.audio_lock.set_volume(settings.AUDIO_VOLUME)

        self.rotation_index = 0

        self.offset_data = (
            ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
            ((0, 0), (1, 0), (1, -1), (0, 2), (+1, 2)),
            ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
            ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)),
        )

        self.tiles, self.type, self.center_index, self.sprite = None, None, None, None

        self.events = set()

        self.touched_the_ground = False
        self.lock_timer = Timer()
        self.moves_left = None

    def draw(self):
        self.draw_tiles(self.tiles, self.sprite)

        ghost_sprite = self.sprite.copy()
        ghost_sprite.set_alpha(50)

        ghost_tiles = self.get_tiles_copy(self.tiles)
        while True:
            if game.board.check_collision(ghost_tiles):
                ghost_tiles = self.move_tiles_vertically(ghost_tiles, -1)
            else:
                ghost_tiles = self.move_tiles_vertically(ghost_tiles, 1)
                break

        self.draw_tiles(ghost_tiles, ghost_sprite)

    @staticmethod
    def get_tiles_copy(tiles):
        return [i.copy() for i in tiles.copy()].copy()

    @staticmethod
    def draw_tiles(tiles, sprite):
        for tile in tiles:
            screen.blit(sprite, (
                Constants.BOARD_TOPLEFT[0] + Constants.SIDE_LENGTH * tile[0],
                Constants.BOARD_TOPLEFT[1] + Constants.SIDE_LENGTH * (Constants.BOARD_SIZE[1] - tile[1] - 1)))

    @staticmethod
    def move_tiles_vertically(tiles, value) -> list:
        result = tiles.copy()
        for tile in tiles:
            tile[1] += value
        return result.copy()

    @staticmethod
    def move_tiles_horizontally(tiles, value) -> list:
        result = tiles.copy()
        for tile in tiles:
            tile[0] += value
        return result.copy()

    def move_tiles(self, direction: int):
        if self.moves_left is not None and self.moves_left > 0:
            self.moves_left -= 1
            game.BLOCK_ANCHOR.start(500)
        moved_tiles = self.move_tiles_horizontally(self.get_tiles_copy(self.tiles), direction)
        if game.board.check_collision(moved_tiles):
            self.tiles = moved_tiles.copy()
            self.audio_move.play()

    def move_right(self):
        self.move_tiles(1)

    def move_left(self):
        self.move_tiles(-1)

    def rotate(self, matrix, value):
        # checking if there are enough moves left
        if self.moves_left is not None and self.moves_left > 0:
            self.moves_left -= 1
            game.BLOCK_ANCHOR.start(500)
        # removing t-spin if it was before
        if self.type == Constants.T:
            self.events.discard(Constants.Events.TSPIN)
        # subtraction from all the tiles value of central one
        tiles = self.centralize_tiles(self.tiles, self.center_index)
        # rotation of all tiles
        rotated_tiles = list()
        for tile in tiles:
            rotated_tiles.append(self.dot_product(matrix, tile))
        # returning the origin positions to tiles
        rotated_tiles = self.uncentralize_tiles(rotated_tiles, self.tiles[self.center_index])
        # wall-kick checking
        result = self.check_offsets(rotated_tiles, (self.rotation_index + value) % 4)
        if result:
            self.rotation_index = (self.rotation_index + value) % 4
            self.tiles = result

    @staticmethod
    def centralize_tiles(tiles, center):
        result = list()
        for i in range(len(tiles)):
            result.append([tiles[i][0] - tiles[center][0], tiles[i][1] - tiles[center][1]].copy())
        return result

    @staticmethod
    def uncentralize_tiles(tiles, center_value):
        return [[i[0] + center_value[0], i[1] + center_value[1]] for i in tiles].copy()

    def check_offsets(self, tiles, new_rotation_index):
        for i in range(len(self.offset_data[self.rotation_index])):
            old_offset = self.offset_data[self.rotation_index][i]
            new_offset = self.offset_data[new_rotation_index][i]
            offset = (old_offset[0] - new_offset[0], old_offset[1] - new_offset[1])
            offset_tiles = [[tile[0] + offset[0], tile[1] + offset[1]].copy() for tile in tiles].copy()
            if game.board.check_collision(offset_tiles):
                # Complicated T-SPIN check
                if self.type == Constants.T:
                    cube_under_left = (offset_tiles[1][0], offset_tiles[1][1] - 1)
                    cube_under_right = (offset_tiles[2][0], offset_tiles[2][1] - 1)
                    cube_over_left = (offset_tiles[1][0], offset_tiles[1][1] + 1)
                    cube_over_right = (offset_tiles[2][0], offset_tiles[2][1] + 1)
                    if (not game.board.check_collision((cube_under_left,)) and \
                        not game.board.check_collision((cube_under_right,)) \
                        and (not game.board.check_collision((cube_over_left,)) or
                             not game.board.check_collision((cube_over_right,))) and self.rotation_index in (1, 3)) \
                            or offset in ((-1, -2), (1, -2)) and self.rotation_index == 0:
                        self.events.add(Constants.Events.TSPIN)
                self.audio_rotate.play()
                return offset_tiles
        return False

    def rotate_left(self):
        self.rotate([[0, -1], [1, 0]], -1)

    def rotate_right(self):
        self.rotate([[0, 1], [-1, 0]], 1)

    def rotate_clockwise(self):
        pass

    @staticmethod
    def dot_product(l1, l2):
        result = list()
        for line in l1:
            result.append(sum([line[index] * l2[index] for index in range(len(line))]))
        return result.copy()

    def anchor(self):
        game.board.anchor_block(self.tiles, self.type)
        game.next_block()

    def fall(self):
        if game.board.check_collision(self.move_tiles_vertically(self.get_tiles_copy(self.tiles), -1)):
            self.tiles = self.move_tiles_vertically(self.tiles, -1)
        elif not self.touched_the_ground:
            self.touched_the_ground = True
            game.BLOCK_ANCHOR.start(500)
            self.moves_left = 15

    def hard_drop(self, is_lock: bool = True):
        while game.board.check_collision(self.move_tiles_vertically(self.get_tiles_copy(self.tiles), -1)):
            self.tiles = self.move_tiles_vertically(self.tiles, -1)
        self.anchor()
        if is_lock:
            self.audio_hard_drop.play()
        else:
            self.audio_lock.play()
        return self.get_rect_for_hard_drop_particle()

    def get_rect_for_hard_drop_particle(self):
        x, y = {tile[0] for tile in self.tiles}, {tile[1] for tile in self.tiles}
        return pygame.Rect((game.board.topleft_x + game.board.side_length * min(x),
                            game.board.topleft_y), (game.board.side_length * (max(x) - min(x)),
                                                    game.board.side_length * (Constants.BOARD_SIZE[1] - min(y))))


class BlockI(Block):
    def __init__(self):
        super().__init__()
        self.tiles = [[3, Constants.BOARD_SIZE[1] - 1], [4, Constants.BOARD_SIZE[1] - 1],
                      [5, Constants.BOARD_SIZE[1] - 1], [6, Constants.BOARD_SIZE[1] - 1]]
        self.center_index = 1
        self.sprite = pygame.transform.scale(pack.singleI, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))
        self.type = Constants.I
        self.offset_data = (
            ((0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)),
            ((-1, 0), (0, 0), (0, 0), (0, 1), (0, -2)),
            ((-1, 1), (1, 1), (-2, 1), (1, 0), (-2, 0)),
            ((0, 1), (0, 1), (0, 1), (0, -1), (0, 2)),
        )

    def get_self(self):
        if self:
            return BlockI()

    @staticmethod
    def get_sprite_for_frame():
        return pygame.transform.scale(pygame.transform.rotate(pack.I, 90), (18 * 4, 18))


class BlockJ(Block):
    def __init__(self):
        super().__init__()
        self.tiles = [[3, Constants.BOARD_SIZE[1] - 1], [3, Constants.BOARD_SIZE[1] - 2],
                      [4, Constants.BOARD_SIZE[1] - 2], [5, Constants.BOARD_SIZE[1] - 2]]
        self.center_index = 2
        self.sprite = pygame.transform.scale(pack.singleJ, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))
        self.type = Constants.J

    def get_self(self):
        if self:
            return BlockJ()

    @staticmethod
    def get_sprite_for_frame():
        return pygame.transform.scale(pack.J, (18 * 3, 18 * 2))


class BlockL(Block):
    def __init__(self):
        super().__init__()
        self.tiles = [[5, Constants.BOARD_SIZE[1] - 1], [3, Constants.BOARD_SIZE[1] - 2],
                      [4, Constants.BOARD_SIZE[1] - 2], [5, Constants.BOARD_SIZE[1] - 2]]
        self.center_index = 2
        self.sprite = pygame.transform.scale(pack.singleL, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))
        self.type = Constants.L

    def get_self(self):
        if self:
            return BlockL()

    @staticmethod
    def get_sprite_for_frame():
        return pygame.transform.scale(pack.L, (18 * 3, 18 * 2))


class BlockO(Block):
    def __init__(self):
        super().__init__()
        self.tiles = [[4, Constants.BOARD_SIZE[1] - 1], [5, Constants.BOARD_SIZE[1] - 1],
                      [4, Constants.BOARD_SIZE[1] - 2], [5, Constants.BOARD_SIZE[1] - 2]]
        self.center_index = 2
        self.sprite = pygame.transform.scale(pack.singleO, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))
        self.type = Constants.O
        self.offset_data = (
            ((0, 0),),
            ((0, -1),),
            ((-1, -1),),
            ((-1, 0),),
        )

    def get_self(self):
        if self:
            return BlockO()

    @staticmethod
    def get_sprite_for_frame():
        return pygame.transform.scale(pack.O, (18 * 2, 18 * 2))


class BlockS(Block):
    def __init__(self):
        super().__init__()
        self.tiles = [[4, Constants.BOARD_SIZE[1] - 1], [5, Constants.BOARD_SIZE[1] - 1],
                      [3, Constants.BOARD_SIZE[1] - 2], [4, Constants.BOARD_SIZE[1] - 2]]
        self.center_index = 3
        self.sprite = pygame.transform.scale(pack.singleS, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))
        self.type = Constants.S

    def get_self(self):
        if self:
            return BlockS()

    @staticmethod
    def get_sprite_for_frame():
        return pygame.transform.scale(pack.S, (18 * 3, 18 * 2))


class BlockT(Block):
    def __init__(self):
        super().__init__()
        self.tiles = [[4, Constants.BOARD_SIZE[1] - 1], [5, Constants.BOARD_SIZE[1] - 2],
                      [3, Constants.BOARD_SIZE[1] - 2], [4, Constants.BOARD_SIZE[1] - 2]]
        self.center_index = 3
        self.sprite = pygame.transform.scale(pack.singleT, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))
        self.type = Constants.T

    def get_self(self):
        if self:
            return BlockT()

    @staticmethod
    def get_sprite_for_frame():
        return pygame.transform.scale(pack.T, (18 * 3, 18 * 2))


class BlockZ(Block):
    def __init__(self):
        super().__init__()
        self.tiles = [[3, Constants.BOARD_SIZE[1] - 1], [4, Constants.BOARD_SIZE[1] - 1],
                      [4, Constants.BOARD_SIZE[1] - 2], [5, Constants.BOARD_SIZE[1] - 2]]
        self.center_index = 2
        self.sprite = pygame.transform.scale(pack.singleZ, (Constants.SIDE_LENGTH, Constants.SIDE_LENGTH))
        self.type = Constants.Z

    def get_self(self):
        if self:
            return BlockZ()

    @staticmethod
    def get_sprite_for_frame():
        return pygame.transform.scale(pack.Z, (18 * 3, 18 * 2))


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
                if not self.block.touched_the_ground:
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

        self.score, self.combo, self.is_combo = 0, 0, False
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

        self.paused = False
        self.pause = None

        self.current_level = 1

        self.back_to_back_counter = 0

    def add_garbage_lines(self, lines):
        pass

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause = None
        self.BLOCK_ANCHOR.toggle_pause()
        pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)

    def render_and_update(self):
        self.board.draw_board()
        if self.paused:
            if self.pause is None:
                self.pause = Pause()
            self.pause.render()
        else:
            if self.current_block.block is None:
                self.next_block()

            self.current_block.update()
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


class Online(Game):
    pass


class Marathon(Game):
    def __init__(self, level, board=None, game_stats=None):
        super().__init__()
        self.loaded_time = 0
        if board is not None:
            self.board.board = board.copy()
            score, self.loaded_time, level = game_stats
            self.score, self.start_time = score, pygame.time.get_ticks() - self.loaded_time
        self.current_level = level
        pygame.time.set_timer(FALL_BLOCK_EVENT, Constants.FALL_TIME // level)
        self.mode = Constants.MARATHON
        self.result = False

    def is_countdown(self):
        return pygame.time.get_ticks() - self.start_time - self.loaded_time < 4700

    def get_current_time(self):
        if self.is_countdown():
            return pygame.time.get_ticks() - self.start_time - self.loaded_time
        return pygame.time.get_ticks() - self.start_time

    def render_and_update(self):
        self.draw_score()
        super().render_and_update()

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


class Stopwatch:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        self.paused = False
        self.pause_time = None

    def get_time(self):
        return pygame.time.get_ticks() - self.start_time

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_time = pygame.time.get_ticks()
        else:
            self.start_time += pygame.time.get_ticks() - self.pause_time


class WorldRecord(Game):
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
        self.mode = Constants.WORLD_RECORD
        self.current_level = 15
        self.result = False

    def countdown(self):
        self.timer = Stopwatch()
        super().countdown()

    def toggle_pause(self):
        super().toggle_pause()
        self.timer.toggle_pause()

    def render_and_update(self):
        self.check_win()
        if not self.paused:
            screen.blit(self.desk_surface, self.desk_rect)
            surface_time_left = self.time_font.render(get_time(self.timer.get_time(), True), True, (255, 255, 255))
            rect_time_left = surface_time_left.get_rect(center=(Constants.WINDOW_SIZE[0] // 10 * 6,
                                                                Constants.WINDOW_SIZE[1] // 20 * 9))
            surface_lines_left = self.time_font.render('Lines left: ' + str(self.get_lines_left()), True,
                                                       (255, 255, 255))
            rect_lines_left = surface_lines_left.get_rect(center=(Constants.WINDOW_SIZE[0] // 10 * 6,
                                                                  Constants.WINDOW_SIZE[1] // 20 * 11))
            screen.blit(surface_time_left, rect_time_left)
            screen.blit(surface_lines_left, rect_lines_left)
        super().render_and_update()

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


class GarbageTraining(Game):
    def __init__(self, lines):
        super().__init__()
        self.lines = lines
        self.garbage_lines_cleared = 0
        self.timer = Stopwatch()

        self.surface = pygame.surface.Surface((Constants.WINDOW_SIZE[0] // 20 * 9, Constants.WINDOW_SIZE[1] // 10 * 2))
        self.surface.fill((102, 204, 204))
        self.surface.set_alpha(100)
        self.rect = self.surface.get_rect(topleft=(Constants.WINDOW_SIZE[0] // 10 * 5,
                                                   Constants.WINDOW_SIZE[1] // 20 * 9))

        self.stats_font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', Constants.WINDOW_SIZE[1] // 12)
        self.timer_line_surface = self.stats_font.render('Time passed: ' + get_time(self.timer.get_time(), True),
                                                         True, (255, 255, 255))
        self.lines_left_surface = self.stats_font.render('Lines left: ' + str(self.lines), True, (255, 255, 255))
        self.timer_line_rect = self.timer_line_surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 20 * 14,
                                                                        Constants.WINDOW_SIZE[1] // 10 * 5))
        self.lines_left_rect = self.lines_left_surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 20 * 14,
                                                                        Constants.WINDOW_SIZE[1] // 10 * 6))

        self.result = False

        for i in range(10):
            self.board.add_garbage_line(random.randint(0, Constants.BOARD_SIZE[0] - 1))

        self.mode = Constants.TRAINING

    def get_lines_left(self):
        return self.lines - self.garbage_lines_cleared

    def add_garbage_lines(self, lines):
        self.garbage_lines_cleared += lines
        if self.get_lines_left() >= 10:
            self.board.add_garbage_line(random.randint(0, Constants.BOARD_SIZE[0] - 1))
        self.lines_left_surface = self.stats_font.render('Lines left: ' + str(self.get_lines_left()),
                                                         True, (255, 255, 255))

    def countdown(self):
        super().countdown()
        self.timer = Stopwatch()

    def toggle_pause(self):
        super().toggle_pause()
        self.timer.toggle_pause()

    def render_and_update(self):
        if not self.paused:
            self.timer_line_surface = self.stats_font.render('Time passed: ' + get_time(self.timer.get_time(), True),
                                                             True, (255, 255, 255))
            self.timer_line_rect = self.timer_line_surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 20 * 14,
                                                                            Constants.WINDOW_SIZE[1] // 10 * 5))
        screen.blit(self.surface, self.rect)
        screen.blit(self.timer_line_surface, self.timer_line_rect)
        screen.blit(self.lines_left_surface, self.lines_left_rect)
        super().render_and_update()
        self.check_win()

    def check_win(self):
        if self.get_lines_left() <= 0:
            self.gameover = True
            self.result = True

    def load_music(self):
        if self:
            pygame.mixer.music.load(pack.main_theme)
            pygame.mixer.music.play(-1)


tetrominoes_chain = list()


def get_random_block():
    global tetrominoes_chain
    if len(tetrominoes_chain) == 0:
        random_index = random.randint(0, 5040)
        for i in list(itertools.permutations(
                [BlockI(), BlockJ(), BlockL(), BlockO(), BlockS(), BlockT(), BlockZ()]))[random_index]:
            tetrominoes_chain.append(i)

    return tetrominoes_chain.pop(-1)


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

    def __init__(self, rect):
        super().__init__(particles)
        self.rect = rect
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
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
        self.transcript = {0: Constants.PROFILE, 1: Constants.GAME_MODE_SELECTION, 2: Constants.SHOP,
                           3: Constants.SETTINGS,
                           4: -1}
        self.profile_button = ProfileButton(Constants.WINDOW_SIZE[0] // 10 * 8, 0, Constants.WINDOW_SIZE[0] // 10 * 2,
                                            Constants.WINDOW_SIZE[1] // 10)
        self.confirm_exit = False
        self.surface_tetris_logo = StartScreen.surface_tetris_logo
        self.rect_tetris_logo = StartScreen.rect_tetris_logo
        self.font_buttons = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', 60)
        self.load_buttons()

    def update(self):
        self.profile_button = ProfileButton(Constants.WINDOW_SIZE[0] // 10 * 8, 0, Constants.WINDOW_SIZE[0] // 10 * 2,
                                            Constants.WINDOW_SIZE[1] // 10)

    def is_transition(self):
        return self.transition

    def do_transition(self):
        if self.rect_tetris_logo.centery > Constants.WINDOW_SIZE[1] // 5:
            self.rect_tetris_logo.centery -= 3
        else:
            self.transition = False

    def load_buttons(self):
        surface_profile = pygame.surface.Surface((Constants.WINDOW_SIZE[0] // 10 * 2, Constants.WINDOW_SIZE[1] // 10))
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
        self.profile_button.render()


def get_time(ms, with_ms=False, with_days=False):
    if not with_ms:
        ms = ms // 1000
        return f'{ms // 60 // 60}:{ms // 60 % 60}:{ms % 60}'
    if with_days:
        ms = ms // 1000 // 60
        return f'{ms // 60 // 24}:{ms // 60 % 24}:{ms % 60}'
    ms = ms // 10
    return f'{ms // 100 // 60}:{ms // 100 % 60}:{ms % 100}'


class EndGameScreen:
    audio_ok = pygame.mixer.Sound('audio/ok.wav')
    audio_gameover = pygame.mixer.Sound('audio/gameover.wav')

    def __init__(self):
        time = game.get_current_time()
        if isinstance(game, WorldRecord) or isinstance(game, GarbageTraining):
            time = game.timer.get_time()
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

        user.add_playtime(time)
        user.add_blocks_dropped(game.blocks)
        user.add_tetrises(game.tetrises)
        user.add_game()

        if game.mode == Constants.MARATHON:
            user.add_marathon_game(game.score, game.lines_cleared, time, game.blocks, game.max_combo,
                                   game.tspins, game.singles, game.doubles, game.triples, game.tetrises)
            user.add_score(game.score)
        elif game.mode == Constants.WORLD_RECORD:
            user.add_world_record_game(game.score, game.lines_cleared, time, game.blocks,
                                       game.max_combo, game.tspins, game.singles, game.doubles, game.triples,
                                       game.tetrises)
            if game.result:
                user.add_world_record_time(time)
        elif game.mode == Constants.TRAINING:
            user.add_training_game(game.score, game.lines_cleared, time, game.blocks, game.max_combo, game.tspins,
                                   game.singles, game.doubles, game.triples, game.tetrises)
        user.update()

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
                settings.MUSIC_VOLUME - time * (self.FADEOUT_TIME / settings.MUSIC_VOLUME))
        except ZeroDivisionError:
            pass
        screen.blit(surface, (0, 0))
        if not time < self.FADEOUT_TIME:
            global program_state
            program_state = Constants.MAIN_MENU
            pygame.mixer.music.load(Constants.MUSIC_MAIN_MENU)
            pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
            menu.update()

    def get_time(self):
        return pygame.time.get_ticks() - self.fadeout_start_time


class Settings:
    try:
        with open('settings', 'r', encoding='utf8') as reader:
            settings = reader.readlines()
        settings = iter(settings)
    except FileNotFoundError:
        print('[SETTINGS] Settings file is not found! Creating one...')
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
    PAUSE_BUTTON = pygame.K_ESCAPE

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
                                            Constants.WINDOW_SIZE[1] // 20 - 10, self.MOVE_LEFT_BUTTON)
        self.move_right_button = ControlsKey(self.BUTTONS_TO_STRING[self.MOVE_RIGHT_BUTTON],
                                             Constants.WINDOW_SIZE[0] // 10 * 6, Constants.WINDOW_SIZE[1] // 20 * 10,
                                             Constants.WINDOW_SIZE[1] // 20 - 10, self.MOVE_RIGHT_BUTTON)
        self.rotate_left_button = ControlsKey(self.BUTTONS_TO_STRING[self.ROTATE_LEFT_BUTTON],
                                              Constants.WINDOW_SIZE[0] // 10 * 4, Constants.WINDOW_SIZE[1] // 20 * 11,
                                              Constants.WINDOW_SIZE[1] // 20 - 10, self.ROTATE_LEFT_BUTTON)
        self.rotate_right_button = ControlsKey(self.BUTTONS_TO_STRING[self.ROTATE_RIGHT_BUTTON],
                                               Constants.WINDOW_SIZE[0] // 10 * 6, Constants.WINDOW_SIZE[1] // 20 * 11,
                                               Constants.WINDOW_SIZE[1] // 20 - 10, self.ROTATE_RIGHT_BUTTON)
        self.hard_drop_button = ControlsKey(self.BUTTONS_TO_STRING[self.HARD_DROP_BUTTON],
                                            Constants.WINDOW_SIZE[0] // 10 * 4, Constants.WINDOW_SIZE[1] // 20 * 12,
                                            Constants.WINDOW_SIZE[1] // 20 - 10, self.HARD_DROP_BUTTON)
        self.soft_drop_button = ControlsKey(self.BUTTONS_TO_STRING[self.SOFT_DROP_BUTTON],
                                            Constants.WINDOW_SIZE[0] // 10 * 6, Constants.WINDOW_SIZE[1] // 20 * 12,
                                            Constants.WINDOW_SIZE[1] // 20 - 10, self.SOFT_DROP_BUTTON)
        self.hold_tetromino_button = ControlsKey(self.BUTTONS_TO_STRING[self.HOLD_BLOCK_BUTTON],
                                                 Constants.WINDOW_SIZE[0] // 20 * 11,
                                                 Constants.WINDOW_SIZE[1] // 20 * 13,
                                                 Constants.WINDOW_SIZE[1] // 20 - 10, self.HOLD_BLOCK_BUTTON)

        self.buttons = [self.move_left_button, self.move_right_button, self.rotate_left_button,
                        self.rotate_right_button, self.hard_drop_button, self.soft_drop_button,
                        self.hold_tetromino_button]

        self.button_getter = None
        self.button_selection = False

    def save_settings(self):
        print('[SETTINGS] Saving settings file...')
        self.MOVE_LEFT_BUTTON = self.move_left_button.value
        self.MOVE_RIGHT_BUTTON = self.move_right_button.value
        self.SOFT_DROP_BUTTON = self.soft_drop_button.value
        self.ROTATE_LEFT_BUTTON = self.rotate_left_button.value
        self.ROTATE_RIGHT_BUTTON = self.rotate_right_button.value
        self.HARD_DROP_BUTTON = self.hard_drop_button.value
        self.HOLD_BLOCK_BUTTON = self.hold_tetromino_button.value
        with open('settings', 'w', encoding='utf8') as wr:
            s = f'{self.AUDIO_VOLUME}\n{self.MUSIC_VOLUME}\n{self.MOVE_LEFT_BUTTON}\n{self.MOVE_RIGHT_BUTTON}\n' \
                f'{self.SOFT_DROP_BUTTON}\n{self.ROTATE_LEFT_BUTTON}\n{self.ROTATE_RIGHT_BUTTON}\n' \
                f'{self.HARD_DROP_BUTTON}\n{self.HOLD_BLOCK_BUTTON}'
            wr.write(s)

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
        if 3 <= self.value <= 97:
            return int(self.value) / 100
        elif 3 > self.value:
            return 0
        elif self.value > 97:
            return 1


class ControlsKey:
    surface_empty_key = pygame.image.load('res/keyboard/empty_key.png').convert_alpha()

    def __init__(self, default_key, x, y, height, value):
        self.key_title = default_key
        self.value = value
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
            self.value = button
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
        self.paused = False
        self.pause_start_time = None

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

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_start_time = pygame.time.get_ticks()
        else:
            self.start_time += self.pause_start_time


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
        self.db, self.user, self.password, self.host = db, userr, password, host
        self.check_database()

    def check_database(self):
        print('[DATABASE] Starting checking...')
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()

        cursor.execute('SHOW TABLES')
        tables = [i[0] for i in list(cursor)]
        if 'users' not in tables:
            print('[DATABASE] users table is not found. Creating one...')
            cursor.execute("CREATE TABLE users (id int PRIMARY KEY auto_increment, username VARCHAR(50), "
                           "password VARCHAR(32), email VARCHAR(50), coins int DEFAULT 0, "
                           "purchased VARCHAR(50) DEFAULT '0;')")
        elif 'stats' not in tables:
            print('[DATABASE] stats table is not found. Creating one...')
            cursor.execute('CREATE TABLE stats (username VARCHAR(50) PRIMARY KEY, games_played int DEFAULT 0, '
                           'blocks_dropped int DEFAULT 0, best_score int DEFAULT 0, playtime int DEFAULT 0, '
                           'rang int DEFAULT 0, wins int DEFAULT 0, loses int DEFAULT 0, experience int DEFAULT 0, '
                           'tetrises int DEFAULT 0, world_record_time int)')
        elif 'games' not in tables:
            print('[DATABASE] games table is not found. Creating one...')
            cursor.execute('CREATE TABLE games(id int auto_increment primary key, score int, lines_cleared int, '
                           'time_played int, blocks_placed int, max_combo int, tspins int, singles int, doubles int, '
                           'triples int, tetrises int, gametype int, player_one varchar(50) null, '
                           'player_two varchar(50) null, result int);')

        cursor.execute('DESCRIBE users')
        if list(cursor) != [('id', b'int', 'NO', bytearray(b'PRI'), None, 'auto_increment'),
                            ('username', b'varchar(50)', 'YES', bytearray(b''), None, ''),
                            ('password', b'varchar(32)', 'YES', bytearray(b''), None, ''),
                            ('email', b'varchar(50)', 'YES', bytearray(b''), None, ''),
                            ('coins', b'int', 'YES', bytearray(b''), b'0', ''),
                            ('purchased', b'varchar(50)', 'YES', bytearray(b''), b'0;', '')]:
            print('[DATABASE] Bad users table, recreating one...')
            cursor.execute('DROP TABLE users')
            cursor.execute("CREATE TABLE users (id int PRIMARY KEY auto_increment, username VARCHAR(50), "
                           "password VARCHAR(32), email VARCHAR(50), coins int DEFAULT 0, "
                           "purchased VARCHAR(50) DEFAULT '0;')")
        cursor.execute('DESCRIBE stats')
        if list(cursor) != [('username', b'varchar(50)', 'NO', bytearray(b'PRI'), None, ''),
                            ('games_played', b'int', 'YES', bytearray(b''), b'0', ''),
                            ('blocks_dropped', b'int', 'YES', bytearray(b''), b'0', ''),
                            ('best_score', b'int', 'YES', bytearray(b''), b'0', ''),
                            ('playtime', b'int', 'YES', bytearray(b''), b'0', ''),
                            ('rang', b'int', 'YES', bytearray(b''), b'0', ''),
                            ('wins', b'int', 'YES', bytearray(b''), b'0', ''),
                            ('loses', b'int', 'YES', bytearray(b''), b'0', ''),
                            ('experience', b'int', 'YES', bytearray(b''), b'0', ''),
                            ('tetrises', b'int', 'YES', bytearray(b''), b'0', ''),
                            ('world_record_time', b'int', 'YES', bytearray(b''), None, '')]:
            print('[DATABASE] Bad stats table, recreating one...')
            cursor.execute('DROP TABLE stats')
            cursor.execute('CREATE TABLE stats (username VARCHAR(50) PRIMARY KEY, games_played int DEFAULT 0, '
                           'blocks_dropped int DEFAULT 0, best_score int DEFAULT 0, playtime int DEFAULT 0, '
                           'rang int DEFAULT 0, wins int DEFAULT 0, loses int DEFAULT 0, experience int DEFAULT 0, '
                           'tetrises int DEFAULT 0, world_record_time int)')
        cursor.execute('DESCRIBE games')
        if list(cursor) != [('id', b'int', 'NO', bytearray(b'PRI'), None, 'auto_increment'),
                            ('score', b'int', 'YES', bytearray(b''), None, ''),
                            ('lines_cleared', b'int', 'YES', bytearray(b''), None, ''),
                            ('time_played', b'int', 'YES', bytearray(b''), None, ''),
                            ('blocks_placed', b'int', 'YES', bytearray(b''), None, ''),
                            ('max_combo', b'int', 'YES', bytearray(b''), None, ''),
                            ('tspins', b'int', 'YES', bytearray(b''), None, ''),
                            ('singles', b'int', 'YES', bytearray(b''), None, ''),
                            ('doubles', b'int', 'YES', bytearray(b''), None, ''),
                            ('triples', b'int', 'YES', bytearray(b''), None, ''),
                            ('tetrises', b'int', 'YES', bytearray(b''), None, ''),
                            ('gametype', b'int', 'YES', bytearray(b''), None, ''),
                            ('player_one', b'varchar(50)', 'YES', bytearray(b''), None, ''),
                            ('player_two', b'varchar(50)', 'YES', bytearray(b''), None, ''),
                            ('result', b'int', 'YES', bytearray(b''), None, '')]:
            print('[DATABASE] Bad games table, recreating one...')
            cursor.execute('DROP TABLE games')
            cursor.execute('CREATE TABLE games(id int auto_increment primary key, score int, lines_cleared int, '
                           'time_played int, blocks_placed int, max_combo int, tspins int, singles int, doubles int, '
                           'triples int, tetrises int, gametype int, player_one varchar(50) null, '
                           'player_two varchar(50) null, result int);')
        print('[DATABASE] Check is done.')
        db.commit()

    def login(self, email, password):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('SELECT password FROM users WHERE email = %s', (email,))
        response = list(cursor)
        if len(response) == 0:
            return False

        hasher = hashlib.md5()
        hasher.update(password.encode())
        password = hasher.hexdigest()
        hashed_password = response[0][0]

        if password == hashed_password:
            cursor.execute('SELECT username FROM users WHERE email = %s', (email,))
            response = list(cursor)
            return response[0][0]
        else:
            return False

    def register(self, username, email, password):
        hasher = hashlib.md5()
        hasher.update(password.encode())
        password = hasher.hexdigest()
        if self.check_username_and_email_availability(username, email):
            db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
            cursor = db.cursor()
            cursor.execute('INSERT INTO users (username, password, email, coins) VALUES (%s, %s, %s, 0)',
                           (username, password, email))
            cursor.execute('INSERT INTO stats (username) VALUES (%s)', (username,))
            db.commit()
            return True
        return Constants.Errors.USERNAME_TAKEN

    def check_username_and_email_availability(self, username, email):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        if len(list(cursor)) > 0:
            return False
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        if len(list(cursor)) > 0:
            return False
        return True

    def get_stats(self, username):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM stats WHERE username = %s', (username,))
        d = dict()
        resp = iter(list(cursor)[0][1::])
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
        cursor.execute('SELECT coins FROM users WHERE username = %s', (username,))
        d['coins'] = list(cursor)[0][0]
        cursor.execute('SELECT purchased FROM users WHERE username = %s', (username,))
        d['purchased'] = list(cursor)[0][0]
        return d

    def set_experience(self, username, experience):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE stats SET experience = %s WHERE username = %s', (experience, username))
        db.commit()

    def set_best_score(self, username, score):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE stats SET best_score = %s WHERE username = %s', (score, username))
        db.commit()

    def set_games(self, username, games):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE stats SET games_played = %s WHERE username = %s', (games, username))
        db.commit()

    def set_playtime(self, username, playtime):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE stats SET playtime = %s WHERE username = %s', (playtime, username))
        db.commit()

    def set_rang(self, username, rang):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE stats SET rang = %s WHERE username = %s', (rang, username))
        db.commit()

    def set_wins(self, username, wins):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE stats SET wins = %s WHERE username = %s', (wins, username))
        db.commit()

    def set_loses(self, username, loses):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE stats SET loses = %s WHERE username = %s', (loses, username))
        db.commit()

    def set_blocks_dropped(self, username, blocks):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE stats SET blocks_dropped = %s WHERE username = %s', (blocks, username))
        db.commit()

    def set_tetrises(self, username, tetrises):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE stats SET tetrises = %s WHERE username = %s', (tetrises, username))
        db.commit()

    def set_world_record_time(self, username, time):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE stats SET world_record_time = %s WHERE username = %s', (time, username))
        db.commit()

    def set_coins(self, username, coins):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE users SET coins = %s WHERE username = %s', (coins, username))
        db.commit()

    def add_game(self, score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles, triples,
                 tetrises, gametype, player_one, player_two, result):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('INSERT INTO games (score, lines_cleared, time_played, blocks_placed, max_combo, tspins, '
                       'singles, doubles, triples, tetrises, gametype, player_one, player_two, result) '
                       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (score, lines_cleared, time_played, blocks_placed, max_combo,
                        tspins, singles, doubles, triples, tetrises, gametype, player_one, player_two, result))
        db.commit()

    def set_purchased(self, name, value):
        db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
        cursor = db.cursor()
        cursor.execute('UPDATE users SET purchased = %s WHERE username = %s', (value, name))
        db.commit()


class User:
    def __init__(self, name, db: Database):
        self.name = name
        self.db = db
        self.stats = self.db.get_stats(name)

    def update(self):
        self.stats = self.db.get_stats(self.name)

    def add_pack(self, p):
        self.db.set_purchased(self.name, str(self.stats['purchased']) + ';' + str(p))
        self.update()

    def get_purchased(self):
        return self.stats['purchased'].split(';')

    def subtract_coins(self, coins):
        self.add_coins(-coins)

    def get_coins(self):
        return self.stats['coins']

    def get_current_level(self):
        return calculate_current_level(self.stats['experience'])

    def get_experience_to_next_level(self):
        return calculate_experience_to_next_level(self.stats['experience'])

    def get_experience_of_current_level(self):
        if self.get_current_level() > 1:
            return self.stats['experience'] - calculate_exp_for_level(self.get_current_level())
        return self.stats['experience']

    def add_world_record_game(self, score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles,
                              doubles, triples, tetrises):
        self.db.add_game(score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles,
                         triples, tetrises, Constants.WORLD_RECORD, self.name, None, Constants.NEUTRAL)
        self.add_experience(game.score // 10)
        self.add_coins(game.score // 10000)
        self.update()

    def add_marathon_game(self, score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles,
                          triples, tetrises):
        self.db.add_game(score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles,
                         triples, tetrises, Constants.MARATHON, self.name, None, Constants.NEUTRAL)
        self.add_experience(game.score // 10)
        self.add_coins(game.score // 10000)
        self.update()

    def add_training_game(self, score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles,
                          triples, tetrises):
        self.db.add_game(score, lines_cleared, time_played, blocks_placed, max_combo, tspins, singles, doubles, triples,
                         tetrises, Constants.TRAINING, self.name, None, Constants.NEUTRAL)
        self.add_experience(game.score // 10)
        self.add_coins(game.score // 10000)
        self.update()

    def add_coins(self, coins):
        self.db.set_coins(self.name, self.stats['coins'] + coins)

    def add_experience(self, experience):
        self.db.set_experience(self.name, self.stats['experience'] + experience)
        self.update()

    def add_game(self, games=1):
        self.db.set_games(self.name, self.stats['games_played'] + games)
        self.update()

    def add_score(self, score):
        if self.stats['best_score'] < score:
            self.db.set_best_score(self.name, score)
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
        if self.stats['world_record_time'] is None or self.stats['world_record_time'] > time:
            self.db.set_world_record_time(self.name, time)
        self.update()

    def get_stats(self):
        return self.stats


KEYBOARD = 'qwertyuiopasdfghjklzxcvbnm'


def check_letter_error(password):
    flag1, flag2 = False, False
    for letter in password:
        if letter in KEYBOARD:
            flag1 = True
        elif letter in KEYBOARD.upper():
            flag2 = True
    return flag1 and flag2


def check_digit_error(password):
    for letter in password:
        if letter.isdigit():
            return True
    return False


def check_password(password):
    if len(password) < 9:
        return 'Password must contain at least 9 symbols'
    if not check_letter_error(password):
        return 'Password must contain lower-case and upper-case English letters'
    if not check_digit_error(password):
        return 'Password must contain at least one digit!'
    return True


def check_username(username):
    if len(username) == 0:
        return 'Username can\'t be blank'
    if len(username) > 20:
        return 'Username is way too long! 20 symbols is the limit!'
    for i in username:
        if i not in KEYBOARD + '1234567890' + KEYBOARD.upper():
            return 'You may use only letters from English alphabet and numbers in your nickname!'
    return True


def check_email(email):
    if '@' not in email or email.count('@') > 1:
        return 'Email is incorrect'
    mail, service = email.split('@')
    if "." not in service or ".." in service:
        return 'Email is incorrect'
    for i in mail:
        if i not in KEYBOARD + '1234567890' + KEYBOARD.upper():
            return 'Email is incorrect'
    return True


class AuthorisationWindow:
    audio_click = MainMenu.audio_click
    audio_alert = pygame.mixer.Sound('audio/alert.wav')

    AUTHORISATION, ANIMATION_TO_DOT, ANIMATION_FROM_DOT, CONNECTION, REGISTRATION = 0, 1, 2, 3, 4

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
            'Log in using Tetris Reloaded account', True, (255, 255, 255))
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

        self.sign_up_button = Button(self.sign_up_button_click, Constants.WINDOW_SIZE[0] // 10 * 9,
                                     Constants.WINDOW_SIZE[1] // 10 * 9, Constants.WINDOW_SIZE[0] // 15,
                                     Constants.WINDOW_SIZE[1] // 10 // 2, 'Sign up', (102, 204, 204))
        self.log_in_button = Button(self.log_in_button_click, Constants.WINDOW_SIZE[0] // 10 * 9,
                                    Constants.WINDOW_SIZE[1] // 10 * 9, Constants.WINDOW_SIZE[0] // 15,
                                    Constants.WINDOW_SIZE[1] // 10 // 2, 'Log up', (102, 204, 204))

        # sign in buttons and inputs

        self.registrate_user_button = Button(self.registrate_user, Constants.WINDOW_SIZE[0] // 10 * 4,
                                             Constants.WINDOW_SIZE[1] // 10 * 8, Constants.WINDOW_SIZE[0] // 10 * 2,
                                             Constants.WINDOW_SIZE[1] // 20, 'Sign up', (102, 204, 204))
        self.registration_username_input = LineEdit(Constants.WINDOW_SIZE[0] // 20 * 7,
                                                    Constants.WINDOW_SIZE[1] // 10 * 5,
                                                    Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 20,
                                                    'Username', (102, 204, 204), 200, self, False)
        self.registration_email_input = LineEdit(Constants.WINDOW_SIZE[0] // 20 * 7, Constants.WINDOW_SIZE[1] // 10 * 6,
                                                 Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 20,
                                                 'E-mail', (102, 204, 204), 200, self, False)
        self.registration_password_input = LineEdit(Constants.WINDOW_SIZE[0] // 20 * 7,
                                                    Constants.WINDOW_SIZE[1] // 10 * 7,
                                                    Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 20,
                                                    'Password', (102, 204, 204), 200, self, False)

        self.sign_up_title_surface = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf',
                                                      Constants.WINDOW_SIZE[1] // 25).render(
            'Sign up', True, (255, 255, 255))

        self.sign_up_title_rect = self.sign_up_title_surface.get_rect(midtop=(Constants.WINDOW_SIZE[0] // 2,
                                                                              Constants.WINDOW_SIZE[1] // 40 * 17))

        self.dialog_window = None

    def sign_up_button_click(self):
        self.audio_click.play()
        self.status = self.REGISTRATION
        self.email_input.input_text = ''
        self.password_input.input_text = ''

        self.size[1] = Constants.WINDOW_SIZE[1] // 10 * 5
        self.frame = pygame.Surface(self.size)
        self.frame.fill(self.color)
        self.frame.set_alpha(self.alpha)
        self.rect = pygame.rect.Rect((Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 10 * 4),
                                     self.size)

    def registrate_user(self):
        self.audio_click.play()
        username = self.registration_username_input.get_text()
        check_username_result = check_username(username)
        if check_username_result is True:
            pass
        else:
            self.call_dialog_window(check_username_result)
            return
        email = self.registration_email_input.get_text()
        check_email_result = check_email(email)
        if check_email_result is True:
            pass
        else:
            self.call_dialog_window(check_email_result)
            return
        password = self.registration_password_input.get_text()
        check_password_result = check_password(password)
        if check_password_result is True:
            pass
        else:
            self.call_dialog_window(check_password_result)
            return
        res = self.database.register(username, email, password)
        if res is True:
            self.log_in_button_click()
        elif res == Constants.Errors.WRONG_FERNET_TOKEN:
            self.call_dialog_window('Critical Error! Wrong fernet token! Use only official releases')
        elif res == Constants.Errors.USERNAME_TAKEN:
            self.call_dialog_window('Username or email has already been taken!')

    def close_dialog(self):
        self.dialog_window = None

    def call_dialog_window(self, text):
        self.audio_alert.play()
        self.dialog_window = DialogWindow(text, {'OK': self.close_dialog})

    def log_in_button_click(self):
        self.audio_click.play()
        self.status = self.AUTHORISATION

        self.size[1] = Constants.WINDOW_SIZE[1] // 10 * 4
        self.frame = pygame.Surface(self.size)
        self.frame.fill(self.color)
        self.frame.set_alpha(self.alpha)
        self.rect = pygame.rect.Rect((Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 10 * 4),
                                     self.size)

    def on_click(self):
        self.audio_click.play()
        self.status = self.ANIMATION_TO_DOT

    def render(self):
        screen.blit(StartScreen.surface_tetris_logo, StartScreen.rect_tetris_logo)
        screen.blit(self.frame, self.rect)
        if self.status == self.AUTHORISATION:
            self.render_authorisation()
        elif self.status == self.REGISTRATION:
            self.render_registration()
        elif self.status == self.ANIMATION_TO_DOT:
            self.render_animation_to_dot()
        elif self.status == self.CONNECTION:
            res = self.database.login(self.email_input.get_text(), self.password_input.get_text())
            if not res:
                self.status = self.ANIMATION_FROM_DOT
                self.audio_alert.play()
                return
            with open('account', 'wb') as wr:
                wr.write(
                    Constants.FERNET.encrypt(
                        (self.email_input.get_text() + ' ' + self.password_input.get_text()).encode()))
            return User(res, self.database)
        elif self.status == self.ANIMATION_FROM_DOT:
            self.render_animation_from_dot()
        return False

    def render_registration(self):
        pygame.draw.rect(screen, 'white', self.rect, 1)
        screen.blit(self.sign_up_title_surface, self.sign_up_title_rect)
        self.registration_email_input.render()
        self.registration_password_input.render()
        self.registration_username_input.render()
        self.log_in_button.render()
        self.registrate_user_button.render()
        if self.dialog_window is not None:
            self.dialog_window.render()

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
        self.sign_up_button.render()


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


def board_to_string(board: list):
    return ';'.join(['-'.join(list(map(str, i))) for i in board])


def string_to_board(string: str):
    return [list(map(int, i.split('-'))) for i in string.split(';')]


class GameModeSelection:
    marathon_cover = pygame.image.load('res/covers/marathon.png').convert_alpha()
    online_cover = pygame.image.load('res/covers/online.png').convert_alpha()
    training_cover = pygame.image.load('res/covers/training.png').convert_alpha()
    world_record_cover = pygame.image.load('res/covers/world_record.png').convert_alpha()

    audio_select = MainMenu.audio_click

    def __init__(self):
        indent_x = Constants.WINDOW_SIZE[0] // 20 * 1
        indent_y = Constants.WINDOW_SIZE[1] // 10 * 3
        width, height = Constants.WINDOW_SIZE[0] // 10 * 2, Constants.WINDOW_SIZE[1] // 10 * 5
        distance = (Constants.WINDOW_SIZE[0] - 2 * indent_x) // 4 - width

        self.marathon_button = GameModePane(self.on_marathon_click, indent_x,
                                            indent_y, width,
                                            height, 'Marathon',
                                            'Classic tetris mode', self.marathon_cover, self)

        self.online_button = GameModePane(self.on_online_click, indent_x + (width + distance),
                                          indent_y, width,
                                          height, 'Online',
                                          'Wanna test your skills?', self.online_cover, self)

        self.world_record_button = GameModePane(self.on_world_record_click, indent_x + (width + distance) * 2,
                                                indent_y, width,
                                                height, 'World record',
                                                'Are you really that good?', self.world_record_cover, self)

        self.training_button = GameModePane(self.on_training_click, indent_x + (width + distance) * 3,
                                            indent_y, width,
                                            height, 'Training',
                                            'Practice is the best way to learn', self.training_cover, self)

        self.title_font = pygame.font.Font('fonts/Nunito-Light.ttf', Constants.WINDOW_SIZE[1] // 10)
        self.title_surface = self.title_font.render('Select a game mode', True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 2,
                                                              Constants.WINDOW_SIZE[1] // 20 * 3))

        self.selected_mode = None
        self.timer = Timer()

        self.clicked_after_main_menu = False
        self.del_self = False

        self.dialog_window = None

    def render(self):
        screen.blit(self.title_surface, self.title_rect)
        if self.selected_mode is None or not self.timer.is_time():
            self.marathon_button.render()
            self.online_button.render()
            self.world_record_button.render()
            self.training_button.render()
            if self.dialog_window is not None:
                self.dialog_window.render()
            return
        global game, program_state
        program_state = Constants.INGAME
        if self.selected_mode == Constants.MARATHON:
            try:
                with open('last_game', 'rb') as reader:
                    read = reader.read().split(b'\n')
                board = Constants.FERNET.decrypt(read[0]).decode()
                board = string_to_board(board)
                game_stats = list(map(int, Constants.FERNET.decrypt(read[1]).decode().split()))
                game = Marathon(1, board, game_stats)
                os.remove('last_game')
            except FileNotFoundError:
                self.render_marathon()
            except fernet.InvalidToken:
                self.render_marathon()
            except Exception as error:
                print('[ERROR] While loading last game:', repr(e))
                try:
                    os.remove('last_game')
                except FileNotFoundError:
                    pass
                self.render_marathon()
        elif self.selected_mode == Constants.ONLINE:
            # self.render_online()
            pass
        elif self.selected_mode == Constants.WORLD_RECORD:
            # self.render_world_record()
            game = WorldRecord()
        elif self.selected_mode == Constants.TRAINING:
            # self.render_training()
            game = GarbageTraining(10)
        self.del_self = True

    def on_marathon_click(self):
        if not self.clicked_after_main_menu:
            self.clicked_after_main_menu = True
            return
        self.selected_mode = Constants.MARATHON
        self.hide_buttons()

    def render_marathon(self):
        global program_state
        program_state = Constants.LEVEL_SELECT

    def hide_buttons(self):
        self.timer.start(1000)
        self.audio_select.play()
        self.online_button.hide = True
        self.world_record_button.hide = True
        self.training_button.hide = True
        self.marathon_button.hide = True

    def on_online_click(self):
        if not self.clicked_after_main_menu:
            self.clicked_after_main_menu = True
            return
        self.dialog_window = DialogWindow('Servers are unavailable', {'OK': self.close_dialog})

    def close_dialog(self):
        self.dialog_window = None
        global game_mode_selection
        game_mode_selection = None

    def on_world_record_click(self):
        if not self.clicked_after_main_menu:
            self.clicked_after_main_menu = True
            return
        self.selected_mode = Constants.WORLD_RECORD
        self.hide_buttons()

    def on_training_click(self):
        if not self.clicked_after_main_menu:
            self.clicked_after_main_menu = True
            return
        self.selected_mode = Constants.TRAINING
        self.hide_buttons()


class GameModePane:
    IDLE, HOVER, PRESSED = 0, 1, 2

    def __init__(self, on_click, x, y, width, height, title, description, image, sender):
        self.sender = sender
        self.on_click = on_click
        self.x, self.y, self.width, self.height, self.title = x, y, width, height, title
        self.description, self.image = description, image

        self.frame_surface = pygame.surface.Surface((width, height))
        self.frame_rect = self.frame_surface.get_rect(topleft=(x, y))

        self.frame_surface.fill((102, 102, 204))
        self.frame_surface.set_alpha(100)

        self.state = self.IDLE

        self.white_surface = pygame.surface.Surface((width, height))
        self.white_surface.fill((255, 255, 255))
        self.white_surface.set_alpha(50)
        self.white_surface_increment = True

        self.black_surface = pygame.surface.Surface((width, height))
        self.black_surface.set_alpha(50)

        self.title_font = pygame.font.Font('fonts/Nunito-Light.ttf', height // 10)
        self.title_surface = self.title_font.render(title, True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(center=(x + width // 2, y + height // 10))

        self.description_font = pygame.font.Font('fonts/Nunito-Light.ttf', height // 20)
        self.description_surface = self.description_font.render(description, True, (255, 255, 255))
        self.description_rect = self.description_surface.get_rect(center=(x + width // 2, y + height // 10 * 2))

        self.image_surface = pygame.transform.scale(image, (width, height // 10 * 7))
        self.image_rect = self.image_surface.get_rect(bottomright=(x + width, y + height))
        self.image_surface.set_alpha(200)

        self.hide = False
        self.hide_speed = Constants.WINDOW_SIZE[1] // 10

    def render(self):
        if self.hide:
            self.render_hide()
        else:
            self.get_state()
        screen.blit(self.frame_surface, self.frame_rect)
        screen.blit(self.title_surface, self.title_rect)
        screen.blit(self.description_surface, self.description_rect)

        screen.blit(self.image_surface, self.image_rect)

        if self.state == self.HOVER:
            self.render_hover()
        elif self.state == self.PRESSED:
            self.render_pressed()

    def render_hide(self):
        if self.frame_rect.centerx > -Constants.WINDOW_SIZE[0]:
            self.frame_rect.centerx -= self.hide_speed
            self.title_rect.centerx -= self.hide_speed
            self.image_rect.centerx -= self.hide_speed
            self.description_rect.centerx -= self.hide_speed

    def render_hover(self):
        pygame.draw.rect(screen, (255, 255, 255), self.frame_rect, 1)
        self.update_white_surface()
        screen.blit(self.white_surface, self.frame_rect)

    def update_white_surface(self):
        alpha = self.white_surface.get_alpha()
        if alpha <= 25:
            self.white_surface_increment = True
        elif alpha >= 75:
            self.white_surface_increment = False
        self.white_surface.set_alpha(alpha + (1 if self.white_surface_increment else -1))

    def render_pressed(self):
        screen.blit(self.black_surface, self.frame_rect)

    def get_state(self):
        if self.frame_rect.collidepoint(pygame.mouse.get_pos()):
            if True in pygame.mouse.get_pressed(3):
                self.state = self.PRESSED
                self.image_surface.set_alpha(255)
                return
            elif self.state == self.PRESSED:
                self.on_click()
            self.state = self.HOVER
            self.image_surface.set_alpha(255)
            return
        self.state = self.IDLE
        self.image_surface.set_alpha(200)


class Pause:
    pause_sound = pygame.mixer.Sound('audio/pause.wav')
    pause_click = MainMenu.audio_click

    def __init__(self):
        self.width, self.height = Constants.WINDOW_SIZE[0] // 10 * 2, Constants.WINDOW_SIZE[1] // 10 * 5
        self.frame_surface = pygame.surface.Surface((self.width, self.height))
        self.frame_surface.fill((0, 153, 153))
        self.frame_surface.set_alpha(150)
        self.frame_rect = self.frame_surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 2,
                                                              Constants.WINDOW_SIZE[1] // 2))
        self.x, self.y = self.frame_rect.topleft

        self.title_font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', Constants.WINDOW_SIZE[1] // 10)
        self.title_surface = self.title_font.render('Pause', True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 2,
                                                              self.y + self.height // 5))

        button_width = self.width // 10 * 8
        button_height = self.height // 20 * 3

        self.resume_button = Button(self.resume, self.x + self.width // 10, self.y + self.height // 20 * 8,
                                    button_width, button_height, 'Resume', (0, 204, 204))
        self.return_to_main_menu_button = Button(self.return_to_main_menu, self.x + self.width // 10,
                                                 self.y + self.height // 20 * 12, button_width,
                                                 button_height, 'Main menu', (0, 204, 204))
        self.exit_button = Button(terminate, self.x + self.width // 10, self.y + self.height // 20 * 16, button_width,
                                  button_height, 'Exit', (0, 204, 204))

        self.black_surface = pygame.surface.Surface((Constants.WINDOW_SIZE[0], Constants.WINDOW_SIZE[1]))
        self.black_surface.set_alpha(10)

        self.pause_sound.play()

        self.alpha_decrease = 5

    def render(self):
        alpha = self.black_surface.get_alpha()
        if alpha < 150:
            self.black_surface.set_alpha(alpha + self.alpha_decrease)
            pygame.mixer.music.set_volume(
                pygame.mixer.music.get_volume() - self.alpha_decrease * (
                        settings.MUSIC_VOLUME / (150 / self.alpha_decrease)))

        screen.blit(self.black_surface, (0, 0))
        screen.blit(self.frame_surface, self.frame_rect)
        pygame.draw.rect(screen, 'white', self.frame_rect, 1)
        screen.blit(self.title_surface, self.title_rect)
        self.resume_button.render()
        self.return_to_main_menu_button.render()
        self.exit_button.render()

    def resume(self):
        self.pause_click.play()
        game.toggle_pause()

    def return_to_main_menu(self):
        global game, program_state
        self.pause_click.play()
        game = None
        program_state = Constants.MAIN_MENU
        pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
        pygame.mixer.music.load(Constants.MUSIC_MAIN_MENU)
        pygame.mixer.music.play(-1)


def calculate_current_level(experience):
    return int((math.sqrt((2 * experience) + 30625) / 50) - 2.5)


def calculate_exp_for_level(level):
    return 1250 * level ** 2 + 6250 * level - 7500


def calculate_experience_to_next_level(experience):
    return calculate_exp_for_level(calculate_current_level(experience) + 1)


class Profile:
    def __init__(self):
        self.title_font = pygame.font.Font('fonts/Nunito-Light.ttf', Constants.WINDOW_SIZE[1] // 10)
        self.profile_title_surface = self.title_font.render('Profile', True, (255, 255, 255))
        self.profile_title_rect = self.profile_title_surface.get_rect(midtop=(Constants.WINDOW_SIZE[0] // 10 * 2,
                                                                              Constants.WINDOW_SIZE[1] // 10))
        self.background_surface = pygame.surface.Surface((Constants.WINDOW_SIZE[0] // 10 * 8,
                                                          Constants.WINDOW_SIZE[1] // 10 * 8))
        self.background_surface.fill((102, 204, 204))
        self.background_surface.set_alpha(150)
        self.background_rect = self.background_surface.get_rect(
            topleft=(Constants.WINDOW_SIZE[0] // 10, Constants.WINDOW_SIZE[1] // 10))

        self.nickname_font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', Constants.WINDOW_SIZE[1] // 10)
        self.nickname_surface = self.nickname_font.render(user.name, True, (255, 255, 255))
        self.nickname_rect = self.nickname_surface.get_rect(topleft=(Constants.WINDOW_SIZE[0] // 20 * 3,
                                                                     Constants.WINDOW_SIZE[1] // 10 * 2))

        self.text_font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', Constants.WINDOW_SIZE[1] // 10 // 2)
        self.games_played_surface = self.text_font.render('Games played: ' + str(user.stats['games_played']), True,
                                                          (255, 255, 255))
        self.games_played_rect = self.games_played_surface.get_rect(topleft=(Constants.WINDOW_SIZE[0] // 20 * 3,
                                                                             Constants.WINDOW_SIZE[1] // 20 * 7))

        self.time_played_surface = self.text_font.render('Playtime: ' + get_time(user.stats['playtime']), True,
                                                         (255, 255, 255))
        self.time_played_rect = self.time_played_surface.get_rect(topleft=(Constants.WINDOW_SIZE[0] // 20 * 3,
                                                                           Constants.WINDOW_SIZE[1] // 20 * 8))

        self.high_score_surface = self.text_font.render('High score: ' + str(user.stats['best_score']), True,
                                                        (255, 255, 255))
        self.high_score_rect = self.high_score_surface.get_rect(topleft=(Constants.WINDOW_SIZE[0] // 20 * 3,
                                                                         Constants.WINDOW_SIZE[1] // 20 * 9))

        self.blocks_dropped_surface = self.text_font.render('Blocks dropped: ' + str(user.stats['blocks_dropped']),
                                                            True, (255, 255, 255))
        self.blocks_dropped_rect = self.blocks_dropped_surface.get_rect(topleft=(Constants.WINDOW_SIZE[0] // 20 * 3,
                                                                                 Constants.WINDOW_SIZE[1] // 20 * 10))

        self.wins_surface = self.text_font.render('Wins: ' + str(user.stats['wins']), True, (255, 255, 255))
        self.wins_rect = self.wins_surface.get_rect(topleft=(Constants.WINDOW_SIZE[0] // 20 * 3,
                                                             Constants.WINDOW_SIZE[1] // 20 * 11))

        self.loses_surface = self.text_font.render('Loses: ' + str(user.stats['loses']), True, (255, 255, 255))
        self.loses_rect = self.loses_surface.get_rect(topleft=(Constants.WINDOW_SIZE[0] // 20 * 3,
                                                               Constants.WINDOW_SIZE[1] // 20 * 12))

        world_record_time = user.stats['world_record_time']
        world_record_time = get_time(world_record_time) if world_record_time is not None else 'No information'
        self.world_record_time_surface = self.text_font.render('World record time: ' + world_record_time, True,
                                                               (255, 255, 255))
        self.world_record_time_rect = self.world_record_time_surface.get_rect(
            topleft=(Constants.WINDOW_SIZE[0] // 20 * 3, Constants.WINDOW_SIZE[1] // 20 * 13))

        self.tetrises_surface = self.text_font.render('Lifetime tetris lines: ' + str(user.stats['tetrises']), True,
                                                      (255, 255, 255))
        self.tetrises_rect = self.tetrises_surface.get_rect(topleft=(Constants.WINDOW_SIZE[0] // 20 * 3,
                                                                     Constants.WINDOW_SIZE[1] // 20 * 15))

        current_level = user.get_current_level()
        current_exp = user.get_experience_of_current_level()
        exp_to_next_level = user.get_experience_to_next_level()

        self.exp_line = LevelLine(Constants.WINDOW_SIZE[0] // 20 * 11, Constants.WINDOW_SIZE[1] // 20 * 5,
                                  Constants.WINDOW_SIZE[0] // 10 * 3, Constants.WINDOW_SIZE[1] // 10, current_level,
                                  current_exp, exp_to_next_level)

    def render(self):
        screen.blit(self.background_surface, self.background_rect)
        pygame.draw.rect(screen, 'white', self.background_rect, 1)
        screen.blit(self.nickname_surface, self.nickname_rect)

        screen.blit(self.games_played_surface, self.games_played_rect)
        screen.blit(self.time_played_surface, self.time_played_rect)
        screen.blit(self.high_score_surface, self.high_score_rect)
        screen.blit(self.blocks_dropped_surface, self.blocks_dropped_rect)
        screen.blit(self.wins_surface, self.wins_rect)
        screen.blit(self.loses_surface, self.loses_rect)
        screen.blit(self.world_record_time_surface, self.world_record_time_rect)
        screen.blit(self.tetrises_surface, self.tetrises_rect)

        self.exp_line.render()


class LevelLine:
    def __init__(self, x, y, width, height, current_level, current_exp, exp_to_next_level, line_color=(102, 204, 204),
                 outline_color=(255, 255, 255)):
        self.x, self.y, self.width, self.level, self.exp = x, y, width, current_level, current_exp
        self.exp_to_next_level = exp_to_next_level
        self.outline_color = outline_color
        self.rect = pygame.rect.Rect((x, y), (width, height))
        height = height // 3

        self.line_box_rect = pygame.rect.Rect((x, y + height), (width, height))

        self.font = pygame.font.Font('fonts/Jura-VariableFont_wght.ttf', int(height * 0.9))
        self.current_level_text_surface = self.font.render(str(current_level), True, (255, 255, 255))
        self.next_level_text_surface = self.font.render(str(current_level + 1), True, (255, 255, 255))
        self.current_exp_text_surface = self.font.render(str(current_exp), True, (255, 255, 255))
        self.exp_to_next_level_surface = self.font.render(str(exp_to_next_level), True, (255, 255, 255))

        self.current_level_text_rect = self.current_level_text_surface.get_rect(topleft=(x, y))
        self.next_level_text_rect = self.next_level_text_surface.get_rect(topright=(x + width, y))
        self.current_exp_text_rect = self.current_exp_text_surface.get_rect(bottomleft=(x, y + height * 3))
        self.exp_to_next_level_rect = self.exp_to_next_level_surface.get_rect(bottomright=(x + width, y + height * 3))

        self.line_surface = pygame.surface.Surface((int(width * (current_exp / exp_to_next_level)), height))
        self.line_surface.fill(line_color)
        self.line_surface.set_alpha(200)
        self.line_rect = self.line_surface.get_rect(topleft=(x, y + height))

    def render(self):
        screen.blit(self.current_level_text_surface, self.current_level_text_rect)
        screen.blit(self.next_level_text_surface, self.next_level_text_rect)
        screen.blit(self.current_exp_text_surface, self.current_exp_text_rect)
        screen.blit(self.exp_to_next_level_surface, self.exp_to_next_level_rect)

        screen.blit(self.line_surface, self.line_rect)
        pygame.draw.rect(screen, 'white', self.line_box_rect, 1)


class Shop:
    coin_surface = pygame.image.load('res/coin.png').convert_alpha()

    default_surface = pygame.image.load('res/default/default.png').convert()
    classic_surface = pygame.image.load('res/classic/classic.png').convert()
    toys_surface = pygame.image.load('res/toys/toys.png').convert()
    space_surface = pygame.image.load('res/space/space.png').convert()
    mario_surface = pygame.image.load('res/mario/mario.png').convert()
    kirby_surface = pygame.image.load('res/kirby/kirby.png').convert()

    def __init__(self):
        self.title_font = pygame.font.Font('fonts/Nunito-Light.ttf', Constants.WINDOW_SIZE[1] // 10)
        self.profile_title_surface = self.title_font.render('Shop', True, (255, 255, 255))
        self.profile_title_rect = self.profile_title_surface.get_rect(midtop=(Constants.WINDOW_SIZE[0] // 10 * 2,
                                                                              Constants.WINDOW_SIZE[1] // 10))

        self.background_surface = pygame.Surface(
            (Constants.WINDOW_SIZE[0] // 10 * 8, Constants.WINDOW_SIZE[1] // 10 * 8))
        self.background_rect = self.background_surface.get_rect(topleft=(Constants.WINDOW_SIZE[0] // 10,
                                                                         Constants.WINDOW_SIZE[1] // 10))
        self.background_surface.fill((102, 204, 204))
        self.background_surface.set_alpha(200)

        self.balance_font = pygame.font.Font('fonts/Orbitron-Bold.ttf', Constants.WINDOW_SIZE[1] // 25)
        self.balance_text_surface = self.balance_font.render(str(user.get_coins()), True, (255, 255, 255))
        self.balance_text_rect = self.balance_text_surface.get_rect(bottomleft=(Constants.WINDOW_SIZE[0] // 10 * 8,
                                                                                Constants.WINDOW_SIZE[1] // 10 * 2))
        height = self.balance_text_surface.get_height()
        self.coin_surface = pygame.transform.scale(self.coin_surface, (height, height))
        self.coin_rect = self.coin_surface.get_rect(
            bottomleft=(Constants.WINDOW_SIZE[0] // 10 * 8 + self.balance_text_surface.get_width(),
                        Constants.WINDOW_SIZE[1] // 10 * 2))

        self.dialog_window = None
        self.selected_name = None

        self.purchased = None
        self.tiles = dict()
        self.update_tiles()

    def update_tiles(self):
        self.purchased = user.get_purchased()

        self.tiles = {'Default': PackTile(Constants.WINDOW_SIZE[0] // 10 * 2, Constants.WINDOW_SIZE[1] // 10 * 3,
                                          Constants.WINDOW_SIZE[0] // 10, Constants.WINDOW_SIZE[1] // 10 * 2, 'Default',
                                          100, self.default_surface, self.on_click, 0, self.purchased),
                      'Classic': PackTile(Constants.WINDOW_SIZE[0] // 10 * 4, Constants.WINDOW_SIZE[1] // 10 * 3,
                                          Constants.WINDOW_SIZE[0] // 10, Constants.WINDOW_SIZE[1] // 10 * 2, 'Classic',
                                          100, self.classic_surface, self.on_click, 1, self.purchased),
                      'Space': PackTile(Constants.WINDOW_SIZE[0] // 10 * 6, Constants.WINDOW_SIZE[1] // 10 * 3,
                                        Constants.WINDOW_SIZE[0] // 10, Constants.WINDOW_SIZE[1] // 10 * 2, 'Space',
                                        100, self.space_surface, self.on_click, 2, self.purchased),
                      'Toys': PackTile(Constants.WINDOW_SIZE[0] // 10 * 2, Constants.WINDOW_SIZE[1] // 10 * 6,
                                       Constants.WINDOW_SIZE[0] // 10, Constants.WINDOW_SIZE[1] // 10 * 2, 'Toys',
                                       100, self.toys_surface, self.on_click, 3, self.purchased),
                      'Kirby': PackTile(Constants.WINDOW_SIZE[0] // 10 * 4, Constants.WINDOW_SIZE[1] // 10 * 6,
                                        Constants.WINDOW_SIZE[0] // 10, Constants.WINDOW_SIZE[1] // 10 * 2, 'Kirby',
                                        1000, self.kirby_surface, self.on_click, 4, self.purchased),
                      'Mario': PackTile(Constants.WINDOW_SIZE[0] // 10 * 6, Constants.WINDOW_SIZE[1] // 10 * 6,
                                        Constants.WINDOW_SIZE[0] // 10, Constants.WINDOW_SIZE[1] // 10 * 2, 'Mario',
                                        1000, self.mario_surface, self.on_click, 5, self.purchased)}

    def render(self):
        pygame.draw.rect(screen, 'white', self.background_rect, 1)
        screen.blit(self.background_surface, self.background_rect)
        screen.blit(self.profile_title_surface, self.profile_title_rect)
        screen.blit(self.balance_text_surface, self.balance_text_rect)
        screen.blit(self.coin_surface, self.coin_rect)

        for i in self.tiles:
            self.tiles[i].render()

        if self.dialog_window is not None:
            self.dialog_window.render()

    def on_click(self, tile):
        if not tile.purchased:
            self.dialog_window = DialogWindow(f'Are you sure you want to purchase {tile.name}?',
                                              {'Yes': self.yes, 'No': self.no})
            self.selected_name = tile.name
        else:
            global pack
            pack = SoundGraphicPack(tile.name.lower())
        self.update_tiles()

    def yes(self):
        self.dialog_window = None
        if user.get_coins() >= self.tiles[self.selected_name].price:
            user.subtract_coins(self.tiles[self.selected_name].price)
            user.add_pack(self.tiles[self.selected_name].id)
            self.update_tiles()

            user.update()
            self.balance_text_surface = self.balance_font.render(str(user.get_coins()), True, (255, 255, 255))
            self.balance_text_rect = self.balance_text_surface.get_rect(bottomleft=(Constants.WINDOW_SIZE[0] // 10 * 8,
                                                                                    Constants.WINDOW_SIZE[1] // 10 * 2))
        else:
            self.dialog_window = DialogWindow(f'You don\'t have enough money to purchase this pack!', {'Ok': self.no})

    def no(self):
        self.dialog_window = None


class DialogWindow:
    def __init__(self, text, options: dict):
        self.font = pygame.font.Font('fonts/Nunito-Light.ttf', Constants.WINDOW_SIZE[1] // 10 // 2)
        self.text_surface = self.font.render(text, True, (255, 255, 255))

        self.surface = pygame.Surface((Constants.WINDOW_SIZE[0] // 10 + self.text_surface.get_width(),
                                       Constants.WINDOW_SIZE[1] // 10 * 2))
        self.rect = self.surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 2, Constants.WINDOW_SIZE[1] // 2))
        x, y = self.rect.topleft
        self.surface.fill((102, 204, 204))
        self.surface.set_alpha(200)

        self.text_rect = self.text_surface.get_rect(center=(Constants.WINDOW_SIZE[0] // 2,
                                                            y + Constants.WINDOW_SIZE[1] // 20))

        button_width, button_height = Constants.WINDOW_SIZE[0] // 10, Constants.WINDOW_SIZE[1] // 20
        button_x = self.surface.get_width() // (len(options) + 1)
        button_y = y + Constants.WINDOW_SIZE[1] // 10

        self.buttons = list()
        i = 1
        for t in options.keys():
            bx = x + button_x * i - button_width // 2
            self.buttons.append(Button(options[t], bx, button_y, button_width, button_height, t, (0, 204, 204)))
            i += 1

        self.black_surface = pygame.Surface(Constants.WINDOW_SIZE)
        self.black_surface.set_alpha(100)

    def render(self):
        screen.blit(self.black_surface, (0, 0))
        screen.blit(self.surface, self.rect)
        pygame.draw.rect(screen, 'white', self.rect, 1)
        screen.blit(self.text_surface, self.text_rect)
        for button in self.buttons:
            button.render()


class PackTile:
    IDLE, HOVER, HOVER_BUTTON = 0, 1, 2

    def __init__(self, x, y, width, height, name, price, image, on_click, idd, purchased):
        self.purchased = str(idd) in purchased
        self.id = idd
        self.price = price
        self.name = name
        self.on_click = on_click
        self.surface = pygame.Surface((width, height))
        self.surface.fill((102, 204, 204))
        self.surface.set_alpha(200)
        self.rect = pygame.rect.Rect((x, y), (width, height))
        self.image = pygame.transform.scale(image, (width // 10 * 8, height // 10 * 6))
        self.image_rect = self.image.get_rect(topleft=(x + width // 10, y + height // 10 * 2))
        self.font = pygame.font.Font('fonts/Nunito-Light.ttf', height // 10)
        self.title_surface = self.font.render(name, True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(center=(x + width // 2, y + height // 10))

        self.button_surface = pygame.Surface((width // 10 * 8, height // 10))
        self.button_surface_hovered = pygame.Surface((width // 10 * 8, height // 10))
        self.button_surface_hovered.fill((10, 152, 149))
        self.button_surface.fill((8, 188, 190))
        self.button_rect = self.button_surface.get_rect(topleft=(x + width // 10, y + height // 20 * 17))

        if not self.purchased:
            self.price_text_surface = self.font.render(str(price) + ' ', True, (255, 255, 255))
            self.price_text_rect = self.price_text_surface.get_rect(center=(x + width // 2 - height // 12 // 2,
                                                                            y + height // 20 * 18))

            self.coin_surface = pygame.transform.scale(Shop.coin_surface, (height // 12, height // 12))
            self.coin_rect = self.coin_surface.get_rect(midleft=self.price_text_rect.midright)
        else:
            self.price_text_surface = self.font.render('SELECT' if pack.name != self.name.lower() else 'SELECTED',
                                                       True, (255, 255, 255))
            self.price_text_rect = self.price_text_surface.get_rect(center=(x + width // 2,
                                                                            y + height // 20 * 18))

        self.state = self.IDLE

    def render(self):
        screen.blit(self.surface, self.rect)
        screen.blit(self.image, self.image_rect)
        screen.blit(self.title_surface, self.title_rect)

        screen.blit(self.button_surface, self.button_rect)

        self.check_state()
        if self.state != self.IDLE:
            pygame.draw.rect(screen, 'white', self.rect, 1)
            if self.state == self.HOVER_BUTTON:
                screen.blit(self.button_surface_hovered, self.button_rect)

        screen.blit(self.price_text_surface, self.price_text_rect)
        if not self.purchased:
            screen.blit(self.coin_surface, self.coin_rect)

    def check_state(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.button_rect.collidepoint(pygame.mouse.get_pos()) and True not in pygame.mouse.get_pressed(3):
                self.state = self.HOVER_BUTTON
                return
            if self.state == self.HOVER_BUTTON and True in pygame.mouse.get_pressed(3):
                self.on_click(self)
                return
            self.state = self.HOVER
        else:
            self.state = self.IDLE


class ProfileButton:
    def __init__(self, x, y, width, height):
        self.rect = pygame.rect.Rect((x, y), (width, height))
        self.surface = pygame.Surface((width, height))
        self.surface.fill((102, 204, 204))
        self.surface.set_alpha(200)
        self.font = pygame.font.Font('fonts/Nunito-Light.ttf', height)
        name, level = user.name, str(user.get_current_level())
        font_height = height
        for i in range(20):
            font_height = int(font_height * 0.9)
            self.font = pygame.font.Font('fonts/Nunito-Light.ttf', font_height)
            if self.font.size(name + '   ' + 'Lv.' + level)[0] <= width:
                break
        self.text_surface = self.font.render(name + '   ' + 'Lv.' + level, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(x + width // 2, y + height // 2))

    def render(self):
        screen.blit(self.surface, self.rect)
        pygame.draw.rect(screen, 'white', self.rect, 1)
        screen.blit(self.text_surface, self.text_rect)


def terminate():
    pygame.quit()
    sys.exit()


FALL_BLOCK_EVENT = pygame.event.custom_type()

connecting_to_db = True
database = None
while connecting_to_db:
    try:
        database = Database(db=Constants.Database.DATABASE,
                            userr=Constants.Database.USER,
                            password=Constants.Database.PASSWORD,
                            host=Constants.Database.HOST)
    except mysql.connector.errors.DatabaseError as e:
        print('[ERROR] While connecting to database:', repr(e))
    else:
        connecting_to_db = False

background = Background()
start_screen = StartScreen()
program_state = Constants.START_SCREEN
level_selection, game, menu, gameover, settings, authorisation, user = None, None, None, None, Settings(), None, None
game_mode_selection, profile, shop = None, None, None
particles = pygame.sprite.Group()
pack = SoundGraphicPack('default')

black_surface = pygame.Surface(Constants.WINDOW_SIZE)
black_surface.set_alpha(0)
for _ in range(255):
    screen.blit(tribute, (0, 0))
    screen.blit(black_surface, (0, 0))
    black_surface.set_alpha(_)
    pygame.display.update()
    pygame.time.wait(10)

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

        if isinstance(r, User):
            user = r
            program_state = Constants.MAIN_MENU

    elif program_state == Constants.MAIN_MENU:
        if menu is None:
            menu = MainMenu(user)
        game_mode_selection = None
        level_selection = None
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

        game_mode_selection.render()

    elif program_state == Constants.LEVEL_SELECT:
        if level_selection is None:
            level_selection = LevelSelection()
            game_mode_selection = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level_selection.check_pos(event.pos):
                    game = Marathon(level_selection.get_selected_level())
                    program_state = Constants.INGAME
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    program_state = Constants.MAIN_MENU

        level_selection.render()

    elif program_state == Constants.INGAME:
        if game is None:
            game = Marathon(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if game.mode == Constants.MARATHON:
                    try:
                        with open('last_game', 'wb') as writer:
                            writer.write(Constants.FERNET.encrypt(board_to_string(game.board.board).encode()))
                            writer.write(b'\n')
                            writer.write(Constants.FERNET.encrypt(
                                f'{game.score} {game.get_current_time()} {game.current_level}'.encode()))
                    except Exception as e:
                        print('[ERROR] While saving last game:', repr(e))
                terminate()
            elif event.type == pygame.KEYDOWN and game.current_block.block:
                if event.key == settings.MOVE_LEFT_BUTTON:
                    game.current_block.move_left = True
                elif event.key == settings.MOVE_RIGHT_BUTTON:
                    game.current_block.move_right = True
                elif event.key == settings.ROTATE_LEFT_BUTTON:
                    game.current_block.block.rotate_left()
                elif event.key == settings.ROTATE_RIGHT_BUTTON:
                    game.current_block.block.rotate_right()
                elif event.key == settings.HARD_DROP_BUTTON:
                    hard_drop_particle = HardDropParticle(game.current_block.block.hard_drop())
                elif event.key == settings.SOFT_DROP_BUTTON:
                    game.current_block.move_down = True
                elif event.key == settings.HOLD_BLOCK_BUTTON and game.may_hold():
                    game.block_queue.hold()
            elif event.type == pygame.KEYUP and game.current_block.block:
                if event.key == settings.MOVE_LEFT_BUTTON:
                    game.current_block.move_left = False
                elif event.key == settings.MOVE_RIGHT_BUTTON:
                    game.current_block.move_right = False
                elif event.key == settings.SOFT_DROP_BUTTON:
                    game.current_block.move_down = False
                elif event.key == settings.PAUSE_BUTTON:
                    game.toggle_pause()
            elif event.type == FALL_BLOCK_EVENT and not game.gameover and not game.paused and game.current_block.block:
                game.current_block.block.fall()

        if game.is_countdown():
            game.countdown()
        elif game is not None:
            if not game.gameover:
                if game.current_block.block and game.current_block.block.touched_the_ground and \
                        game.BLOCK_ANCHOR.is_time():
                    game.current_block.block.hard_drop(False)
                game.render_and_update()
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

    elif program_state == Constants.PROFILE:
        if profile is None:
            profile = Profile()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    program_state = Constants.MAIN_MENU
                    profile = None

        if profile is not None:
            profile.render()

    elif program_state == Constants.SHOP:
        if shop is None:
            shop = Shop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    program_state = Constants.MAIN_MENU
                    shop = None

        if shop is not None:
            shop.render()

    elif program_state == -1:
        terminate()

    clock.tick(Constants.FPS)
    pygame.display.update()
