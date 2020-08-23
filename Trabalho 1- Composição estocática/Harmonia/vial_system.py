from random import random, choice
import music21 as m21

pitches = list(range(48, 60))

def vial(pitch):
    t = [(pitch + 3 * x) for x in range(4)]
    s = [(pitch + 5 + 3 * x) for x in range(4)]
    d = [(pitch + 7 + 3 * x) for x in range(4)]
    return t, s, d


def major(pitch):
    return [pitch, (pitch + 4), (pitch + 7)]

def minor(pitch):
    return [pitch, (pitch + 3), (pitch + 7)]

def major_or_minor(pitch):
    rand = random()
    if rand < 0.5:
        return major(pitch)
    else:
        return minor(pitch)


def vial_system(num):
    count = 0
    start_pitch = choice(pitches)
    tonic, sub, dom = vial(start_pitch)
    modes = [tonic, sub, dom]
    result = []
    
    while count < num:
        i = 0
        while i < 3:
            pitch = choice(modes[i])
            mode = major_or_minor(pitch)
            result.append(mode)
            i += 1
            if count == num - 1:
                if i == 2:
                    rand = random()
                    if rand > 0.5:
                        i += 1
        count += 1
    return result


keys = vial_system(3)
piece = m21.stream.Stream()
for i in keys:
    key = m21.chord.Chord(i)
    key.quarterLength = 4
    piece.append(key)
    
piece.show("musicxml")












