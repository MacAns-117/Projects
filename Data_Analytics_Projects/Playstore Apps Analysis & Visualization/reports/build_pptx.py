"""Rebuild Playstore_Report.pptx. Run from project root."""
from pathlib import Path
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "reports/figures"
OUT = ROOT / "reports/Playstore_Report.pptx"
NAVY = RGBColor(0x1B, 0x4F, 0x72)
ORANGE = RGBColor(0xD3, 0x54, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x2C, 0x3E, 0x50)
MUTED = RGBColor(0x5D, 0x6D, 0x7E)
CREAM = RGBColor(0xF7, 0xF5, 0xF2)
W, H = Inches(13.333), Inches(7.5)


def rect(s, l, t, w, h, fill):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill; sh.line.fill.background()


def txt(s, l, t, w, h, text, size=14, bold=False, color=INK, align=PP_ALIGN.LEFT):
    box = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.color.rgb = color; r.font.name = "Calibri"


def footer(s, n, total=9):
    rect(s, 0, 7.28, 13.333, 0.22, NAVY)
    txt(s, 0.4, 7.28, 8, 0.22, "Play Store  ·  practice project", 9, False, WHITE)
    txt(s, 11.4, 7.28, 1.5, 0.22, f"{n} / {total}", 9, False, WHITE, PP_ALIGN.RIGHT)


def pic(s, name, l, t, w, h):
    s.shapes.add_picture(str(FIG / name), Inches(l), Inches(t), Inches(w), Inches(h))


def header(s, title):
    rect(s, 0, 0, 13.333, 7.5, CREAM)
    rect(s, 0, 0, 13.333, 0.7, NAVY)
    txt(s, 0.5, 0.18, 12, 0.4, title, 22, True, WHITE)


def build():
    prs = Presentation(); prs.slide_width = W; prs.slide_height = H
    blank = prs.slide_layouts[6]

    s = prs.slides.add_slide(blank)
    rect(s, 0, 0, 13.333, 7.5, NAVY); rect(s, 0, 0, 0.22, 7.5, ORANGE)
    txt(s, 0.7, 2.0, 12, 0.35, "GOOGLE PLAY STORE", 14, True, ORANGE)
    txt(s, 0.7, 2.4, 12, 1.2, "14 SQL questions on 9,648 apps", 32, True, WHITE)
    txt(s, 0.7, 4.0, 11, 0.8, "Pandas + SQLite. Ratings not filled with the mean.\nInstalls are bucket floors, not exact counts.", 16, False, WHITE)

    s = prs.slides.add_slide(blank); header(s, "What is in the file"); footer(s, 2)
    txt(s, 0.6, 1.1, 12, 5.5,
        "9,648 unique apps after dropping the Category=1.9 row and duplicate names.\n"
        "8,190 have a rating (median 4.3). 1,458 have none — left missing.\n"
        "8,895 free / 753 paid.\n\n"
        "29,692 unique reviews (duplicates dropped) across 865 apps.\n"
        "64% positive, 21% negative, 15% neutral.", 16, False, INK)

    s = prs.slides.add_slide(blank); header(s, "Q1–Q3  ·  rating vs reviews"); footer(s, 3)
    pic(s, "rating_hist.png", 0.4, 1.0, 6.5, 3.3)
    txt(s, 7.1, 1.1, 5.7, 5.5,
        "Highest rating is 5.0 — 271 apps.\nMost of those have <150 reviews.\nTop 5.0 by reviews: Ríos de Fe (141).\n\n"
        "Most reviewed app overall:\nFacebook  ·  SOCIAL\n78,158,306 reviews  ·  1B+ installs.\n\n"
        "A 5.0 with a hundred reviews is not a better product than Facebook at 4.x.", 15, False, INK)

    s = prs.slides.add_slide(blank); header(s, "Q4–Q6  ·  money, installs, catalogue"); footer(s, 4)
    pic(s, "category_installs.png", 0.35, 0.9, 7.4, 3.8)
    pic(s, "paid_revenue.png", 7.9, 0.9, 5.0, 3.8)
    txt(s, 0.5, 4.9, 12.3, 2.0,
        "GAME leads installs: 13.88 billion (bucket floor). COMMUNICATION is second.\n"
        "Paid revenue estimate $291.1M. Minecraft $69.9M, then the joke “I am rich” apps.\n"
        "Most published genre: Tools (824 apps).", 15, False, INK)

    s = prs.slides.add_slide(blank); header(s, "Q7–Q10  ·  games, Android, free/paid, dating"); footer(s, 5)
    pic(s, "top_games.png", 0.35, 0.9, 7.4, 3.5)
    pic(s, "free_vs_paid.png", 8.0, 0.9, 4.8, 3.3)
    txt(s, 0.5, 4.6, 12.3, 2.3,
        "Subway Surfers is the only game at 1B+ installs.\n"
        "1,395 apps list Android Ver = “4.0.3 and up” (exact string, not “4.0.3 or later”).\n"
        "92% free. Best dating app by reviews: Zoosk (516,801 reviews, rating 4.0).", 15, False, INK)

    s = prs.slides.add_slide(blank); header(s, "Q11–Q14  ·  review table"); footer(s, 6)
    pic(s, "sentiment.png", 0.4, 1.0, 5.0, 5.0)
    txt(s, 5.7, 1.2, 7.0, 5.5,
        "10 Best Foods for You — unique reviews:\n79 positive, 11 neutral, 5 negative.\n\n"
        "ASUS SuperNote, polarity=1 and subjectivity=1:\n“Awesome!!!!”  (one row)\n\n"
        "Abs Training-Burn belly fat, Neutral: 5 comments.\n\n"
        "Adobe Acrobat Reader, Negative: 20 unique comments.", 15, False, INK)

    s = prs.slides.add_slide(blank); header(s, "What I would not claim"); footer(s, 7)
    txt(s, 0.6, 1.1, 12, 5.5,
        "• 5.0 is not a ranking. It is a small-sample ceiling.\n\n"
        "• $291M is not Google’s revenue. It is list price times a rounded install bucket.\n\n"
        "• Q8 is an exact version string. Apps on 4.1+ are a different count.\n\n"
        "• Reviews cover 865 of 9,648 apps. Sentiment is not store-wide.", 16, False, INK)

    s = prs.slides.add_slide(blank); header(s, "How this was run"); footer(s, 8)
    txt(s, 0.6, 1.1, 12, 5.5,
        "Stack: pandas and SQLite. No Power BI in this repo.\n\n"
        "Cleaning: drop Category=1.9, drop duplicate app names, restore missing ratings, drop duplicate reviews.\n\n"
        "SQL: sql/queries.sql. The notebook checks that pandas and SQLite match on the headline queries.", 16, False, INK)

    s = prs.slides.add_slide(blank)
    rect(s, 0, 0, 13.333, 7.5, NAVY); rect(s, 0, 0, 0.22, 7.5, ORANGE)
    txt(s, 0.7, 2.3, 12, 1.4, "Facebook has the reviews.\nGAME has the installs.\n5.0 is a crowded room.", 28, True, WHITE)

    prs.save(OUT)
    print("wrote", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    build()
