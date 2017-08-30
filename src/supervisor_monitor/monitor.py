from xmlrpc.client import ServerProxy as RpcServer
from xmlrpc.client import ProtocolError
from http.client import RemoteDisconnected
import re


class Monitor(object):
    _server = None
    def __init__(self, url, username, password):
        self.url = getUrl(url, username, password)
        print(self.url)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        if exc_type is None:
            return
        if issubclass(exc_type, (ProtocolError,)):
            raise PermissionError
        if issubclass(exc_type, (RemoteDisconnected,)):
            raise ConnectionRefusedError

    def reload(self):
        with self:
            return self.getRpcServer().supervisor.reloadConfig()

    def getRpcServer(self):
        if self._server is None:
            self._server = RpcServer(self.url)
        return self._server

    def shutdown(self):
        self.getRpcServer().supervisor.shutdown()

    def reboot(self):
        self.getRpcServer().supervisor.restart()


    def getIdentification(self):
        with self:
            return self.getRpcServer().supervisor.getIdentification()

    def getStatus(self):
        try:
            return self.getRpcServer().supervisor.getState()['statecode']
        except:
            return -100

    def getPid(self):
        try:
            return self.getRpcServer().supervisor.getPid()
        except:
            return 0

    def getProcessStatus(self, name):
            return self.getRpcServer().supervisor.getProcessInfo(name)

    def getServiceIter(self):
        try:
            with self:
                for service in self.getRpcServer().supervisor.getAllProcessInfo():
                    print(service)
                    res = {
                        'name': service['name'],
                        'group': service['group'],
                        'pid': service['pid'],
                        'state': service['state'],
                        'now': service['now'],
                        'start': service['start'],
                        'stop': service['stop'],
                        'exit_status': service['exitstatus']
                    }
                    yield res
        except PermissionError:
            pass

    def start(self, name=None, wait=True):
        if name is None:
            self.getRpcServer().supervisor.startAllProcesses()
        self.getRpcServer().supervisor.startProcess(name)

    def stop(self, name=None, wait=True):
        if name is None:
            self.getRpcServer().supervisor.stopAllProcesses()
        self.getRpcServer().supervisor.stopProcess(name)

    def restart(self, name=None):
        if name is None:
            self.stop()
            self.start()
        self.stop(name)
        self.start(name)

    def sendChars(self, name, chars):
        self.getRpcServer().supervisor.sendProcessStdin(name, chars)


def getUrl(url, username=None, password=None):
    if username:
        url_freg_res = re.match(r'(?:(?P<proto>http|https)://)?'
                                r'(?:'
                                r'(?P<username>[^\:@]*)'
                                r'(?:\:(?P<password>[^@]*))?'
                                r'@)?(?P<domain>[^/@]+)(?P<path>/.*)?', url, flags=re.I)
        if url_freg_res:
            url_freg = url_freg_res.groupdict(default='')
            url_freg['username'] = username
            url_freg['password'] = password
            url_freg['proto'] = url_freg['proto'] or 'https'
            uri = "{proto}://{username}:{password}@{domain}{path}".format(
                **url_freg
            )
        else:
            raise SyntaxError(url)
    else:
        uri = url
    return uri

def getIdentification(url, username=None, password=None):
    with RpcServer(getUrl(url, username, password)) as client:
        identification = client.supervisor.getIdentification()
    return identification



