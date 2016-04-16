import tachyonxml, commands, re
import xml.dom
import numpy as np, sys

NNOTES = 200

sharpNotes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
noteOffsets = dict([[note, i] for i, note in enumerate(sharpNotes)])
flatNotes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
for i, note in enumerate(flatNotes):
    noteOffsets[note] = i
    
scalePattern = [0, 2, 4, 5, 7, 9, 11]
sharpScales = []
sharpScaleOffsets = []
for iFifth in range(5):
    startNote = (iFifth * 7) % 12
    scale = []
    for offset in scalePattern:
        note = sharpNotes[(startNote + offset) % 12]
        scale.append(note)
    sharpScales.append(scale)
    noteToOffsets = {}
    for note in scale:
        noteToOffsets[note[0]] = noteOffsets[note]
    sharpScaleOffsets.append(noteToOffsets)

flatScales = []
flatScaleOffsets = []
for iFifth in range(5):
    startNote = (-iFifth * 7) % 12
    scale = []
    for offset in scalePattern:
        note = flatNotes[(startNote + offset) % 12]
        scale.append(note)
    flatScales.append(scale)
    noteToOffsets = {}
    for note in scale:
        noteToOffsets[note[0]] = noteOffsets[note]
    flatScaleOffsets.append(noteToOffsets)
    #print scale, noteToOffsets

def procFile(fname):
    musicxml = tachyonxml.XMLParseFile(open(fname))
    score = musicxml.getChildNode('score-partwise')
    divisions = None
    fifths = 0
    noteOffsets = None
    totalScore = []
    scaleOffset = 0
    for part in score.getChildNodes('part'):
        for iMeasure, measure in enumerate(part.getChildNodes('measure')):
            attr = measure.getChildNode('attributes')
            if attr != None:
                key = attr.getChildNode('key')
                if key != None:
                    f = key.getChildNode('fifths')
                    if f != None:
                        fifths = int(f.getValue())
                        if fifths > 0: noteOffsets = sharpScaleOffsets[fifths]
                        else: noteOffsets = flatScaleOffsets[fifths]
                        scaleOffset = (fifths * 7) % 12
                divisions = int(attr.getChildNode('divisions').getValue())
                beats = int(attr.getChildNode('beats').getValue())
                beatType = int(attr.getChildNode('beat-type').getValue())

            totQuarterNotes = 4 * beats / beatType
            measureTotDivs = int(totQuarterNotes * divisions)
            #print totQuarterNotes, beats, beatType, divisions, measureTotDivs
            measureDat = [[] for i in range(measureTotDivs)]
            pos = 0
            lastLen = None
            for node in measure.theElem.childNodes:
                if node.nodeType == node.ELEMENT_NODE:
                    xmlNode = tachyonxml.XMLNode(node)
                    if xmlNode.name == 'backup':
                        duration = int(xmlNode.getChildNode('duration').getValue())
                        pos -= duration
                    if xmlNode.name == 'note':
                        if xmlNode.getChildNode('duration') == None: continue
                        duration = int(xmlNode.getChildNode('duration').getValue())
                        chord = xmlNode.getChildNode('chord')
                        if chord != None:
                            if lastLen == None: 
                                pass
                                #print 'chord with no lastLen!!!'
                            else: pos -= lastLen
                        lastLen = duration
                        rest = xmlNode.getChildNode('rest')
                        if rest != None:
                            pass
                            #print 'rest'
                        pitch = xmlNode.getChildNode('pitch')
                        if pitch != None:
                            note = pitch.getChildNode('step').getValue()
                            oct = pitch.getChildNode('octave')
                            if oct != None: octave = int(oct.getValue())
                            alter = 0
                            alt = pitch.getChildNode('alter')
                            if alt != None: alter = int(alt.getValue())
                            noteNumber = octave * 12 + noteOffsets[note] + alter - scaleOffset
                            measureDat[pos].append([noteNumber, duration])
                            #print 'measure: %d, pos: %d, pitch: %d, duration: %d'%(iMeasure, pos, noteNumber, duration)
                        pos += duration
            #print 'position at end of measure:', pos
            totalScore.extend(measureDat)
    return totalScore

#fname = 'lg-73176162.xml'
#if len(sys.argv) > 1: fname = sys.argv[1]
#totScore = procFile(fname)
#print totScore
#fls = open('Music/clavierFiles.txt').read().splitlines()
#fls = ['Music/' + re.sub(':', '', fl) for fl in fls]
fls = commands.getoutput('ls Music/*xml').splitlines()
ofl = open('allnotes.txt', 'w')
for f in fls:
    print f
    try:
        result = procFile(f)
        if result != None: 
            print >>ofl, result
    except: pass
                    
                
                    
