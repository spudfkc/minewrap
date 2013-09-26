import util
import server
import os
import subprocess

class Engine:
  javacmd = 'java'
  modRegistry = {}
  serverProcesses = {}
  servers = []

  def __init__(self):
    self._loadServers()

  def _loadServers(self):
    '''
    creates servers for all the servers in the 'servers' directory

    A server object will attempt to be made if a server.properties
    file exists in the directory.
    '''
    serversDir = 'servers'
    if not os.path.exists(serversDir):
      raise UserWarning('servers directory not found')
    for item in os.listdir(serversDir):
      itemPath = serversDir + os.sep + item
      propsPath = itemPath + os.sep + 'server.properties'
      if os.path.isdir(itemPath) and os.path.exists(propsPath):
        self.servers.append(server.Server(item))

  def generateCommands(self):
    '''
    Returns all available commands that this engine can run
    '''
    cmds = { 
      'start' : self.startServer, 
      'stop'  : self.stopServer, 
      'restart' : self.restartServer, 
      'info' : self.infoServer, 
      'list' : self.listServers, 
      'download-mod' : self.downloadMod, 
      'create-server' : self.createServer, 
      'delete-server' : self.deleteServer 
    } 
    return cmds

  def startServer(self, server, opts=[], logfile='server.out'):
    '''
    Starts the given server

    This will start a server with the specified options. 
    The server is started in a subprocess and a file, 'server.out'
    is created in the server's directory to handle logging.
    '''
    if not 'nogui' in opts:
      opts.append('nogui')
    cmd = [self.javacmd]
    cmd.append('-jar')
    cmd.append(modRegistry[server.mod])

    cmd.extend(opts)
    serverLog = open(server.path+os.sep+logfile, 'wb')
    
    serverProcess = subprocess.Popen(cmd, stdout=serverLog, stderr=serverLog, cwd=server.path)
    self.serverProcesses[server.name] = serverProcess, serverLog
    
  def stopServer(self, server):
    if not server.name in self.serverProcesses:
      raise UserWarning("Server not running: " + server.name)
    serverProcess = self.serverProcesses[server.name]
    serverProcess[0].terminate()
    serverProcess[1].close()
    del self.serverProcesses[serverProcess]

  def restartServer(self, server, opts=[]):
    self.stopServer(server)
    self.startServer(server, opts)

  def infoServer(self, server):
    # refactor this to have a fn that builds/returns
    # the info string then this will print it.
    return '''
      ==========
      == %s 
      ==
      -- TODO TODO TODO --
    ''' % server.name

  def listServers(self):
    for server in self.servers:
      result = '* ' + server.name
      status = 'NOT STARTED'
      if server.name in self.serverProcesses:
        status = 'RUNNING'
      result = result + '\t[' + status + ']'
      print result

  def shutdown(self, callback=None):
    '''
    Shutsdown all servers, then calls callback
    '''
    for server in self.servers:
      self.stopServer(server)
    if not callback is None:
      callback()

  def downloadMod(self, modName, modVersion):
    pass

  def createServer(self, serverName, props, mod='vanilla'):
    '''
    check cache for mod + version
      download if not there
    create server directory
    copy mod
    put props 
    '''
    pass

  def deleteServer(self, serverName):
    '''
    make sure server exists
    check if server is running - ask to shutdown first?
    delete directory
    '''
    pass

  def restoreServer(self, serverName):
    '''
    Returns a server object given a server name
    '''
    server = [item for item in self.servers if item.name == serverName]
    found = len(server)
    if found == 1:
      return server[0]
    elif found > 1:
      raise UserWarning("Multiple servers found with name: " + serverName)
    else:
      raise UserWarning("No server found with name: " + serverName)
