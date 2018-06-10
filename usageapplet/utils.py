def kibibytes_to(kibibytes, to='g', bsize=1024):
    a = {'m': 1, 'g': 2}
    r = float(kibibytes)
    for i in range(a[to]):
        r = r / bsize
    return r
