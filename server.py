import os
import util


class Server:
  def __init__(self, name, mod=None):
    self.name = name
    self.mod = mod
    self.path = 'servers' + os.sep + self.name
    self.status = 'unknown'
    self.loadProps()

  def updateProp(self, key, value):
    '''
    This will update a server property in memory
    '''
    self.props[key] = value

  def writeProps(self):
    '''
    Writes out the server.properties file for the server.

    Updated properties will not be saved until this is called.
    '''
    util.writePropsFile(self.props, self.path + os.sep + 'server.properties')

  def loadProps(self):
    '''
    Loads the server.properties file for the server into the app
    '''
    self.props = util.loadPropsFile(self.path + os.sep + 'server.properties')

  def findMod(self):
    '''
    Attempts to find and set the mod based on the jars in the server directory

    This will raise a UserWarning exception if there is not exactly 1 jar found.
    If an exception is raised, the mod will have to be manually specified.
    '''
    serverdir = 'servers'
    foundJars = []   
    for files in os.listdir(self.path):
      if files.endswith('.jar'):   
        foundJars.append(files)   
   
    numberOfJars = len(foundJars)   
   
    if numberOfJars > 1:   
      util.log('you will need to specify a mod manually')        
      raise UserWarning("Multiple jars found for server")   
    elif numberOfJars < 1:   
      util.log('you will need to specify a mod manually')        
      raise UserWarning("No jars found for server")   
    else:   
      util.log('using mod: ' + str(foundJars[0]))        
      self.mod = foundJars[0]
