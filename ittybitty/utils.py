from math import floor

# Why is this hardcoded? Because there's no point in computing these values
# over and over again.  Should handle up to 18,446,744,073,709,551,615 URLs, and
# by the time you get that many URLs, your limitation will most likely be your
# disk space and whatnot...
VALID = [('Z',9223372036854775808L),('Y',4611686018427387904L),
('X',2305843009213693952L),('W',1152921504606846976L),('V',576460752303423488L),
('U',288230376151711744L),('T',144115188075855872L),('S',72057594037927936L),
('R',36028797018963968L),('Q',18014398509481984L),('P',9007199254740992L),
('O',4503599627370496L),('N',2251799813685248L),('M',1125899906842624L),
('L',562949953421312L),('K',281474976710656L),('J',140737488355328L),
('I',70368744177664L),('H',35184372088832L),('G',17592186044416L),
('F',8796093022208L),('E',4398046511104L),('D',2199023255552L),
('C',1099511627776L),('B',549755813888L),('A',274877906944L),
('z',137438953472L),('y',68719476736L),('-',34359738368L),('x',17179869184L),
('w',8589934592L),('_',4294967296L),('v',2147483648L),('u',1073741824),
('9',536870912),('t',268435456),('s',134217728),('8',67108864),('r',33554432),
('q',16777216),('7',8388608),('p',4194304),('o',2097152),('6',1048576),
('n',524288),('m',262144),('5',131072),('l',65536),('k',32768),('4',16384),
('j',8192),('i',4096),('3',2048),('h',1024),('g',512),('2',256),('f',128),
('e',64),('1',32),('d',16),('c',8),('0',4),('b',2),('a',1)]

def gen_shortcut_old(num):
    """
    Generates a short URL for any URL on your Django site.  It is intended to
    make long URLs short, a la TinyURL.com.
    """
    short = ''
    for key, val in VALID:
        if floor(num / val) != 0:
            short += key
            num -= val
    return short
    
def gen_shortcut(input):
    CLIST="0123456789abcdefghijklmnopqrstuvwxyz"
    rv = ""
    while input != 0:
        rv = CLIST[input % 36] + rv
        input /= 36
    return rv
