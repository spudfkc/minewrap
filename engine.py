import util
import server
import os
import subprocess

class Engine:
  javacmd = 'java'
  modRegistry = {}
  serverProcesses = {}

  def __init__(self, severs):
    self.servers = servers

  def startServer(self, server, opts=[], logfile='server.out'):
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
    print '''
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

  def restoreServer(self, serverName):
    server = [item for item in self.servers if item.name == serverName]
    found = len(server)
    if found == 1:
      return server[0]
    elif found > 1:
      raise UserWarning("Multiple servers found with name: " + serverName)
    else:
      raise UserWarning("No server found with name: " + serverName)
    
  def build(self, cmd):
    raise NotImplementedError("TODO")
