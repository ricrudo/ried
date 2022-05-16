from ried.note.note_generator import Note
from ried.beat.beat_generator import Beat

from collections import namedtuple
import copy

class Measure:
    
    Subdivision = namedtuple('Subdivision', 'beat_grouping figure_subidivision')

    centralLineNote = {'treble 1':'D5', 'treble 2':'B4', 'treble 3':'G4', 'treble 4':'E4', 'treble 5':'C4',
            'bass 1':'C4', 'bass 2':'A3', 'bass 3':'F3', 'bass 4':'D3', 'bass 5':'B2',
            'alto 1':'G4', 'alto 2':'E4', 'alto 3':'C4', 'alto 4':'A3', 'alto 5':'F3'}

    def __init__(self, measure=None, num=None, den=None, subdivision=None, num_max_dots=4, clef='treble 2'):
        self.num_max_dots = num_max_dots
        self.subdivision = subdivision
        if measure or (den and num):
            if num:
                self.num = self._number_formats(num)
                if den:
                    self.den = self._number_formats(self._check_den(den, self.num_max_dots))
                else:
                    self.den = 4
            else:
                self.num, self.den = self._analyze_measure(measure)
            self.subdivision = self._gen_subdivision(subdivision)
        else:
            self.measure, self.den, self.num, self.subdivision = None, None, None, None
        self.centralLine = self.set_clef(clef)
        self.clef = clef

    def set_clef(self, clef):
        try:
            return Note(self.centralLineNote[clef])
        except KeyError:
            raise ValueError(f'"{clef}" is not a valid clef. Options are "treble ", "bass ", "alto " follow by its line position. ie. "treble 2"')

    def _check_den(self, value, n=4):
        if value in (1,2):
            return value
        if 1.25 < value < 2:
            for x in range(1,n+1):
                if 1 + (((2**x)-1)/(2**x)) == value:
                    return value
            raise ValueError(f'{value} is not a valid number as a denominator')
        for x in range(1,8):
            if value == 2 ** x:
                return value
        base = 1
        while True:
            if 2 ** (base + 1) < value:
                base += 1
            else:
                base = 2 ** base
                break
                
        dots = value - base
        for x in range(1,n+1):
            if base + base*((2**x) - 1)/(2**x) == value:
                return value
        raise ValueError(f'{value} is not a valid number as a denominator')

    def _number_formats(self, number):
        '''
        Delete the unneeded '.0' in float 
        '''
        if number % 1 == 0:
            return int(number)
        return number

    def _analyze_measure(self, measure):
        if isinstance(measure, str):
            sep = list({x for x in measure if not x.isdigit()})
            if len(sep) > 1:
                raise ValueError(f'{measure} is not valid format to create a Measure')
            if not sep:
                return int(measure), 4
            else:
                measure = measure.split(sep[0])
        elif isinstance(measure, int):
            return measure, 4
        if isinstance(measure, (list, tuple)) and len(measure) != 2:
            raise ValueError(f'{measure} is not valid format to create a Measure')
        num = self._number_formats(float(measure[0]))
        den = self._number_formats(self._check_den(float(measure[1]), self.num_max_dots))
        return num, den

    def _gen_subdivision(self, subdivision=None):
        if subdivision:
            return self._check_subdivision(subdivision)
        else:
            return self._get_common_subdivions()

    def _check_subdivision(self, subdivision):
        subdivision = self._subdivision_as_number(subdivision)
        subdivision = self._grouping_subdivision(subdivision)
        return subdivision

    def _subdivision_as_number(self, subdivision):
        if isinstance(subdivision, str):
            if subdivision.lower() == 'ternary': return 3
            if subdivision.lower() == 'binary': return 2
        elif isinstance(subdivision, (int, float)) and subdivision > 0:
            if subdivision % 1 == 0:
                return int(subdivision)
            return subdivision
        elif isinstance(subdivision, (list, tuple)):
            grouping = []
            for x in subdivision:
                if not isinstance(x, (int, float)):
                    raise ValueError(f'{self.subdivision} is not a valid subdivision to create a bar')
                grouping.append(self._subdivision_as_number(x))
            return tuple(grouping)
        raise ValueError(f'{self.subdivision} is not a valid subdivision to create a bar')

    def _grouping_subdivision(self, subdivision):
        if subdivision == 2:
            grouping = [2 for x in range((self.num * 2) // 2)]
            if (self.num * 2) % 2:
                grouping.append((self.num * 2) % 2)
            return self.Subdivision(tuple(grouping), self.den*2)
        elif isinstance(subdivision, int):
            grouping = [subdivision for x in range(self.num // subdivision)]
            if self.num % subdivision:
                grouping.append(self.num % subdivision)
            return self.Subdivision(tuple(grouping), self.den*1)
        elif isinstance(subdivision, tuple):
            if sum(subdivision) == self.num:
                return self.Subdivision(tuple(subdivision), self.den*1)
            elif sum(subdivision) == self.num*2:
                return self.Subdivision(tuple(subdivision), self.den*2)
        raise ValueError(f'{self.subdivision} is not a valid subdivision to create a bar')

    def _get_common_subdivions(self):
        if self.den <= 4:
            return self._grouping_subdivision(2)
        else:
            return self._grouping_subdivision(3)

    def modify_subdivision(self, subdivision):
        self.subdivision = self._gen_subdivision(subdivision)

class Bar(Measure):
    def __init__(self, measure=None, num=None, den=None, subdivision=None, content=None, distribution='equal', clef='treble 2'):
        '''
        subdivision can be set to str "distribution" in order to get the subdivision from distribution 
        distribution applies when content is None or when elements in content are instances of Note. distribution can be a str 'equal', 'start' and 'end' or a tuple/list of tuples/lists by every beat
            equal: it takes the bar and divided it into same parts according to len(content)
            start: it takes the note and try to put them first by beat, if it's not posible go down into the subdivision, if silences are needed those will be allocated at the end
            end: it takes the note and try to put them first by beat, if it's not posible go down into the subdivision, if silences are needed those will be allocated at the beginning
        '''
        if not measure and not num:
            raise ValueError('measure or numerator are required to create a bar')
        if subdivision == 'distribution':
            super().__init__(measure=measure, num=num, den=den, clef=clef)
            self._subdivision_from_distribution(distribution)
        else:
            super().__init__(measure=measure, num=num, den=den, subdivision=subdivision, clef=clef)
        self.content = self._add_content(content)
        self.distribution = self._add_distribution(distribution)
        self.content = self._create_beats()

    def __repr__(self):
        if self.content:
            return f'Bar({[x for x in self.content]})'
        else:
            return f'Bar()'

    def _add_content(self, content):
        if isinstance(content, (list, tuple)):
            if isinstance(content, tuple):
                content = list(content)
            for i, x in enumerate(content):
                if not isinstance(x, (Beat, Note, str)):
                    raise ValueError(f'{x} is not a valid Beat to put into a Bar')
                elif isinstance(x, str):
                    content[i] = Note(x)
            for i, first in enumerate(content):
                for other in range(i+1, len(content)):
                    if content[other] is first:
                        content[other] = copy.deepcopy(content[other])
            return content
        if content:
            raise ValueError(f'{x} is not a valid Beat to put into a Bar')

    def _create_beats(self):
        response = [] 
        if self.content and self.distribution:
            for i, beat in enumerate(self.distribution, 1):
                sounds = []
                for tick in beat: 
                    if tick > 0:
                        try:
                            sounds.append(self.content.pop(0))
                        except IndexError:
                            raise IndexError(f'There is not enough content for the distribution entered')
                response.append(Beat(content=sounds, bar_position=i, pattern=beat, clef=self.clef, centralLine=self.centralLine))
            return response
        return self.content

    def _check_size_beat(self, beat, position):
        '''
        debe testear si la cantidad de figuras que tiene el beat equivales a las posibles para el bar según denominador y Subdivision.beat_grouping
        '''
        pass

    def add_beat(self, beat, position):
        if not isinstance(position, int):
            raise ValueError(f'position must be a int but recieved a {type(position)}')
        if position < 0 and abs(position) > len(self.subdivision.beat_grouping):
            raise IndexError(f'position {position} is not available in a {self.num}/{self.den} bar')
        self._check_size_beat(beat, position)

    def _check_distribution(self, distribution):
        if isinstance(distribution, (tuple, list)) and all([isinstance(x, (tuple, list)) for x in distribution]) and all([isinstance(value, (int, float)) for beat in distribution for value in beat]):
            return 'tuple'
        if distribution in ('equal', 'start', 'end'):
            return 'string'

    def _add_distribution(self, distribution):
        if distribution:
            if not self.content or all([isinstance(x, Note) for x in self.content]):
                if self._check_distribution(distribution) == 'tuple': 
                    if len(distribution) != len(self.subdivision.beat_grouping):
                        raise IndexError('This amount of beats admitted in this bar and the value in "distribution" do not correspond')
                    distribution = tuple([tuple([x for x in group]) for group in distribution])
                    return self._convert_distribution(distribution)
            if not self.content or all([isinstance(x, Beat) for x in self.content]):
                if self._check_distribution(distribution) != 'string': 
                    raise ValueError(f'distribution="{distribution}" is not valid when content is not specified. If you insert a tuple with only one element, you need a "," to be a accepted tuple format. i.e. (1,)')
                return distribution
            raise ValueError(f'distribution="{distribution}" is not valid to create a Bar')

    def _subdivision_from_distribution(self, distribution):
        if self._check_distribution(distribution) == 'tuple':
            proportion = [sum([abs(x) for x in beat]) for beat in distribution]
            sum_proportion = sum(proportion)
            total_subdivision_figure = sum(self.subdivision.beat_grouping)
            conversor = sum_proportion / total_subdivision_figure
            proportion = [x/conversor for x in proportion]
            self.modify_subdivision(proportion)
            return
        raise ValueError(f'It is not posible to get a subdivision from "disribution={distribution}"')

    def _convert_distribution(self, distribution):
        distribution_figured = []
        for i, group in enumerate(self.subdivision.beat_grouping):
            available_room = (4/self.subdivision.figure_subidivision*group)
            distribution_total = sum([abs(x) for x in distribution[i]])
            distribution_percentage = [x/distribution_total for x in distribution[i]]
            distribution_figured.append([x*available_room for x in distribution_percentage])
        del distribution_percentage
        del distribution_total
        del available_room
        return distribution_figured
        
