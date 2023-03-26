from typing import Union
from ried.scale.possible_modes import PossibleModes
from ried.scale.scale_analysis import Scale_Analysis

class Scale(Scale_Analysis):

    ionian_skeleton = 'n.n.nn.n.n.n'
    major_pentatonic_skeleton = 'n.n.n._n.n._'

    def generate_scale(self, root:Union[dict, str], mode:Union[str,int]='ionian', dots:bool=True) -> list:
        '''
        Returns a scale from root (dict {'root':str, 'alter':int, 'octave': int} and with a mode structure in any of these formats:
        dots=False => ['C', 'D', 'E', 'F, 'G', 'A', 'B']
        dots=True (default) => ['C', '.', 'D', '.', 'E', 'F, '.', 'G', '.', 'A', '.', 'B']
        '''
        root = self.analyze_root(root)
        mode = self.analyze_mode(mode)
        hepta_naturalScale = self.heptaphonic_natural_scale(root['root'])
        skeleton = self._get_skeleton(mode)
        rootNatural_Scale = self._get_naturalRoot_scale(hepta_naturalScale, skeleton)
        realScale = self.add_alterarions(root['alter'], rootNatural_Scale, mode)
        return realScale

    def heptaphonic_natural_scale(self, root:str, dots:bool=True) -> Union[str, list]:
        '''
        Returns a heptaphonic scale from a given root, without structure nor alterations
        '''
        if root == 'C':
            heptaScale = 'C.D.EF.G.A.B'
        else:
            post, pre = 'C.D.EF.G.A.B'.split(root)
            heptaScale = "".join([root, pre, post])
        if dots:
            return heptaScale
        return list(heptaScale.replace('.', ''))

    def check_mode(self, mode:Union[str, int]):
        '''
        Checks if mode name or int is within the options
        '''
        if isinstance(mode, str) and not getattr(PossibleModes, mode.replace(' ', '_'), None):
            raise ValueError(f'{mode} in not a valid mode')
        if isinstance(mode, int) and mode not in {x.value for x in PossibleModes}:
            raise ValueError(f'{mode} in not a valid mode')

    def _get_skeleton(self, mode:dict) -> list:
        '''
        Returns the respective skeleton according to the mode
        '''
        if 700 <= mode['modeNumber'] < 900:
            skeleton = list(self.ionian_skeleton)
        if 500 <= mode['modeNumber'] < 700:
            skeleton = list(self.major_pentatonic_skeleton)
        if mode['modeNumber'] % 100 == 0:
            return skeleton
        counter = 0
        while counter < mode['modeNumber'] % 100:
            n = skeleton.pop(0)
            skeleton.append(n)
            if n != '.':
                counter += 1
        if skeleton[0] == '.':
            del skeleton[0]
            skeleton.append('.')
        return skeleton

    def _get_naturalRoot_scale(self, hepta_naturalScale: list, skeleton:list) -> list:
        '''
        Returns a scale with a natural root, following the structure of the skeleton
        '''
        skeleton_note_cache = []
        hepta_note_cache = []
        alter_cache = []
        natural_root_scale = []
        for i, note in enumerate(skeleton):
            if note != '.': skeleton_note_cache.append(note)
            if hepta_naturalScale[i] != '.': hepta_note_cache.append(hepta_naturalScale[i])
            if skeleton_note_cache and hepta_note_cache:
                alter = alter_cache and alter_cache.pop(0) or 0
                symbol = alter < 0 and 'b' * abs(alter) or alter > 0 and '#' * alter or ''
                natural_root_scale.append(hepta_note_cache.pop(0) + symbol)
                if skeleton_note_cache[0] == '_':
                    del natural_root_scale[-1]
                del skeleton_note_cache[0]
            if skeleton_note_cache:
                for i, x in enumerate(alter_cache):
                    alter_cache[i] -= 1
                if note != '.':
                    alter_cache.append(-1)
            if hepta_note_cache:
                for i, x in enumerate(alter_cache):
                    alter_cache[i] += 1
                if hepta_naturalScale[i] != '.':
                    alter_cache.append(1)
        return natural_root_scale
       
    def add_alterarions(self, alter, naturalScale, mode):
        for i, note in enumerate(naturalScale):
            if note == '.':
                continue
            mod = alter * 1
            mod -= note.count('b')
            mod += note.count('#')
            mod = mod > 0 and '#' * mod or mod < 0 and 'b' * abs(mod) or ''
            naturalScale[i] = note[0] + mod
            if i == 6 and mode['modeName'] in ['melodic minor', 'harmonic minor']:
                flats = naturalScale[i].count('b')
                if flats:
                    naturalScale[i] = naturalScale[i][:-1]
                else:
                    naturalScale[i] += '#'
        return naturalScale

