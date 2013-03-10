#!/usr/bin/env python

# by jiva

import sys
from struct import pack,unpack

if '-h' in sys.argv or '--help' in sys.argv:
	print 'pngparser by jiva'
	print 'Usage:\t' + sys.argv[0] + ' [OPTION]... [FILE] '
	print '\t-h  --help  \tPrint usage information.'
	print '\t-e  --header\tPrint PNG header.'
	print '\t-l  --length\tPrint lengths of each chunk.'
	print '\t-t  --type  \tPrint types of each chunk.'
	print '\t-c  --crc   \tPrint CRC of each chunk.'
	print '\t-d  --dump  \tDump each chunk (default).'
	sys.exit(0)

png = open(sys.argv[-1]).read()

critical_chunks = ['IHDR', 'PLTE', 'IDAT', 'IEND']
ancillary_chunks = ['bKGD', 'cHRM', 'gAMA', 'hIST', 'iCCP', 'iTXt', 'pHYs', 'sBIT', 'sPLT', 'sRGB', 'sTER', 'tEXt', 'tIME', 'tRNS', 'zTXt']

header = png[:8]

if '-e' in sys.argv or '--header' in sys.argv: 
	print 'Header:\t',
	for h in header:print h.encode('hex'),

chunk_offset = 8

while True:
	chunk_length = unpack('>i', png[chunk_offset:chunk_offset+4])[0]
	if '-l' in sys.argv or '--length' in sys.argv:
		print 'Chunk Length:\t', chunk_length
	chunk_offset += 4

	chunk_type = png[chunk_offset:chunk_offset+4]
	if '-t' in sys.argv or '--type' in sys.argv:
		print 'Chunk Type:\t', repr(chunk_type),
		if chunk_type in ancillary_chunks:
			print '(Ancillary chunk)'
		elif chunk_type in critical_chunks:
			print '(Critical chunk)'
		else:
			print '(Unknown chunk)'
	chunk_offset += 4

	chunk_data = png[chunk_offset:chunk_offset+chunk_length]
	if '-d' in sys.argv or '--dump' in sys.argv:
		open(chunk_type + '_' + str(chunk_offset) + '.chunk','w').write(chunk_data)
	chunk_offset += chunk_length

	chunk_crc = png[chunk_offset:chunk_offset+4]
	if '-c' in sys.argv or '--crc' in sys.argv:
		print 'Chunk CRC:\t', chunk_crc.encode('hex')
	chunk_offset += 4

	if chunk_offset == len(png):
		break
