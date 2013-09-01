import util
import engine

class Shell:
  def __init__(self, engine):
    self.engine = engine

  def getInput(self):
    return raw_input('>').split()

  def start(self):
    while(True):
      i = self.getInput()
      if len(i) > 0:
        if i == 'exit':
          engine.shutdown(exit(0))
        try:
          engine.build(i)
        except ValueError:
          util.log('command not recognized: ' + cmd[0], '')
