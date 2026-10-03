# mp3Id3Check
check mp3 files for a set of expected id3 tags

## Use

### Run from a checkout

This is the simplest option, as the tool is currently only published and available from a private repo

```commandline
git clone https://github.com/rdepping/mp3Id3Check.git
cd mp3Id3Check
make install
make run
# Or provide an MP3 folder:
uv run mp3-id3-check /path/to/mp3s
```

Edit `src/mp3_id3_check/cli.py` to update the expected tags or CSV export headers.

### Install as a dependency

All options need Cloudsmith credentials with repository-read access:

```commandline
export UV_INDEX_CLOUDSMITH_USERNAME="YOUR_CLOUDSMITH_USERNAME"
export UV_INDEX_CLOUDSMITH_PASSWORD="YOUR_CLOUDSMITH_API_KEY"
```

Add Cloudsmith as the default index in the consuming project's `pyproject.toml`:

```toml
[[tool.uv.index]]
name = "cloudsmith"
url = "https://dl.cloudsmith.io/basic/secure-apps/app-repo/python/simple/"
default = true
```

Then install and run the application from that project:

```commandline
uv add mp3-id3-check
uv run mp3-id3-check /path/to/mp3s
```

### Install as a local tool

```commandline
uv tool install \
  --system-certs \
  --default-index cloudsmith=https://dl.cloudsmith.io/basic/secure-apps/app-repo/python/simple/ \
  mp3-id3-check
mp3-id3-check /path/to/mp3s
```

## Help

```commandline
❯ uv run mp3-id3-check --help
usage: mp3-id3-check [-h] [-s] [-c] [-x] [FOLDER_PATH]

Check MP3 files for expected ID3 tags.

positional arguments:
  FOLDER_PATH    path to the folder (default: current folder)

options:
  -h, --help     show this help message and exit
  -s, --summary  include a summary
  -c, --correct  prompt to correct tags using filename suggestions
  -x, --export   Export csv summary
```

Example run with summary

```commandline
❯  uv run mp3-id3-check /Users/user/mp3-folder -s

Total files checked: 6, Compliant: 6 Non-compliant: 0

Tag Summary:

=== album:
Galatians - Gospel of Grace (1 file(s))
Carrigaline Baptist Church (1 file(s))
Christmas (2 file(s))
Revelation - Victory Through Suffering (1 file(s))
Genesis - The Promised Seed (1 file(s))

=== albumartist:
Carrigaline Baptist Church (6 file(s))

=== artist:
Joe Smart (1 file(s))
Barry Reader (2 file(s))
Henry Bloggs (3 file(s))

=== title:
Revelation Ch22v6-21 - Jesus Is Coming (1 file(s))
Jesus Comfort For All People  - Luke Ch2:22-40 (2 file(s))
Daniel: Dreams Do Come True (1 file(s))
Genesis Ch26v1-33 - Relentlessly Faithful (1 file(s))
Grace Restoration - Galatians 6:1-6 (1 file(s))

=== date:
2020 (1 file(s))
2019 (2 file(s))
2022 (1 file(s))
2014 (1 file(s))
2023 (1 file(s))
```

Example run with export

```commandline
❯  uv run mp3-id3-check /Users/user/mp3-folder -x
Skipping export of tag genre from Genesis Ch26v1-33 - Relentlessly Faithful.mp3
Skipping export of tag genre from danielCh2_dreamsDoComeTrue_20140914.mp3
Skipping export of tag genre from jesusComfortForAllPeople_20191229.mp3
Skipping export of tag genre from galatiansCh6_graceRestoration_20200705.mp3
Skipping export of tag genre from jesusComfortForAllPeople_20191229 (1).mp3
Skipping export of tag genre from revelation22_JesusIsComing_20221218.mp3
Exported 6 to sermons.csv
```
