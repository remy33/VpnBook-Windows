#!/usr/bin/python
# Filename: VnpBook.py

#Created by Remy Berg, 08/12/15

import urllib2


class VpnBookHandler(object):
    """Access vpn book and grab the password"""

    __startString = "<li>Password: <strong>"
    __endString = "</strong></li>"
    version = '0.1'

    def getVpnPassword(self):
        """Do some things.
        """
        #content = urllib2.urlopen("https://www.vpnbook.com/freevpn").read()
        #password = self.CutPassword(content)

        r = urllib2.Request("https://www.vpnbook.com/freevpn");
        f = urllib2.build_opener().open(r)
        response = f.read()
        s = self.__CutPassword(response)

        return (s)


    def __CutPassword(self, httpContent):
        """Cut the password.
        :param httpContent: VpnHandler.
        """
        
        startIndex = httpContent.find(self.__startString)
        stopIndex = httpContent.find(self.__endString, startIndex)
        password = httpContent[startIndex + len(self.__startString):stopIndex]
        return (password)

class WindowsVpnHandler(object):
    POWERSHELL = "powershell "

    def StartVpn(self, vpnName, ServerAddress, username, password, tunnelType = "Pptp"):
        if (self._IsVpnExist(vpnName) == False):
            print(self._CreateVpn(vpnName, ServerAddress, tunnelType))
        print(self._Connect(vpnName, username, password))

    def _IsVpnExist(self, vpnName):
        return False

    def _Connect(self, vpnName, userName, password):
        return subprocess.call(self.POWERSHELL + "rasdial {0} {1} {2}".format(vpnName, userName, password))

    def _CreateVpn(self, vpnName, ServerAddress, TunnelType):
        return  subprocess.call(self.POWERSHELL +
                                "Add-VpnConnection -Name \"{0}\" -ServerAddress \"{1}\" -TunnelType \"{2}\""
                                .format(vpnName, ServerAddress, TunnelType))

if (__name__ == '__main__'):
    c = VpnBookHandler()
    password = c.getVpnPassword()
    print(password)
    import platform
    is_windows = any(platform.win32_ver())
    if (is_windows == True):
        import subprocess
        windowsHandler = WindowsVpnHandler()
        windowsHandler.StartVpn("'Canadian Vpn'","ca1.vpnbook.com", "vpnbook", password,)

# End of VnpBook.py