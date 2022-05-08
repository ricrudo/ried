import csv
fileCSV = []

for note in 'ABCDEFG':
    for alter in range(6):
        for symbol_alter in ('#', 'b'):
            for octave in range(-10, 11):
                string = [f'{note}{symbol_alter * alter}{octave}',\
                        f'{note}']
                fileCSV.append(string)

for note in 'ABCDEFG':
    for alter in range(6):
        for symbol_alter in ('#', 'b'):
            string = [f'{note}{symbol_alter * alter}',\
                    f'{note}']
            fileCSV.append(string)


with open('test/note/name_without_alter/origen.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fileCSV)


