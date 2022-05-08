from ried.note.note_generator import Note
from ried.scale.scale_generator import Scale
from ried.interval.interval_generator import Interval


class ScaleRange:

    symbols = 'ABCDEFG#b'
    posible_modes = Scale.posible_modes
    interval = Interval()

    def __init__(self, start, end=None, length=None, key=None, mode=None):
        self.start = self._check_note(start)
        self.end = self._check_note(end)
        self.length = self._check_length(length)
        self.key = self._check_key(key)
        self.mode = self._check_mode(mode)
        self.range = [self.start]
        self._generate_range()

    def _check_note(self, value):
        if value and not isinstance(value, Note):
            raise ValueError(f'{value} is not a valid class Note to create a range')
        return value

    def _check_length(self, value):
        if self.end:
            inter = self.start ^ self.end
            inter = int("".join([x for x in inter if x.isdigit()]))
            return inter
        if not isinstance(value, int):
            raise ValueError(f'{value} is not a valid length to create a range')
        return value

    def _check_key(self, value):
        if value:
            if value not in self.symbols:
                raise ValueError(f'{value} is not a valid key to create a range')
            return value
        if self.start.key:
            return self.start.key
        return self.start.name

    def _check_mode(self, value):
        if value:
            if value not in self.posible_modes:
                raise ValueError(f'{value} is not a valid mode to create a range')
            return value
        if self.start.mode:
            return self.start.mode
        return 'ionian'

    def _generate_range(self):
        self.direction = self._get_direction()
        if self.direction:
            self._fill_range()
            self._trim_ends()
        else:
            if not self.end:
                self.range = None

    def _get_direction(self):
        if self.end:
            if self.start < self.end: return 'up'
            if self.start > self.end: return 'down'
        elif self.length > 1: return 'up'
        elif self.length < 1: return 'down'
        return None

    def _fill_range(self):
        if self.direction == 'up':
            length = abs(self.length)
            self.range = [Note(self.interval.get_note_from_interval(self.start.full_name, x, scale=(self.key, self.mode))) for x in range(length)]
        elif self.direction == 'down':
            length = abs(self.length) * -1
            self.range = [Note(self.interval.get_note_from_interval(self.start.full_name, x, scale=(self.key, self.mode))) for x in range(0, length, -1)]

    def _trim_ends(self):
        if self.direction == 'up':
            while self.start > self.range[0]: del self.range[0]
            while self.end < self.range[-1]: del self.range[-1]
        else:
            while self.start < self.range[0]: del self.range[0]
            while self.end > self.range[-1]: del self.range[-1]

        




