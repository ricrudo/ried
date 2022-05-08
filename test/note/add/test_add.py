import pytest

from ried.note.note_generator import Note

import csv

with open('test/note/add/origen.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'inputNote,number,response',
        origen
        )
def test_add(inputNote, number, response):
    note = Note(inputNote)
    response = Note(response)
    assert note + int(number) == response

