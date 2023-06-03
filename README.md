# mp3Id3Check
check mp3 files for a set of expected id3 tags

Install dependencies
`poetry install` or `pip install mutagen`

Edit `mp3_id3_check.py` to update for the list of expected tags



Help

```commandline
❯ poetry run python mp3_id3_check.py --help
usage: mp3_id3_check.py [-h] [-s] [-c] [FOLDER_PATH]

Check MP3 files for expected ID3 tags.

positional arguments:
  FOLDER_PATH    path to the folder (default: current folder)

options:
  -h, --help     show this help message and exit
  -s, --summary  include a summary
  -c, --correct  (future) automatically correct missing tags where possible
```

Example run with summary

```commandline
❯  poetry run python mp3_id3_check.py /Users/user/mp3-folder -s

Total files checked: 4
Compliant files: 4
Non-compliant files: 0

Tag Summary:

=== albumartist:
Carrigaline Baptist Church (4 file(s))

=== date:
2022 (1 file(s))
2019 (1 file(s))
2023 (1 file(s))
2020 (1 file(s))

=== album:
Galatians - Gospel of Grace (1 file(s))
Genesis - The Promised Seed (1 file(s))
Christmas (1 file(s))
Revelation - Victory Through Suffering (1 file(s))

=== title:
Jesus Comfort For All People  - Luke Ch2:22-40 (1 file(s))
Revelation Ch22v6-21 - Jesus Is Coming (1 file(s))
Genesis Ch26v1-33 - Relentlessly Faithful (1 file(s))
Grace Restoration - Galatians 6:1-6 (1 file(s))

=== artist:
Joe Bloggs (1 file(s))
Jonny Supreme (2 file(s))
Sam Roberts (1 file(s))

=== genre:
sermon (4 file(s))
```
