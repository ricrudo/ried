from ried.notation import notation_analyzer
from ried.interval.interval_generator import Interval
from ried.interval.interval_identifier import Interval_Identifier

from collections import namedtuple

class Note:

    nttnAnlzr = notation_analyzer.Note()
    intrvl = Interval()
    intvrl_idntfcd = Interval_Identifier()
    Beat_Position = namedtuple('BeatPosition', 'j8ths j16ths j32nds j64ths')

    def __init__(self, name, octave='none', alter='none', duration='none', beat_position=None, key=None, mode=None, chord=None):
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
        self.duration, self.relative_duration = duration != 'none'and self.set_duration(duration) or ('none','none') 
        self.beat_position = beat_position and self.set_beatPosition(beat_position) or None
        self.key = self._setKey(key)
        self.mode = self._setMode(mode)
        self.chord = self._setChord(chord)

    def __repr__(self):
        return f'Note(full_name={self.full_name})'

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

    def __add__(self, other):
        if type(other) in (list, tuple):
            if  len(other) == 2:
                interval = other[0]
                scale = other[1]
            elif len(other) == 1:
                interval = other[0]
            else:
                raise ValueError(f'{other} is not allowed for addition')
        else:
            interval = other
            scale = self.key
                               
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
        return self.intvrl_idntfcd.identify_interval(self, other)['intervalName']



    def equalPitch(self, other):
        if all([x != 'none' for x in (self.midi_number, other.midi_number)]):
            if self.midi_number == other.midi_number:
                return True
            return False
        if any([x == 'none' for x in (self.midi_number, other.midi_number)]) and self.pitch_index == other.pitch_index:
            return True
        return False
        
    def _setKey(self, key):
        return None

    def _setMode(self, mode):
        return None

    def _setChord(self, chord):
        pass

    def set_beatPosition(self, j8ths=None, j16ths=None, j32nds=None, j64ths=None):
        '''
        returns a namedtuple('BeatPosition', 'j8ths j16ths j32nds j64ths') when values can be
        'start', 'middle', 'end', None
        '''
        return Beat_Position(j8ths, j16ths, j32nds, j64ths)

