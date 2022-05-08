from typing import Union

class Root_Analysis:

    def analyze_root(self, original: Union[str, dict]) -> dict:
        ''' 
        Returns a dict {'root', 'alter', 'octave'} with root information
        '''
        if self._check_root_conditions(original) == dict:
            return original
        root = original[0]
        alter = [x for x in original if x in '#b']
        if alter:
            if '#' in alter and 'b' in alter:
                raise ValueError(f'"{original}" is not a valid value for get an interval')
            alter = 'b' in alter and len(alter) * -1 or '#' in alter and len(alter)
        else:
            alter = 0
        octave = [x for x in original if x.isdigit() or x == '-']
        if octave:
            octave = int("".join(octave))
        else:
            octave = None

        return {'root': root, 'alter': alter, 'octave': octave}

    def build_root_string(self, root):
        alter = root['alter'] > 0 and '#' * root['alter'] or root['alter'] < 0 and 'b' * abs(root['alter']) or ''
        octave = root['octave'] != None and str(root['octave']) or ''
        return f'{root["root"]}{alter}{octave}'

    def _check_root_conditions(self, root):
        if type(root) == dict:
            if len(root) == 3 and all([x in ('root', 'alter', 'octave') for x in root]):
                return dict
            raise ValueError(f'{root} is not a valid dict for a root')
        elif type(root) == str:
            if root[0] not in 'ABCDEFG':
                raise ValueError(f'"{root}" is not a valid value for get an interval')
            if not all([x in '#b-' for x in root[1:] if not x.isdigit()]):
                raise ValueError(f'"{root}" is not a valid value for get an interval')
            return str


