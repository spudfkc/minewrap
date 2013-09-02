import util
import engine

class Shell:

  def __init__(self, engine):
    self.engine = engine
    cmds = {
      'start' : engine.startServer,
      'stop'  : engine.stopServer,
      'restart' : engine.restartServer,
      'info' : engine.infoServer,
      'list' : engine.listServers
    }

  def getInput(self):
    return raw_input('>').split()

  def start(self):
    while(True):
      i = self.getInput()
      self.process(i)
  
  def process(self, *i):
    if len(i) > 0:
      if i[0] == 'exit':
        engine.shutdown(exit(0))
      if i[0] in self.cmds:
        f = cmds[i[0]]
        if len(i) > 1:
          f(i[:1])
        else: 
          f()
      else:
        util.log('command not recognized: ' + i[0], '')
