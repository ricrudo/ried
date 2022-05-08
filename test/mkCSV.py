import csv

solfeo = {'C': 'do', 'D': 're', 'E': 'mi', 'F': 'fa', 'G': 'sol', 'A': 'la', 'B': 'si'}

fileCSV = []
for i, l in enumerate('C.D.EF.G.A.B'):
    if l == '.':
        continue
    for alt in range(12):
        pitch = i + alt
        while pitch > 11:
            pitch -= 12
        fileCSV.append([f'{l}{"#"*alt}','none',f'{alt}',l,f'{l}{"#"*alt}',pitch,'none','none',f'{solfeo[l]}{"#"*alt}'])
        if alt > 0:
            pitch = i - alt
            while pitch < 0:
                pitch += 12
            fileCSV.append([f'{l}{"b"*alt}','none',f'{alt*(-1)}',l,f'{l}{"b"*alt}',pitch,'none','none',f'{solfeo[l]}{"b"*alt}'])

#with open('test/test_Note_onlyName.csv', 'w', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerows(fileCSV)


fileCSV = []
for i, l in enumerate('C.D.EF.G.A.B'):
    if l == '.':
        continue
    for alt in range(12):
        for octa in range(-8,9):
            pitch = i + alt
            midi = pitch + (octa*12)
            while pitch > 11:
                pitch -= 12
            fileCSV.append([f'{l}{"#"*alt}',f'{octa}',f'{octa}',f'{alt}',l,f'{l}{"#"*alt}',pitch,midi,'none',f'{solfeo[l]}{"#"*alt}'])
            if alt > 0:
                pitch = i - alt
                midi = pitch + (octa*12)
                while pitch < 0:
                    pitch += 12
                fileCSV.append([f'{l}{"b"*alt}',f'{octa}',f'{octa}',f'{alt*(-1)}',l,f'{l}{"b"*alt}',pitch,midi,'none',f'{solfeo[l]}{"b"*alt}'])


#with open('test/test_Note_octave.csv', 'w', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerows(fileCSV)



#'inputNote,alter,respOctave,respAlter,respNoteWAlter,respNote,respPitchIndex,respMidiNumber,respDuration',
fileCSV = []
for i, l in enumerate('C.D.EF.G.A.B'):
    if l == '.':
        continue
    for alt in range(12):
        pitch = i + alt
        while pitch > 11:
            pitch -= 12
        fileCSV.append([f'{l}',f'{alt}','none',f'{alt}',l,f'{l}{"#"*alt}',pitch,'none','none',f'{solfeo[l]}{"#"*alt}'])
        if alt > 0:
            pitch = i - alt
            while pitch < 0:
                pitch += 12
            fileCSV.append([f'{l}',f'{alt*(-1)}','none',f'{alt*(-1)}',l,f'{l}{"b"*alt}',pitch,'none','none',f'{solfeo[l]}{"b"*alt}'])


#with open('test/test_Note_alter.csv', 'w', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerows(fileCSV)




#'inputNoteOctave,respOctave,respAlter,respNoteWAlter,respNote,respPitchIndex,respMidiNumber,respDuration',
fileCSV = []
for i, l in enumerate('C.D.EF.G.A.B'):
    if l == '.':
        continue
    for alt in range(12):
        for octa in range(-8,9):
            pitch = i + alt
            midi = pitch + (octa*12)
            while pitch > 11:
                pitch -= 12
            fileCSV.append([f'{l}{"#"*alt}{octa}',f'{octa}',f'{alt}',l,f'{l}{"#"*alt}',pitch,midi,'none',f'{solfeo[l]}{"#"*alt}'])
            if alt > 0:
                pitch = i - alt
                midi = pitch + (octa*12)
                while pitch < 0:
                    pitch += 12
                fileCSV.append([f'{l}{"b"*alt}{octa}',f'{octa}',f'{alt*(-1)}',l,f'{l}{"b"*alt}',pitch,midi,'none',f'{solfeo[l]}{"b"*alt}'])


#with open('test/test_NoteWithOctave.csv', 'w', newline='') as f:
#    writer = csv.writer(f)
#   writer.writerows(fileCSV)


fileCSV = []

for octave in range(16):
    for alter in ['', 'b', 'bb', 'bbb', '#', '##', '###']:
        for root in 'ACBDEFG':
            if octave == 15:
                octaveq, octavea = '', 'None'
            else:
                octaveq, octavea = str(octave), str(octave)
            if not alter:
                alterq, altera = '', 0
            else:
                alterq = alter
                altera = 'b' in alter and len(alter) * -1 or len(alter)

            fileCSV.append([f'{root}{octaveq}{alterq}',f'{root}',f'{altera}',f'{octavea}'])
            fileCSV.append([f'{root}{alterq}{octaveq}',f'{root}',f'{altera}',f'{octavea}'])


with open('test/test_analyze_root.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fileCSV)


