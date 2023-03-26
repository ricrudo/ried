from typing import Union
from collections import namedtuple

from ried.scale.scale_generator import Scale
from ried.interval.interval_analysis import Interval_Analysis

class Note_from_interval(Interval_Analysis, Scale): 

    def get_note_from_interval(self, original, interval, scale=None):
        rules = self.get_interval_data(interval)
        start_point = self.analyze_root(original)
        if scale:
            if not isinstance(scale, dict):
                scale = self.get_property_scale(scale=scale)
            reference = self.heptaphonic_natural_scale(start_point['root'], dots=False)
        else:
            reference = self.generate_scale(start_point, dots=False)
        end = self.get_endpoint(interval, rules, reference, scale)
        end = self.fix_octave(start_point, end, rules)
        return end

    def get_endpoint(self, interval, rules, reference, scale=None):
        if isinstance(interval, str) or not scale:
            return self.chromatic_endpoint(rules, reference)
        return self.diatonic_endpoint(rules, reference, scale)

    def chromatic_endpoint(self, rules: dict, reference: list) -> str:
        '''
        Return a chormatic endpoint interval
        rules keys: 'interval':int, 'octave':int, 'mod':int, 'direction':'up/down'
        reference: major scale root=startpoint i.e. ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        endpoint: i.e. 'Db'
        '''
        end = reference[rules['interval']]
        end = self.analyze_root(end)
        end['alter'] += rules['mod']
        end = self.build_root_string(end)
        return end

    def diatonic_endpoint(self, rules: dict, reference: list, scale: dict) -> str:
        '''
        Return a diatonic endpoint interval 
        rules keys: 'interval':int, 'octave':int, 'mod':int, 'direction':'up/down'
        reference: major scale root=startpoint i.e. ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        scale keys: 'root': dict,  'mode': dict
        endpoint: i.e. 'Db'
        '''
        ionian_root = self.get_ionian_root(scale)
        ionian_root = self.analyze_root(ionian_root)
        ionianScaleRef = self.generate_scale(ionian_root, dots=False)
        target = reference[rules['interval']][0]
        end = [x for x in ionianScaleRef if target in x][0]
        return end

    def get_ionian_root(self, scale):
        rootInterval = [None, '-2M', '-3M', '-4p', '-5p', '-6M', '-7M'][scale['mode']['modeNumber']%100]
        preRoot = self.build_root_string(scale['root'])
        if rootInterval:
            return self.get_note_from_interval(preRoot, rootInterval)
        else:
            return preRoot

    def get_property_scale(self, root=None, mode='ionian', scale=None):
        if not root:
            if not scale:
                raise ValueError(f'root or scale must be specified')
            return self.scale_from_list(scale)
        root = self.analyze_root(root)
        mode = self.analyze_mode(mode)
        return {'root': root, 'mode': mode}

    def fix_octave(self, start_point, end, rules):
        if start_point['octave'] != None:
            finalOctave = start_point['octave'] + rules['octave']
            start_index = 'CDEFGAB'.index(start_point['root'])
            end_index = 'CDEFGAB'.index(end[0])
            if rules['direction'] == 'up' and end_index < start_index:
                finalOctave += 1
            if rules['direction'] == 'down' and end_index > start_index:
                finalOctave -= 1
            return f'{end}{finalOctave}'
        return end


