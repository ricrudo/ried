import csv
fileCSV = []

# segundas
notes = ['C', 'D', 'E', 'F#', 'G#', 'A#', 'B#', 'C##']

def Major_second(note, symbol):
    if len(note) == 1 or '#' in symbol:
        question = note + symbol
    elif len(note) == 2 and 'b' in symbol:
        question = note[0] + symbol[1:]
    if len(notes[i+1]) == 1 or '#' in symbol:
        other = notes[i+1] + symbol
    elif len(notes[i+1]) == 2 and 'b' in symbol:
        other = notes[i+1][0] + symbol[1:]
    elif len(notes[i+1]) == 3 and 'b' in symbol:
        if len(symbol) > 1:
            other = notes[i+1][0] + symbol[2:]
        if len(symbol) == 1:
            other = notes[i+1][:-1]
    return question, other


for i, note in enumerate(notes):
    if note == 'C##': break
    for symbol in ['####', '###', '##', '#', 'b', 'bb', 'bbb', 'bbbb']:
        question, other = Major_second(note, symbol)
        fileCSV.append([question, other, '2M'])
        for mod in range(-5, 6):
            if mod == 0:
                continue
            question, other = Major_second(note, symbol)
            if mod < 0:
                if '#' not in other:
                    other += 'b' * abs(mod)
                else:
                    other = other[0] + 'b' * abs(mod+1)
            if mod > 0:
                if 'b' not in other:
                    other += '#' * mod
                else:
                    other = other[0] + 'b' * (mod-1)
            if mod < -1:
                answer = '2' + 'd' * abs(mod + 1)
            elif mod == -1:
                answer = '2m'
            elif mod == 0:
                answer = '2M'
            else:
                answer = '2' + 'a' * mod
            fileCSV.append([question, other, answer])



with open('test/note/xor/origen.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fileCSV)




