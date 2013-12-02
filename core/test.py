from phyModel import phyModel

argv = {}
argv['sigma'] = 2
argv['PACKET_LENGTH'] = 4*20
argv['DATA_RATE'] = 250000

test = phyModel(argv)

print test.calPSR()
