from ried.notation import notation_analyzer
from ried.interval.interval_generator import Note_from_interval, Interval
from ried.scale.possible_modes import PossibleModes

from collections import namedtuple

class Duration:

    def __init__(self, duration, dots):
        self._dot = dots and 0 < dots < 3 and dots or None
        if duration:
            self.duration, self._graph_dur = self._check_duration(duration)
        else:
            self.duration, self._graph_dur = None, None
    
    def _check_duration(self, duration):
        if duration:
            try:
                return float(duration), self._check_64ths_factor(float(duration))
            except ValueError:
                try:
                    value = self._check_64ths_factor(float(duration*2/3))
                    self._dot = 1
                    return float(duration), value
                except ValueError:
                    try:
                        value = self._check_64ths_factor(float(duration*4/7))
                        self._dot = 2
                        return float(duration), value
                    except:
                        raise ValueError(f'"{duration}" is not a valid duration to create a Silence or Note')

    def _check_64ths_factor(self, value):

        if 4/64 > value or value > 8:
            raise ValueError()
        elif value == 1:
            return value
        elif value < 1:
            m = 1/value
        else:
            m = value * 1
            
        while m > 2: m /= 2
            
        if m != 2:
            raise ValueError()
        return value

    def set_duration(self, duration):
        self._dot = None
        self.duration, self._graph_dur = self._check_duration(duration)

    def get_graph_duration(self):
        return {'figure': self._graph_dur, 'dots': self._dot}

class Silence(Duration):

    def __init__(self, duration, dots=None):
        super().__init__(duration, dots)
        if not duration:
            raise ValueError(f'"{duration} is not a valid duration to create a Silence"')

    def __repr__(self):
        return f'Silence(duration={self.duration})'


