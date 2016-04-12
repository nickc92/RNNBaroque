lenCnts = {}
for ln in open('allnotes.txt'):
    dat = eval(ln)
    for slice in dat:
        for note in slice:
            if note[1] not in lenCnts: lenCnts[note[1]] = 0
            lenCnts[note[1]] += 1

    for length in sorted(lenCnts):
        print length, lenCnts[length]
    print '-------'
    
