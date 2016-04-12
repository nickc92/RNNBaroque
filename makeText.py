
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789)!@#$%%^&*('
ofl = open('outstr.txt', 'w')
for ln in open('allnotes.txt'):
    dat = eval(ln)
    for slice in dat:
        for note in slice:
            dur = note[1]
            if dur > 8: dur = 8
            noteInd = note[0] - 10
            if noteInd < 0: noteInd = 0
            if noteInd >= len(chars): noteInd = len(chars) - 1
            ofl.write(chars[noteInd] * dur)
        ofl.write(' ')
ofl.close()

        
        
