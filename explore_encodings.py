#!/usr/bin/env python3

import base64
import struct

VAL = b'EFG'

#
# Various representations of b'EFG'
#
vals = {}
vals[1] =  '454647' # string rep of hexlified bytes
vals[2] =  b'454647' # bytes rep of vals1
vals[3] =  '343534363437' # (hexlified string of val1)
vals[4] =  b'343534363437' # bytes rep of vals3
vals[5] =  '45 46 47' # (string with spaces)
vals[6] =  ['45', '46', '47'] # (list of strings)
vals[7] =  'fffe450046004700' # (string representation of utf-16 encoding of 'EFG') 
vals[8] =  b'\xff\xfe\x45\x00\x46\x00\x47\x00' # (bytes representation of utf-16 encoding of 'EFG')
vals[9] =  b'\x00\x00\x00\x45\x00\x00\x00\x46\x00\x00\x00\x47' # (bytes representation of 32-bit, big-endian ints)
vals[10] = b'\x45\x00\x46\x00\x47\x00' # similar to vals9; bytes of 16-bit, l-e ints
vals[11] = [0x45, 0x46, 0x47] # similar to vals6
vals[12] = 'EFG' # string rep of bytes
vals[13] = 'RUZH\n' # base64-encoded string rep

#
# Tools to explore
#

# bytes.decode()

# bytes.fromhex(): same as binascii.unhexlify(str).  Converts hexlified string to binary, e.g. 
# >>> bytes.fromhex('454647')
# b'EFG'

# s.encode(): encode s with given encoding; return bytes.  e.g.
# >>> s = 'EFG'
# >>> s.encode() # default is utf-8
# b'EFG'
# >>> s.encode('utf-16')
# b'\xff\xfeE\x00F\x00G\x00'

# struct.unpack()
# int(), hex(), ord(), str()
# base64 (and maybe binascii, uu, binhex)

def getval(idx):
    return vals[idx]

def main():

    # encode/decode each val

    x = getval(1)
    y = bytes.fromhex(x)
    assert VAL == y

    x = getval(2)
    z = bytes.decode(x) # decodes bytes to str
    y = bytes.fromhex(z)
    assert VAL == y

    x = getval(3)
    z = bytes.fromhex(x)
    z = bytes.decode(z)
    x = bytes.fromhex(z)
    assert VAL == y

    x = getval(4)
    z = bytes.decode(x)
    z = bytes.fromhex(z)
    z = bytes.decode(z)
    y = bytes.fromhex(z)
    assert VAL == y

    x = getval(5)
    y = bytes.fromhex(x)
    assert VAL == y
    
    x = getval(6)
    z = ''.join(x)
    y = bytes.fromhex(z)
    assert VAL == y
    
    x = getval(7)
    z = bytes.fromhex(x)
    z = bytes.decode(z, 'utf-16')
    y = z.encode()
    assert VAL == y

    x = getval(8)
    z = bytes.decode(x, 'utf-16')
    y = z.encode()
    assert VAL == y

    x = getval(9)
    zlist = []
    idx = 0
    INT_LEN = struct.calcsize(">I")
    while idx < len(x):
        zlist.append(struct.unpack(">I", x[idx:idx+INT_LEN])[0])
        idx += INT_LEN
    y = bytes(zlist)
    assert VAL == y

    x = getval(10)
    zlist = []
    idx = 0
    SHORT_LEN = struct.calcsize("<H")
    while idx < len(x):
        zlist.append(struct.unpack("<H", x[idx:idx+SHORT_LEN])[0])
        idx += SHORT_LEN
    y = bytes(zlist)
    assert VAL == y
    
    x = getval(11)
    y = bytes(x)
    assert VAL == y
    
    x = getval(12)
    y = x.encode()
    assert VAL == y
    
    x = getval(13)
    y = base64.b64decode(x)
    assert VAL == y

if __name__ == "__main__":
    main()

