import time
from pathlib import Path
from scrape_ import _requests


def request():
    time.sleep(2.0)
    return _requests


# https://www.mediawiki.org/wiki/API:Categorymembers
def get_category_pages(name):
    data = request().get("https://en.touhouwiki.net/api.php", params={
        "action": "query",
        "cmtitle": f"Category:{name}",
        "cmlimit": 500,
        "list": "categorymembers",
        "format": "json"
    }).json()

    # TODO: handle long category lists
    assert 'continue' not in data
    return [page['title'] for page in data['query']['categorymembers']]


def save_raw_pages(name, pages):
    data = {'pages': '\n'.join(pages), 'curonly': True}
    resp = request().post("https://en.touhouwiki.net/wiki/Special:Export", data=data)
    with open(Path("raw") / f"{name}.xml", 'w') as f:
        f.write(resp.text)


def main():
    all_categories = [
        'Music_by_Game',
        'Characters',
        'Official_Games',
        'Bestiary',
        'Locations',
    ]

    all_pages = [
        'Glossary',
    ]

    for category in all_categories:
        print(f"[category/save] {category}")
        pages = get_category_pages(category)
        save_raw_pages(category, pages)

    for page in all_pages:
        print(f"[page/save] {page}")
        save_raw_pages(page, [page])


if __name__ == '__main__':
    main()
