

class CLIHelper:

    cmds = {
        'start' : engine.startServer,
        'stop'  : engine.stopServer,
        'restart' : engine.restartServer,
        'info' : self.infoServer,
        'list' : engine.listServers,
        'download-mod' : engine.downloadMod,
        'create-server' : self.createServerCli,
        'delete-server' : self.deleteServerCli
    }

    def __init__(self, engine):
        self.engine = engine
      
    def infoServer(self, serverName):
        server = self.engine.restoreServer(serverName)
        info = self.engine.infoServer(server)
        # maybe do formatting here instead of in engine?
        print info

    def createServerCli(self, serverName, serverMod):
        pass

    def deleteServerCli(self, serverName):
        pass

    def shutdown(self, callback):
        pass
