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
      'info' : engine.infoServer,
      'list' : engine.listServers
    }

  def getInput(self):
    ''' Grabs the input from the user, parses it
      and then returns it '''
    return raw_input('>').split()

  def start(self):
    while(True):
      i = self.getInput()
      if i == 'exit':
        exit(0)
      if len(i) > 0 and i[0] in self.cmds:
        self.cmds[i[0]](i[0:])
        # self.cmds[i[0]](i[1], i[2:])
      else:
        print 'command not recognized: ' + str(i)
        # throw exception

class Engine:
  javacmd = 'java'
  modRegistry = {
    'vanilla' : 'minecraft.jar',
    'tekkit'  : 'Tekkit.jar'
  }

  def __init__(self, servers):
    self.servers = servers

  def startServer(self, opts):
    print "opts " + str(opts)
    servern = opts[1]
    opts = opts[1:]
    if type(servern) is str:
      server = self.restoreServer(servern)
    if server is None:
      print 'server %s does not exist!' % servern
      return
    print 'starting server: ' + server.name

    cmd = [self.javacmd]
    cmd.extend(opts)
    cmd.append('-jar')
    mod = self.modRegistry[server.mod]
    cmd.append(mod)

    serverLog = open('server.out', 'wb')
    subprocess.check_call(cmd, stdout = serverLog, stderr = serverLog)

  def stopServer(self, server):
    pass

  def restartServer(self, server, opts=[]):
    stopServer(server)
    startServer(server, opts)

  def infoServer(self, server):
    for prop in server.props:
      print str(prop)
    pass

  def listServers(self, filtr):
    for server in self.servers:
      print '* ',
      print server.name

  def restoreServer(self, serverName):
    server = [item for item in self.servers if item.name == serverName]
    if len(server) == 1:
      return server[0]

class Server:
  started = False
  def __init__(self, name, props, mod = 'vanilla'):
    self.name = name
    self.props = props
    self.mod = mod

  def updateProp(self, key, value):
    self.prop[key] = value

  def writeProps(self):
    pass

  def loadProps(self):
    pass


########## DO STUFF HERE ##########
servers = loadServers()
servers[0].mod = 'tekkit'
eng = Engine(servers)

shell = Shell(eng)
shell.start()
