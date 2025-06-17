import pygame
import random

# フォント初期化（グローバル）
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 14)


class WordAgent:
    def __init__(self, pos, color, memory):
        self.x, self.y = pos
        self.color = color
        self.memory = memory

        # 速度ベクトル
        self.vx = random.uniform(-2.0, 2.0)  # ← 値を大きくすると移動量UP
        self.vy = random.uniform(-2.0, 2.0)

    def move(self, width, height):
        self.x += self.vx
        self.y += self.vy

        # 壁バウンド（端にぶつかったら反射）
        if self.x <= 0 or self.x >= width:
            self.vx *= -1
        if self.y <= 0 or self.y >= height:
            self.vy *= -1

        self.pos = (self.x, self.y)

    def draw(self, screen, font):
        x, y = self.pos
        pygame.draw.circle(screen, self.color, (int(x), int(y)), 5)

        # 表示する単語
        mem_text = ",".join(self.memory)
        text_surface = font.render(mem_text, True, (0, 0, 0))
        screen.blit(text_surface, (int(x) - text_surface.get_width() // 2, int(y) - 20))
