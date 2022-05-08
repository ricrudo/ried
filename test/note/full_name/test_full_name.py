import pytest

from ried.note.note_generator import Note

import csv

with open('test/note/full_name/origen.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'inputNote,response',
        origen
        )
def test_full_name(inputNote, response):
    note = Note(inputNote)
    assert note.full_name == response



