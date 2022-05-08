import pytest

from ried.note.note_generator import Note

import csv

with open('test/note/alter/origen.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'inputNote,response',
        origen
        )
def test_alter(inputNote, response):
    note = Note(inputNote)
    assert str(note.alter) == response
