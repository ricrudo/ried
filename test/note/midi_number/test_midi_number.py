import pytest

from ried.note.note_generator import Note

import csv

with open('test/note/midi_number/origen.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'inputNote,response',
        origen
        )
def test_midi_number(inputNote, response):
    note = Note(inputNote)
    assert str(note.midi_number) == response


