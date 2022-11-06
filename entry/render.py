from typing import Literal

from mwparserfromhell.nodes import Template, Tag, Text, Wikilink, ExternalLink, Comment, HTMLEntity


def render(node, template=None, strip=True):
    def r(n):
        return render(n, template, strip=False)

    text = ""
    for child in node.nodes:
        if isinstance(child, Template):
            result = None
            if template:
                result = template(child)
            if result is None:
                if child.name.matches('H:title'):
                    result = str(child.get(1))
                elif child.name.matches('lang'):
                    result = str(child.get(2))
                elif child.name.matches('nihongo'):
                    result = r(child.get(1).value)
                elif child.name.matches('zh'):
                    # Take only literal translation.
                    result = r(child.get('l').value)
                elif child.name.matches('!'):
                    result = "|"
                elif child.name.matches('sic'):
                    result = ""
                elif child.name.matches('cn') or child.name.matches('reference needed'):
                    # Ignore citation needed.
                    result = ""
                elif child.name.matches('ruby-ja') or child.name.matches('Ruby'):
                    result = f"<ruby>{child.get(1)}<rt>{child.get(2)}</rt></ruby>"
                elif child.name.matches('thtitle'):
                    result = ''.join([r(p.value) for p in child.params if not p.showkey])
                else:
                    assert False, f"unhandled template: {child}"
            text += result
        elif isinstance(child, Tag):
            if child.tag in ['ref', 'br', 'hr', 'big', 'small', 'dd']:
                # `<dd>` tag only used for article disambiguation.
                pass
            elif child.tag in ['i', 'b', 'tt', 'dt', 'li', 'div', 'blockquote']:
                text += f"<{child.tag}>{r(child.contents)}</{child.tag}>"
            elif child.tag in ['nowiki']:
                text += str(child.contents)
            else:
                assert False, f"unhandled tag: {child.tag} ({child})"
        elif isinstance(child, Text):
            text += child.value
        elif isinstance(child, Wikilink):
            if child.title and str(child.title).startswith('File:'):
                # Ignore files.
                continue
            text += r(child.text or child.title)
        elif isinstance(child, ExternalLink):
            text += r(child.title)
        elif isinstance(child, HTMLEntity):
            text += str(child)
        elif isinstance(child, Comment):
            pass
        else:
            assert False, f"unhandled node: {type(child)} ({child})"
    return text.strip() if strip else text


def render_ruby_jp(node, only: Literal['kanji', 'kana']):
    def template(child):
        if child.name.matches('ruby-ja') or child.name.matches('ruby'):
            kanji, kana = str(child.get(1)), str(child.get(2))
            if not kanji:
                return kana
            elif not kana:
                return kanji
            else:
                return kanji if only == 'kanji' else kana

    return render(node, template)
