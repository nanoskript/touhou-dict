from entry.common import parse_raw, get_parameter, unique, templated
from entry.game import official_games
from entry.render import render, render_ruby_jp


def convert_game_music(gloss):
    official_game_names = set([p[0] for p in official_games()])
    for title, page in parse_raw("./raw/Music_by_Game.xml"):
        game = title.split('/')[0]
        if game not in official_game_names:
            # Only add entries for official games.
            continue

        print(f"[music/game] {game}")
        for item in page.filter_templates():
            if not item.name.matches('MusicRoom'):
                continue

            title = get_parameter(item, 'title')
            title_en = get_parameter(item, 'titleEN')
            if not title:
                continue

            words = unique([
                render(title_en),
                render_ruby_jp(title, 'kanji'),
                render_ruby_jp(title, 'kana'),
            ])

            fields = [('Game', game)]
            if item.has('category'):
                fields.append(('Category', render(get_parameter(item, 'category'))))
            if item.has('composer'):
                fields.append(('Composer', render(get_parameter(item, 'composer'))))

            # Add definition.
            print(f"[music/item] {words[0]}")
            content = templated(
                'music.html',
                title=words[0],
                # Ignore transliteration if text is identical.
                transliteration=render(title) if str(title) != str(title_en) else None,
                fields=fields,
            )

            entry = gloss.newEntry(words, content)
            gloss.addEntryObj(entry)
