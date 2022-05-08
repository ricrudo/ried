import pytest

from ried.chord.chord_generator import Chord

import csv

with open('test/chord/notes/third/origen.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'inputNote,response3,response4,response5,response6,response7,response9,response11,response13',
        origen#[30000:]
        )
def test_add(inputNote, response3, response4, response5, response6, response7, response9, response11, response13):
    NewChord = Chord(inputNote)
    if NewChord.third:
        assert NewChord.third.name == response3
    else:
        assert NewChord.third == eval(response3)

    if NewChord.fourth:
        assert NewChord.fourth.name == response4
    else:
        assert NewChord.fourth == eval(response4)

    if NewChord.fifth:
        if isinstance(NewChord.fifth, list):
            if len(NewChord.fifth) == 1:
                assert NewChord.fifth[0].name == response5
            elif len(NewChord.fifth) == 2:
                assert 'b5' in (NewChord.fifth[0].name, NewChord.fifth[1].name)
                assert '#5' in (NewChord.fifth[0].name, NewChord.fifth[1].name)
        else:
            assert NewChord.fifth.name == response5
    else:
        assert NewChord.fifth == eval(response5)

    if NewChord.sixth:
        assert NewChord.sixth.name == response6
    else:
        assert NewChord.sixth == eval(response6)

    if NewChord.seventh:
        assert NewChord.seventh.name == response7
    else:
        assert NewChord.seventh == eval(response7)


    if NewChord.ninth:
        ninths = [x.name for x in NewChord.ninth]
        if len(ninths) == 1:
            assert ninths[0] == response9
        else:
            response9 = response9.split('y')
            assert ninths[0] in response9
            assert ninths[1] in response9
    else:
        assert NewChord.ninth == eval(response9)

    if NewChord.eleventh:
        assert NewChord.eleventh.name == response11
    else:
        assert NewChord.eleventh == eval(response11)

    if NewChord.thirteenth:
        if isinstance(NewChord.thirteenth, list):
            thirteenths = [x.name for x in NewChord.thirteenth]
            if len(thirteenths) == 2:
                response13 = response13.split('y')
                assert thirteenths[0] in response13
                assert thirteenths[1] in response13
            elif len(thirteenths) == 1:
                assert thirteenths[0] == response13
        else:
            assert NewChord.thirteenth.name == response13
    else:
        assert NewChord.thirteenth == eval(response13)

