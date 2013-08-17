import io
import os
import subprocess


def parseProps(filepath):
  ''' parses a properties file into a dict '''
  props = {}
  file = open(filepath)
  lines = file.readlines()
  for line in lines:
    # possible problem if any props contain a =
    if line[0] == '#':
      continue
    line = line.strip().split('=')
    if len(line) != 2:
      print 'bad property - keep going'
      print '  ' + str(line)
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

class Shell:
  def __init__(self, engine):
    self.engine = engine
    self.cmds = {
      'start' : engine.startServer,
      'stop' : engine.stopServer,
      'restart' : engine.restartServer,
      'info' : engine.infoServer
    }

  def getInput(self):
    ''' Grabs the input from the user, parses it
      and then returns it '''
    return raw_input('>').split()

  def start(self):
    i = getInput()
    if i in cmds:
      self.cmds[f](i)
    else:
      print 'command not recognized: ' + i[0]
      # throw exception

class Engine:
  java_cmd = 'java'
  server_jar_name = 'minecraft.jar'
  server_start_base_opts = ['-jar', server_jar_name]

  def __init__(self, servers):
    self.servers = servers

  def startServer(self, server, opts=[]):
    print 'starting server: ' + server.name
    serverLog = open('server.out', 'wb')
    subprocess.check_call(java_cmd, server_start_base_opts + opts, stdout=serverLog, stderr=serverLog)

  def stopServer(self, server):
    pass

  def restartServer(self, server, opts=[]):
    stopServer(server)
    startServer(server, opts)

  def infoServer(self, server):
    for prop in server.props:
      print str(prop)
    pass

  def invokeJava(self, cmds):
    pass 

class Server:
  started = False
  def __init__(self, name, props):
    self.name = name
    self.props = props

  def updateProp(self, key, value):
    self.prop[key] = value

  def writeProps(self):
    pass

  def loadProps(self):
    pass

# DO STUFF HERE
for item in loadServers():
  print item.name

