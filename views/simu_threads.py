# main.pyのFlask用
import threading
import time
import pygame
from common.config import SETTINGS
from common.model import TrendModel
from common.plotter import Plotter
from views.share_config import simulation_config
from flask import session, has_request_context
import os

def simulation_loop():
    pygame.init()
    screen = pygame.display.set_mode((SETTINGS["width"], SETTINGS["height"]))
    pygame.display.set_caption("流行語シミュレータ")
    clock = pygame.time.Clock()

    initial_agents = SETTINGS.get("initial_agents", {})
    try:
        if has_request_context() and "initial_agents" in session:
            initial_agents = session["initial_agents"]
    except Exception:
        pass

    config = dict(SETTINGS)
    if "initial_agents" in simulation_config:
        config["initial_agents"] = simulation_config["initial_agents"]

    model = TrendModel(config)
    plot = Plotter(model.word_counts.keys())
    font = pygame.font.SysFont(None, 24)

    last_save_time = time.time()
    running = True
    while running:
        # pygameが強制終了しないように
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        for agent in model.agents_list:
            x, y = agent.pos
            pygame.draw.circle(screen, agent.color, (int(x), int(y)), 5)
            mem_text = ",".join(agent.memory[-3:])
            text_surface = font.render(mem_text, True, (0, 0, 0))
            screen.blit(
                text_surface, (int(x) - text_surface.get_width() // 2, int(y) - 20)
            )
        y_offset = 10
        for word, count in model.word_counts.items():
            text = font.render(f"{word}: {count}", True, (0, 0, 0))
            screen.blit(text, (10, y_offset))
            y_offset += 20

        model.step()
        plot.update(model.word_counts)
        plot.draw()

        pygame.display.flip()
        clock.tick(30)

        # 1秒ごとにグラフ画像を保存
        now = time.time()
        if now - last_save_time > 1.0:
            plot.fig.savefig(os.path.join("static", "graph.png"))
            last_save_time = now

    pygame.quit()
    plot.close()

def start_simulation_thread():
    sim_thread = threading.Thread(target=simulation_loop, daemon=True)
    sim_thread.start()