import pytest

from ried.bar.bar_generator import Bar
from ried.beat.beat_generator import Beat
from ried.note.note_generator import Note, Silence

import csv
from itertools import combinations
from random import choice

with open('test/bar/origen.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'measure,num,den,grouping,indicator',
        origen
        )
def test_bar1(measure, num, den, grouping, indicator):
    '''
    prueba ingresando solo el measure (i.e. '4-4')
    '''
    bar = Bar(measure)
    assert bar.num == int(num)
    assert bar.den == int(den)
    assert bar.subdivision.beat_grouping == tuple([int(x) for x in grouping if x.isdigit()])
    assert bar.subdivision.figure_subidivision == int(indicator)


###################################################


with open('test/bar/origen2.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'measure,num,den,grouping,indicator',
        origen
        )
def test_bar2(measure, num, den, grouping, indicator):
    '''
    prueba que al ingresar el measure (i.e. '4-4') y la subdivision
    '''
    subdi = tuple([int(x) for x in grouping if x.isdigit()])
    bar = Bar(measure, subdivision=subdi)
    assert bar.num == int(num)
    assert bar.den == int(den)
    assert bar.subdivision.beat_grouping == subdi
    assert bar.subdivision.figure_subidivision == int(indicator)


###################################################


with open('test/bar/origen3.csv') as f:
    origen = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'measure,distribution,num,den,grouping,indicator',
        origen
        )
def test_bar3(measure, distribution, num, den, grouping, indicator):
    '''
    prueba que al ingresar el measure (i.e. '4-4') y la subdivision
    '''
    distribution = tuple([tuple([int(x) for x in pulso.split('.')]) for pulso in distribution.split('x')])
    subdi = tuple([int(x) for x in grouping if x.isdigit()])
    bar = Bar(measure, subdivision=subdi, distribution=distribution)
    assert bar.num == int(num)
    assert bar.den == int(den)
    assert bar.subdivision.beat_grouping == subdi
    assert bar.subdivision.figure_subidivision == int(indicator)



##################################


def test_bar4():
    posibilidadesBinario = {'pulsos':[[1],
                                      [-1]],
                            'primeraSub':[[.5,.5],
                                          [0.5,-.5],
                                          [-.5,.5]],
                            'segundaSub':[[.25,.25,.25,.25],
                                          [.25,.5,.25],
                                          [.25,-.5,.25],
                                          [.5,.25,.25],
                                          [.25,.25,.5],
                                          [-.5,.25,.25],
                                          [.25,.25,-.5],
                                          [.75,.25]]
                           }

    joiner = {(1,):None,\
            (-1,):None, \
            (0.5,0.5): {0: {'join8ths': 'start'}, 1: {'join8ths': 'end'}}, \
            (0.5,-0.5):None, \
            (-.5,0.5):None, \
            (0.25,0.25,0.25,0.25):{0:{'join8ths':'start', 'join16ths':'start'},\
                    1:{'join8ths':'middle', 'join16ths':'middle'}, \
                    2:{'join8ths':'middle', 'join16ths':'middle'}, \
                    3:{'join8ths':'end', 'join16ths':'end'}}, \
            (0.25,-0.5,0.25):{0:{'join8ths':'start', 'join16ths':'unique_start'}, \
                    2:{'join8ths':'end', 'join16ths':'unique_end'}}, \
            (0.25,0.5,0.25):{0:{'join8ths':'start', 'join16ths':'unique_start'}, \
                    1:{'join8ths':'middle'}, \
                    2:{'join8ths':'end', 'join16ths':'unique_end'}}, \
            (0.5,0.25,0.25):{0:{'join8ths':'start'}, \
                    1:{'join8ths':'middle', 'join16ths':'start'}, \
                    2:{'join8ths':'end', 'join16ths':'end'}}, \
            (0.25,0.25,0.5):{0:{'join8ths':'start', 'join16ths':'start'}, \
                    1:{'join8ths':'middle', 'join16ths':'end'}, \
                    2:{'join8ths':'end'}}, \
            (-0.5,0.25,0.25):{1:{'join8ths':'start', 'join16ths':'start'}, \
                    2:{'join8ths':'end', 'join16ths':'end'}}, \
            (0.25,0.25,-0.5):{0:{'join8ths':'start', 'join16ths':'start'}, \
                    1:{'join8ths':'end', 'join16ths':'end'}}, \
            (.75,.25):{0:{'join8ths':'start'}, \
                    1:{'join8ths':'end', 'join16ths':'unique_end'}}
            }

    silence_in_between = ((0.25,-0.5,0.25),)

    allBinarios = [x for values in posibilidadesBinario.values() for x in values] 
    notesAv = ['B3', 'B4', 'B5']

    for pulsos in range(2,5):
        combs = combinations(allBinarios, pulsos)
        resultados = []
        for i, comb in enumerate(combs):
            content = [choice(notesAv) for beat in comb for sound in beat if sound > 0]
            contenido = Bar(f'{pulsos}-4', subdivision='distribution', content=content, distribution=comb)
            assert len(contenido.content) == pulsos
            for pulso in range(pulsos):
                assert len(contenido.content[pulso].content) == len(comb[pulso])
                for index, note in enumerate(contenido.content[pulso].content):
                    assert abs(comb[pulso][index]) == note.duration
                    if comb[pulso][index] > 0:
                        if note.full_name == 'B3':
                            assert note.aditional_line == -1
                        elif note.full_name == 'B5':
                            assert note.aditional_line == 1
                        else:
                            assert note.aditional_line == None
                if joiner[tuple(comb[pulso])]:
                    for index in joiner[tuple(comb[pulso])].keys():
                        for key, value in joiner[tuple(comb[pulso])][index].items():
                            assert value == contenido.content[pulso].content[index].joiner[key]
                if tuple(comb[pulso]) in silence_in_between:
                    assert contenido.content[pulso].silence_in_between == True
                else:
                    assert contenido.content[pulso].silence_in_between == False


