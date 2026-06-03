from ried.notation import notation_analyzer
from ried.note.note_generator import Note

class Chord_symbol:

    nttnAnlzr = notation_analyzer.Chord()
    _written_category = {
        'major' : '',
        'augmented add2' : '#5 add2',
        'augmented dominant' : '7(#5)',
        'dominant' : '7',
        'major seventh' : 'maj7',
        'minor' : 'm',
        'minor seventh b6' : 'm7(b6)',
        'minor seventh' : 'm7',
        'minor major seventh' : 'm(maj7)',
        'diminished': 'dim',
        'diminished major seventh' : 'dim(maj7)',
        'half diminished' : 'm7(b5)',
        'whole diminished' : 'º7',
        'suspended' : 'sus4',
        'suspended dominant': '7sus4',
        'suspended maj7' : 'maj7sus4'
    }
    
    def __init__(self, name, sufix=None, alter=None, duration='none', key=None):
        self._resume = self.nttnAnlzr.generator_chord(name, sufix, alter)
        self._set_types()
        #self._set_root()
        self._category = self._set_chord_category()
        #self._set_notes()

    def _set_types(self):
        type_third = isinstance(self._resume['sufix'], dict) and (self._resume['sufix'].get('third') or self._resume['sufix'].get('fourth')) or 'major'
        self.type_third = type_third in ['m', 'min', '-'] and 'minor' or type_third
        self.type_fourth = isinstance(self._resume['sufix'], dict) and self._resume['sufix'].get('fourth') or 'no specified'
        self.type_fifth = isinstance(self._resume['sufix'], dict) and self._resume['sufix'].get('fifth') or 'perfect'
        self.type_sixth = isinstance(self._resume['sufix'], dict) and self._resume['sufix'].get('sixth') or 'no specified'
        self.type_seventh = isinstance(self._resume['sufix'], dict) and self._resume['sufix'].get('seventh') or 'no specified'
        self.type_ninth = isinstance(self._resume['sufix'], dict) and self._resume['sufix'].get('ninth') or 'no specified'
        self.type_eleventh = isinstance(self._resume['sufix'], dict) and self._resume['sufix'].get('eleventh') or 'no specified'
        self.type_thirteenth = isinstance(self._resume['sufix'], dict) and self._resume['sufix'].get('thirteenth') or 'no specified'

    def _set_chord_category(self):
        if self.type_third == 'major':
            if self.type_seventh == 'no specified':
                if any(['add' in x for x in self.type_ninth]):
                    if self.type_fifth == ['#5']: return 'augmented add2'
                    return 'major add2'
                return 'major'
            if self.type_seventh == '7':
                if self.type_fifth == ['#5']: return 'augmented dominant'
                return 'dominant'
            if self.type_seventh == 'maj7': return 'major seventh'
        elif self.type_third == 'minor':
            if self.type_fifth == 'perfect':
                if self.type_seventh == 'no specified': 
                    if any(['add' in x for x in self.type_ninth]): return 'minor add2'
                    return 'minor'
                if self.type_seventh == '7':
                    if self.type_sixth == 'b6': return 'minor seventh b6'
                    return 'minor seventh'
                if self.type_seventh == 'maj7': return 'minor major seventh'
            if self.type_fifth == ['b5']:
                if self.type_seventh == 'no specified': return 'diminished'
                if self.type_seventh == 'maj7': return 'diminished major seventh'
                if self.type_seventh == '7': return 'half diminished'
                if self.type_seventh == 'º7': return 'whole diminished'
                if all([x in ('º7', 'maj7') for x in self.type_seventh]): return 'whole diminished major seventh'
        elif any(['sus4' in self.type_third, 'sus4' in self.type_fourth]):
            if self.type_seventh == 'no specified': return 'suspended'
            if self.type_seventh == '7': return 'suspended dominant'
            if self.type_seventh == 'maj7': return 'suspended maj7'
        #self.name_without_alter = predata['name_without_alter']
        #self.full_name = predata['full_name']
        #self.alter = predata['alter']
        #self.alter_str = predata['alter_str']
        #self.pitch_index_without_alter = predata['pitch_index_without_alter'] 
        #self.pitch_index = predata['pitch_index']
        #self.solfeo_without_alter = predata['solfeo_without_alter'].upper()
        #self.solfeo = predata['solfeo'].upper()
        #self.duration = self._duration(duration)
        #self.key = self._setKey(key)

    def get_root(self):
        if not hasattr(self, '_third'):
            self._root = Note(self._resume['name'])
        return self._root

    def get_third(self):
        if not hasattr(self, '_third'):
            if self.type_third in ['major', 'add3']:
                self._third = self.get_root() + '3M'
            elif self.type_third in ['minor', 'addb3']:
                self._third =  self.get_root() + '3m'
            elif '4' in self.type_fourth:
                self._third = self.get_fourth()
            else:
                self._third = None
        return self._third

    def get_fourth(self):
        if not hasattr(self, '_fourth'):
            if '4' in self.type_fourth:
                self._fourth = self.get_root() + '4p'
            else:
                self._fourth = None
        return self._fourth

    def get_fifth(self):
        if not hasattr(self, '_fifth'):
            if self.type_fifth == 'perfect': self._fifth = self.get_root() + '5p'
            elif isinstance(self.type_fifth, list):
                fifth = []
                for x in self.type_fifth:
                    if x == 'b5': fifth.append(self.get_root() + '5d')
                    elif x == '#5': fifth.append(self.get_root() + '5a')
                    elif x == 'omit5': fifth = None
                self._fifth = fifth
            else:
                self._fifth = None
        return self._fifth

    def get_sixth(self):
        if not hasattr(self, '_sixth'):
            if self.type_sixth == 'b6': self._sixth = self.get_root() + '6m'
            elif self.type_sixth == '6': self._sixth = self.get_root() + '6M'
            else: self._sixth = None
        return self._sixth

    def get_seventh(self):
        if not hasattr(self, '_seventh'):
            if self.type_seventh == 'maj7': self._seventh = self.get_root() + '7M'
            elif self.type_seventh == '7': self._seventh = self.get_root() + '7m'
            elif self.type_seventh == 'º7': self._seventh = self.get_root() + '7d'
            else: self._seventh = None
        return self._seventh

    def get_ninth(self):
        if not hasattr(self, '_ninth'):
            if isinstance(self.type_ninth, list):
                ninth = []
                for x in self.type_ninth:
                    if x in ('9', 'add9', 'add2'): ninth.append(self.get_root() + '2M')
                    if x in ('b9', 'b2', 'addb2', 'addb9'): ninth.append(self.get_root() + '2m')
                    if x in ('#9', '#2', 'add#2', 'add#9'): ninth.append(self.get_root() + '2a')
                self._ninth = ninth
            else:
                self._ninth = None
        return self._ninth

    def get_eleventh(self):
        if not hasattr(self, '_eleventh'):
            if self.type_eleventh == '11': self._eleventh = self.get_root() + '4p'
            elif self.type_eleventh == '#11': self._eleventh = self.get_root() + '4a'
            else: self._eleventh = None
        return self._eleventh

    def get_thirteenth(self):
        if not hasattr(self, '_thirteenth'):
            if isinstance(self.type_thirteenth, list):
                thirteenth = []
                for x in self.type_thirteenth:
                    if x == 'b13': thirteenth.append(self.get_root() + '6m')
                    elif x == '13': thirteenth.append(self.get_root() + '6M')
                    elif x == '#13': thirteenth.append(self.get_root() + '6a')
                self._thirteenth = thirteenth
            else: self._thirteenth = None
        return self._thirteenth

    def get_content(self):
        if not hasattr(self, '_content'):
            self._content = [getattr(self, f'get_{x}')() for x in ('root','third','fourth','fifth','sixth','seventh', 'ninth', 'eleventh', 'thirteenth') if getattr(self, f'get_{x}')() is not None]
            for x in range(len(self._content)-1, -1, -1):
                if self._content[x] in self._content[:x]:
                    self._content.remove(self._content[x])
        return self._content

    def __repr__(self):
        return f'chord_generator.Chord_symbol("{self.get_root().name}{self._written_category[self._category]}")'


