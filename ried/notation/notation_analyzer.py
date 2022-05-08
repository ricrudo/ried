class Notation_Analyzer:

    C_reference = {x:i for i, x in enumerate('C.D.EF.G.A.B') if x != '.'}
    solfeo = {'C': 'do', 'D': 're', 'E': 'mi', 'F': 'fa', 'G': 'sol', 'A': 'la', 'B': 'si'}
   
    def _alter(self, predata):
        predata['alter'] = self._checkInteger(predata['alter'], 'alter')
    
    def _checkInteger(self, value, var):
        if value != 'none':
            if isinstance(value, float):
                raise ValueError(f'positional argument "{var}" must be an int')
            try:
                return int(value)
            except ValueError:
                raise ValueError(f'positional argument "{var}" must be int o string_number. ie: -1 or "-1"')
        return 'none'

    def _get_alter_from_string(self, predata, alter):
        if predata['alter'] == 'none':
            if not alter:
                predata['alter'] = 0
            if 'b' in alter:
                predata['alter'] = len(alter) * (-1)
            elif '#' in alter:
                predata['alter'] = len(alter)

    def _check_value_name(self, name, opt):
        if name not in 'ABCDEFG':
            raise ValueError(f'"{name}" is not a valid {opt.title()}')

    def _generateNames(self, predata):
        if predata['alter'] > 0:
            value =  predata['name_without_alter'] + '#' * predata['alter']
        elif predata['alter'] < 0:
            value = predata['name_without_alter'] + 'b' * abs(predata['alter'])
        else:
            value = predata['name_without_alter']
        predata['name'] = value

    def _alterString(self, predata):
        if predata['alter'] >= 0:
            predata['alter_str'] = '#' * predata['alter']
        else:
            predata['alter_str'] = 'b' * abs(predata['alter'])

    def _solfeoName(self, predata):
        predata['solfeo_without_alter'] = self.solfeo[predata['name'][0]]
        predata['solfeo'] = predata['solfeo_without_alter'] + predata['alter_str']

class Note(Notation_Analyzer):
    
    def generator_note(self, name, octave, alter):
        predata = {'name': name, 'octave': octave, 'alter': alter}
        self._octave(predata)
        self._alter(predata)
        self._noteWithoutAlter(predata)
        self._generateNames(predata)
        self._alterString(predata)
        self._fullName(predata)
        self._pitch_index(predata)
        self._setMidiNumber(predata)
        self._solfeoName(predata)
        return predata

    def _octave(self, predata):
        predata['octave'] = self._checkInteger(predata['octave'], 'octave')

    def _noteWithoutAlter(self, predata):
        name, octave, alter = self._isolatePartsName(predata)
        self._check_value_name(name, 'note')
        self._get_alter_from_string(predata, alter)
        if octave and predata['octave'] == 'none':
            try:
                predata['octave'] = int("".join(octave))
            except ValueError:
                raise ValueError(f'{predata["name"]} is not a valid Note')
        predata['name_without_alter'] = name

    def _isolatePartsName(self, predata):
        name = predata['name'][0]
        stuffs = predata['name'][1:]
        other = [x for x in stuffs if x not in 'b#']
        alter = [x for x in stuffs if x in 'b#']
        return name, other, alter

    def _fullName(self, predata):
        predata['full_name'] = predata['octave'] != 'none' and f'{predata["name"]}{predata["octave"]}' or f'{predata["name"]}'

    def _pitch_index(self, predata):
        predata['pitch_index_without_alter'] = self.C_reference[predata['name_without_alter']]
        pitch_index = predata['pitch_index_without_alter'] + predata['alter']
        predata['pitch_index'] = pitch_index % 12

    def _setMidiNumber(self, predata):
        if predata['octave'] == 'none':
            predata['midi_number'] = 'none'
            return
        predata['midi_number'] = ((predata['octave']+1) * 12) +\
                predata['pitch_index_without_alter'] +\
                predata['alter']