class Note(Duration):

    nttnAnlzr = notation_analyzer.Note()
    intrvl = Note_from_interval()
    Beat_Position = namedtuple('BeatPosition', 'j8ths j16ths j32nds j64ths')

    def __init__(self, name, octave='none', alter='none', duration=None, dots=None, joiner_pos=None, key=None, mode=None, chord=None, centralLine=None):
        predata = self.nttnAnlzr.generator_note(name, octave, alter)
        self.name = predata['name']
        self.name_without_alter = predata['name_without_alter']
        self.full_name = predata['full_name']
        self.alter = predata['alter']
        self.alter_str = predata['alter_str']
        self.octave = predata['octave']
        self.pitch_index_without_alter = predata['pitch_index_without_alter'] 
        self.pitch_index = predata['pitch_index']
        self.midi_number = predata['midi_number']
        self.solfeo_without_alter = predata['solfeo_without_alter']
        self.solfeo = predata['solfeo']
        super().__init__(duration, dots) 
        self.joiner_pos = joiner_pos and self.set_beatPosition(joiner_pos) or None
        self.key = self._setKey(key)
        self.mode = self._setMode(mode)
        self.chord = self._setChord(chord)
        self.pos = self._set_line_pos(centralLine)
        self.aditional_line = self._set_additional_line()

    def __repr__(self):
        if not self.duration:
            return f'Note(full_name={self.full_name})'
        return f'Note(full_name={self.full_name}, duration={self.duration})'

    def _duration(self, duration):
        return 'none'

    def __eq__(self, other):
        if self.octave != 'none':
            if other.octave != 'none':
                if self.midi_number == other.midi_number: return True
                else: return False
            else:
                cache = Note(other.full_name + str(self.octave))
                result = self.midi_number == cache.midi_number
                del cache
                return result
        else:
            if other.octave != 'none':
                cache = Note(self.full_name + str(other.octave))
                result = cache.midi_number == other.midi_number
                del cache
                return result
            else:
                cache = Note(self.full_name + '1')
                cacheOther = Note(other.full_name + '1')
                result = cache.midi_number == cacheOther.midi_number
                del cache
                del cacheOther
                return result

    def __lt__(self, other):
        if self.octave != 'none':
            if other.octave != 'none':
                if self.midi_number < other.midi_number: return True
                else: return False
            else:
                cache = Note(other.full_name + str(self.octave))
                result = self.midi_number < cache.midi_number
                del cache
                return result
        else:
            if other.octave != 'none':
                cache = Note(self.full_name + str(other.octave))
                result = cache.midi_number < other.midi_number
                del cache
                return result
            else:
                cache = Note(self.full_name + '1')
                cacheOther = Note(other.full_name + '1')
                result = cache.midi_number < cacheOther.midi_number
                del cache
                del cacheOther
                return result

    def __le__(self, other):
        if self < other or self == other:
            return True
        return False

    def __add__(self, other):
        if any([isinstance(other, x) for x in (list, tuple)]):
            if  len(other) == 2:
                interval = other[0]
                scale = other[1]
            elif len(other) == 1:
                interval = other[0]
            else:
                raise ValueError(f'{other} is not allowed for addition')

        else:
            if isinstance(other, Interval.Interval):
                interval = other.intervalNotation
            else:
                interval = other
            if self.key and isinstance(interval, int):
                scale = (self.key, self.mode or 'ionian')
            else:
                scale = None

        result = self.intrvl.get_note_from_interval(self.full_name, interval, scale=scale)
        return Note(result)

    def __sub__(self, other):
        if type(other) in (list, tuple):
            if type(other[0]) == int:
                interval = other[0] * -1
            else:
                interval = f'-{other[0]}'
            other = [interval] + list(other[1:])
        elif type(other) == int:
            other *= -1
        else:
            other = f'-{other}'
        return self.__add__(other)

    def __mul__(self, other):
        if type(other) != int:
            raise ValueError(f'{other} is not allowed for multiplication')
        if other == 0:
            raise ZeroDivisionError
        if other == 1:
            other = 0
        else:
            other = (other-1) * 7
        return self.__add__(other)

    def __truediv__(self, other):
        if type(other) != int:
            raise ValueError(f'{other} is not allowed for division')
        if other == 0:
            raise ZeroDivisionError
        if other == 1:
            other = 0
        else:
            other = (other-1) * -7
        return self.__add__(other)

    def __pow__(self, other):
        if type(other) != int or other < 0:
            raise ValueError(f'{other} is not allowed for power')
        overtones = (0, '8p', '12p', '15p', '17M', '19p', '21m', '22p', '23M', '24M', '25a', '26p', '27m', '28m', '28M', '29p', '30m', '30M', '31m', '31M', '32p', '32a', '32a', '33p')
        if other > len(overtones) - 1:
            raise ValueError(f'{other} is not allowed for power. This function is limited to a number between 0 and {len(overtones)-1}')
        return self.__add__(overtones[other])

    def __xor__(self, other):
        if not isinstance(other, Note):
            raise ValueError(f'{other} is not a valid class Note')
        interval = Interval()
        response = interval.identify_interval(self, other)
        del interval
        return response

    def equalPitch(self, other):
        if all([x != 'none' for x in (self.midi_number, other.midi_number)]):
            if self.midi_number == other.midi_number:
                return True
            return False
        if any([x == 'none' for x in (self.midi_number, other.midi_number)]) and self.pitch_index == other.pitch_index:
            return True
        return False
        
    def _setKey(self, key):
        if not key: return None
        if 'b' in key and '#' in key:
            raise ValueError(f'{key} is not a valid root for a key.')
        for x in key:
            if x not in 'ABCDEFGb#':
                raise ValueError(f'{key} is not a valid root for a key.')
        return key

    def _setMode(self, mode):
        if mode:
            if not getattr(PossibleModes, mode.replace(' ', '_'), None):
                raise ValueError(f'{mode} is not a valid root for a mode.')
            return mode
        if self.key:
            return 'ionian'
        return None

    def _setChord(self, chord):
        pass

    def set_beatPosition(self, j8ths=None, j16ths=None, j32nds=None, j64ths=None):
        '''
        returns a namedtuple('BeatPosition', 'j8ths j16ths j32nds j64ths') when values can be
        'start', 'middle', 'end', None
        '''
        return Beat_Position(j8ths, j16ths, j32nds, j64ths)


    def _set_line_pos(self, centralLine):
        if centralLine and isinstance(centralLine, Note):
            if self.octave != 'none':
                distance = centralLine ^ self
                distance = (distance.octaves * 7) + distance.steps
                return distance
        return None

    def set_line_pos(self, centralLine):
        self.pos = self._set_line_pos(centralLine)
        self.aditional_line = self._set_additional_line()

    def _set_additional_line(self):
        if self.pos:
            if abs(self.pos) < 6:
                return None
            aditional = (abs(self.pos) - 4) // 2
            if self.pos < 0:
                aditional *= -1
            return aditional
