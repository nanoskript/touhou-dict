import json

from pyglossary.glossary import Glossary

from entry.bestiary import convert_bestiary
from entry.character import convert_characters
from entry.game import convert_official_games
from entry.glossary import convert_glossary
from entry.location import convert_locations
from entry.music import convert_game_music


def main():
    Glossary.init()
    gloss = Glossary()
    gloss.setInfo("title", "Touhou")
    gloss.setInfo("author", "Nanoskript")
    gloss.setInfo("copyright", "Definitions extracted from https://en.touhouwiki.net/ under CC BY-SA 4.0")

    # Write definitions.
    convert_characters(gloss)
    convert_game_music(gloss)
    convert_official_games(gloss)
    convert_locations(gloss)
    convert_bestiary(gloss)
    convert_glossary(gloss)

    # FIXME: Hack to avoid clearing entries after writing dictionary.
    gloss.clear = lambda *args: None

    # Write dictionary files.
    # gloss.write('./build/html', 'HtmlDir')

    # Write JSON file.
    gloss.write('./build/web/data.json', 'Json')
    with open('./build/web/data.json', 'r') as r:
        # Remove unnecessary entries.
        data = json.load(r)
        data.pop("")
        data.pop("##name")
        data.pop("##author")
        data.pop("##copyright")
        with open('./build/web/data.json', 'w') as w:
            json.dump(data, w, indent=2)

    # Write Apple dictionary sources.
    gloss.write(
        './build/apple/Touhou',
        'AppleDict',
        css="./styles/apple.css",
    )


if __name__ == '__main__':
    main()
