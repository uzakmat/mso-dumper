#!/usr/bin/env python

import globals
import struct

class DOCDirStream:
    """Represents one single word file subdirectory, like e.g. 'WordDocument'."""

    def __init__(self, bytes, params = None, name = None, mainStream = None, doc = None):
        self.bytes = bytes
        self.size = len(self.bytes)
        self.pos = 0
        self.params = params
        self.name = name
        self.mainStream = mainStream
        self.doc = doc
    
    def printAndSet(self, key, value, hexdump = True, end = True):
        setattr(self, key, value)
        if hexdump:
            value = hex(value)
        if end:
            print '<%s value="%s"/>' % (key, value)
        else:
            print '<%s value="%s">' % (key, value)

    def getuInt8(self, bytes = None, pos = None):
        if not bytes:
            bytes = self.bytes
        if not pos:
            pos = self.pos
        return struct.unpack("<B", bytes[pos:pos+1])[0]

    def getuInt16(self, bytes = None, pos = None):
        if not bytes:
            bytes = self.bytes
        if not pos:
            pos = self.pos
        return struct.unpack("<H", bytes[pos:pos+2])[0]

    def getInt16(self, bytes = None, pos = None):
        if not bytes:
            bytes = self.bytes
        if not pos:
            pos = self.pos
        return struct.unpack("<h", bytes[pos:pos+2])[0]

    def getuInt32(self, bytes = None, pos = None):
        if not bytes:
            bytes = self.bytes
        if not pos:
            pos = self.pos
        return struct.unpack("<I", bytes[pos:pos+4])[0]

    def getuInt64(self, bytes = None, pos = None):
        if not bytes:
            bytes = self.bytes
        if not pos:
            pos = self.pos
        return struct.unpack("<Q", bytes[pos:pos+8])[0]

    def getString(self):
        bytes = []
        while True:
            i = self.getuInt8()
            self.pos += 1
            j = self.getuInt8()
            self.pos += 1
            if i != 0 or j != 0:
                bytes.append(i)
                bytes.append(j)
            else:
                break
        return globals.getUTF8FromUTF16("".join(map(lambda x: chr(x), bytes)))

    def getBit(self, byte, bitNumber):
        return (byte & (1 << bitNumber)) >> bitNumber

    def dump(self):
        print '<stream name="%s" size="%s"/>' % (globals.encodeName(self.name), self.size)

# vim:set filetype=python shiftwidth=4 softtabstop=4 expandtab:
