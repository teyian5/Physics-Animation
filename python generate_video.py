import pandas as pd
from manim import *

# 读取 Excel 文件
file_path = '/Users/gean/Downloads/Teyian (3).xlsx'
questions_df = pd.read_excel(file_path, sheet_name='questions')

# 选择题目 ID
question_id = int(input("请输入题目 ID: "))

# 获取题目信息
question_info = questions_df[questions_df['id'] == question_id].iloc[0]
content = question_info['content']
difficulty = question_info['difficulty']
answer = question_info['answer']
explanation = question_info['explanation']

# 定义 Manim 场景
class QuestionScene(Scene):
    def construct(self):
        # 创建文本对象
        content_text = Text(content, font_size=24).to_edge(UP)
        difficulty_text = Text(f"难度: {difficulty}", font_size=20).next_to(content_text, DOWN)
        answer_text = Text(f"答案: {answer}", font_size=20).next_to(difficulty_text, DOWN)
        explanation_text = Text(f"解析: {explanation}", font_size=20).next_to(answer_text, DOWN)

        # 添加文本到场景
        self.play(Write(content_text))
        self.play(Write(difficulty_text))
        self.play(Write(answer_text))
        self.play(Write(explanation_text))
        self.wait(5)

# 生成 16:9 视频
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 30
config.output_file = f"question_{question_id}_16_9.mp4"
scene = QuestionScene()
scene.render()

# 生成 9:16 视频
config.pixel_height = 1920
config.pixel_width = 1080
config.output_file = f"question_{question_id}_9_16.mp4"
scene = QuestionScene()
scene.render()

print(f"视频已生成: question_{question_id}_16_9.mp4 和 question_{question_id}_9_16.mp4")