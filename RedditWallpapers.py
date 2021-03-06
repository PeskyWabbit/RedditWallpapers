import requests
import os
import ctypes
import queue
from idna import idnadata
import configparser

USERAGENT = "fake_user_agent v1.0"
FILEPATH = os.path.join(os.getcwd(), r'\images\wallpaper')


def get_pictures_from_subreddit(data, subreddit):
    global extension
    for i, x in enumerate(data):
        current_post = data[i]['data']
        image_url = current_post['url']
        if '.png' in image_url:
            extension = '.png'
        elif '.jpg' in image_url or '.jpeg' in image_url:
            extension = '.jpeg'
        elif 'imgur' in image_url:
            image_url += '.jpeg'
            extension = '.jpeg'
        else:
             continue

        print('Attempting to download picture from r/' + subreddit + '.. ')
        # redirects = False prevents thumbnails denoting removed images from getting in
        image = requests.get(image_url, allow_redirects=False)
        if (image.status_code == 200):
            try:
                output_filehandle = open(FILEPATH + extension, 'wb')
                output_filehandle.write(image.content)
            except Exception as e:
                print(str(e))
            else:
                #no exception, break
                break
    return extension

def get_image():
    config = configparser.ConfigParser()
    config.read('args.ini')
    top = config['Default']['top']
    subreddit = config['Default']['subreddit']
    number = config['Default']['number']

    print('Connecting to r/' + subreddit)
    url = 'https://www.reddit.com/r/{}/top/.json?sort=top&t={}&limit={}'.format(subreddit, top, number)
    response = requests.get(url, headers={'User-agent': USERAGENT})

    if not response.ok:
        print("Error check the name of the subreddit", response.status_code)
        exit()

    if not os.path.exists(os.getcwd() + '\\images'):
        os.mkdir(os.getcwd() + '\\images')

    data = response.json()['data']['children']
    return get_pictures_from_subreddit(data, subreddit)


def set_wallpaper(extension):
    if '.' in (extension):
        print(FILEPATH + extension)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, FILEPATH + extension, 3)
    else:
        print("No image posts were found...\n")

def main():
    set_wallpaper(get_image())

if __name__.endswith('__main__'):
    main()
