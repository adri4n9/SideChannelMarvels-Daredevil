#!/usr/bin/env python3

multinv=[
    0x00, 0x01, 0x8D, 0xF6, 0xCB, 0x52, 0x7B, 0xD1, 0xE8, 0x4F, 0x29, 0xC0, 0xB0, 0xE1, 0xE5, 0xC7,
    0x74, 0xB4, 0xAA, 0x4B, 0x99, 0x2B, 0x60, 0x5F, 0x58, 0x3F, 0xFD, 0xCC, 0xFF, 0x40, 0xEE, 0xB2,
    0x3A, 0x6E, 0x5A, 0xF1, 0x55, 0x4D, 0xA8, 0xC9, 0xC1, 0x0A, 0x98, 0x15, 0x30, 0x44, 0xA2, 0xC2,
    0x2C, 0x45, 0x92, 0x6C, 0xF3, 0x39, 0x66, 0x42, 0xF2, 0x35, 0x20, 0x6F, 0x77, 0xBB, 0x59, 0x19,
    0x1D, 0xFE, 0x37, 0x67, 0x2D, 0x31, 0xF5, 0x69, 0xA7, 0x64, 0xAB, 0x13, 0x54, 0x25, 0xE9, 0x09,
    0xED, 0x5C, 0x05, 0xCA, 0x4C, 0x24, 0x87, 0xBF, 0x18, 0x3E, 0x22, 0xF0, 0x51, 0xEC, 0x61, 0x17,
    0x16, 0x5E, 0xAF, 0xD3, 0x49, 0xA6, 0x36, 0x43, 0xF4, 0x47, 0x91, 0xDF, 0x33, 0x93, 0x21, 0x3B,
    0x79, 0xB7, 0x97, 0x85, 0x10, 0xB5, 0xBA, 0x3C, 0xB6, 0x70, 0xD0, 0x06, 0xA1, 0xFA, 0x81, 0x82,
    0x83, 0x7E, 0x7F, 0x80, 0x96, 0x73, 0xBE, 0x56, 0x9B, 0x9E, 0x95, 0xD9, 0xF7, 0x02, 0xB9, 0xA4,
    0xDE, 0x6A, 0x32, 0x6D, 0xD8, 0x8A, 0x84, 0x72, 0x2A, 0x14, 0x9F, 0x88, 0xF9, 0xDC, 0x89, 0x9A,
    0xFB, 0x7C, 0x2E, 0xC3, 0x8F, 0xB8, 0x65, 0x48, 0x26, 0xC8, 0x12, 0x4A, 0xCE, 0xE7, 0xD2, 0x62,
    0x0C, 0xE0, 0x1F, 0xEF, 0x11, 0x75, 0x78, 0x71, 0xA5, 0x8E, 0x76, 0x3D, 0xBD, 0xBC, 0x86, 0x57,
    0x0B, 0x28, 0x2F, 0xA3, 0xDA, 0xD4, 0xE4, 0x0F, 0xA9, 0x27, 0x53, 0x04, 0x1B, 0xFC, 0xAC, 0xE6,
    0x7A, 0x07, 0xAE, 0x63, 0xC5, 0xDB, 0xE2, 0xEA, 0x94, 0x8B, 0xC4, 0xD5, 0x9D, 0xF8, 0x90, 0x6B,
    0xB1, 0x0D, 0xD6, 0xEB, 0xC6, 0x0E, 0xCF, 0xAD, 0x08, 0x4E, 0xD7, 0xE3, 0x5D, 0x50, 0x1E, 0xB3,
    0x5B, 0x23, 0x38, 0x34, 0x68, 0x46, 0x03, 0x8C, 0xDD, 0x9C, 0x7D, 0xA0, 0xCD, 0x1A, 0x41, 0x1C
]

def ROTL8(x,shift):
    return (((x) << (shift)) & 0xff) | ((x) >> (8 - (shift)))

def p(name, f):
    with open(name, 'wb') as out:
        s=b""
        for q in range(256):
            if q % 16 != 0:
                s+=b" "
            s+=b"0x%02x," % f(q)
            if q % 16 == 15:
                out.write(s+b"\n")
                s=b""

def getrots(x):
    l=[]
    for n in range(8):
        l.append(ROTL8(x,n))
    return str(sorted(l)), l[0]

# generate list of non-redundant targets
fingerprints=set()
targets=[]
for i in range(1,256):
    fingerprint, c = getrots(i)
    if fingerprint not in fingerprints:
        fingerprints.add(fingerprint)
        targets.append(c)

def genaff(b, c=0):
    bits=[]
    for i in range(8):
        if b & (1<<i):
            bits.append(i)
    #print(bits)
    a=[]
    for q in range(256):
        qq=0
        for bb in bits:
            qq^=ROTL8(q, bb)
        a.append(qq ^ c)
    return a

def gensboxinv(b, c=0):
    a = genaff(b, c)
    # AES sboxinv affine transformation:
    affinv = genaff(0x4a, 0x05)
    s=[]
    for q in range(256):
        s.append(a[multinv[affinv[q]]])
    name="AES_AFTER_SBOXINV"
    name+="_x%02X" % b
    if c != 0:
        name+="+%02x" % c
    p(name, lambda x: s[x])

def gensbox(b, c=0):
    a = genaff(b, c)
    # AES sbox affine transformation:
    aff = genaff(0x1f, 0x63)
    s=[]
    for q in range(256):
        s.append(a[aff[multinv[q]]])
    name="AES_AFTER_SBOX"
    name+="_x%02X" % b
    if c != 0:
        name+="+%02x" % c
    p(name, lambda x: s[x])

# old multinv target
gensbox(0x4a, 0x05)

for i in targets:
    gensboxinv(i)

for i in targets:
    gensbox(i)
