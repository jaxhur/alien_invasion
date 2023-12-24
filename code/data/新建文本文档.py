import pandas as pd
from PIL import Image, ImageDraw, ImageFont


df = pd.read_csv('./data/history_score.csv')[-5:]
last_5_rows = df.tail(5)

# 创建图像
img_size = (300,200)
img_bg = (255, 255, 255, 0)
image = Image.new('RGBA', img_size ,img_bg)
draw = ImageDraw.Draw(image)

font_size = 20
font = ImageFont.truetype("./素材/font/2.ttf", font_size)
font_color = (72,209,204,255)  # 完全不透明

# 最高分
draw.text((10, 0), f"最高分\t\t{df.columns[0]:^} \t\t\t\t {df.columns[1]:>7} ",fill=font_color, font=font)
draw.text((10, 25), f"{df.loc[df['score'].idxmax()]['time']:^} {df.loc[df['score'].idxmax()]['score']:>7} ",fill=font_color, font=font)

# 最近5局
draw.text((10, 55), f"最近5局\t{df.columns[0]:^} \t\t\t\t {df.columns[1]:>7} ",fill=font_color, font=font)
text_y = 75
for _, row in last_5_rows.iterrows():
    text = f"{row['time']:^} {row['score']:>7} "  # 根据实际列名修改
    draw.text((10, text_y), text,fill=font_color, font=font)
    text_y += font_size + 5
# 保存图像
image.save('./素材/img/history_score.png', quality=95)