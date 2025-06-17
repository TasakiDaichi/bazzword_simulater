import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

class Plotter:
    def __init__(self, initial_words):
        self.fig, self.ax = plt.subplots()
        self.word_history = {word: [] for word in initial_words}

    def update(self, word_counts):
        for word in word_counts:
            if word not in self.word_history:
                self.word_history[word] = []
        for word in self.word_history:
            self.word_history[word].append(word_counts.get(word, 0))

    def draw(self):
        self.ax.clear()
        for word, history in self.word_history.items():
            self.ax.plot(history, label=word)
        self.ax.set_title("buzzword")
        self.ax.set_xlabel("Step")
        self.ax.set_ylabel("Count")
        self.ax.legend()
        plt.pause(0.01)

    def close(self):
        plt.ioff()
