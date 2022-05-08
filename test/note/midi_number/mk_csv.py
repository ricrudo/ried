import csv
fileCSV = []

dic = {'C': 0, 'D': 2, 'E': 4, 'F':5, 'G': 7, 'A': 9, 'B': 11}

for note, index in dic.items():
    for alter in range(6):
        for symbol_alter in ('#', 'b'):
            for octave in range(-10, 11):
                if symbol_alter == '#':
                    response = index + alter
                elif symbol_alter == 'b':
                    response = index - alter
                while response < 0:
                    response += 12
                while response > 11:
                    response -= 12
                if symbol_alter == '#':
                    response = index + alter
                elif symbol_alter == 'b':
                    response = index - alter
                response += (octave + 1) * 12 
                string = [f'{note}{symbol_alter * alter}{octave}',\
                        f'{response}']
                fileCSV.append(string)

for note, index in dic.items():
    for alter in range(6):
        for symbol_alter in ('#', 'b'):
            string = [f'{note}{symbol_alter * alter}',\
                    f'none']
            fileCSV.append(string)


with open('test/note/midi_number/origen.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fileCSV)


