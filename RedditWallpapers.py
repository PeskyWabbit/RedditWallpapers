import requests
import os
import ctypes
import configparser


USERAGENT = "fake_user_agent v1.0"
extension = ""
FILEPATH = os.getcwd() + '\\images\\wallpaper'


def get_pictures_from_subreddit(data, subreddit):
    global extension
    fileNotSaved = True
    for i in range(len(data)):
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
            extension = ".jpeg"

        if (fileNotSaved):
            if os.path.exists(FILEPATH + extension):
                os.remove(FILEPATH + extension)
            print('downloading pictures from r/' + subreddit + '.. ' + str((i*100)//len(data)) + '%')
            # redirects = False prevents thumbnails denoting removed images from getting in
            image = requests.get(image_url, allow_redirects=False)
            if(image.status_code == 200):
                try:
                    output_filehandle = open(FILEPATH + extension, mode='bx')
                    output_filehandle.write(image.content)
                except:
                    pass
            if(os.path.exists(FILEPATH + extension)):
                print(FILEPATH + extension + " exists!")
                fileNotSaved = False

def getImage():
    config = configparser.ConfigParser()
    config.read('args.ini')
    top = config['Default']['top']
    subreddit = config['Default']['subreddit']
    number = config['Default']['number']

    print('Connecting to r/' + subreddit)
    url = 'https://www.reddit.com/r/' + subreddit + '/top/.json?sort=top&t=' + \
            top + '&limit=' + str(number)
    response = requests.get(url, headers={'User-agent': USERAGENT})

    if not response.ok:
        print("Error check the name of the subreddit", response.status_code)
        exit()

    if not os.path.exists(os.getcwd() + '\\images'):
        os.mkdir(os.getcwd() + '\\images')

    data = response.json()['data']['children']
    get_pictures_from_subreddit(data, subreddit)

def setWallpaper2():
    print(FILEPATH + extension)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, FILEPATH + extension, 3)

getImage()
setWallpaper2()
