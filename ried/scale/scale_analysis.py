from typing import Union

from ried.root.root_analysis import Root_Analysis

class Scale_Analysis(Root_Analysis):
    
    def get_property_scale(root:str=None, mode:str='ionian', scale:Union[tuple, list]=None) -> dict:
        '''
        Returns a dict {'root': rootName, 'mode': modeName}
        '''
        if not root:
            if not scale:
                raise ValueError(f'root or scale must be specified')
            return scale_from_list(scale)
        root = self.analyze_root(root)
        mode = self.analyze_mode(mode)
        return {'root': root, 'mode': mode}

    def analyze_mode(self, mode:Union[str, int]) -> dict:
        '''
        Returns a dict with two keys, modeName and modeNumebr
        '''
        self.check_mode(mode)
        if type(mode) == str:
            modeName = mode.lower()
            modeNumber = self.posible_modes[mode]
            return {'modeName': modeName, 'modeNumber': modeNumber}
        if type(mode) == int:
            modeNumber = int(mode)
            modeName = [x for x in posible_modes.keys() if posible_modes[x] == mode][0]
        return {'modeName': modeName, 'modeNumber': modeNumber}


    def scale_from_list(self, scale):
        '''

        '''
        if type(scale) not in (list, tuple, dict):
            raise ValueError(f'{type(scale)} is not allowed. Scale must be a list, tuple or dict.')
        if len(scale) != 2:
            raise ValueError(f'scale must be has two option, root and mode')
        if isinstance(scale, dict) and not all([x in ['root', 'mode'] for x in list(scale.keys())]):
            raise ValueError(f'scale keys must be "root" and "mode"')
        root = isinstance(scale, dict) and scale['root'] or scale[0]
        mode = isinstance(scale, dict) and scale['mode'] or scale[1]
        root = self.analyze_root(root)
        mode = self.analyze_mode(mode)
        return {'root': root, 'mode': mode}


