import pandas as pd
from manim import *
import requests
from PIL import Image
from io import BytesIO
import re
import os

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

# 定义缓存目录
cache_dir = "media/cache"
os.makedirs(cache_dir, exist_ok=True)

# 解析文本中的图片链接和选项
pattern = r"([A-D]\..*?)\s*!\[.*?\]\((https?://.*?)\)"
matches = re.findall(pattern, content)

# 下载图片并保存到本地
image_objects = {}
for option_text, image_url in matches:
    image_path = os.path.join(cache_dir, f"{option_text.strip()}.png")
    if not os.path.exists(image_path):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image.save(image_path)
                print(f"图片已下载并保存到 {image_path}")
            else:
                print(f"无法下载图片: {image_url}")
        except Exception as e:
            print(f"下载图片时出错: {image_url}, 错误: {e}")
    image_objects[option_text.strip()] = image_path

# 定义 Manim 场景
class QuestionScene(Scene):
    def construct(self):
        # 分离题干和选项
        stem, *options = content.split('\n')

        # 创建题干文本对象
        stem_text = Text(stem, font_size=24).to_edge(UP)
        self.play(Write(stem_text))

        # 询问用户选项排列方式
        print("请选择选项排列方式：")
        print("1. 1行显示所有选项")
        print("2. 2行显示选项")
        option_layout = input("请输入选项排列方式（1/2）：")
        option_layout = int(option_layout) if option_layout in ['1', '2'] else 1

        # 创建选项组
        option_group = Group()
        for option in options:
            # 检查是否包含图片链接
            match = re.match(r"([A-D]\..*?)\s*!\[.*?\]\((.*?)\)", option)
            if match:
                option_text, image_url = match.groups()
                option = option_text  # 移除图片链接部分
                image_path = image_objects.get(option_text.strip())
                if image_path:
                    # 创建文本对象
                    text_obj = Text(option, font_size=24)
                    option_group.add(text_obj)

                    # 创建图片对象
                    image_obj = ImageMobject(image_path).scale(0.5)
                    option_group.add(image_obj)
            else:
                # 创建文本对象
                text_obj = Text(option, font_size=24)
                option_group.add(text_obj)

        # 根据用户选择排列选项
        if option_layout == 1:
            option_group.arrange(RIGHT, buff=0.5).next_to(stem_text, DOWN, buff=0.5)
        elif option_layout == 2:
            option_group.arrange_in_grid(rows=2, cols=2, buff=0.5).next_to(stem_text, DOWN, buff=0.5)

        # 添加选项到场景
        self.play(*[Write(obj) if isinstance(obj, VMobject) else FadeIn(obj) for obj in option_group])

        # 添加难度、答案和解析文本
        difficulty_text = Text(f"难度: {difficulty}", font_size=20).next_to(option_group, DOWN, buff=0.5)
        answer_text = Text(f"答案: {answer}", font_size=20).next_to(difficulty_text, DOWN, buff=0.5)
        explanation_text = Text(f"解析: {explanation}", font_size=20).next_to(answer_text, DOWN, buff=0.5)

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