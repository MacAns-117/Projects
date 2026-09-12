"""Build the Social Buzz insights deck from saved figures + hardcoded stats."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import nsmap
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "reports" / "figures"
OUT = ROOT / "reports" / "Social_Buzz_Insights.pptx"

NAVY = RGBColor(0x1C, 0x28, 0x33)
PURPLE = RGBColor(0x5B, 0x2C, 0x6F)
TEAL = RGBColor(0x1A, 0x7A, 0x6D)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CREAM = RGBColor(0xF7, 0xF5, 0xF2)
GRAY = RGBColor(0x5D, 0x6D, 0x7E)
DARK = RGBColor(0x21, 0x21, 0x21)
GOLD = RGBColor(0xC4, 0x9A, 0x3C)

W, H = Inches(13.333), Inches(7.5)


def _set_run(run, size, bold=False, color=DARK, font="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def add_text(slide, l, t, w, h, text, size=18, bold=False, color=DARK, align=PP_ALIGN.LEFT, font="Calibri"):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    _set_run(run, size, bold, color, font)
    return box


def add_rect(slide, l, t, w, h, fill):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    return sh


def footer(slide, page, total=12):
    add_rect(slide, 0, 7.28, 13.333, 0.22, PURPLE)
    add_text(slide, 0.4, 7.28, 8, 0.22, "Social Buzz  ·  content popularity  ·  Forage / Accenture VE", 10, False, WHITE)
    add_text(slide, 11.6, 7.28, 1.4, 0.22, f"{page} / {total}", 10, False, WHITE, PP_ALIGN.RIGHT)


def kpi(slide, l, t, value, label):
    add_rect(slide, l, t, 2.7, 1.35, WHITE)
    add_rect(slide, l, t, 0.08, 1.35, TEAL)
    add_text(slide, l + 0.2, t + 0.18, 2.4, 0.6, value, 26, True, PURPLE)
    add_text(slide, l + 0.2, t + 0.75, 2.4, 0.45, label, 12, False, GRAY)


def new(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_rect(s, 0, 0, 13.333, 7.5, CREAM)
    return s


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H

    # 1 title
    s = new(prs)
    add_rect(s, 0, 0, 0.22, 7.5, PURPLE)
    add_rect(s, 0, 0, 13.333, 0.12, PURPLE)
    add_text(s, 0.7, 1.7, 12, 0.4, "FORAGE  ·  ACCENTURE VIRTUAL EXPERIENCE", 14, True, TEAL)
    add_text(s, 0.7, 2.15, 12, 1.3, "What people react to\non Social Buzz", 40, True, NAVY)
    add_text(s, 0.7, 4.6, 11, 0.8, "Top 5 content categories by popularity score\n22,534 reactions  ·  962 posts  ·  Jun 2020 – Jun 2021", 18, False, GRAY)
    add_text(s, 0.7, 6.4, 11, 0.4, "Maqsood Ansari  ·  Data Analyst", 16, True, PURPLE)
    footer(s, 1)

    # 2 agenda
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "Agenda", 28, True, WHITE)
    items = [
        ("01", "Brief", "Why Social Buzz asked for a category ranking"),
        ("02", "Data", "What is in the sample and how I cleaned it"),
        ("03", "Top 5", "Popularity score, not raw reaction count"),
        ("04", "Extras", "Sentiment, format, and a quiet month pattern"),
        ("05", "So what", "Three things a content team could try next"),
    ]
    for i, (n, t, d) in enumerate(items):
        y = 1.4 + i * 1.05
        add_rect(s, 0.5, y, 12.3, 0.9, WHITE)
        add_text(s, 0.7, y + 0.18, 1.0, 0.55, n, 22, True, PURPLE)
        add_text(s, 1.8, y + 0.12, 10, 0.35, t, 18, True, NAVY)
        add_text(s, 1.8, y + 0.48, 10, 0.3, d, 14, False, GRAY)
    footer(s, 2)

    # 3 recap
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "Project recap", 28, True, WHITE)
    add_text(s, 0.5, 1.3, 12, 0.7, "Social Buzz is a fast-growing social platform. This Forage brief is a three-month POC story with three workstreams. This analysis is the third one.", 16, False, GRAY)
    cards = [
        ("01", "Big data audit", "How they handle volume. Not this deck."),
        ("02", "IPO readiness", "Process and controls. Not this deck."),
        ("03", "Top 5 categories", "This deck. Score the sample and rank topics."),
    ]
    for i, (n, t, d) in enumerate(cards):
        x = 0.5 + i * 4.2
        add_rect(s, x, 2.3, 3.95, 3.6, WHITE)
        add_rect(s, x, 2.3, 3.95, 0.12, PURPLE if i == 2 else TEAL)
        add_text(s, x + 0.25, 2.6, 3.4, 0.5, n, 20, True, PURPLE)
        add_text(s, x + 0.25, 3.2, 3.4, 0.7, t, 20, True, NAVY)
        add_text(s, x + 0.25, 4.1, 3.4, 1.4, d, 15, False, GRAY)
    footer(s, 3)

    # 4 problem
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "The problem", 28, True, WHITE)
    add_text(s, 0.5, 1.35, 12, 1.0, "The client story is 100,000+ posts a day. That is too much to steer by gut. The ask for this sample is simple: which categories actually get love?", 16, False, GRAY)
    kpis = [
        ("100k+", "posts / day  (client context)"),
        ("22,534", "reactions in this sample"),
        ("16", "categories after cleaning"),
        ("sum of scores", "definition of “popular”"),
    ]
    for i, (v, lab) in enumerate(kpis):
        x = 0.5 + i * 3.2
        add_rect(s, x, 2.6, 3.0, 2.4, WHITE)
        add_text(s, x + 0.15, 2.85, 2.7, 1.0, v, 22, True, PURPLE, PP_ALIGN.CENTER)
        add_text(s, x + 0.15, 4.0, 2.7, 0.7, lab, 13, False, GRAY, PP_ALIGN.CENTER)
    add_text(s, 0.5, 5.3, 12, 1.4, "I do not treat reaction count as popularity. A peek (35) is not a super-love (75). Ranking uses the score table that came with the reaction types.", 16, False, DARK)
    footer(s, 4)

    # 5 data
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "What I used", 28, True, WHITE)
    add_text(s, 0.5, 1.25, 12, 0.7, "Joined Content × Reactions × Reaction types. One row = one reaction. Window: 18 Jun 2020 – 18 Jun 2021.", 16, False, GRAY)
    rows = [
        ("22,534", "reactions (no nulls, no duplicate rows)"),
        ("962", "distinct posts"),
        ("500", "users who reacted"),
        ("16", "categories after stripping quotes and lowercasing"),
        ("4", "formats: photo, video, GIF, audio"),
        ("16", "reaction types, scores 0 to 75"),
    ]
    for i, (v, lab) in enumerate(rows):
        y = 2.1 + (i % 3) * 1.4
        x = 0.5 if i < 3 else 7.0
        add_rect(s, x, y, 5.8, 1.25, WHITE)
        add_text(s, x + 0.25, y + 0.18, 5.3, 0.45, v, 22, True, PURPLE)
        add_text(s, x + 0.25, y + 0.65, 5.3, 0.4, lab, 13, False, GRAY)
    footer(s, 5)

    # 6 process
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "Process", 28, True, WHITE)
    steps = [
        ("1", "Understand", "Read the six-table model. Only Content, Reactions, and scores are needed for the ranking."),
        ("2", "Clean", "Drop unused User/Profile tables. Fix \"animals\" vs Animals. Parse dates day-first."),
        ("3", "Score", "Popularity = sum(Reaction_Score) by category."),
        ("4", "Check", "Compare count vs score, sentiment, format, month."),
        ("5", "Tell", "Five headlines + a short recommendation."),
    ]
    for i, (n, t, d) in enumerate(steps):
        x = 0.4 + i * 2.56
        add_rect(s, x, 1.5, 2.42, 5.1, WHITE)
        add_rect(s, x, 1.5, 2.42, 0.12, PURPLE)
        add_text(s, x + 0.15, 1.8, 2.1, 0.5, n, 28, True, PURPLE)
        add_text(s, x + 0.15, 2.5, 2.1, 0.7, t, 18, True, NAVY)
        add_text(s, x + 0.15, 3.3, 2.1, 2.8, d, 13, False, GRAY)
    footer(s, 6)

    # 7 snapshot numbers
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "Four numbers worth keeping", 28, True, WHITE)
    kpi(s, 0.5, 1.4, "16", "categories (quoted labels merged)")
    kpi(s, 3.5, 1.4, "1,738", "Animals reactions — count, not score")
    kpi(s, 6.5, 1.4, "68,624", "Animals popularity score")
    kpi(s, 9.5, 1.4, "May 2021", "busiest month (1,954 reactions)")
    add_text(s, 0.5, 3.05, 12, 0.5, "The old “1,738 popularity score” figure was the reaction count. Score is ~40× larger.", 15, False, GRAY)
    add_rect(s, 0.5, 3.7, 12.3, 3.0, WHITE)
    add_text(s, 0.75, 3.9, 11.8, 0.4, "Also true in this sample", 16, True, NAVY)
    bullets = [
        "Top 5 share of all score: 36.0%. The tail is long — travel, cooking, culture sit just under Food.",
        "2020 has 12,195 reactions vs 10,339 in 2021. The file is mid-year to mid-year, so this is not a “lockdown year” claim.",
        "May is the peak month, but January is 5 reactions behind. Do not overfit a season story.",
        "56.2% of reactions are positive. That mix is similar inside every top-5 category.",
    ]
    for i, b in enumerate(bullets):
        add_text(s, 0.75, 4.4 + i * 0.5, 11.8, 0.5, "•  " + b, 14, False, DARK)
    footer(s, 7)

    # 8 top 5 chart
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "Top 5 categories by popularity score", 28, True, WHITE)
    s.shapes.add_picture(str(FIG / "top5_score.png"), Inches(0.4), Inches(1.25), Inches(7.6), Inches(5.6))
    add_rect(s, 8.2, 1.4, 4.6, 5.3, WHITE)
    add_text(s, 8.4, 1.6, 4.2, 0.4, "Rank", 14, True, GRAY)
    lines = [
        "1  Animals            68,624",
        "2  Science            65,405",
        "3  Healthy eating     63,138",
        "4  Technology         63,035",
        "5  Food               61,598",
    ]
    for i, line in enumerate(lines):
        add_text(s, 8.4, 2.15 + i * 0.55, 4.2, 0.5, line, 15, True if i == 0 else False, PURPLE if i == 0 else NAVY)
    add_text(s, 8.4, 5.1, 4.2, 1.2, "Healthy eating sits above Food. Science sits above Technology. Gaps inside the top 5 are small.", 13, False, GRAY)
    footer(s, 8)

    # 9 share + full ranking
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "The top 5 are close. The tail is not empty.", 26, True, WHITE)
    s.shapes.add_picture(str(FIG / "top5_share.png"), Inches(0.3), Inches(1.2), Inches(6.3), Inches(5.7))
    s.shapes.add_picture(str(FIG / "score_by_category.png"), Inches(6.6), Inches(1.25), Inches(6.3), Inches(5.6))
    footer(s, 9)

    # 10 extras
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "Two extra cuts", 28, True, WHITE)
    s.shapes.add_picture(str(FIG / "sentiment_top5.png"), Inches(0.3), Inches(1.2), Inches(6.4), Inches(4.0))
    s.shapes.add_picture(str(FIG / "score_by_type.png"), Inches(6.8), Inches(1.2), Inches(6.1), Inches(4.0))
    add_text(s, 0.5, 5.35, 12.3, 1.5, "Sentiment does not explain the ranking — every top category is ~56–58% positive. Format does: photos hold the most total score (241,090). Animals is unusually photo-heavy (35% of its reactions). Technology is more GIF/audio than video.", 15, False, DARK)
    footer(s, 10)

    # 11 month
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "Reactions by month", 28, True, WHITE)
    s.shapes.add_picture(str(FIG / "reactions_by_month.png"), Inches(0.4), Inches(1.2), Inches(12.5), Inches(4.5))
    add_text(s, 0.5, 5.85, 12.3, 1.0, "Peak is May 2021 (1,954). The line is fairly flat — no month is a collapse. I would not sell a “holiday season” campaign off this sample alone.", 15, False, DARK)
    footer(s, 11)

    # 12 summary
    s = new(prs)
    add_rect(s, 0, 0, 13.333, 1.05, NAVY)
    add_text(s, 0.5, 0.28, 12, 0.55, "What I would do with this", 28, True, WHITE)
    recs = [
        ("Animals first", "Highest score and most reactions. Nature / pet creators are the obvious partnership list."),
        ("Food is two buckets", "Healthy eating beats Food. A wellness brand fit is closer than a generic restaurant campaign."),
        ("Science + tech", "Together they almost match Animals. How-to and explainers are not a niche here."),
        ("Watch volume, not vibe", "Mean score is ~40 everywhere. To move the ranking you need more posts (or more reactions), not “better” emojis."),
        ("Do not stop at five", "Travel, cooking and culture are within ~8k points of Food. A six-month refresh should include them."),
        ("Next measurement", "This is a static sample. Production would score categories weekly and split by format."),
    ]
    for i, (t, d) in enumerate(recs):
        r, c = divmod(i, 3)
        x = 0.45 + c * 4.25
        y = 1.35 + r * 2.75
        add_rect(s, x, y, 4.05, 2.55, WHITE)
        add_rect(s, x, y, 0.1, 2.55, TEAL if i % 2 == 0 else PURPLE)
        add_text(s, x + 0.3, y + 0.2, 3.55, 0.55, t, 16, True, NAVY)
        add_text(s, x + 0.3, y + 0.85, 3.55, 1.4, d, 13, False, GRAY)
    footer(s, 12)

    prs.save(OUT)
    print("wrote", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    build()
