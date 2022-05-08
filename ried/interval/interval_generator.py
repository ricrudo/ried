from typing import Union

from ried.scale.scale_generator import Scale
from ried.interval.interval_analysis import Interval_Analysis

class Interval(Interval_Analysis, Scale): 

    def get_endpoint(self, typeSource, rules, reference, scale=None):
        if typeSource == str or not scale:
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
        root = analyze_root(root)
        mode = analyze_mode(mode)
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

    def get_note_from_interval(self, original, interval, scale=None):
        rules = self.get_interval_data(interval)
        start_point = self.analyze_root(original)
        if scale:
            scale = self.get_property_scale(scale=scale)
            reference = self.heptaphonic_natural_scale(start_point['root'], dots=False)
        else:
            reference = self.generate_scale(start_point, dots=False)
        end = self.get_endpoint(type(interval), rules, reference, scale)
        end = self.fix_octave(start_point, end, rules)
        return end

