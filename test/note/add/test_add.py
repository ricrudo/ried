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

def test_add_with_specific_key():
    note = Note('C3', key='Ab')
    assert (note + 1).full_name == 'Db3'

def test_specific_case_1():
    note = Note('Eb4', key='C', mode='dorian')
    assert (note + '4p').full_name == 'Ab4'
