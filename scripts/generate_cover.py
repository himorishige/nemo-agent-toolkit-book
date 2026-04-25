"""Zenn Book のカバー画像を生成する.

NVIDIA グリーン (#76B900) を基調に、タイトルのみをシンプルに配置.
出力サイズは Zenn 公式推奨の 500x700.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUTPUT = Path(__file__).resolve().parent.parent / "cover.png"

WIDTH = 500
HEIGHT = 700

NVIDIA_GREEN = (118, 185, 0)  # #76B900
NVIDIA_DARK = (15, 17, 18)  # #0F1112 - ほぼ黒、NVIDIA 公式 dark
WHITE = (255, 255, 255)
ACCENT = (174, 232, 0)  # 明るめの緑アクセント

FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def draw_title(draw: ImageDraw.ImageDraw) -> None:
    """タイトルを 4 行に分けて中央配置.

    "NeMo Agent Toolkit" は 1 行に収まる最大サイズで強調.
    """
    title_lines = [
        ("クラウド NIM +", 36),
        ("Docker ではじめる", 36),
        ("NeMo Agent Toolkit", 40),
        ("ハンズオン", 36),
    ]

    fonts = [ImageFont.truetype(FONT_PATH, size=size, index=2) for _, size in title_lines]
    line_heights = []
    for line, font in zip(title_lines, fonts, strict=True):
        bbox = font.getbbox(line[0])
        line_heights.append(bbox[3] - bbox[1])

    line_gap = 24
    total_height = sum(line_heights) + line_gap * (len(title_lines) - 1)

    y = (HEIGHT - total_height) // 2 - 30

    for (text, _), font, h in zip(title_lines, fonts, line_heights, strict=True):
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2 - bbox[0]
        draw.text((x, y - bbox[1]), text, font=font, fill=NVIDIA_DARK)
        y += h + line_gap


def draw_accents(draw: ImageDraw.ImageDraw) -> None:
    """上下のアクセント帯と細い罫線."""
    # 上部の細い NVIDIA グリーン帯
    draw.rectangle([(0, 0), (WIDTH, 8)], fill=NVIDIA_GREEN)
    # 下部の同じ帯
    draw.rectangle([(0, HEIGHT - 8), (WIDTH, HEIGHT)], fill=NVIDIA_GREEN)

    # 中央上部の小さなアクセントライン（タイトル直下に）
    line_y = HEIGHT - 110
    line_w = 80
    draw.rectangle(
        [((WIDTH - line_w) // 2, line_y), ((WIDTH + line_w) // 2, line_y + 4)],
        fill=NVIDIA_GREEN,
    )


def draw_subtitle(draw: ImageDraw.ImageDraw) -> None:
    """下部の小さなサブテキスト（NAT バージョンのみ）."""
    font_small = ImageFont.truetype(FONT_PATH, size=18, index=2)

    sub = "NVIDIA NeMo Agent Toolkit 1.6.0"
    bbox = font_small.getbbox(sub)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) // 2 - bbox[0]
    y = HEIGHT - 75
    draw.text((x, y - bbox[1]), sub, font=font_small, fill=NVIDIA_GREEN)


def main() -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)

    draw_accents(draw)
    draw_title(draw)
    draw_subtitle(draw)

    img.save(OUTPUT, "PNG", optimize=True)
    print(f"Saved: {OUTPUT} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
