from mesa import Model
from mesa.space import ContinuousSpace
from collections import defaultdict
from agent import TrendAgent
import random


class TrendModel(Model):
    def __init__(self, config):
        super().__init__(seed=config.get("seed"))
        self.config = config
        self.space = ContinuousSpace(config["width"], config["height"], torus=True)
        self.word_counts = defaultdict(int)
        self.uid_counter = 0
        self.agents_list = []

        self.init_agents()

    def init_agents(self):
        for word, count in self.config["initial_agents"].items():
            for _ in range(count):
                agent_type = "initial"
                color = self.config["agent_colors"][agent_type]
                agent = TrendAgent(self.uid_counter, self, agent_type, color, word)
                pos = self.random_position()
                self.space.place_agent(agent, pos)
                self.agents_list.append(agent)
                self.uid_counter += 1

        for _ in range(self.config["general_agents"]):
            self.agent_process("general")

        for _ in range(self.config["persistent_agents"]):
            self.agent_process("persistent")

        for _ in range(self.config["forgetful_agents"]):
            self.agent_process("forgetful")

        for _ in range(self.config["contrarian_agents"]):
            self.agent_process("contrarian")

    def agent_process(self, agent_type):
        color = self.config["agent_colors"][agent_type]
        agent = TrendAgent(self.uid_counter, self, agent_type, color)
        pos = self.random_position()
        self.space.place_agent(agent, pos)
        self.agents_list.append(agent)
        self.uid_counter += 1

    def random_position(self):
        return (
            random.uniform(0, self.space.width),
            random.uniform(0, self.space.height),
        )

    def step(self):
        self.word_counts.clear()
        for agent in self.agents_list:
            for word in agent.memory:
                self.word_counts[word] += 1

        random.shuffle(self.agents_list)
        for agent in self.agents_list:
            agent.step()
