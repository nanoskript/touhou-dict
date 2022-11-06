from entry.common import parse_raw, get_template, get_parameter, unique, take_after, templated
from entry.render import render, render_ruby_jp


def official_games():
    return parse_raw("./raw/Official_Games.xml")


def convert_official_games(gloss):
    for title, page in official_games():
        box = get_template(page, 'Infobox Game')
        title_en = get_parameter(box, 'titleEn')
        title_jp = get_parameter(box, 'titleN')
        words = unique([
            title,
            render(title_en),
            render_ruby_jp(title_jp, 'kanji'),
            render_ruby_jp(title_jp, 'kana'),
        ])

        lead = take_after(page.get_sections()[0], box)
        synopsis = render(lead)

        content = templated(
            'game.html',
            title=words[0],
            transliteration=render(title_jp),
            synopsis=synopsis,
        )

        # Add definition.
        print(f"[game] {title}")
        entry = gloss.newEntry(words, content)
        gloss.addEntryObj(entry)
