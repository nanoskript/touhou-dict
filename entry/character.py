from entry.common import parse_raw, get_template, get_parameter, unique, templated, take_after
from entry.render import render, render_ruby_jp


def convert_characters(gloss):
    for title, page in parse_raw("./raw/Characters.xml"):
        # Ignore problematic pages.
        if title in ['Minor Characters']:
            continue

        # Extract character template box.
        box = get_template(page, 'Infobox Character')
        if not box:
            continue

        # Extract character names.
        words = []
        name_en = get_parameter(box, 'nameEn')
        name_jp = get_parameter(box, 'nameJp')
        if name_en:
            string = render(name_en)
            words.append(string)
            if title not in ['Hakurei God']:
                # Split character name.
                words += string.split()
        if name_jp:
            words.append(render_ruby_jp(name_jp, 'kanji'))
            words.append(render_ruby_jp(name_jp, 'kana'))
        if not words:
            continue

        # Combine words.
        words.append(title)
        words = unique(words)

        # Render synopsis.
        # Assumption: `Infobox` template will always precede.
        def skip_templates(child):
            if child.name in ['stub', 'TOC limit']:
                return ""

        lead = take_after(page.get_sections()[0], box)
        synopsis = render(lead, template=skip_templates)

        # Render entry.
        content = templated(
            'character.html',
            title=words[0],
            transliteration=render(name_jp) if name_jp else None,
            synopsis=synopsis,
        )

        # Add definition.
        print(f"[character] {title}")
        entry = gloss.newEntry(words, content)
        gloss.addEntryObj(entry)
