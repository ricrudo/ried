import csv
fileCSV = []

dic = {'C': 'do', 'D': 're', 'E': 'mi', 'F': 'fa', 'G': 'sol', 'A': 'la', 'B': 'si'}

for note, solfeo in dic.items():
    for alter in range(6):
        for symbol_alter in ('#', 'b'):
            for octave in range(-10, 11):
                string = [f'{note}{symbol_alter * alter}{octave}',\
                        f'{solfeo}{symbol_alter * alter}']
                fileCSV.append(string)

for note, solfeo in dic.items():
    for alter in range(6):
        for symbol_alter in ('#', 'b'):
            string = [f'{note}{symbol_alter * alter}',\
                    f'{solfeo}{symbol_alter * alter}']
            fileCSV.append(string)


with open('test/note/solfeo/origen.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fileCSV)



