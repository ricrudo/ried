import pytest
from ried.notation.notation_analyzer import Chord
import csv

def test_extract_data_from_name():
    ca = Chord()
    assert ca._extract_data_from_name({'input':'Gm7'}) == ['G', 'm', '7']
    assert ca._extract_data_from_name({'input':'Gm13'}) == ['G', 'm', '7', '13']
    assert ca._extract_data_from_name({'input':'Gmaj7'}) == ['G', 'maj7']
    assert ca._extract_data_from_name({'input':'Gm(maj7)'}) == ['G', 'm', 'maj7']
    assert ca._extract_data_from_name({'input':'Gm7(b5)'}) == ['G', 'm', '7', 'b5']
    assert ca._extract_data_from_name({'input':'Gbb7sus4'}) == ['G', 'bb', '7', 'sus4']
    assert ca._extract_data_from_name({'input':'G7sus4addb3'}) == ['G', '7', 'sus4', 'addb3']
    assert ca._extract_data_from_name({'input':'G7_sus4addb3'}) == ['G', '7', 'sus4', 'addb3']

def test_isolatePartsName_chord():
    ca = Chord()
    assert ca._isolatePartsName({'input':'Gmaj7'}) == ('G', ['maj7'], None)
    assert ca._isolatePartsName({'input':'Gbb7sus4'}) == ('G', ['7', 'sus4'], 'bb')

def test_get_alter_from_string():
    ca = Chord()
    predata = {'alter':None}
    ca._get_alter_from_string(predata, None)
    assert predata['alter'] == 0 
    predata = {'alter':None}
    ca._get_alter_from_string(predata, 'bb')
    assert predata['alter'] == -2 
    predata = {'alter':None}
    ca._get_alter_from_string(predata, '###')
    assert predata['alter'] == 3

def test_noteWithoutAlter():
    ca = Chord()
    ca._noteWithoutAlter({'input':'G', 'alter':None})

def test_check_sufix():
    ca = Chord()

    predata = {
        'input':'Gmaj7',
        'alter': 0,
        'sufix': ['maj7'],
        'name_without_alter': 'G'
    }
    assert ca._check_sufix(predata) is None

    predata = {
        'input':'G7sus4addb3',
        'alter': 0,
        'sufix': ['7', 'sus4', 'addb3'],
        'name_without_alter': 'G'
    }
    assert ca._check_sufix(predata) is None

    predata = {
        'input':'Gbb7sus4addb3',
        'alter': -2,
        'sufix': ['7', 'sus4', 'addb3'],
        'name_without_alter': 'G'
    }
    assert ca._check_sufix(predata) is None
    with pytest.raises(ValueError):
        predata = {
            'input':'Gbb7_sus4addb3',
            'alter': -2,
            'sufix': ['7', 'sus4', 'addb3'],
            'name_without_alter': 'G'
        }
        assert ca._check_sufix(predata) is None

def test_chord_sufix():
    ca = Chord()
    assert ca._chord_sufix({'sufix':None}) is None
    
    predata = {
        'input':'G7susaddb3',
        'alter': 0,
        'sufix': ['7', 'sus', 'addb3'],
        'name_without_alter': 'G'
    }
    ca._chord_sufix(predata)
    expected_suffix = {
        'third': 'addb3',
        'fourth': 'sus4',
        'fifth': None,
        'sixth': None,
        'seventh': '7',
        'ninth': None, 
        'eleventh': None,
        'thirteenth': None
    }
    for key, value in expected_suffix.items():
        assert predata['sufix'][key] == value

    predata = {
        'input':'G7bbsus4',
        'alter': -2,
        'sufix': ['7', 'sus4'],
        'name_without_alter': 'G'
    }
    ca._chord_sufix(predata)
    expected_suffix = {
        'third': None,
        'fourth': 'sus4',
        'fifth': None,
        'sixth': None,
        'seventh': '7',
        'ninth': None, 
        'eleventh': None,
        'thirteenth': None
    }
    for key, value in expected_suffix.items():
        assert predata['sufix'][key] == value

def test_generator_chord():
    ca = Chord()
    resultado =  ca.generator_chord('Gmaj7', None, None)
    assert resultado == {
        'input': 'Gmaj7', 
        'sufix': {
            'third': None,
            'fourth': None,
            'fifth': None,
            'sixth': None, 
            'seventh': 'maj7', 
            'ninth': None,
            'eleventh': None, 
            'thirteenth': None
        },
        'alter': 0,
        'name_without_alter': 'G',
        'name': 'G'
    }


    resultado =  ca.generator_chord('Gm7', None, None)
    assert resultado == {
        'input': 'Gm7', 
        'sufix': {
            'third': 'm',
            'fourth': None,
            'fifth': None,
            'sixth': None, 
            'seventh': '7', 
            'ninth': None,
            'eleventh': None, 
            'thirteenth': None
        },
        'alter': 0,
        'name_without_alter': 'G',
        'name': 'G'
    }


    resultado =  ca.generator_chord('Gm(maj7)', None, None)
    assert resultado == {
        'input': 'Gm(maj7)', 
        'sufix': {
            'third': 'm',
            'fourth': None,
            'fifth': None,
            'sixth': None, 
            'seventh': 'maj7', 
            'ninth': None,
            'eleventh': None, 
            'thirteenth': None
        },
        'alter': 0,
        'name_without_alter': 'G',
        'name': 'G'
    }

    resultado =  ca.generator_chord('Gbb7sus4addb3', None, None)
    assert resultado == {
        'input': 'Gbb7sus4addb3', 
        'sufix': {
            'third': 'addb3',
            'fourth': 'sus4',
            'fifth': None,
            'sixth': None, 
            'seventh': '7', 
            'ninth': None,
            'eleventh': None, 
            'thirteenth': None
        },
        'alter': -2,
        'name_without_alter': 'G',
        'name': 'Gbb'
    }
