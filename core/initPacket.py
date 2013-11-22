from source import source
from event import event

def initPacket(t,src,n):
	argv = {}
	argv['time'] = t
	argv['actType'] = 'sendMac'
	argv['src'] = src
	argv['des'] = n - 1
	argv['pacSize'] = 60
	argv['pacData'] = src
	argv['pacType'] = 'data'
	argv['pacAckReq'] = True
	e = event(argv)
	return e

