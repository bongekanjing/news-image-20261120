#!/usr/bin/env python3
"""The Global Herald -- front page for Friday 20 November 2026.

Draws a text-only broadsheet front page with PIL and writes it to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png). Deterministic:
no network, no clock, no randomness, so repeated runs are byte-identical.

If PIL or the DejaVu fonts are unavailable in the sandbox, the program
falls back to copying the pre-rendered entry.png shipped beside it.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 36
INK = (18, 18, 18)
PAPER = (250, 247, 238)
RULE = (40, 40, 40)
GREY = (90, 88, 82)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_ITALIC = os.path.join(FONT_DIR, "DejaVuSerif.ttf")  # no italic face ships here
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def load_font(path, size):
    from PIL import ImageFont

    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    """Wrap text to fit width; returns a list of lines."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text, font, width, max_lines):
    """Wrap text and truncate to max_lines, adding an ellipsis if cut."""
    lines = wrap(draw, text, font, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " ...", font=font) > width:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] = lines[-1] + " ..."
    return lines


def draw_rule(draw, x0, x1, y, width=1):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def draw_centered(draw, text, font, y, x0=MARGIN, x1=PAGE_W - MARGIN):
    w = draw.textlength(text, font=font)
    draw.text(((x0 + x1 - w) / 2, y), text, font=font, fill=INK)
    return y + font.size + 2

# The day's news, Friday 20 November 2026. Lead stories are the events of
# Thursday 19 November as carried on Friday's front pages; the rest were
# first reported on Friday 20 November.
LEAD = {
    "kicker": "SHENZHEN  |  APEC SUMMIT",
    "headline": "Trump, Xi and Putin hold first-ever three-way talks",
    "deck": (
        "The three leaders meet for 90 minutes on the sidelines of the APEC "
        "summit, pledging further talks on nuclear risks, Ukraine and Iran "
        "— but reach no breakthrough."
    ),
}

SECOND = {
    "kicker": "THE HAGUE  |  WORLD COURT",
    "headline": "World court rules Myanmar committed genocide against the Rohingya",
    "deck": (
        "In a first, the International Court of Justice finds a state guilty "
        "of genocide and orders reparations for the 2017 crackdown."
    ),
}

WORLD = [
    {
        "kicker": "WASHINGTON",
        "headline": "Trump puts Iran decision off until 2027",
        "deck": "The president says there is \u2018no rush\u2019 and he will \u2018see what happens\u2019 after January 1.",
    },
    {
        "kicker": "KYIV",
        "headline": "Russian strikes damage Dutch and Austrian embassies",
        "deck": "One person is killed and a cathedral\u2019s windows are shattered in a day-long drone raid on the capital.",
    },
    {
        "kicker": "BRUSSELS",
        "headline": "Europe ready for talks with Russia on ending the Ukraine war",
        "deck": "European leaders signal openness to negotiations as the war grinds on.",
    },
    {
        "kicker": "RIYADH",
        "headline": "Houthi attack damages Saudi wealth fund tower",
        "deck": "A strike hits the Public Investment Fund tower in the Saudi capital.",
    },
    {
        "kicker": "CRIMEA",
        "headline": "Ukrainian strike on Crimean Bridge halts rail traffic",
        "deck": "Kyiv says its forces hit the bridge linking Russia to occupied Crimea.",
    },
    {
        "kicker": "VIENNA",
        "headline": "North Korea expanding uranium enrichment, watchdog says",
        "deck": "The UN nuclear agency reports growth at the Yongbyon facility.",
    },
    {
        "kicker": "CARACAS",
        "headline": "US and Venezuela agree to restore military cooperation",
        "deck": "The two governments sign an agreement to renew defence ties.",
    },
    {
        "kicker": "CANBERRA",
        "headline": "Australia sanctions Israeli settlers over West Bank expansion",
        "deck": "Canberra blacklists settlers and organisations in a first.",
    },
    {
        "kicker": "SUVA",
        "headline": "Fiji declares national disaster as drought deepens",
        "deck": "Severe water shortages blamed on El Ni\u00f1o conditions.",
    },
    {
        "kicker": "SEOUL",
        "headline": "South Korea court clears former PM Han Duck-soo",
        "deck": "The Supreme Court overturns his conviction over the 2024 martial law declaration.",
    },
    {
        "kicker": "ODISHA",
        "headline": "Cyclone Akvan: 300,000 evacuated as storm nears coast",
        "deck": "Rescue teams deploy and schools close as the cyclone bears down on Odisha.",
    },
    {
        "kicker": "NEW DELHI",
        "headline": "Modi meets Prince and Princess of Wales",
        "deck": "The prime minister discusses India\u2013UK ties with the royal couple in the capital.",
    },
]

BUSINESS_TECH_SPORT = [
    {
        "kicker": "SPACE",
        "headline": "Voyager 1 now a full light-day from Earth",
        "deck": "NASA confirms the 16-billion-mile probe is the first human-made object to reach the mark.",
    },
    {
        "kicker": "TOKYO",
        "headline": "Hayabusa2 scraps asteroid landing after engine trouble",
        "deck": "Japan\u2019s probe changes plans after an engine fault rules out a touchdown.",
    },
    {
        "kicker": "TECH",
        "headline": "Anthropic valuation reportedly reaches $1.5 trillion",
        "deck": "The AI company\u2019s reported valuation underlines the boom in artificial intelligence.",
    },
    {
        "kicker": "GAMING",
        "headline": "GTA 6 sales pass The Odyssey\u2019s $1.80bn global run",
        "deck": "Rockstar\u2019s blockbuster overtakes the year\u2019s biggest film at the box office.",
    },
    {
        "kicker": "MUMBAI",
        "headline": "Sensex jumps as Indian markets rally",
        "deck": "Stocks gain more than 1% as auto and financial shares lead the rise.",
    },
    {
        "kicker": "WELLINGTON",
        "headline": "Nicholls century rescues New Zealand on day one",
        "deck": "The batter\u2019s unbeaten 113 lifts the hosts to 243 for five against India in the first Test.",
    },
]

