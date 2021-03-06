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

def writeProps(filepath, **props):
  propsFile = open(filepath, 'w')
  for prop in props:
    propsFile.write(prop+'='+props[prop]+'\n')
  propsFile.close()

def loadServers():
  '''
    loads all the servers from the servers dir 
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

  serverProcesses = {}

  def __init__(self, servers):
    self.servers = servers

  def startServer(self, opts):
    ''' starts the named server with any given options
        also adds the new process to the list of running
        server processes '''
    servern = opts[1]
    opts = opts[2:]
    if type(servern) is str:
      server = self.restoreServer(servern)
    if server is None:
      print 'server %s does not exist!' % servern
      return
    print 'starting server: ' + server.name

    opts.append('nogui')

    cmd = [self.javacmd]
    cmd.append('-jar')
    mod = self.modRegistry[server.mod]
    cmd.append(mod)

    cmd.extend(opts)
    
    serverLog = open('servers/'+servern+'/server.out', 'wb')
    print "[DEBUG] "+str(cmd)
    serverProcess = subprocess.Popen(cmd, stdout=serverLog, stderr=serverLog, cwd='servers/'+servern)
    self.serverProcesses[server.name] = serverProcess

  def stopServer(self, opts):
    ''' stops the given server ''' 
    server = opts[1]
    if type(server) is str:
      server = self.restoreServer(server)
    if server is None: 
      print 'server %s does not exist!' % servern 
      return
    print '[DEBUG] ' + str(server)
    if server.name in self.serverProcesses: 
      serverProcess = self.serverProcesses[server.name]
      print 'stopping server: ' + server.name
      serverProcess.terminate()
      del self.serverProcesses[server.name]
    else:
      print 'server: ' + server.name + ' not found'

  def restartServer(self, opts):
    print 'restarting server'
    self.stopServer(opts)
    self.startServer(opts)

  def infoServer(self, opts):
    server = opts[1]
    if type(server) is str:
      server = self.restoreServer(server)
    if server is None:
      print 'server %s does not exist!' % servern
      return
    print '''
      ========================================
      ==  %s
      ==
      ---- This is all TODO ----
      ==  Players: 0/999
      ==  Ops: #
      ==    list ops here
      ==  wolds 
      
      == == == ==
      ==  host
      ==  port
      ==  
      ''' % server.name

  def listServers(self, filtr):
    for server in self.servers:
      print '* ',
      print server.name,
      status = 'NOT STARTED'
      if server.name in self.serverProcesses: 
        status = 'RUNNING'
      print '\t[' + status + ']'

  def restoreServer(self, serverName):
    ''' restores the server object from the given server name '''
    server = [item for item in self.servers if item.name == serverName]
    if len(server) == 1:
      return server[0]

class Server:
  ''' contains all the attributes of a server, but holds no state '''

  def __init__(self, name, props, mod = 'vanilla'):
    self.name = name
    self.props = props
    self.mod = mod

  def updateProp(self, key, value):
    ''' updates a property on the server in memory, to save you 
        will need to write out the props '''
    self.prop[key] = value

  def writeProps(self):
    writeProps('servers'+os.sep+self.server.name+os.sep+'server.properties', self.props)

  def loadProps(self):
    self.props = parseProps('servers'+os.sep+self.server.name+os.sep+'server.properties')

  def findMod(self):
    foundJars = []
    for files in os.listdir('servers'+os.sep+self.server.name):
      if files.endswith('.jar'):
        foundJars.append(files)
    if len(foundJars) > 1:
      # TODO exception?
      print 'warning - found multiple jars for server'
      if 'minecraft_server.jar' in foundJars:
        print 'defaulting to vanilla'
        self.mod = 'vanilla'
      else: 
        print 'defaulting to first found'
        self.mod = foundJars[0]
    elif len(foundJars) < 1:
      # TODO exception
      print 'error - no jars found for server'
      self.mod = None

########## DO STUFF HERE ##########
servers = loadServers()
servers[0].mod = 'tekkit'
eng = Engine(servers)

shell = Shell(eng)
shell.start()