def test_bar5():

    posibilidadesTernario = {'pulsos': [[1.5],
                                       [-1.5]],
                             'primeraSub':[[.5,.5,.5],
                                           [-.5,.5,.5],
                                           [.5,-.5,.5],
                                           [.5,.5,-.5],
                                           [1,.5],
                                           [-1,.5],
                                           [1,-.5]],
                             'segundaSub':[[.25,.25,.25,.25,.25,.25],
                                           [.5,.25,.25,.5],
                                           [.25,.25,.5,.5],
                                           [.5,.5,.25,.25],
                                           [.25,.25,.25,.25,.5],
                                           [.5,.25,.25,.25,.25],
                                           [.25,.25,.5,.25,.25]]
                            }

    joiner = {(1.5,):None, (-1.5,):None, \
            (0.5,0.5,0.5): {0: {'join8ths': 'start'}, \
                    1: {'join8ths': 'middle'}, \
                    2: {'join8ths': 'end'}}, \
            (-0.5,0.5,0.5):{1: {'join8ths': 'start'}, \
                    2: {'join8ths': 'end'}}, \
            (0.5,-0.5,0.5):{0: {'join8ths': 'start'}, \
                    2: {'join8ths': 'end'}}, \
            (0.5,0.5,-0.5):{0: {'join8ths': 'start'}, \
                    1: {'join8ths': 'end'}}, \
            (1,0.5):None, (-1,0.5):None, (1,-0.5):None, \
            (0.25,0.25,0.25,0.25,0.25,0.25):{0:{'join8ths':'start', 'join16ths':'start'},\
                    1:{'join8ths':'middle', 'join16ths':'middle'}, \
                    2:{'join8ths':'middle', 'join16ths':'middle'}, \
                    3:{'join8ths':'middle', 'join16ths':'middle'}, \
                    4:{'join8ths':'middle', 'join16ths':'middle'}, \
                    5:{'join8ths':'end', 'join16ths':'end'}}, \
            (0.5,0.25,0.25,0.5):{0:{'join8ths':'start'},\
                    1:{'join8ths':'middle', 'join16ths':'start'}, \
                    2:{'join8ths':'middle', 'join16ths':'end'}, \
                    3:{'join8ths':'end'}}, \
            (0.25,0.25,0.5,0.5):{0:{'join8ths':'start', 'join16ths':'start'},\
                    1:{'join8ths':'middle', 'join16ths':'end'}, \
                    2:{'join8ths':'middle'}, \
                    3:{'join8ths':'end'}}, \
            (0.5,0.5,0.25,0.25):{0:{'join8ths':'start'},\
                    1:{'join8ths':'middle'}, \
                    2:{'join8ths':'middle', 'join16ths':'start'}, \
                    3:{'join8ths':'end', 'join16ths':'end'}}, \
            (0.25,0.25,0.25,0.25,0.5):{0:{'join8ths':'start', 'join16ths':'start'},\
                    1:{'join8ths':'middle', 'join16ths':'middle'}, \
                    2:{'join8ths':'middle', 'join16ths':'middle'}, \
                    3:{'join8ths':'middle', 'join16ths':'end'}, \
                    4:{'join8ths':'end'}}, \
            (0.5,0.25,0.25,0.25,0.25):{0:{'join8ths':'start'},\
                    1:{'join8ths':'middle', 'join16ths':'start'}, \
                    2:{'join8ths':'middle', 'join16ths':'middle'}, \
                    3:{'join8ths':'middle', 'join16ths':'middle'}, \
                    4:{'join8ths':'end', 'join16ths':'end'}}, \
            (0.25,0.25,0.5,0.25,0.25):{0:{'join8ths':'start', 'join16ths':'start'},\
                    1:{'join8ths':'middle', 'join16ths':'end'}, \
                    2:{'join8ths':'middle'}, \
                    3:{'join8ths':'middle', 'join16ths':'start'}, \
                    4:{'join8ths':'end', 'join16ths':'end'}}, \
            }

    allTernarios = [x for values in posibilidadesTernario.values() for x in values] 
    notesAv = ['B3', 'B4', 'B5']

    for pulsos in [2,3]:
        combs = combinations(allTernarios, pulsos)
        resultados = []
        for i, comb in enumerate(combs):
            content = [choice(notesAv) for beat in comb for sound in beat if sound > 0]
            try:
                contenido = Bar(f'{pulsos*3}-8', subdivision='distribution', content=content, distribution=comb)
                assert len(contenido.content) == pulsos
                for pulso in range(pulsos):
                    assert len(contenido.content[pulso].content) == len(comb[pulso])
                    for index, note in enumerate(contenido.content[pulso].content):
                        assert abs(comb[pulso][index]) == note.duration
                        if comb[pulso][index] > 0:
                            if note.full_name == 'B3':
                                assert note.aditional_line == -1
                            elif note.full_name == 'B5':
                                assert note.aditional_line == 1
                            else:
                                assert note.aditional_line == None
                    if joiner[tuple(comb[pulso])]:
                        for index in joiner[tuple(comb[pulso])].keys():
                            for key, value in joiner[tuple(comb[pulso])][index].items():
                                assert value == contenido.content[pulso].content[index].joiner[key]
            except:
                breakpoint()



