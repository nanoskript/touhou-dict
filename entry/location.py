import mwparserfromhell

from entry.common import parse_raw, get_template, get_parameter, unique, take_after, take_until, templated
from entry.render import render_ruby_jp, render


def convert_locations(gloss):
    for title, page in parse_raw("./raw/Locations.xml"):
        box = get_template(page, 'Infobox Location')
        if not box:
            continue

        name_en = get_parameter(box, 'nameEn')
        name_jp = get_parameter(box, 'nameJp')
        if not name_jp:
            # Ignore locations without an official Japanese name.
            continue

        # Hack to split on alternate Japanese names.
        name_jp_tokens = [mwparserfromhell.parse(s) for s in name_jp.split('{{!}}')]

        # Collect entry words.
        words = [title]
        words += name_en.split('{{!}}')
        words += [render_ruby_jp(s, 'kanji') for s in name_jp_tokens]
        words += [render_ruby_jp(s, 'kana') for s in name_jp_tokens]
        words = unique([s.strip() for s in words])

        # Render synopsis.
        # Assumption: `Infobox` template will always precede.
        def skip_templates(child):
            if child.name in ['Distinguish', 'stub', 'Uwabami note']:
                return ""

        lead = take_after(page.get_sections()[0], box)
        bottom = get_template(lead, 'Navbox Locations')
        if bottom:
            # Hack to allow single section pages.
            lead = take_until(lead, bottom)
        synopsis = render(lead, template=skip_templates)

        # Render entry.
        content = templated(
            'location.html',
            title=words[0],
            transliteration=render(name_jp),
            synopsis=synopsis,
        )

        # Add definition.
        print(f"[location] {title}")
        entry = gloss.newEntry(words, content)
        gloss.addEntryObj(entry)