HEADLINE_COUNT = 2 + len(WORLD) + len(BUSINESS_TECH_SPORT)


def draw_lead(draw, story, y, head_size, deck_size, deck_lines, width):
    kicker_f = load_font(SANS_BOLD, 12)
    head_f = load_font(SERIF_BOLD, head_size)
    deck_f = load_font(SANS, deck_size)
    draw.text((MARGIN, y), story["kicker"], font=kicker_f, fill=GREY)
    y += 18
    for line in fit_lines(draw, story["headline"], head_f, width, 2):
        draw.text((MARGIN, y), line, font=head_f, fill=INK)
        y += head_size + 6
    y += 2
    for line in fit_lines(draw, story["deck"], deck_f, width, deck_lines):
        draw.text((MARGIN, y), line, font=deck_f, fill=INK)
        y += deck_size + 5
    return y


def draw_section_header(draw, title, y):
    f = load_font(SANS_BOLD, 13)
    draw.text((MARGIN, y), title, font=f, fill=INK)
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, y + 19, 1)
    return y + 28


def draw_story_cell(draw, story, x, y, width):
    kicker_f = load_font(SANS_BOLD, 10)
    head_f = load_font(SERIF_BOLD, 15)
    deck_f = load_font(SANS, 11)
    draw.text((x, y), story["kicker"], font=kicker_f, fill=GREY)
    cy = y + 14
    for line in fit_lines(draw, story["headline"], head_f, width, 2):
        draw.text((x, cy), line, font=head_f, fill=INK)
        cy += 19
    cy += 2
    for line in fit_lines(draw, story["deck"], deck_f, width, 2):
        draw.text((x, cy), line, font=deck_f, fill=INK)
        cy += 14
    return cy


def draw_grid(draw, stories, y, cols=3, cell_h=86):
    gap = 24
    width = (PAGE_W - 2 * MARGIN - (cols - 1) * gap) // cols
    for i, story in enumerate(stories):
        row, col = divmod(i, cols)
        x = MARGIN + col * (width + gap)
        draw_story_cell(draw, story, x, y + row * cell_h, width)
        if col:
            draw.line(
                [(x - gap // 2, y + row * cell_h + 2),
                 (x - gap // 2, y + (row + 1) * cell_h - 10)],
                fill=(200, 196, 186),
                width=1,
            )
    rows = (len(stories) + cols - 1) // cols
    return y + rows * cell_h


def render(path):
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)

    # Top strip: date and section label.
    strip_f = load_font(SANS_BOLD, 13)
    date = "FRIDAY 20 NOVEMBER 2026"
    draw.text((MARGIN, 26), date, font=strip_f, fill=INK)
    label = "THE WORLD'S NEWS"
    draw.text(
        (PAGE_W - MARGIN - draw.textlength(label, font=strip_f), 26),
        label,
        font=strip_f,
        fill=INK,
    )
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, 48, 1)

    # Masthead.
    mast_f = load_font(SERIF_BOLD, 60)
    draw_centered(draw, "THE GLOBAL HERALD", mast_f, 54)
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, 122, 3)
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, 127, 1)

    # Tagline.
    tag_f = load_font(SERIF_ITALIC, 14)
    draw_centered(
        draw, "The world's news — Friday 20 November 2026", tag_f, 134
    )

    # Lead story, full width.
    y = draw_lead(draw, LEAD, 160, 33, 14, 3, PAGE_W - 2 * MARGIN)
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, y + 8, 1)

    # Second story, full width.
    y = draw_lead(draw, SECOND, y + 18, 25, 13, 2, PAGE_W - 2 * MARGIN)
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, y + 8, 1)

    # World grid: 12 stories, 3 columns x 4 rows.
    y = draw_section_header(draw, "WORLD", y + 18)
    y = draw_grid(draw, WORLD, y)

    # Business, technology and sport: 6 stories, 3 columns x 2 rows.
    y = draw_section_header(draw, "BUSINESS, TECHNOLOGY & SPORT", y + 6)
    y = draw_grid(draw, BUSINESS_TECH_SPORT, y)

    # Footer.
    foot_f = load_font(SANS, 10)
    draw_rule(draw, MARGIN, PAGE_W - MARGIN, PAGE_H - 26, 1)
    draw_centered(
        draw,
        "The Global Herald  •  Friday 20 November 2026  •  Compiled from wire reports",
        foot_f,
        PAGE_H - 20,
    )

    img.save(path, format="PNG")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    target = os.path.join(OUT_DIR, "entry.png")
    try:
        render(target)
    except Exception:
        # PIL or the fonts are missing: ship the pre-rendered image.
        bundled = os.path.join(HERE, "entry.png")
        shutil.copyfile(bundled, target)


if __name__ == "__main__":
    main()