class Chord(Notation_Analyzer):

    opt = 'chord'

    def generator_chord(self, name, sufix, alter):
        predata = {'input': name, 'sufix': sufix, 'alter': alter}
        self._alter(predata)
        self._chord_sufix(predata)
        self._noteWithoutAlter(predata)
        self._generateNames(predata)
        return predata

    def _noteWithoutAlter(self, predata):
        name, other, alter = self._isolatePartsName(predata)
        self._check_value_name(name, self.opt)
        self._get_alter_from_string(predata, alter)
        if other and predata['sufix'] == 'none':
            predata['sufix'] = other
            self._chord_sufix(predata)
        predata['name_without_alter'] = name

    def _checkName(self, name, other, opt):
        error = False
        if name not in 'ABCDEFG':
            error = True
        if other:
            if opt == 'note' and not all([x in '0123456789-' for x in other]):
                error = True
            if opt == 'chord':
                self._check_sufix(predata)
        if error:
            raise ValueError(f'"{name}" is not a valid {opt.title()}')

    def _check_sufix(self, predata):
        if not all([x in 'ot12345679º-minMajdug#b()s, ' for x in predata['sufix']]):
            name = predata['input']
            raise ValueError(f'"{name}" is not a valid Chord')
        if predata['alter'] not in ('none', 0):
            if predata['sufix'][0] not in 'sºo7(Mm-ad':
                name = predata['input']
                raise ValueError(f'"{name}" is not a valid Chord')

    def _isolatePartsName(self, predata):
        name = predata['input'][0]
        stuffs = predata['input'][1:]
        alter = []
        other = []
        if stuffs:
            if stuffs[0] in ['#', 'b']:
                alter.append(stuffs[0])
                stuffs = stuffs[1:]
                if stuffs:
                    for x in range(len(stuffs)):
                        if x == alter[0]:
                            alter.append(stuffs[0])
                            stuffs = stuffs[1:]
                        else:
                            other = stuffs[:]
                            break
            else:
                other = stuffs[:]
        return name, other, alter

    def _chord_sufix(self, predata):
        if predata['sufix'] == 'none':
            return
        self._check_sufix(predata)
        value = predata['sufix']
        predata['sufix'] = {}
        value, predata['sufix']['third'] = self._get_third(value)
        value, predata['sufix']['fourth'] = self._get_fourth(value, predata['sufix'])
        value, predata['sufix']['fifth'] = self._get_fifth(value, predata['sufix'])
        value, predata['sufix']['sixth'] = self._get_sixth(value)
        value, predata['sufix']['seventh'] = self._get_seventh(value, predata['sufix'])
        value, predata['sufix']['ninth'] = self._get_ninth(value, predata['sufix'])
        value, predata['sufix']['eleventh'] = self._get_eleventh(value, predata['sufix'])
        value, predata['sufix']['thirteenth'] = self._get_thirteenth(value, predata['sufix'])
        value, predata['sufix']['third'] = self._get_minor(value, predata['sufix'])
        self._extra_sufix(value)

    def _get_third(self, value):
        if not value:
            return None, None
        third = [x for x in ('omit3', 'add3', 'addb3') if x in value]
        if not third:
            return value, None
        if len(third) > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        value = value.replace(third[0], '')
        return value, third[0]

    def _get_fourth(self, value, sufix):
        if not value:
            return None, None
        fourth = value.count('sus4')
        if fourth > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        elif fourth == 1:
            if sufix['third'] == 'omit3':
                raise ValueError(f'...{value} is not valid as a chord sufix')
            value = value.replace('sus4', '')
            return value, 'sus4'
        fourth = value.count('sus')
        if fourth > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        elif fourth == 1:
            if sufix['third'] == 'omit3':
                raise ValueError(f'...{value} is not valid as a chord sufix')
            value = value.replace('sus', '')
            return value, 'sus4'
        fourth = value.count('4')
        if fourth > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        elif fourth == 1:
            if sufix['third'] == 'omit3':
                raise ValueError(f'...{value} is not valid as a chord sufix')
            value = value.replace('4', '')
            return value, '4'

        return value, None

    def _get_fifth(self, value, sufix):
        if not value:
            return None, None
        fifth = [x for x in ('b5', '#5', 'omit5', 'aug') if x in value]
        if not fifth:
            return value, None
        if len(fifth) > 3 or \
                (len(fifth) > 1 and any(['omit5' in fifth, 'aug' in fifth])) or \
                (len(fifth) == 2 and fifth[0] == fifth[1]) or \
                all(['#5' in fifth and 'aug' in fifth]) or \
                (sufix['fourth'] and 'sus' in sufix['fourth'] and fifth):
            raise ValueError(f'...{value} is not valid as a chord sufix')
        for x in fifth:
            value = value.replace(x, '')
        if fifth == ['aug']:
            fifth = ['#5']
        return value, fifth

    def _get_sixth(self, value):
        if not value:
            return None, None
        sixth = value.count('b6')
        if sixth > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        elif sixth == 1:
            value = value.replace('b6', '')
            return value, 'b6'
        sixth = value.count('6')
        if sixth > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        elif sixth == 1:
            value = value.replace('6', '')
            return value, '6'
        return value, None

    def _get_seventh(self, value, sufix):
        if not value:
            return None, None
        seventh = [x for x in ('maj7', 'Maj7', 'M7') if x in value]
        for x in seventh:
            value = value.replace(x, '')
        seventh.extend([x for x in ('maj', 'Maj') if x in value])
        if seventh:
            if len(seventh) > 1 or sufix['sixth']:
                raise ValueError(f'...{value} is not valid as a chord sufix')
            value = value.replace(seventh[0], '')
            return value, 'maj7'
        seventh = [x for x in ('º7', 'o7') if x in value]
        if len(seventh) > 1 or (seventh and (sufix['sixth'] or sufix['fourth'])):
            raise ValueError(f'...{value} is not valid as a chord sufix')
        if seventh:
            if sufix['fifth'] and sufix['fifth'] != ['b5']:
                raise ValueError(f'...{value} is not valid as a chord sufix')
            value = value.replace(seventh[0], '')
            sufix['third'] = 'minor'
            sufix['fifth'] = ['b5']
            return value, 'º7'
        seventh = [x for x in ('º', 'o') if x in value]
        if len(seventh) > 1 or (seventh and (sufix['sixth'] or sufix['fourth'])):
            raise ValueError(f'...{value} is not valid as a chord sufix')
        if seventh:
            if sufix['fifth'] and sufix['fifth'] != ['b5']:
                raise ValueError(f'...{value} is not valid as a chord sufix')
            sufix['third'] = 'minor'
            sufix['fifth'] = ['b5']
            value = value.replace(seventh[0], '')
            return value, 'º7'
        seventh = value.count('7')
        if seventh > 1 or (seventh and (sufix['sixth'] not in ('b6', None) or sufix['fourth'] == '4')):
            raise ValueError(f'...{value} is not valid as a chord sufix')
        if seventh:
            value = value.replace('7', '')
            return value, '7'
        return value, None

    def _get_ninth(self, value, sufix):
        if not value:
            return None, None
        ninth = value.count('9')
        if ninth > 2 or (ninth == 2 and not all(['#9' in value, 'b9' in value])):
            raise ValueError(f'...{value} is not valid as a chord sufix')
        second = value.count('2')
        if second and ninth:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        if second:
            value = value.replace('2', '9')
            ninth = second
        add = tuple([x for x in ('add9', 'add#9', 'addb9') if x in value])
        if add:
            if len(add) != ninth or (len(add) == 2 and not all(['add#9' in add, 'addb9' in add])) or sufix['seventh']:
                raise ValueError(f'...{value} is not valid as a chord sufix')
            for x in add:
                value = value.replace(x, '')
            return value, add
        ninth = []
        for x in ('#9', 'b9', '9'):
            if x in value:
                if len(x) == 2 and not sufix['seventh']:
                    raise ValueError(f'...{value} is not valid as a chord sufix')
                if x == '9' and not sufix['seventh']:
                    sufix['seventh'] == '7'
                value = value.replace(x, '')
                ninth.append(x)
        return ninth and (value, ninth) or (value, None)

    def _get_eleventh(self, value, sufix):
        if not value:
            return None, None
        if value.count('11') > 2 or (value.count('11') and sufix['fourth']):
            raise ValueError(f'...{value} is not valid as a chord sufix')
        if value.count('11') == 0:
            return value, None
        eleventh = []
        for x in ('add#11', 'add11', '#11', '11'):
            if x in value:
                if ('add' in x and sufix['seventh']) or (x == '#11' and not sufix['seventh']):
                    raise ValueError(f'...{value} is not valid as a chord sufix')
                if x == '11' and not sufix['seventh']:
                    sufix['seventh'] = '7'
                value = value.replace(x, '')
                eleventh.append(x)
        if eleventh:
            return value, eleventh[0]
        return value, None

    def _get_thirteenth(self, value, sufix):
        if not value:
            return None, None
        thirteenth = [x for x in ('#13', 'b13') if x in value]
        if thirteenth:
            if len(thirteenth) > 2 or \
                    (len(thirteenth) == 2 and thirteenth[0] == thirteenth[1]) or \
                    (not sufix['seventh']) or sufix['sixth'] or \
                    (sufix['seventh'] == 'º7' and 'b13' in thirteenth):
                raise ValueError(f'...{value} is not valid as a chord sufix')
            for x in thirteenth:
                value = value.replace(x, '')
            return value, thirteenth
        thirteenth = value.count('13')
        if thirteenth:
            if thirteenth > 2 or sufix['sixth'] or sufix['seventh'] == 'º7':
                raise ValueError(f'...{value} is not valid as a chord sufix')
            if not sufix['seventh']:
                sufix['seventh'] = '7'
            value = value.replace('13', '')
            return value, ['13']
        return value, None

    def _get_minor(self, value, sufix):
        if not value:
            return None, sufix['third']
        if sufix['third']:
            return value, sufix['third'] 
        minor = len([x for x in ('min', '-') if x in value])
        value = value.replace('min', '')
        value = value.replace('-', '')
        minor += value.count('m')
        value = value.replace('m', '')
        if minor > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        if minor:
            if sufix['third'] or (sufix['fourth'] and sufix['fourth'] != '4') or (sufix['fifth'] and '#5' in sufix['fifth']):
                raise ValueError(f'...{value} is not valid as a chord sufix')
            return value, 'minor'
        return value, False
      
    def _extra_sufix(self, value):
        if value: 
            value = value.replace('(', '')
            value = value.replace(')', '')
            value = value.replace(' ', '')
            value = value.replace(',', '')
            if value:
                raise ValueError(f'...{value} is not valid as a chord sufix')



