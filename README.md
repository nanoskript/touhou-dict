# touhou-dict

System dictionaries for the Touhou universe.

![Picture](docs/picture.png)

## Entries

Dictionary entries are present for the following categories
from [en.touhouwiki.net](https://en.touhouwiki.net/):

- Characters

  ![Picture](docs/character.png)

- Official game music

  ![Picture](docs/music.png)

- Official games

  ![Picture](docs/game.png)

- Locations

  ![Picture](docs/location.png)

- Bestiary

  ![Picture](docs/bestiary.png)

- Glossary

  ![Picture](docs/glossary.png)

## Installation

### Apple dictionary (macOS)

1. Download the latest `Touhou.dictionary.tar.gz` from
   the [releases page](https://github.com/Nanoskript/touhou-dict/releases/tag/latest).
2. Double-click on the downloaded `Touhou.dictionary.tar.gz` file to extract it.
3. Open macOS's Dictionary application and go to `File` > `Open Dictionaries Folder`:

   ![Picture](docs/apple/open_dictionaries_folder.png)

4. Drag the extracted `Touhou.dictionary` folder into the `Dictionaries` folder:

   ![Picture](docs/apple/dictionaries_folder.png)

## Scraping

The included `scrape.py` script is not immediately functional without an additional
module to deter unwarranted requests to the wiki servers. Pages can be manually exported
by accessing the [Special:Export](https://en.touhouwiki.net/wiki/Special:Export) page in
your browser.

## License

The code in this repository is licensed under the MIT license.
However, any dictionary artifacts are licensed
under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
with attribution to <https://en.touhouwiki.net/>. 