class Interval(Scale):

    perf_intervals = (0, 3, 4)
    Interval = namedtuple('Interval', 'intervalNotation closedOctNotation steps octaves alterations direction')

    def identify_interval(self, start, end):
        '''
        Returns a namedtuple('Interval', 'intervalNotation closedOctNotation steps octaves alterations direction')
        '''
        self._check_inputs(start, end)
        predata = {'intervalName': None, 'steps': None, 'octave': 0, 'mod': None, 'direction': None}
        self._get_direction_and_octave(start, end, predata)
        lowest, highest = self._get_lowest_highest(start, end, predata)
        scaleReference = self.generate_scale(lowest.full_name, dots=False)
        self._get_interval_name_parts(predata, scaleReference, highest)
        self._fix_intervalName(predata)
        self._fix_mod(predata)
        return self._gen_IntervalNamedTupled(predata)

        self._get_actual_octave(predata, lowest, highest)
        predata['steps'] = predata['steps'] > 0 and predata['direction'] == 'down' and predata['steps'] * -1 or predata['steps']
        return predata

    def _gen_IntervalNamedTupled(self, predata):
        return self.Interval(predata['intervalName'], predata['closedOctNotation'], predata['steps'], predata['octave'], predata['mod'], predata['direction'])

    def _check_inputs(self, start, end):
        if not hasattr(start, 'midi_number'):
            raise ValueError(f'{start} is not a valid class Note for Interval')
        if not hasattr(end, 'midi_number'):
            raise ValueError(f'{end} is not a valid class Note for Interval')

    def _get_lowest_highest(self, start, end, predata):
        '''
        Compare start against end and determine which is the lowest and the highest note 
        '''
        if predata['direction'] == 'up':
            return start, end
        else:
            return end, start

    def _get_interval_name_parts(self, predata: dict, scaleReference: list, highest) -> None:
        '''
        defines the interval name within a octave
        '''
        for i, note in enumerate(scaleReference):
            if note[0] == highest.name_without_alter:
                predata['steps'] = i
                predata['quantity'] = i+1
                alter = note.count('#') - note.count('b')
                mod = highest.alter - alter
                predata['mod'] = mod
                if mod > 0:
                    predata['quality'] = f'{"a"*mod}'
                elif mod == 0:
                    if predata['steps'] in self.perf_intervals:
                        predata['quality'] = 'p'
                    else:
                        predata['quality'] = 'M'
                elif mod == -1 and predata['steps'] not in self.perf_intervals:
                    predata['quality'] = 'm'
                else:
                    predata['quality'] = f'{"d"*abs(mod)}'
                    if predata['steps'] not in self.perf_intervals:
                        predata['quality'] = predata['quality'][:-1]
                return

    def _get_direction_and_octave(self, start, end, predata):
        '''
        determines the direction od the interval
        '''
        if any([x.octave == 'none' for x in (start, end)]):
            predata['octave'] = 0
            predata['direction'] = 'up'
            return
        # unison and octaves
        if start.name_without_alter == end.name_without_alter:
            predata['octave'] = end.octave - start.octave
            if start.octave == end.octave:
                predata['direction'] = 'up'
                return
            elif start.octave < end.octave:
                predata['direction'] = 'up'
                return
            else:
                predata['direction'] = 'down'
                return
        # other 
        if start.octave == end.octave:
            predata['octave'] = 0
            if start.pitch_index_without_alter <= end.pitch_index_without_alter:
                predata['direction'] = 'up'
                return
            else:
                predata['direction'] = 'down'
                return
        elif start.octave < end.octave:
            if start.pitch_index_without_alter <= end.pitch_index_without_alter:
                predata['octave'] = end.octave - start.octave
            else:
                predata['octave'] = (end.octave - 1) - start.octave
            predata['direction'] = 'up'
            return
        else:
            if start.pitch_index_without_alter <= end.pitch_index_without_alter:
                predata['octave'] = (end.octave + 1) - start.octave
            else:
                predata['octave'] = end.octave - start.octave
            predata['direction'] = 'down'
            return

    def _fix_intervalName(self, predata):
        '''
        Generates en intervalName from predata['octave'], predata['quantity'], predata['quality']
        Deletes predata['quantity'] and predata['quality']
        '''
        symbol = predata['direction'] == 'down' and '-' or ''
        predata['steps'] *= predata['direction'] == 'up' and 1 or -1

        if predata['octave'] != 0:
            quantity = (7 * abs(predata['octave'])) + predata['quantity']
            predata['intervalName'] = f'{symbol}{quantity}{predata["quality"]}'
        else:
            predata['intervalName'] = f'{symbol}{predata["quantity"]}{predata["quality"]}'
        predata['closedOctNotation'] = f'{symbol}{predata["quantity"]}{predata["quality"]}'
        del predata['quantity'] 
        del predata['quality']

    def _fix_mod(self, predata):
        '''
        Adjusts predata['mod'] if direction is 'down'
        '''
        if predata['direction'] == 'up':
            return
        if predata['mod'] == 0:
            if predata['steps'] in self.perf_intervals:
                return
            predata['mod'] = -1
            return
        if predata['mod'] > 0:
            predata['mod'] *= -1
            return
        if predata['mod'] < 0:
            predata['mod'] *= -1
            if predata['steps'] in self.perf_intervals:
                return
            predata['mod'] -= 1
            return