##############################


def test_bar_6():
    compas = Bar('2-4', content=['A3', 'B4', 'C5'], subdivision='distribution', distribution=[[-1], [0.25, 0.5, 0.25]])
    assert compas.content[1].beam_direction == 'up'
    compas = Bar('2-4', content=['A4', 'B4', 'E5'], subdivision='distribution', distribution=[[-1], [0.25, 0.5, 0.25]])
    assert compas.content[1].beam_direction == 'down'
    compas = Bar('2-4', content=['F4', 'B4', 'E5'], subdivision='distribution', distribution=[[-1], [0.25, 0.5, 0.25]])
    assert compas.content[1].beam_direction == 'up'
    compas = Bar('2-4', content=['F4', 'B4', 'A5'], subdivision='distribution', distribution=[[-1], [0.25, 0.5, 0.25]])
    assert compas.content[1].beam_direction == 'down'
    compas = Bar('2-4', content=['F4', 'E5'], subdivision='distribution', distribution=[[-1], [0.25, -0.5, 0.25]])
    assert compas.content[1].beam_direction == 'up'
    compas = Bar('2-4', content=['E4', 'E5'], subdivision='distribution', distribution=[[-1], [0.25, -0.5, 0.25]])
    assert compas.content[1].beam_direction == 'up'
    compas = Bar('2-4', content=['G4', 'E5'], subdivision='distribution', distribution=[[-1], [0.25, -0.5, 0.25]])
    assert compas.content[1].beam_direction == 'down'
