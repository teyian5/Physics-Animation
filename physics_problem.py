from manim import *

class PhysicsProblemExplanation(Scene):
    def construct(self):
        # 创建题目文本
        problem_text = Text("题目：一个质点做直线运动，下列描述其位移$x$或速度$v$随时间$t$变化的图像中，可能正确的是（  ）", font_size=24)
        problem_text.to_edge(UP)

        # 创建选项文本
        option_a = Text("A. 图像A", font_size=20)
        option_b = Text("B. 图像B", font_size=20)
        option_c = Text("C. 图像C", font_size=20)
        option_d = Text("D. 图像D", font_size=20)

        # 将选项文本排列在下方
        options = VGroup(option_a, option_b, option_c, option_d)
        options.arrange(DOWN, aligned_edge=LEFT)
        options.next_to(problem_text, DOWN, buff=1)

        # 显示题目和选项
        self.play(Write(problem_text))
        self.play(FadeIn(options))

        # 解释正确答案
        explanation_text = Text("正确答案是 C，因为...", font_size=24)
        explanation_text.next_to(options, DOWN, buff=1)

        self.play(Write(explanation_text))
        self.wait(2)

# 运行脚本
if __name__ == "__main__":
    scene = PhysicsProblemExplanation()
    scene.render()