class Chord:

    def __init__(self, content, lowestNote=None, highestNote=None, position=None, duration=None, centralLine=None):
        '''
        content puede ser: list/tuple con varias Note(), list/tuple con str note ('Ab4', 'F4', 'D3'), or Chord_symbol()
        lowestNote and highestNote: Puede ser Note() or str note si ambas omite position y crea una posición distribuída equitativamente, si solo una forma la posición en dirección ascendente o descendente respectivamente
        position: puede ser 'close', 'semiopen' 'open' 'drop2' 'drop3' 'drop2-4', 'spread', 'target-chromatic', 'target-diatonic' 'target-dominant' 'target-diminished' 
        '''
        self.lowestNote, self.highestNote = self._set_borders(lowestNote, highestNote)
        self.content = self._set_content(content, duration, centralLine)
        self.position = self._set_position(position)

    def __repr__(self):
        return f'Chord({self.content})'

    def _set_borders(self, lowestNote, highestNote):
        '''
        return a tuple of Note() or None to each value, in the order lowestNote, highestNote
        '''
        if not lowestNote and not highestNote:
            return None, None
        if not lowestNote:
            lowestNote = None
        elif not isinstance(lowestNote, Note):
                lowestNote = Note(lowestNote)
        if not highestNote:
            highestNote = None
        elif not isinstance(highestNote, Note):
                highestNote = Note(highestNote)
        if lowestNote > highestNote:
            lowestNote, highestNote = highestNote, lowestNote
        return lowestNote, highestNote

    def _set_content(self, content, duration, centralLine):
        '''
        return a list of Note() from bottom to top
        C = [Note('C'), Note('E'), Note('G')]
        '''
        if isinstance(content, (tuple, list)):
            error = [x for x in content if not isinstance(x, (str, Note))]
            if error:
                raise ValueError(f'{error} contains not valid elements to create a Chord()')
            note = [Note(x, duration=duration, centralLine=centralLine) for x in content if isinstance(x, str)]
            note.extend([x for x in content if isinstance(x, Note)])
            return sorted(note)
        elif isinstance(content, Chord_symbol):
            raise(f'Ried Calculation is not able to crete chords from Chord_symbol, yet')

    def _set_position(self, position):
        '''''
        return a tuple of Interval in the order from bottom to top of the distance bewteen Chord notes. If both self.lowestNote and self.highestNote
        have values, ommit the variable position and try to create a homogeneous distribution
        '''

        pass

    def set_duration(self, duration):
        for note in self.content:
            note.set_duration(duration)
        self.duration = note.duration

    def set_line_pos(self, centralLine):
        for note in self.content:
            note.set_line_pos(centralLine)
        self.centralLine = centralLine
