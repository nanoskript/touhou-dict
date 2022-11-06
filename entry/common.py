from xml.etree import ElementTree

import mwparserfromhell

from jinja2 import Environment, PackageLoader
from mwparserfromhell.nodes import Tag
from mwparserfromhell.wikicode import Wikicode

TEMPLATE_ENV = Environment(
    loader=PackageLoader('entry'),
    autoescape=False,
)


def templated(file, **kwargs):
    return TEMPLATE_ENV.get_template(file).render(**kwargs)


def unique(seq):
    return list(dict.fromkeys(seq))


def parse_raw(name):
    tree = ElementTree.parse(name)
    for page in tree.findall('{*}page'):
        text = page.find('{*}revision/{*}text').text
        title = page.find('{*}title').text

        # Ignore special pages.
        if ':' in title:
            continue

        # Fix fatal syntax errors.
        lines = []
        for line in text.splitlines():
            if line.count("''") == 1:
                lines.append(line.replace("''", ""))
            else:
                lines.append(line)

        text = '\n'.join(lines)
        parsed = mwparserfromhell.parse(text)
        yield title, parsed


def parse_page(file, title):
    for page_title, parsed in parse_raw(file):
        if page_title == title:
            return parsed


def get_template(page, includes):
    for template in page.filter_templates():
        if includes in template.name:
            return template


def get_parameter(template, name):
    for param in template.params:
        if name.lower() == param.name.strip().lower():
            return param.value


def take_after(page, element):
    start = page.index(element) + 1
    return Wikicode(page.nodes[start:])


def take_until(page, element):
    end = page.index(element)
    return Wikicode(page.nodes[:end])


def page_list_items(page):
    nodes = iter(page.nodes)
    try:
        while True:
            node = next(nodes)
            if isinstance(node, Tag) and node.tag == 'li':
                children = []
                try:
                    while True:
                        node = next(nodes)
                        children.append(node)
                        if str(node).endswith('\n'):
                            break
                except StopIteration:
                    pass
                yield Wikicode(children)
    except StopIteration:
        pass
