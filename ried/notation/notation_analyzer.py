import re

def str_striper(value):
    if isinstance(value, str):
        return value.strip()
    return value

def note_name_formatting(name):
    return f'{name[0].upper()}{name[1:]}'

class Notation_Analyzer:

    C_reference = {x:i for i, x in enumerate('C.D.EF.G.A.B') if x != '.'}
    solfeo = {'C': 'do', 'D': 're', 'E': 'mi', 'F': 'fa', 'G': 'sol', 'A': 'la', 'B': 'si'}


   
    def _alter(self, predata):
        predata['alter'] = self._checkInteger(predata['alter'], 'alter')
    
    def _checkInteger(self, value, var):
        if value is not None:
            if isinstance(value, float):
                raise ValueError(f'positional argument "{var}" must be an int')
            try:
                return int(value)
            except ValueError:
                raise ValueError(f'positional argument "{var}" must be int o string_number. ie: -1 or "-1"')

    def _get_alter_from_string(self, predata, alter):
        if predata['alter'] is None:
            if alter is None:
                predata['alter'] = 0
            elif 'b' in alter:
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
    
    TOKEN = re.compile(r"""

        # --- Octava ---
       -?\d{1,2}                              # 6, 7, 9, 11, 13

        # --- Nota raíz y accidentales separados ---
      | [A-G]                                # raíz (A..G)
      | [#♯b♭]+                              # secuencia de alteraciones (##, bb)

    """, re.X)

    def _extract_data_from_name(self, predata:dict)->None:
        response = re.findall(self.TOKEN, predata["input"])
        return response

    def generator_note(self, name, octave, alter):
        predata = {'input': note_name_formatting(str_striper(name)), 'octave': str_striper(octave), 'alter': str_striper(alter)}
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
        predata['name_without_alter'] = name
        self._get_alter_from_string(predata, alter)
        if octave and predata['octave'] is None:
            try:
                predata['octave'] = int("".join(octave))
            except ValueError:
                raise ValueError(f'{predata["name"]} is not a valid Note')

    def _isolatePartsName(self, predata):
        input_list = self._extract_data_from_name(predata)
        name = input_list[0]
        stuffs = input_list[1:]
        other = None
        alter = None
        for x in stuffs:
            if x[0] not in 'b#':
                other = x
            else:
                alter = x
        return name, other, alter

    def _fullName(self, predata):
        predata['full_name'] = predata['octave'] is not None and f'{predata["name"]}{predata["octave"]}' or f'{predata["name"]}'

    def _pitch_index(self, predata):
        predata['pitch_index_without_alter'] = self.C_reference[predata['name_without_alter']]
        pitch_index = predata['pitch_index_without_alter'] + predata['alter']
        predata['pitch_index'] = pitch_index % 12

    def _setMidiNumber(self, predata):
        if predata['octave'] is None:
            predata['midi_number'] = 'none'
            return
        predata['midi_number'] = ((predata['octave']+1) * 12) +\
                predata['pitch_index_without_alter'] +\
                predata['alter']

