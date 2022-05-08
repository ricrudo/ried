import csv


fileCSV = []

for third in ('', 'omit3', 'add3', 'addb3', 'min', 'm', '-'):
    for fourth in ('', 'sus4', 'sus', '4'):
        if third in ('omit3', 'min', 'm', '-') and fourth in ('sus4', 'sus'):
            continue
        elif third not in ('min', 'm', '-') and fourth in ('4'):
            continue
        for fifth in ('', 'b5', '#5', 'omit5', 'aug'):
            if fifth and 'sus' in fourth:
                continue
            if fifth in ('#5', 'aug') and third in ('min', 'm', '-'):
                continue
            for sixth in ('', 'b6', '6'):
                for seventh in ('', 'maj7', 'Maj7', 'M7', 'maj', 'Maj', 'º7', 'o7', 'º', 'o', '7'):
                    if sixth and seventh in ('maj7', 'Maj7', 'M7', 'maj', 'Maj'):
                        continue
                    elif any([x in seventh for x in ('o', 'º')]) and sixth:
                        continue
                    elif any([x in seventh for x in ('o', 'º')]) and third != '':
                        continue
                    elif any([x in seventh for x in ('o', 'º')]) and fourth:
                        continue
                    elif not seventh and fifth and fifth[0] in ['b', '#']:
                        continue
                    elif not seventh and sixth and sixth[0] in ['b', '#']:
                        continue
                    elif seventh and fourth == '4':
                        continue
                    if seventh and seventh[0] in ('º', 'o') and fifth and fifth != 'b5':
                        continue
                    for ninth in ('', '9', '2', '#9', 'b9', '#2', 'b2', 'add9', 'add#9', 'addb9', 'add2', 'add#2', 'addb2', '#9b9', 'add#9addb9', '#2b2'):
                        if not seventh and ninth and ninth[0] in ('#', 'b'):
                             continue
                        elif seventh and 'add' in ninth:
                            continue
                        for eleventh in ('', '11', '#11', 'add11', 'add#11'):
                            if eleventh and fourth:
                                continue
                            if seventh and 'add' in eleventh:
                                continue
                            elif not seventh and eleventh and eleventh[0] == '#':
                                continue
                            for thirteenth in ('', '13', 'b13', '#13', '#13b13'):
                                if sixth:
                                    continue
                                if not seventh and thirteenth and thirteenth[0] in ('b', '#'):
                                    continue
                                elif 'º' in seventh and '13' in thirteenth:
                                    continue
                                elif 'o' in seventh and '13' in thirteenth:
                                    continue
                                elif (not seventh) and ('add' in eleventh or 'add' in ninth):
                                    continue

                                string = f'C{third}{seventh}{fourth}{fifth}{sixth}{ninth}{eleventh}{thirteenth}'

                                if third == '' and 'sus' in fourth:
                                    result3 = 'F'
                                elif third in ('addb3', 'min', 'm', '-'):
                                    result3 = 'Eb'
                                elif seventh in ['º7', 'o7', 'º', 'o']:
                                    result3 = 'Eb'
                                elif third == 'omit3':
                                    result3 = 'None'
                                else:
                                    result3 = 'E'

                                if fourth:
                                    result4 = 'F'
                                else:
                                    result4 = 'None'

                                if fifth:
                                    if fifth in ('#5', 'aug'):
                                        result5 = 'Gb'
                                    if fifth in ('b5'):
                                        result5 = 'Gb'
                                    if fifth in ('omit5'):
                                        result5 = 'None'
                                else:
                                    result5 = 'G'

                                if sixth:
                                    if sixth == 'b6':
                                        result6 = 'Ab'
                                    elif sixth == '6':
                                        result6 = 'A'
                                    pass
                                else:
                                    result6 = 'None'

                                if seventh:
                                    if seventh in ('maj7', 'Maj7', 'M7', 'maj', 'Maj'):
                                        result7 = 'B'
                                    elif seventh == '7':
                                        result7 = 'Bb'
                                    elif seventh in ('º7', 'o7', 'º', 'o'):
                                        result7 = 'Bbb'
                                else:
                                    if thirteenth == '13':
                                        result7 = 'Bb'
                                    elif eleventh == '11':
                                        result7 = 'Bb'
                                    else:
                                        result7 = 'None'

                                if ninth:
                                    if any([ninth == x for x in ('9', '2', 'add9', 'add2')]):
                                        result9 = 'D'
                                    elif any([ninth == x for x in ('#9', '#2', 'add#9', 'add#2')]):
                                        result9 = 'D#'
                                    elif any([ninth == x for x in ('b9', 'b2', 'addb9', 'addb2')]):
                                        result9 = 'Db'
                                    elif any([ninth == x for x in ('#9b9', 'add#9addb9', '#2b2')]):
                                        result9 = 'DbyD#'
                                else:
                                    result9 = 'None'

                                if eleventh:
                                    if eleventh in ('11', 'add11'):
                                        result11 = 'F'
                                    elif eleventh in ('#11', 'add#11'):
                                        result11 = 'F#'
                                else:
                                    result11 = 'None'



                                if thirteenth:
                                    if thirteenth == '13':
                                        result13 = 'A'
                                    elif thirteenth == 'b13':
                                        result13 = 'Ab'
                                    elif thirteenth == '#13':
                                        result13 = 'A#'
                                    elif thirteenth == '#13b13':
                                        result13 = 'A#yAb'
                                else:
                                    result13 = 'None'

                                fileCSV.append([string,result3,result4,result5,result6,result7,result9,result11,result13])

with open('test/chord/notes/third/origen.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fileCSV)
