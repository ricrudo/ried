import pytest

from ried.note.note_generator import Note

import csv

with open('test/note/comparison/origen.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'input1,input2,response',
        origen#[30000:]
        )
def test_comparison(input1, input2, response):
    a = Note(input1)
    b = Note(input2)

    if response == '=':
        assert str(a < b) == 'False'
        assert str(a > b) == 'False'
        assert str(a == b) == 'True'
    elif response == '>':
        assert str(a < b) == 'False'
        assert str(a == b) == 'False'
        assert str(a > b) == 'True'
    elif response == '<':
        assert str(a == b) == 'False'
        assert str(a > b) == 'False'
        assert str(a < b) == 'True'

