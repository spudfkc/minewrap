import io
import os

class Engine:
  def __init__(self, servers):
    self.servers = servers

  def startServer(self, server, opts={}):
    pass

  def stopServer(self, server):
    pass

  def restartServer(self, server, opts={}):
    stopServer(server)
    startServer(server, opts)

class Server:
  def __init__(self, name, props):
    self.name = name
    self.props = props

  def updateProps(self, props):
  ''' updates server.properties 
      if no property specified, then no change
  '''
    pass

def parseProps(filepath):
''' parses a properties file into a dict '''
  props = {}
  file = open(filepath)
  lines = file.readlines()
  for line in lines:
    # possible problem if any props contain a =
    line = line.strip().split('=')
    if len(line) != 2:
      print 'bad properties file - keep going'
      continue
    props[line[0]] = line[1]
  return props

def loadServers():
''' loads all the servers from the servers dir 
    a server.properties file must exist in the 
    server directory for the server to be 
    recognized
'''
  servers = []
  serverDir = 'servers'
  if not os.path.exists(serverDir):
    print 'No server directory!'
    return None
  for item in os.listdir(serverDir):
    itemPath = serverDir + os.sep + item
    propsPath = itemPath + os.sep + 'server.properties'
    if os.path.isdir(itemPath) and os.path.exists(propsPath):
      servers.append(Server(item, parseProps(propsPath)))
  print 'Loaded %d servers' % len(servers)
  return servers

print loadServers()

