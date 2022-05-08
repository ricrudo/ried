class Beat:

    counter_beats = 0

    def __init__(self, notes, pattern=None):
        self.pattern = self._check_pattern(pattern)
        self.content = self._check_notes(notes)

    def _check_pattern(pattern):
        if not pattern:
            return
        if isinstance(pattern, list) or isinstance(pattern, tuple):
            if all([isinstance(x, int) for x in pattern]):
                self._check_beat_size(pattern)
            else:
                raise ValueError(f'{pattern} is not a valid pattern to create a beat.')

        pass

    def _check_

