from mesa.agent import Agent
import random

class TrendAgent(Agent):
    def __init__(self, unique_id, model, agent_type, color, initial_word=None):
        self.unique_id = unique_id
        self.model = model
        self.agent_type = agent_type
        self.color = color
        self.memory = []
        if initial_word:
            self.memory.append(initial_word)
        self.timer = 0
        self.pos = None

    def step(self):
        self.move()
        self.check_collisions()
        if self.agent_type == "forgetful":
            self.timer += 1

    def move(self):
        dx = random.uniform(-3, 3)
        dy = random.uniform(-3, 3)
        x, y = self.pos
        width, height = self.model.space.width, self.model.space.height
        self.pos = ((x + dx) % width, (y + dy) % height)

    def check_collisions(self):
        for other in self.model.agents_list:
            if other is self:
                continue
            if self.in_collision_range(other):
                self.interact(other)

    def in_collision_range(self, other):
        dist = (
            (self.pos[0] - other.pos[0]) ** 2 + (self.pos[1] - other.pos[1]) ** 2
        ) ** 0.5
        return dist < 10  # 半径5ずつ想定で10以内を衝突とする

    def interact(self, other):
        if not other.memory:
            return

        # 　現在の単語の認知度（昇順)
        word_counts = self.model.word_counts
        min_word_counts = sorted(word_counts.items(), key=lambda x: x[1])
        min_word_counts_keys = [item[0] for item in min_word_counts]

        # agentモデル生成
        if self.agent_type == "general":
            for word in other.memory:
                if word not in self.memory:
                    self.memory.append(word)
        # 忘却型
        # 一定時間経過後先頭から順に削除
        if self.agent_type == "forgetful":
            for word in other.memory:
                if word not in self.memory:
                    self.memory.append(word)
            if self.timer >= 5:
                if self.memory != []:
                    del self.memory[-1]
                    self.timer = 0
        # 固執型
        # はじめの衝突時のみ先頭単語だけを記憶する
        if self.agent_type == "persistent":
            if self.memory == []:
                word = other.memory[0]
                self.memory.append(word)

        # 逆張り型
        # 現状最も認知度が低い単語かつ衝突相手が覚えている単語だけを覚える
        if self.agent_type == "contrarian":
            if self.memory == []:
                for word in min_word_counts_keys:
                    if word in other.memory and word not in self.memory:
                        self.memory.append(word)
                        break
        # 大衆迎合型
        # 現状最も認知度が高い単語かつ衝突相手が覚えている単語だけを覚える
        if self.agent_type == "mass_follower":
            if self.memory == []:
                max_word_counts_keys = min_word_counts_keys[::-1]
                for word in max_word_counts_keys:
                    if word in other.memory and word not in self.memory:
                        self.memory.append(word)
                        break

        # 重複排除
        self.memory = list(set(self.memory))
