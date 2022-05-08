from typing import Union
from ried.scale.scale_generator import Scale
from ried.interval.interval_analysis import Interval_Analysis

class Interval_Identifier(Scale):

    
    perf_intervals = (0, 3, 4)

    def identify_interval(self, start, end):
        '''
        Returns a dict {'intervalName', 'interval', 'octave', 'mod', 'direction'}
        '''
        self._check_inputs(start, end)
        predata = {'intervalName': None, 'interval': None, 'octave': 0,'mod': None, 'direction': None}
        self._get_direction_and_octave(start, end, predata)
        lowest, highest = self._get_lowest_highest(start, end, predata)
        scaleReference = self.generate_scale(lowest.full_name, dots=False)
        self._get_interval_name_parts(predata, scaleReference, highest)
        self._fix_intervalName(predata)
        self._fix_mod(predata)
        return predata
        self._get_actual_octave(predata, lowest, highest)
        predata['interval'] = predata['interval'] > 0 and predata['direction'] == 'down' and predata['interval'] * -1 or predata['interval']
        return predata
            
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
                predata['interval'] = i
                predata['quantity'] = i+1
                alter = note.count('#') - note.count('b')
                mod = highest.alter - alter
                predata['mod'] = mod
                if mod > 0:
                    predata['quality'] = f'{"a"*mod}'
                elif mod == 0:
                    if predata['interval'] in self.perf_intervals:
                        predata['quality'] = 'p'
                    else:
                        predata['quality'] = 'M'
                elif mod == -1 and predata['interval'] not in self.perf_intervals:
                    predata['quality'] = 'm'
                else:
                    predata['quality'] = f'{"d"*abs(mod)}'
                    if predata['interval'] not in self.perf_intervals:
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
        if predata['octave'] != 0:
            quantity = (7 * abs(predata['octave'])) + predata['quantity']
            if predata['direction'] == 'down':
                quantity *= -1
                predata['interval'] *= -1
            predata['intervalName'] = f'{quantity}{predata["quality"]}'
        else:
            predata['intervalName'] = f'{predata["quantity"]}{predata["quality"]}'
        del predata['quantity'] 
        del predata['quality']

    def _fix_mod(self, predata):
        '''
        Adjusts predata['mod'] if direction is 'down'
        '''
        if predata['direction'] == 'up':
            return
        if predata['mod'] == 0:
            if predata['interval'] in self.perf_intervals:
                return
            predata['mod'] = -1
            return
        if predata['mod'] > 0:
            predata['mod'] *= -1
            return
        if predata['mod'] < 0:
            predata['mod'] *= -1
            if predata['interval'] in self.perf_intervals:
                return
            predata['mod'] -= 1
            return




