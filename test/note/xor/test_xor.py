import pytest

from ried.note.note_generator import Note

import csv

with open('test/note/xor/origen.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'inputNote,input2,response',
        origen
        )
def test_xor(inputNote, input2, response):
    note1 = Note(inputNote)
    note2 = Note(input2)
    result = note1 ^ note2
    assert result.intervalNotation == response




