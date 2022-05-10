from ried.note.note_generator import Note, Silence

from typing import Union

class Beat:

    counter_beats = 0

    def __init__(self, notes:Union[list, tuple] =None, pattern:Union[str, list, tuple] =None):
        self.counter_beats += 1
        self.id = self.counter_beats
        self.pattern = self._check_pattern(pattern)
        self.content = self._check_notes(notes)
        self.fix_pattern()
        #self._check_beat_size()

    def _check_pattern(self, pattern):
        if pattern:
            try:
                if isinstance(pattern, (list, tuple)):
                    return [float(x) for x in pattern]
                elif isinstance(pattern, str):
                    sep = {x for x in pattern if x in ',-'}
                    if sep:
                        return [float(x) for x in pattern.split(list(sep)[0])]
                    else:
                        return [float(pattern)]
                else:
                    return [float(pattern)]
                    raise ValueError()
            except ValueError:
                raise ValueError(f'{pattern} is not a valid pattern to create a beat.')
    
    def _check_beat_size(self):
        print('cheking beat size')
        pass

    def _check_notes(self, notes):
        if not isinstance(notes, list):
            notes = [notes]
        if notes:
            for i, note in enumerate(notes):
                if isinstance(note, (Note, Silence)):
                    continue
                note[i] = Note(note)
            return notes

    def fix_pattern(self):
        '''
        Unfies the rhythms prevailing those in self.pattern 
        '''
        if self.pattern and self.content:
            if len(self.pattern) != len(self.content):
                raise ValueError(f'The amount of notes and rhythms are not equal')
            if self.pattern:
                for i, note in enumerate(self.content):
                    self.content[i].set_duration(self.pattern[i])
            



