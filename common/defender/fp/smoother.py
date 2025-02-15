import matplotlib.pyplot as plt
import os


class Smoother:
    def __init__(self, window_size=200):
        self.window_size = window_size
        self.values = []
        self.moving_averaged_values = []

    def update(self, new_value):
        self.values.append(new_value)
        self.moving_averaged_value = self.calculate_moving_average()
        self.moving_averaged_values.append(self.moving_averaged_value)
        min_values = self.find_min(self.values)
        if len(min_values) > 0:
            return True
        return False

    def calculate_moving_average(self):
        if len(self.values) < self.window_size:
            return sum(self.values) / len(self.values)
        else:
            return sum(self.values[-self.window_size :]) / self.window_size

    def find_min(self, values, window_size=100):
        min_values = []
        for i, value in enumerate(values):
            if i < window_size or i >= len(values) - window_size:
                continue
            other_values = values[
                max(0, i - window_size) : min(len(values), i + window_size)
            ]
            if value == min(other_values) and value < 0:
                min_values.append((i, value))
        return min_values

    def plot(self, output_dir):
        plt.figure(figsize=(10, 6))
        plt.plot(self.values, label="raw", marker="o")
        plt.plot(self.moving_averaged_values, label="moving average", marker="x")
        plt.xlabel("Step")
        plt.ylabel("Value")
        plt.title("Moving Average Smoothing")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, "moving_average_smoothing.png"), dpi=300)