class Chord(Notation_Analyzer):

    opt = 'chord'

    TOKEN = re.compile(r"""
        # --- Bajo con slash (/B, /F#, /Eb) ---
        /[A-G](?:[#♯b♭]+)?
      | 6/9                                  # seis-nueve como token único

        # --- Calidades / tipos ---
      | maj(?:7|9|11|13)?                    # maj, maj7, maj9, maj11, maj13
      | m(?:7|9|11|13)?                      # m, m7, m9, m11, m13
      | dim(?:7)?                            # dim, dim7
      | aug                                  # aug
      | sus(?:2|4)?                          # sus, sus2, sus4
      | add(?:2|3|b3|4|9|11|13)?             # add9 / add11 / ...

        # --- Símbolos alternativos comunes ---
      | Δ(?:7|9|11|13)?                      # Δ, Δ7, Δ9 (mayor)
      | [øØ]7?                               # ø, ø7 (semi-disminuido)
      | [°º]7?                               # °, º, °7 (disminuido)
      | \+                                   # + como "aug"

        # --- Alteraciones dentro de paréntesis: (b9,#11,13) -> b9, #11, 13 ---
      | (?<=\()[#♯b♭]?\d{1,2}(?=[,\s\)])     # matchea SIN capturar paréntesis

        # --- Alteraciones sueltas ---
      | [#♯b♭](?:2|4|5|6|7|9|11|13)          # b9, #11, b5, etc.

        # --- Tensiones simples ---
      | \d{1,2}                              # 6, 7, 9, 11, 13

        # --- Nota raíz y accidentales separados ---
      | [A-G]                                # raíz (A..G)
      | [#♯b♭]+                              # secuencia de alteraciones (##, bb)

    """, re.X)

    def _extract_data_from_name(self, predata:dict)->None:
        response = re.findall(self.TOKEN, predata["input"])
        for index in range(len(response)-1,-1,-1):
            match = re.search(r'm(7|9|11|13)', response[index])
            if match:
                response[index] = 'm'
                response.insert(index + 1, '7')
                if match.group(1) != '7':
                    response.insert(index + 2, match.group(1))
        return response

    def generator_chord(self, name, sufix, alter):
        predata = {'input': note_name_formatting(str_striper(name)), 'sufix': str_striper(sufix), 'alter': str_striper(alter)}
        self._chord_sufix(predata)
        self._noteWithoutAlter(predata)
        self._generateNames(predata)
        return predata

    def _noteWithoutAlter(self, predata):
        name, other, alter = self._isolatePartsName(predata)
        self._check_value_name(name, self.opt)
        predata['name_without_alter'] = name
        self._get_alter_from_string(predata, alter)
        if other and predata['sufix'] is None:
            predata['sufix'] = other
            self._chord_sufix(predata)

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
        if predata['alter'] == 0:
            alter = ''
        elif predata['alter'] > 0:
            alter = '#' * predata['alter']
        elif predata['alter'] < 0:
            alter = 'b' * abs(predata['alter'])
        generate_input = predata['name_without_alter']
        generate_input += alter
        generate_input += "".join(predata['sufix'])
        if sorted(generate_input) != sorted(predata['input'].
                                            replace('(','').
                                            replace(')','').
                                            replace('[','').
                                            replace(']','')):
            raise ValueError(f'<<{predata["input"]}>> is not a valid Chord')

    def _isolatePartsName(self, predata):
        input_list = self._extract_data_from_name(predata)
        name = input_list[0]
        stuffs = input_list[1:]
        alter = None
        if stuffs:
            if stuffs[0][0] in ['#', 'b'] and all([x == stuffs[0][0] for x in stuffs[0]]):
                alter = stuffs.pop(0)
        other = stuffs if stuffs else None
        return name, other, alter

    def _chord_sufix(self, predata):
        if predata['sufix'] is None:
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

    def _get_third(self, value):
        if not value:
            return None, None
        third = [x for x in ('omit3', 'add3', 'addb3', 'm') if x in value]
        if not third:
            return value, None
        if len(third) > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
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
            return value, 'sus4'
        fourth = value.count('sus')
        if fourth > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        elif fourth == 1:
            if sufix['third'] == 'omit3':
                raise ValueError(f'...{value} is not valid as a chord sufix')
            return value, 'sus4'
        fourth = value.count('4')
        if fourth > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        elif fourth == 1:
            if sufix['third'] == 'omit3':
                raise ValueError(f'...{value} is not valid as a chord sufix')
            return value, '4'

        return value, None

    def _get_fifth(self, value, sufix):
        if not value:
            return None, None
        fifth = [x for x in ('b5', '#5', 'omit5', 'aug', 'dim') if x in value]
        if not fifth:
            return value, None
        if len(fifth) > 3 or \
                (len(fifth) > 1 and any(['omit5' in fifth, 'aug' in fifth])) or \
                (len(fifth) == 2 and fifth[0] == fifth[1]) or \
                all(['#5' in fifth and 'aug' in fifth]) or \
                (sufix['fourth'] and 'sus' in sufix['fourth'] and fifth):
            raise ValueError(f'...{value} is not valid as a chord sufix')
        if fifth == ['aug']:
            fifth = ['#5']
        elif fifth == ['dim']:
            fifth = ['b5']
        return value, fifth

    def _get_sixth(self, value):
        if not value:
            return None, None
        sixth = value.count('b6')
        if sixth > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        elif sixth == 1:
            return value, 'b6'
        sixth = value.count('6')
        if sixth > 1:
            raise ValueError(f'...{value} is not valid as a chord sufix')
        elif sixth == 1:
            return value, '6'
        return value, None

    def _get_seventh(self, value, sufix):
        if not value:
            return None, None
        seventh = [x for x in ('maj7', 'Maj7', 'M7') if x in value]
        seventh.extend([x for x in ('maj', 'Maj') if x in value])
        if seventh:
            if len(seventh) > 1 or sufix['sixth']:
                raise ValueError(f'...{value} is not valid as a chord sufix')
            return value, 'maj7'
        seventh = [x for x in ('º7', 'o7') if x in value]
        if len(seventh) > 1 or (seventh and (sufix['sixth'] or sufix['fourth'])):
            raise ValueError(f'...{value} is not valid as a chord sufix')
        if seventh:
            if sufix['fifth'] and sufix['fifth'] != ['b5']:
                raise ValueError(f'...{value} is not valid as a chord sufix')
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
            return value, 'º7'
        seventh = value.count('7')
        if seventh > 1 or (seventh and (sufix['sixth'] not in ('b6', None) or sufix['fourth'] == '4')):
            raise ValueError(f'...{value} is not valid as a chord sufix')
        if seventh:
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
            ninth = second
        add = tuple([x for x in ('add9', 'add#9', 'addb9') if x in value])
        if add:
            if len(add) != ninth or (len(add) == 2 and not all(['add#9' in add, 'addb9' in add])) or sufix['seventh']:
                raise ValueError(f'...{value} is not valid as a chord sufix')
            return value, add
        ninth = []
        for x in ('#9', 'b9', '9'):
            if x in value:
                if len(x) == 2 and not sufix['seventh']:
                    raise ValueError(f'...{value} is not valid as a chord sufix')
                if x == '9' and not sufix['seventh']:
                    sufix['seventh'] == '7'
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
            return value, thirteenth
        thirteenth = value.count('13')
        if thirteenth:
            if thirteenth > 2 or sufix['sixth'] or sufix['seventh'] == 'º7':
                raise ValueError(f'...{value} is not valid as a chord sufix')
            if not sufix['seventh']:
                sufix['seventh'] = '7'
            return value, ['13']
        return value, None


