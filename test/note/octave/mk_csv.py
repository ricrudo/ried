import csv
fileCSV = []

for note in 'ABCDEFG':
    for alter in range(6):
        for symbol_alter in ('#', 'b'):
            for octave in range(-10, 11):
                string = [f'{note}{symbol_alter * alter}{octave}',\
                        f'{octave}']
                fileCSV.append(string)

for note in 'ABCDEFG':
    for alter in range(6):
        for symbol_alter in ('#', 'b'):
            string = [f'{note}{symbol_alter * alter}',\
                    f'none']
            fileCSV.append(string)


with open('test/note/octave/origen.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fileCSV)

