import util
import engine

class Shell:

  def __init__(self, engine):
    self.engine = engine
    self.cmds = engine.generateCommands()

  def getInput(self):
    return raw_input('>').split()

  def start(self):
    try:
      while(True):
        i = self.getInput()
        self.process(i)
    except KeyboardInterrupt:
      util.log('\nShutting down...', 'INFO')
  
  def process(self, *i):
    if len(i) > 0:
      i = i[0]
      if i[0] == 'exit':
        engine.shutdown(exit(0))
      if i[0] in self.cmds:
        f = self.cmds[i[0]]
        try:
          if len(i) > 1:
            f(i[:1])
          else: 
            f()
        except TypeError as e:
          print "Bad command: " + str(e)
      else:
        util.log('command not recognized: ' + i[0], '')
