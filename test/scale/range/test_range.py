import pytest

from ried.note.note_generator import Note
from ried.scale.scale_range import ScaleRange

import csv

with open('test/scale/range/origen.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'start,end,response',
        origen
        )
def test_range(start, end, response):
    result = ScaleRange(Note(start), Note(end)).range
    result = "-".join([x.full_name for x in result])
    assert result == response

def test_range_from_note_with_key_included():
    note = Note('C3', key='Ab')
    end = Note('C3')

    sr = ScaleRange(end, length=2)
    sr = ScaleRange(note, length=2)
    assert sr.mode == 'ionian'
    assert sr.key == 'Ab'
    assert sr.end.full_name == 'Db3'
