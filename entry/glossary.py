import re

import mwparserfromhell

from entry.common import parse_page, page_list_items
from entry.render import render


def convert_glossary(gloss):
    page = parse_page("./raw/Glossary.xml", "Glossary")
    for line in page_list_items(page):
        # Hack to extract glossary entries.
        name, details = re.split(r"[-—]", str(line), maxsplit=1)
        name = mwparserfromhell.parse(name.strip())
        details = mwparserfromhell.parse(details.strip())

        # Format contents.
        name = str(name.nodes[0].contents)
        content = render(details)

        print(f"[glossary] {name}")
        entry = gloss.newEntry([name], content)
        gloss.addEntryObj(entry)
