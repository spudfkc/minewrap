import urllib2
import os
import io

class Downloader:
  modlinks = {
    'vanilla' : 'https://s3.amazonaws.com/Minecraft.Download/versions/1.6.2/minecraft_server.1.6.2.jar'
  }

  def __init__(self):
    pass

  def download(self, mod, version='default'):
    url = self.modlinks[mod]
    response = urllib2.urlopen(url)
    self.saveFile(response.read(), os.path.basename(url))

  def load(self):
    pass 

  def saveFile(self, tosave, where):
    f = open('tmp/'+where, 'wb')
    f.write(tosave)
