import pygame, random
import sys, os


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        sheet = pygame.transform.scale(sheet, (512, 128))
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def load_image(name, colorkey=None):
    fullname = os.path.join("sprites", name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet):
        super().__init__(all_sprites)
        pl_image = sheet
        pl_image = pygame.transform.scale(pl_image, (64, 64))
        self.image = pl_image
        self.rect = self.image.get_rect()
        self.rect.x = 240
        self.rect.y = 200

    def move(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect.y = -self.rect.y
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect.x = -self.rect.x
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.rect.y -= 10
            elif event.key == pygame.K_DOWN:
                self.rect.y += 10
            elif event.key == pygame.K_RIGHT:
                self.rect.x += 10
            elif event.key == pygame.K_LEFT:
                self.rect.x -= 10


class MainMenu:
    def __init__(self):
        width = 1280
        height = 720
        Border(5, 5, width - 5, 5)
        Border(5, height - 5, width - 5, height - 5)
        Border(5, 5, 5, height - 5)
        Border(width - 5, 5, width - 5, height - 5)

    def render(self, screen):
        # main_char = AnimatedSprite(load_image("main_char.png"), 4, 1, 32, 32)
        # main_char.rect.x = 240
        # main_char.rect.y = 200

        play_image = load_image("play.png")
        play_image = pygame.transform.scale(play_image, (500, 500))
        play = pygame.sprite.Sprite(all_sprites, text_sprite)
        play.image = play_image
        play.rect = play.image.get_rect()
        play.rect.x = 360
        play.rect.y = 200

        pyg_image = load_image("pygame.png")
        pyg_image = pygame.transform.scale(pyg_image, (500, 500))
        pyg = pygame.sprite.Sprite(all_sprites, text_sprite)
        pyg.image = pyg_image
        pyg.rect = pyg.image.get_rect()
        pyg.rect.x = 360
        pyg.rect.y = 0


class Board:
    def __init__(self):
        self.width = 42
        self.height = 23
        self.board = [[0] * 42 for _ in range(23)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size, self.cell_size), 1)


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    text_sprite = pygame.sprite.Group()
    clock = pygame.time.Clock()
    FPS = 30
    screen = pygame.display.set_mode((1280, 720))
    main = MainMenu()
    board = Board()
    player = Player(load_image("main_char1.png"))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(FPS)
        screen.fill((70, 89, 70))
        all_sprites.draw(screen)
        main.render(screen)
        player.move()
        pygame.display.flip()
    pygame.quit()
