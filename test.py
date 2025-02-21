from manim import *

# 自定义 TexTemplate
ctex = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    preamble=r"""
        \usepackage[english]{babel}
        \usepackage[utf8]{inputenc}
        \usepackage[T1]{fontenc}
        \usepackage{lmodern}
        \usepackage{amsmath}
        \usepackage{amssymb}
        \usepackage{dsfont}
        \usepackage{setspace}
        \usepackage{tipa}
        \usepackage{relsize}
        \usepackage{textcomp}
        \usepackage{mathrsfs}
        \usepackage{calligra}
        \usepackage{wasysym}
        \usepackage{ragged2e}
        \usepackage{physics}
        \usepackage{xcolor}
        \usepackage{microtype}
        \usepackage[UTF8]{ctex}
        % 设置默认字体为 MapleMono
        % 设置中文字体为 MiSans
        \setCJKmainfont{MapleMono}
        \setCJKsansfont{MapleMono}
        \setCJKmonofont{MapleMono}

        % 设置西文字体为 MiSans（可选）
        \setmainfont{MiSans}
        \setsansfont{MiSans}
        \setmonofont{MiSans}
        \linespread{1}
    """
)

class QuestionScene(Scene):
    def construct(self):
        t1 = Tex(
            r"$E=mc^2$321哒哒哒哒哒答案是大哒哒哒哒哒哒答案是大哒哒哒哒哒哒答案是大哒哒哒哒哒哒哒答案是大哒哒哒哒哒哒答案是大哒哒哒哒哒哒答案是大哒哒哒哒哒哒答案是大哒哒哒哒哒哒答案是大哒哒哒哒哒哒答案是大",
            font_size=20,
            tex_template=ctex,  # 使用自定义模板
            tex_environment="minipage}{22cm"  # 设置 minipage 宽度为 10cm
        )
        self.play(Write(t1))
        self.wait()