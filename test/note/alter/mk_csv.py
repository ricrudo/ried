import csv
fileCSV = []

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


with open('test/note/alter/origen.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fileCSV)
