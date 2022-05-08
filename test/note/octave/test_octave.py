import pytest

from ried.note.note_generator import Note

import csv

with open('test/note/octave/origen.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'inputNote,response',
        origen
        )
def test_octave(inputNote, response):
    note = Note(inputNote)
    assert str(note.octave) == response
