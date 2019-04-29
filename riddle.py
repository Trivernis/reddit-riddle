import os
import shutil
import yaml
import praw
import optparse
import zipfile
import urllib.request as urlreq

user_agent = 'python:riddle:3.0 (by u/Trivernis)'
img_ext = ['jpg', 'jpeg', 'png', 'svg', 'gif']


def assert_dir_exist(dirpath):
    """
    Creates the directory if it doesn't exist
    :param dirpath: path to the directory
    :return: None
    """
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)


def download_file(url: str, dest: str):
    """
    Downloads a url to a file
    :param url: download url
    :param dest: download destination
    :return: None
    """
    f = open(dest, "wb")
    req = urlreq.Request(url)
    try:
        image = urlreq.urlopen(req)
        f.write(image.read())
        f.close()
    except ConnectionError:
        print('\r[-] Connection Error \r')
    except urlreq.HTTPError as err:
        print('\r[-] HTTPError for %s: %s \r' % (url, err))


class ProgressBar:
    def __init__(self, total=100, prefix='', suffix='', length=50, fill='█'):
        self.prefix = prefix
        self.suffix = suffix
        self.fill = fill
        self.length = length
        self.total = total
        self.progress = 0

    def tick(self):
        self.progress += 1
        self._print_progress()

    def setprogress(self, progress):
        self.progress = progress
        self._print_progress()

    def _print_progress(self):
        iteration = self.progress
        total = self.total
        prefix = self.prefix
        suffix = self.suffix

        percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(self.length * iteration // total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
        # Print New Line on Complete
        if iteration == total:
            print()


def parser_init():
    """
    Initializes and parses command line arguments
    :return: dict, list
    """
    parser = optparse.OptionParser(usage="usage: %prog [options] [subreddits]")
    parser.add_option('-c', '--count', dest='count',
                      type='int', default=None,
                      help="""The number of images to download for each subreddit.
                      If not set it is the maximum fetchable number.""")
    parser.add_option('-o', '--output', dest='output',
                      type='str', default=None,
                      help='The name of the output folder. If none is specified, it\'s the subreddits name.')
    parser.add_option('-z', '--zip', dest='zip',
                      action='store_true', default=False,
                      help='Stores the images in a zip file if true')
    return parser.parse_args()


def get_images(reddit_client: praw.Reddit, subreddit: str, limit: int):
    """
    Uses the reddit api to fetch all image posts
    :param reddit_client: instance of the reddit client
    :param subreddit: reddit subreddit name
    :param limit: max images to download. if set to None the maximum fetchable amout is used.
    :return: list of images
    """
    print('[~] Fetching images for %s...' % subreddit)
    urls = [submission.url for submission in reddit_client.subreddit(subreddit).hot(limit=limit)]
    return [url for url in urls if url.split('.')[-1] in img_ext]


def download_images(images: list, dl_dir: str):
    """
    Downloads a list of image urls to a folder
    :param images: list of image urls
    :param dl_dir: destination directory
    :return: None
    """
    imgcount = len(images)
    print('[~] Downloading %s images to %s' % (imgcount, dl_dir))
    pb = ProgressBar(total=imgcount, prefix='[~] Downloading', suffix='Complete')
    assert_dir_exist(dl_dir)
    
    for img in images:
        pb.tick()
        imgname = img.split('/')[-1]
        name = os.path.join(dl_dir, imgname)
        if not os.path.isfile(name):
            download_file(img, name)


def compress_folder(folder: str, zip_fname: str):
    """
    Zips the contents of a folder to the destination zipfile name.
    :param folder: the folder to zip
    :param zip_fname: the name of the destination zipfile
    :return: None
    """
    print('[~] Compressing folder...')
    mode = 'w'
    if os.path.isfile(zip_fname):
        mode = 'a'
    zfile = zipfile.ZipFile(zip_fname, mode)
    for _, _, files in os.walk(folder):
        for file in files:
            zfile.write(os.path.join(folder, file), file)
    zfile.close()
    print('[+] Folder %s compressed to %s.' % (folder, zip_fname))


def main():
    options, subreddits = parser_init()
    with open('config.yaml', 'r') as file:
        try:
            settings = yaml.safe_load(file)
        except yaml.YAMLError as err:
            print(err)
    if settings:
        if 'image-extensions' in settings:
            global img_ext
            img_ext = settings['image-extensions']
        credentials = settings['credentials']
        client = praw.Reddit(
            client_id=credentials['client_id'],
            client_secret=credentials['client_secret'],
            user_agent=user_agent
        )
        for subreddit in subreddits:
            dldest = subreddit
            if options.output:
                dldest = options.output
            images = get_images(client, subreddit, limit=options.count)
            if options.zip:
                download_images(images, '.cache')
                compress_folder('.cache', dldest+'.zip')
                shutil.rmtree('.cache')
            else:
                download_images(images, dldest)


if __name__ == '__main__':
    main()
