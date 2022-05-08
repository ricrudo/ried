from typing import Union

class Interval_Analysis:

    def get_interval_data(self, value: Union[str, int]) -> dict:
        if type(value) == str:
            return self._get_parts_from_string(value)
        if type(value) == int:
            return self.get_parts_int(value)
        raise ValueError(f'{value} ({type(value)}) is not a valid format for interval notation')

    def _get_parts_from_string(self, value:str) -> dict: 
        '''
        Recieves an str quantity and quality string form. i.e. '2m'
        Returns a dict with the interval, octave, mod (number of alterations), and direction (up/down)
        '''
        self._check_startpoint_1(value)
        interval, octave = self._interval_octave_row_data(value)
        mod, direction = self._get_modification(value, interval)
        interval, octave = self._interval_octave_fix_data(interval, octave, direction)
        return {'interval': interval, 'octave': octave, 'mod': mod, 'direction': direction}

    def _interval_octave_row_data(self, value: str) -> tuple:
        '''
        Recieves an str quantity and quality string form. i.e. '2m'
        Returns a tuple with interval (int) and octave(int)
        '''
        digit = int("".join([x for x in value if x.isdigit()]))
        interval = digit > 7 and (digit % 7) or digit
        interval = digit % 7 == 0 and 6 or interval -1
        self._check_startpoint_2(value, interval)
        octave = digit > 7 and (digit - 1)// 7 or 0
        return interval, octave

    def _interval_octave_fix_data(self, interval: int, octave: int, direction: str) -> tuple:
        '''
        Recieves interval (int), octave (int), and direction (str: up/down)
        Returns a tuple with interval (int) and octave(int) modified according to direction
        '''
        octave = direction == 'down' and octave * -1 or octave
        interval = interval > 0 and direction == 'down' and interval * -1 or interval
        return interval, octave

    def _get_modification(self, value: str, interval:int) -> tuple:
        '''
        Recieve 
          "value": an str interval quantity anf quality forma. i.e. '2m'
          "interval": numerical representation of the value
        return a dict with the interval, octave, mod (number of alterations), and direction (up/down)
        '''
        value = [x for x in value if x in 'Mmadp-']
        count_M = value.count('M') > 0 and 1 or 0
        count_m = value.count('m') > 0 and 1 or 0
        count_a = value.count('a')
        count_d = value.count('d')
        count_p = value.count('p') > 0 and 1 or 0
        direction = value.count('-') > 0 and 'down' or 'up'
        
        if count_M:
            return direction == 'down' and -1 or 0, direction
        elif count_m:
            return direction == 'up' and -1 or 0, direction
        elif count_a:
            if direction == 'up':
                return count_a, direction
            else:
                if interval in (1,2,5,6):
                    return (count_a + 1) * -1, direction
                else:
                    return count_a * -1, direction
        elif count_d:
            if direction == 'up':
                if interval in [1,2,5,6]:
                    return (count_d + 1) * (-1), direction
                else:
                    return count_d * (-1), direction
            else:
                return count_d, direction
        return 0, direction

    def _check_startpoint_1(self, value: str):
        '''
        Checks if value(str) is in a valid quantity, quality interval format
        '''
        error = set()
        if (not any([x.isdigit() for x in value])):
            error.add('missing digit') 
        if not all([x in 'Mmadp-' for x in value if not x.isdigit()]):
            error.add('unknow caracther')
        if len({x for x in value if x in 'Mmpad'}) > 1:
            error.add('wrong quality')
        if error:
            raise ValueError(f'"{value}" is not a valid interval notation')

    def _check_startpoint_2(self, value: str, interval: int):
        '''
        Checks if data interval quality and quantity are compitibles.
        i.e. '2m' is good but '2p' is wrong
        '''
        error = set()
        if interval in (3,4,0) and any([x in 'Mm' for x in value]):
            error.add('wrong quality')
        elif interval not in (3,4,0) and any([x in 'p' for x in value]):
            error.add('wrong quality')
        if error:
            raise ValueError(f'"{value}" is not a valid interval notation')

    def get_parts_int(self, value: int) -> dict:
        '''
        Recieves an value int
        Returns a dict with the interval, octave, mod (number of alterations), and direction (up/down)
        '''
        interval = abs(value) % 7
        octave = abs(value) // 7
        if value < 0:
            direction = 'down'
            interval *= -1
            octave *= -1
        else:
            direction = 'up'
        return {'interval': interval, 'octave': octave, 'mod': 0, 'direction': direction}
