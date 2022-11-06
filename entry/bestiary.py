from collections import defaultdict

from mwparserfromhell.nodes import Wikilink
from mwparserfromhell.wikicode import Wikicode

from entry.common import parse_raw, take_after, get_template, take_until, get_parameter, unique, templated

from entry.render import render, render_ruby_jp


def convert_bestiary(gloss):
    sections, redirects = defaultdict(dict), []
    for title, page in parse_raw("./raw/Bestiary.xml"):
        # Check for redirect.
        if str(page.nodes[1]).strip() == 'REDIRECT':
            link = page.nodes[2]
            assert isinstance(link, Wikilink)
            [target, heading] = link.title.split('#')
            redirects.append((title, (target, heading)))
            continue

        # Add sections.
        for section in page.get_sections(include_lead=False, flat=True):
            heading_node = section.nodes[0]
            heading = str(heading_node.title).strip()
            sections[title][heading] = section

        # Specially handled pages.
        if title in ["Bakeneko", "Saigyou Ayakashi"]:
            continue

        # Render synopsis.
        synopsis = page.get_sections()[0]
        box = get_template(page, 'Infobox Species')
        name_jp = None
        if box:
            synopsis = take_after(synopsis, box)
            name_jp = get_parameter(box, 'nameJp')
            if not str(name_jp).strip():
                # Empty string.
                name_jp = None

        def skip_templates(child):
            if child.name in ['seihou note', 'about', 'Delete', 'stub', 'DEFAULTSORT:']:
                return ""

        # Trim content.
        bottom = get_template(synopsis, 'Navbox Bestiary')
        if bottom:
            # Hack to allow single section pages.
            synopsis = take_until(synopsis, bottom)
        synopsis = render(synopsis, template=skip_templates).strip()
        assert synopsis

        content = templated(
            'bestiary.html',
            title=title,
            transliteration=render(name_jp) if name_jp else None,
            synopsis=synopsis,
        )

        # Collect words.
        title_base = title.replace("(species)", "").strip()
        words = [title, title_base]
        if name_jp:
            words += render_ruby_jp(name_jp, 'kanji').split("/")
            words += render_ruby_jp(name_jp, 'kana').split("/")
        words = unique([s.strip() for s in words])

        print(f"[bestiary] {title}")
        entry = gloss.newEntry(words, content)
        gloss.addEntryObj(entry)

    # Special redirects.
    redirects.append(("Bakeneko", ("Bakeneko", "Nekomata")))

    # Convert redirect sections.
    for title, (page, heading) in redirects:
        if heading not in sections[page]:
            continue

        section = sections[page][heading]
        synopsis = render(Wikicode(section.nodes[1:])).strip()
        assert synopsis

        content = templated(
            'bestiary.html',
            title=title,
            synopsis=synopsis,
        )

        print(f"[bestiary/redirect] {title}")
        entry = gloss.newEntry([title], content)
        gloss.addEntryObj(entry)
