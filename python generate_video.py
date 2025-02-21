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
paper_questions_df = pd.read_excel(file_path, sheet_name='paper_questions')
papers_df = pd.read_excel(file_path, sheet_name='papers')
categories_df = pd.read_excel(file_path, sheet_name='categories')  # 读取分类表

# 选择题目 ID
question_id = 15  # 直接指定题目 ID

# 获取题目信息
question_info = questions_df[questions_df['id'] == question_id].iloc[0]
content = question_info['content']
difficulty = question_info['difficulty']
answer = question_info['answer']
explanation = question_info['explanation']
question_type = question_info['type']  # 获取题目类型
category_id = question_info['category_id']  # 获取分类 ID

# 通过分类 ID 获取分类名称
category_name = categories_df[categories_df['id'] == category_id]['name'].values[0]
# 通过 paper_questions 表找到试卷 ID
paper_id = paper_questions_df[paper_questions_df['question_id'] == question_id]['paper_id'].values[0]
# 通过试卷 ID 找到试卷标题
paper_title = papers_df[papers_df['id'] == paper_id]['title'].values[0]

# 定义缓存目录
cache_dir = "media/cache"
os.makedirs(cache_dir, exist_ok=True)

# 解析文本中的图片链接
pattern = r"!\[.*?\]\((https?://.*?)\)"
matches = re.findall(pattern, content)

# 下载图片并保存到本地
image_objects = {}
for image_url in matches:
    image_name = image_url.split("/")[-1].split("?")[0]  # 提取图片文件名
    image_path = os.path.join(cache_dir, image_name)
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
    image_objects[image_url] = image_path

# 替换 content 中的图片链接为本地路径
for image_url, image_path in image_objects.items():
    content = content.replace(image_url, image_path)

class QuestionScene(Scene):
    def construct(self):
        # 创建题干内容组
        stem_group = Group()
        # 创建选项内容组（仅用于选择题）
        options_group = Group()
        # 图片路径正则表达式
        local_image_pattern = r"!\[(.*?)\]\((media/cache/.*?)\)"

        # 按行分割内容
        lines = content.split('\n')

        # 分离题干和选项
        stem_lines = []
        option_lines = []

        if question_type == "选择题":
            # 对于选择题，分离题干和选项
            is_option = False
            for line in lines:
                if line.strip().startswith(("A.", "B.", "C.", "D.")):
                    is_option = True
                if is_option:
                    option_lines.append(line)
                else:
                    stem_lines.append(line)
        else:
            # 对于其他题型，所有内容都是题干
            stem_lines = lines

        # 处理题干内容
        for line in stem_lines:
            line = line.strip()  # 去掉首尾空白字符
            if not line:  # 如果是空行，跳过
                continue

            local_matches = re.findall(local_image_pattern, line)
            if local_matches:
                # 如果有图片，直接处理图片
                for match in local_matches:
                    image_path = match[1].strip()  # 获取图片路径
                    if os.path.exists(image_path):
                        image_obj = ImageMobject(image_path).scale(0.3)
                        stem_group.add(image_obj)
                    else:
                        print(f"警告：图片路径不存在 - {image_path}")
            else:
                # 如果没有图片，直接添加文本
                text_obj = Tex(line, tex_template=TexTemplateLibrary.ctex, font_size=20, tex_environment="minipage}{23cm")
                stem_group.add(text_obj)

        # 处理选项内容（仅选择题）
        if question_type == "选择题":
            for line in option_lines:
                local_matches = re.findall(local_image_pattern, line)
                for match in local_matches:
                    image_path = match[1].strip()  # 获取图片路径
                    if os.path.exists(image_path):
                        image_obj = ImageMobject(image_path).scale(0.3)
                        option_text = line.split("!")[0].strip()  # 提取选项文本（A、B、C、D）
                        text_obj = Tex(option_text, tex_template=TexTemplateLibrary.ctex, font_size=20)
                        option_group = Group(text_obj, image_obj).arrange(RIGHT, buff=0.2)
                        options_group.add(option_group)
                        line = line.replace(f"![]({image_path})", "")  # 移除图片标记
                    else:
                        print(f"警告：图片路径不存在 - {image_path}")

        # 排列题干和选项
        stem_group.arrange(DOWN,buff=0.2)
        if question_type == "选择题":
            options_group.arrange(RIGHT)
            options_group.next_to(stem_group, DOWN, buff=0.5)

        # 添加试卷来源和难度信息
        source_text = Tex(f"来源: {paper_title}", tex_template=TexTemplateLibrary.ctex, font_size=20).to_corner(UL)
        difficulty_text = Tex(f"难度: {difficulty}", tex_template=TexTemplateLibrary.ctex, font_size=20).to_corner(UP)
        category_text = Tex(f"分类: {category_name}", tex_template=TexTemplateLibrary.ctex, font_size=20).to_corner(UR)

        # 题干放在难度的下面
        stem_group.next_to(difficulty_text, DOWN)

        # 选项放在题干的下面
        options_group.next_to(stem_group, DOWN, buff=0.2)

        # 答案和解析
        answer_text = Tex(f"答案: {answer}", tex_template=TexTemplateLibrary.ctex, font_size=20).next_to(options_group, DOWN, buff=0.2)
        explanation_text = Tex(f"解析: {explanation}", tex_template=TexTemplateLibrary.ctex, font_size=20, tex_environment="minipage}{23cm").next_to(answer_text, DOWN, buff=0.2)
    
        # 添加所有内容到场景
        self.add(source_text, difficulty_text, stem_group, options_group, answer_text, explanation_text,category_text)

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