import midi, sys

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789)!@#$%%^&*('
charToInd = {}
for i, c in enumerate(chars):
    charToInd[c] = i

s = open(sys.argv[1]).read().strip()
events = []
pos = 0
delta = 100
pcs = s.split(' ')
for pc in pcs:
    charCnts = {}
    for c in pc:
        if c not in charCnts: charCnts[c] = 0
        charCnts[c] += 1
    for c, cnt in charCnts.items():
        events.append([pos, 1, charToInd[c]])
        events.append([pos + cnt * delta, 0, charToInd[c]])
        #events.append([pos + delta / 2, 0, charToInd[c]])
    pos += delta

events.sort()
pattern = midi.Pattern()
track = midi.Track()
pattern.append(track)
lastT = 0
for ev in events:
    print ev, ev[0] - lastT
    if ev[1] == 1:
        track.append(midi.NoteOnEvent(tick = ev[0] - lastT, velocity=80, pitch=ev[2] + 12))
    elif ev[1] == 0:
        track.append(midi.NoteOffEvent(tick = ev[0] - lastT, pitch=ev[2] + 12))
    print track[-1]
    lastT = ev[0]

track.append(midi.EndOfTrackEvent(tick=1))
#print pattern
midi.write_midifile('rnnmusic.mid', pattern)
