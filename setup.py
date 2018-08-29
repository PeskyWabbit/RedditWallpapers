from cx_Freeze import setup, Executable


setup(name='RedditWallpapers',
      version='0.1',
      description='Set Wallpaper',
      executables=[Executable("RedditWallpapers.py")])


