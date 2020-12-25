import sys
import pygame


class Constants:
    I, J, L, O, S, T, Z = 1, 2, 3, 4, 5, 6, 7
    SIDE_LENGTH = 30
    WINDOW_SIZE = (400, 650)
    BOARD_TOPLEFT = (50, 20)
    BOARD_SIZE = (10, 20)
    MAX_VOLUME = 0.5
    FALL_TIME = 2000


class Settings:
    AUDIO_VOLUME = 100
    MUSIC_VOLUME = 100

    def set_audio_volume(self, value):
        self.AUDIO_VOLUME = value

    def get_audio_volume(self):
        return self.AUDIO_VOLUME


pygame.mixer.pre_init()
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(Constants.WINDOW_SIZE)


class Board:
    audio_single = pygame.mixer.Sound('audio/single.wav')
    audio_double = pygame.mixer.Sound('audio/double.wav')
    audio_triple = pygame.mixer.Sound('audio/triple.wav')
    audio_tetris = pygame.mixer.Sound('audio/tetris.wav')

    def __init__(self, side_length, topleft):
        self.board = list()
        self.init_board()
        self.topleft_x, self.topleft_y = topleft
        self.side_length = side_length

    def init_board(self):
        for i in range(Constants.BOARD_SIZE[1]):
            line = list()
            for j in range(Constants.BOARD_SIZE[0]):
                line.append(0)
            self.board.append(line)

    def draw_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(screen, (119, 136, 153),
                                 (self.topleft_x + self.side_length * j, self.topleft_y + self.side_length * i,
                                  self.side_length, self.side_length), 1 if self.board[i][j] == 0 else 0)

    def get_line(self, position, length, height):
        try:
            return self.board[position[1] + height][position[0]:position[0] + length]
        except IndexError:
            return [1 for _ in range(length)]

    def anchor_block(self, position, block_pattern):
        for i in range(len(block_pattern)):
            for j in range(len(block_pattern[i])):
                self.board[position[1] + i][position[0] + j] = block_pattern[i][j]
        self.check_lines()

    def check_lines(self):
        lines = list()
        for line in range(len(self.board)):
            if 0 not in self.board[line]:
                lines.append(line)
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
            cursor = line
            while cursor > 0:
                self.board[cursor] = self.board[cursor - 1]
                cursor -= 1


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
    audio_move.set_volume(Constants.MAX_VOLUME)
    audio_rotate.set_volume(Constants.MAX_VOLUME)
    audio_hard_drop.set_volume(Constants.MAX_VOLUME)
    audio_soft_drop.set_volume(Constants.MAX_VOLUME)

    def __init__(self):
        self.status = 0
        self.position = [4, 0]

    def draw(self):
        screen.blit(self.get_sprite(), (Constants.BOARD_TOPLEFT[0] + Constants.SIDE_LENGTH * self.position[0],
                                        Constants.BOARD_TOPLEFT[1] + Constants.SIDE_LENGTH * self.position[1]))

    def get_sprite(self):
        pass

    def move_left(self):
        if self.position[0] > 0:
            self.position[0] -= 1
        self.audio_move.play()

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
        self.audio_hard_drop.play()
        self.anchor()

    def check_bottom(self):
        pass

    def anchor(self):
        pass


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
        self.audio_rotate.play()

    def move_right(self):
        if self.status == 1 and self.position[0] < Constants.BOARD_SIZE[0] - 4:
            self.position[0] += 1
        elif self.status == 0 and self.position[0] < Constants.BOARD_SIZE[0] - 1:
            self.position[0] += 1
        self.audio_move.play()

    def get_sprite(self):
        if self.status == 0:
            return self.sprite.image
        elif self.status == 1:
            return pygame.transform.rotate(self.sprite.image, 90)

    def check_bottom(self):
        if self.status == 0:
            if self.position[1] >= Constants.BOARD_SIZE[1] - 4:
                return False
            length = 1
            height = 4
        else:
            if self.position[1] >= Constants.BOARD_SIZE[1] - 1:
                return False
            length = 4
            height = 1
        if sum(board.get_line(self.position, length, height)) == 0:
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

    def anchor(self):
        board.anchor_block(self.position, self.get_pattern())
        global current_block
        current_block = None


class BlockJ(Block):
    def __init__(self):
        super().__init__()
        self.sprite = self.sprite_J

    def rotate(self):
        if self.status in (1, 3):
            if self.position[0] == Constants.BOARD_SIZE[0] - 2:
                self.position[0] = Constants.BOARD_SIZE[0] - 3

        self.status += 1
        self.status = self.status % 4
        self.audio_rotate.play()

    def move_right(self):
        if self.status in (1, 3):
            if self.position[0] < Constants.BOARD_SIZE[0] - 2:
                self.position[0] += 1
        elif self.status in (0, 2):
            if self.position[0] < Constants.BOARD_SIZE[0] - 3:
                self.position[0] += 1

    def get_sprite(self):
        if self.status == 0:
            return self.sprite.image
        elif self.status == 1:
            return pygame.transform.rotate(self.sprite.image, 90)
        elif self.status == 2:
            return pygame.transform.rotate(self.sprite.image, 180)
        elif self.status == 3:
            return pygame.transform.rotate(self.sprite.image, 270)


class BlockL(Block):
    pass


class BlockO(Block):
    pass


class BlockS(Block):
    pass


class BlockT(Block):
    pass


class BlockZ(Block):
    pass


board = Board(Constants.SIDE_LENGTH, Constants.BOARD_TOPLEFT)
current_level = 1

current_block = None

FALL_BLOCK_EVENT = pygame.USEREVENT
pygame.time.set_timer(FALL_BLOCK_EVENT, Constants.FALL_TIME // current_level)

pygame.mixer.music.load('music/main_theme.ogg')
pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_block.move_left()
            elif event.key == pygame.K_RIGHT:
                current_block.move_right()
            elif event.key == pygame.K_UP:
                current_block.rotate()
            elif event.key == pygame.K_SPACE:
                current_block.hard_drop()
            elif event.key == pygame.K_DOWN:
                current_block.fall()
        elif event.type == FALL_BLOCK_EVENT:
            current_block.fall()

    if current_block is None:
        current_block = BlockI()

    screen.fill('black')
    board.draw_board()
    current_block.draw()

    clock.tick(30)
    pygame.display.update()
