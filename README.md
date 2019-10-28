# riddle.py [![CodeFactor](https://www.codefactor.io/repository/github/trivernis/reddit-riddle/badge)](https://www.codefactor.io/repository/github/trivernis/reddit-riddle) [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0) 

This is a script for downloading images (or other media) from reddit subreddits.

## Install

This script requires at least Python 3.6.
After cloning this repository you need to install the requirements via 

```sh
pipenv install
```
or
```sh
pip3 install -r requirements.txt
```

## Configuration

Before running you need to provide information for the reddit api.
To do so you must create an app in your reddit [account preferences](https://www.reddit.com/prefs/apps).
The application must be of type 'script'. 
That must be done via a config.yaml file in the scripts directory.
You can copy the `default-config.yaml` file to the `config.yaml` file and change the keys
`client_id` and `client_secret` under `credentials`.

```yaml
# user app credentials
credentials:
  client_id: your app-client id  # change this
  client_secret: your app-client secret  # change this

# required extension of the file to be downloaded
image-extensions:
  - png
  - jpg
  - jpeg

min-size: 5 # minimum size in kilobytes
```

## Running

### Help output

```
Usage: riddle.py [options] [subreddits]

Options:
  -h, --help            show this help message and exit
  -c COUNT, --count=COUNT
                        The number of images to download for each subreddit.
                        If not set it is the maximum fetchable number.
  -o OUTPUT, --output=OUTPUT
                        The name of the output folder. If none is specified,
                        it's the subreddits name.
  -z, --zip             Stores the images in a zip file if true
  --nsfw                If set nsfw-content is also downloaded.
  --lzma                If set the lzma-compression module is used.
```

### Example

Download all images from [r/EarthPorn](https://EarthPorn.reddit.com):

```sh
python3 riddle.py EarthPorn
```

Download all images from [r/astrophotography](https://astrophotography.reddit.com) to a zip-file:

```sh
python3 riddle.py -z astrophotography
```

Download a maximum of 200 images from [r/astrophotography](https://astrophotography.reddit.com) and [r/EarthPorn](https://EarthPorn.reddit.com) to one zip-file named coolpics.zip:

```sh
python3 riddle.py -z -c 100 -o coolpics astrophotography EarthPorn
```
