import pygame
from config import SETTINGS
from model import TrendModel
from plotter import Plotter

WIDTH, HEIGHT = SETTINGS["width"], SETTINGS["height"]
FPS = 120


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("流行語シミュレータ")
    clock = pygame.time.Clock()

    model = TrendModel(SETTINGS)
    plot = Plotter(model.word_counts.keys())

    running = True
    font = pygame.font.SysFont(None, 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # 描画
        screen.fill((255, 255, 255))
        for agent in model.agents_list:
            x, y = agent.pos
            pygame.draw.circle(screen, agent.color, (int(x), int(y)), 5)
            # エージェントの頭上にメモリリストを表示
            mem_text = ",".join(agent.memory[-3:])
            text_surface = font.render(mem_text, True, (0, 0, 0))
            screen.blit(
                text_surface, (int(x) - text_surface.get_width() // 2, int(y) - 20)
            )

        # 単語カウントの表示
        y_offset = 10
        for word, count in model.word_counts.items():
            text = font.render(f"{word}: {count}", True, (0, 0, 0))
            screen.blit(text, (10, y_offset))
            y_offset += 20

        model.step()
        plot.update(model.word_counts)
        plot.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    plot.close()


if __name__ == "__main__":
    main()
