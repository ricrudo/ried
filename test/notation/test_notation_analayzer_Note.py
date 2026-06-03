import pytest
from ried.notation.notation_analyzer import Note

def test_extract_data_from_name():
    na = Note()
    assert na._extract_data_from_name({'input':'C8'}) == ['C', '8']
    assert na._extract_data_from_name({'input':'Db8'}) == ['D', 'b', '8']
    assert na._extract_data_from_name({'input':'Dbb-2'}) == ['D', 'bb', '-2']
    assert na._extract_data_from_name({'input':'D##-2'}) == ['D', '##', '-2']

def test_isolatePartsName():
    na = Note()
    assert na._isolatePartsName({'input':'C8'}) == ('C', '8', None)
    assert na._isolatePartsName({'input':'Db8'}) == ('D', '8', 'b')
    assert na._isolatePartsName({'input':'Dbb-2'}) == ('D', '-2', 'bb')
    assert na._isolatePartsName({'input':'D##-2'}) == ('D', '-2', '##')

def test_noteWithoutAlter():
    na = Note()

    predata = {'input':'C8', 'octave':None, 'alter':None}
    na._noteWithoutAlter(predata)
    predata == {
        'input': 'C8',
        'octave': 8,
        'alter': 0,
        'name_without_alter': 'C'
    }

    predata = {'input':'Db8', 'octave':None, 'alter':None}
    na._noteWithoutAlter(predata)
    predata == {
        'input': 'Db8',
        'octave': 8,
        'alter': -1,
        'name_without_alter': 'D'
    }

    predata = {'input':'Dbb-2', 'octave':None, 'alter':None}
    na._noteWithoutAlter(predata)
    predata == {
        'input': 'Dbb-2',
        'octave': -2,
        'alter': -2,
        'name_without_alter': 'D'
    }

    predata = {'input':'D##-2', 'octave':None, 'alter':None}
    na._noteWithoutAlter(predata)
    predata == {
        'input': 'D##-2',
        'octave': -2,
        'alter': 2,
        'name_without_alter': 'D'
    }

def test_generator_note():
    na = Note()


    assert na.generator_note('C8', None, None) == {
        'input': 'C8',
        'octave': 8,
        'alter': 0, 
        'name_without_alter': 'C',
        'name': 'C', 
        'alter_str': '',
        'full_name': 'C8',
        'pitch_index_without_alter': 0,
        'pitch_index': 0,
        'midi_number': 108, 
        'solfeo_without_alter': 'do',
        'solfeo': 'do'
    }

    assert na.generator_note('Db8', None, None) == {
        'input': 'Db8',
        'octave': 8,
        'alter': -1, 
        'name_without_alter': 'D',
        'name': 'Db', 
        'alter_str': 'b',
        'full_name': 'Db8',
        'pitch_index_without_alter': 2,
        'pitch_index': 1,
        'midi_number': 109, 
        'solfeo_without_alter': 're',
        'solfeo': 'reb'
    }

    assert na.generator_note('Dbb-2', None, None) == {
        'input': 'Dbb-2',
        'octave': -2,
        'alter': -2, 
        'name_without_alter': 'D',
        'name': 'Dbb', 
        'alter_str': 'bb',
        'full_name': 'Dbb-2',
        'pitch_index_without_alter': 2,
        'pitch_index': 0,
        'midi_number': -12, 
        'solfeo_without_alter': 're',
        'solfeo': 'rebb'
    }

    assert na.generator_note('D##-2', None, None) == {
        'input': 'D##-2',
        'octave': -2,
        'alter': 2, 
        'name_without_alter': 'D',
        'name': 'D##', 
        'alter_str': '##',
        'full_name': 'D##-2',
        'pitch_index_without_alter': 2,
        'pitch_index': 4,
        'midi_number': -8, 
        'solfeo_without_alter': 're',
        'solfeo': 're##'
    }
