import matplotlib.pyplot as plt
import os


class Smoother:
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.values = []
        self.moving_averaged_values = []
        self.presum_values = []

    def update(self, new_value):
        self.values.append(new_value)
        if len(self.presum_values) == 0:
            self.presum_values.append(new_value)
        else:
            self.presum_values.append(self.presum_values[-1] + new_value)
        self.moving_averaged_value = self.calculate_moving_average()
        self.moving_averaged_values.append(self.moving_averaged_value)

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
            if value == min(other_values):
                min_values.append((i, value))
        return min_values

    def plot(self, output_dir):
        plt.figure(figsize=(10, 6), facecolor="lightgray")
        plt.scatter(
            range(len(self.values)),
            self.values,
            label="Raw",
            marker="o",
            color="blue",
            alpha=0.7,
            s=50,
        )

        # 绘制移动平均数据的折线图
        plt.plot(
            range(len(self.moving_averaged_values)),
            self.moving_averaged_values,
            label="Moving Average",
            marker="x",
            linestyle="-",
            color="red",
            linewidth=1.5,  # 使用更细的线条
        )

        # 添加标题和轴标签
        plt.xlabel("Step", fontsize=12, fontfamily="serif")  # 使用更清晰的字体
        plt.ylabel("Value", fontsize=12, fontfamily="serif")  # 使用更清晰的字体
        plt.title(
            "Moving Average Smoothing", fontsize=14, fontfamily="serif"
        )  # 使用更清晰的字体

        # 添加图例
        plt.legend(
            loc="upper left", bbox_to_anchor=(1, 1), fontsize=10
        )  # 将图例放置在图表外部

        # 添加网格
        plt.grid(True, linestyle="--", alpha=0.5)  # 使用更细的网格线

        plt.xlabel("Step")
        plt.ylabel("Value")
        plt.title("Moving Average Smoothing")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, "moving_average_smoothing.png"), dpi=300)
