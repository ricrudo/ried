import csv
fileCSV = []

notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

notes = [[x, '',-10] for x in notes]
for x in range(130):
    for num in range(30):
        question = ["".join([str(x) for x in notes[0]]), str(num)]
        question2 = ["".join([str(x) for x in notes[0][:2]]), str(num)]
        counter = 0
        while num >= len(notes):
            num -= 7
            counter += 1
        question.append(f'{notes[num][0]}{notes[num][1]}{notes[num][2]+counter}')
        question2.append(f'{notes[num][0]}{notes[num][1]}')
        fileCSV.append(question)
        fileCSV.append(question2)

    notes.append(notes.pop(0))
    if notes[-1][0] == 'C':
        notes[-1][2] += 1
    else:
        notes[-1][-1] = notes[-2][2] * 1
    alter = None
    for note in range(len(notes)):
        notes[note][1] = ''
    if notes[0][0] == 'D': alter = ('#', (2, 6))
    if notes[0][0] == 'E': alter = ('#', (1, 2, 5, 6))
    if notes[0][0] == 'F': alter = ('b', (3,))
    if notes[0][0] == 'G': alter = ('#', (6,))
    if notes[0][0] == 'A': alter = ('#', (1, 5, 6))
    if notes[0][0] == 'B': alter = ('#', (1, 2, 4, 5, 6))
    if alter:
        for al in alter[1]:
            notes[al][1] = alter[0]
'''

notes = ['B', 'A', 'G', 'F', 'G', 'A', 'C']

notes = [[x, '', 9] for x in notes]
for x in range(130):
    for num in range(30):
        question = ["".join([str(x) for x in notes[0]]), str(num * -1)]
        question2 = ["".join([str(x) for x in notes[0][:2]]), str(num * -1)]
        counter = 0
        while num >= len(notes):
            num -= 7
            counter -= 1
        question.append(f'{notes[num][0]}{notes[num][1]}{notes[num][2]+counter}')
        question2.append(f'{notes[num][0]}{notes[num][1]}')
        fileCSV.append(question)
        fileCSV.append(question2)

    notes.append(notes.pop(0))
    if notes[-1][0] == 'B':
        notes[-1][2] -= 1
    else:
        notes[-1][-1] = notes[-2][2] * 1
    alter = None
    for note in range(len(notes)):
        notes[note][1] = ''
    if notes[0][0] == 'A': alter = ('b', (3, 6))
    if notes[0][0] == 'G': alter = ('b', (2, 3, 5, 6))
    if notes[0][0] == 'F': alter = ('b', (1, 2, 3, 4, 5, 6))
    if notes[0][0] == 'E': alter = ('b', (3,))
    if notes[0][0] == 'D': alter = ('b', (2, 3, 6))
    if notes[0][0] == 'C': alter = ('#', (1, 2, 3, 5, 6))
    if alter:
        for al in alter[1]:
            notes[al][1] = alter[0]
'''


with open('test/note/add/origen.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fileCSV)
exit()


for note in 'ABCDEFG':
    for alter in range(6):
        for symbol_alter in ('#', 'b'):
            for octave in range(-10, 11):
                response = symbol_alter == '#' and alter or alter * -1
                string = [f'{note}{symbol_alter * alter}{octave}',\
                        f'{response}']
                fileCSV.append(string)

for note in 'ABCDEFG':
    for alter in range(6):
        for symbol_alter in ('#', 'b'):
            response = symbol_alter == '#' and alter or alter * -1
            string = [f'{note}{symbol_alter * alter}',\
                    f'{response}']
            fileCSV.append(string)



