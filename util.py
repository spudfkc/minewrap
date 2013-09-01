import os

def writePropsFile(props, filepath):
  '''
  writes out a dict to a file

  uses os specific line separators 

  the contents of the file will be:
  prop1=value1
  ...
  propn=valuen
  
  '''
  f = open(filepath, 'w')
  for prop in props:
    f.write(prop+'='+props[prop]+os.linesep)
  f.close()

def loadPropsFile(filepath):
  '''
  Loads a properties file into a dict
  '''
  props = {}
  f = open(filepath)
  lines = f.readlines()
  for line in lines:
    line = line.strip()
    if line[0] == '#':
      continue
    line = line.split('=')
    if len(line) != 2:
      log('bad property - keep going\n\t'+str(line), 'WARNING') 
    props[line[0]] = line[1]
  return props    


def log(msg, level='INFO'):
  '''
  Very basic logger. It just wraps print
  '''
  prefix = '[' + level + '] '
  print prefix+msg 

def enum(**enums):
  '''
  Creates and return an Enum type
  '''
  return type('Enum', (), enums)
