import pytest
from ried import generate_interval

import csv

with open('test/test_get_parts_int.csv') as f:
    data_get_parts_int = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'integer,interval,octave,mod,direction',
        data_get_parts_int
        )
def test_get_parts_int(integer, interval, octave, mod, direction):
    response = generate_interval.get_parts_int(int(integer))
    assert response['interval'] == int(interval)
    assert response['octave'] == int(octave)
    assert response['mod'] == int(mod)
    assert response['direction'] == direction



with open('test/test_get_parts_string.csv') as f:
    data_get_parts_string = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'value,interval,octave,mod,direction',
        data_get_parts_string
        )
def test_get_parts_string(value, interval, octave, mod, direction):
    response = generate_interval.get_parts_string(value)
    assert response['interval'] == int(interval)
    assert response['octave'] == int(octave)
    assert response['mod'] == int(mod)
    assert response['direction'] == direction

with open('test/test_analyze_root.csv') as f:
    data_arrange_root = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'value,root,alter,octave',
        data_arrange_root
        )
def test_analyze_root(value, root, alter, octave):
    response = generate_interval.analyze_root(value)
    if alter == 'None':
        alter = None
    if octave == 'None':
        octave = None
    else:
        octave = int(octave)
    assert len(response) == 3
    assert response['root'] == root
    assert response['alter'] == int(alter)
    assert response['octave'] == octave


with open('test/test_get_major_scale_with_dots.csv') as f:
    data_get_major_scale = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'root,scale',
        data_get_major_scale
        )
def test_get_major_scale_with_dots(root, scale):
    root = generate_interval.analyze_root(root)
    response = generate_interval.get_major_scale(root)
    assert "".join(response) == scale



with open('test/test_get_major_scale_without_dots.csv') as f:
    data_get_major_scale_without_dots = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'root,scale',
        data_get_major_scale_without_dots
        )
def test_get_major_scale_without_dots(root, scale):
    root = generate_interval.analyze_root(root)
    response = generate_interval.get_major_scale(root, dots=False)
    assert "".join(response) == scale




with open('test/test_get_endpoint.csv') as f:
    data_get_endpoint = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'root,interval,endpoint',
        data_get_endpoint
        )
def test_get_endpoint(root, interval, endpoint):
    root = generate_interval.analyze_root(root)
    reference = generate_interval.get_major_scale(root, dots=False)
    try:
        interval = int(interval)
    except ValueError:
        pass
    rules = generate_interval.define_rules(interval)
    end = generate_interval.get_endpoint(type(interval), rules, reference)
    assert end == endpoint




with open('test/test_analyze_mode.csv') as f:
    data_analyze_mode = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'input1,name,number',
        data_analyze_mode
        )
def test_analyze_mode(input1, name, number):
    try:
        input1 = int(input1)
    except ValueError:
        pass
    response = generate_interval.analyze_mode(input1)
    assert response['modeName'] == name
    assert response['modeNumber'] == int(number)




with open('test/test_scale_from_list.csv') as f:
    data_scale_from_list = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'root,mode',
        data_scale_from_list
        )
def test_scale_from_list(root, mode):
    response = generate_interval.scale_from_list((root,mode))
    assert type(response) == dict
    assert all([x in ['root', 'mode'] for x in list(response.keys())])
    response = generate_interval.scale_from_list([root,mode])
    assert type(response) == dict
    assert all([x in ['root', 'mode'] for x in list(response.keys())])
    response = generate_interval.scale_from_list({'root': root, 'mode': mode})
    assert type(response) == dict
    assert all([x in ['root', 'mode'] for x in list(response.keys())])
    
    




with open('test/test_get_property_scale.csv') as f:
    data_get_property_scale = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'root,mode,scaleR,scaleM,roota,altera,modea,nummodea',
        data_get_property_scale
        )
def test_get_property_scale(root, mode, scaleR, scaleM, roota, altera, modea, nummodea):
    root = root != 'none' and root or None
    mode = mode != 'none' and mode or None
    scaleR = scaleR != 'none' and scaleR or None
    scaleM = scaleM != 'none' and scaleM or None
    scale = scaleR and scaleM and (scaleR, scaleM) or None

    if mode:
        response = generate_interval.get_property_scale(root=root, mode=mode, scale=scale)
    else:
        response = generate_interval.get_property_scale(root=root, scale=scale)
    assert response['root']['root'] == roota
    assert response['root']['alter'] == int(altera)
    assert response['mode']['modeName'] == modea
    assert response['mode']['modeNumber'] == int(nummodea)






with open('test/test_diatonic_endpoint.csv') as f:
    data_diatonic_endpoint = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'r_interval,r_octave,r_mod,r_direction,r1,r2,r3,r4,r5,r6,r7,s_r_root,s_r_alter,s_r_octave,s_m_name,s_m_number,result',
        data_diatonic_endpoint
        )
def test_diatonic_endpoint(r_interval,r_octave,r_mod,r_direction,r1,r2,r3,r4,r5,r6,r7,s_r_root,s_r_alter,s_r_octave,s_m_name,s_m_number,result):

    rules = {'interval': int(r_interval),\
            'octave': int(r_octave),\
            'mod': int(r_mod),\
            'direction':r_direction}

    reference = [r1,r2,r3,r4,r5,r6,r7]

    if s_r_octave == 'None':
        s_r_octave = None
    else:
        s_r_octave = int(s_r_octave)
        
    root = {'root': s_r_root,\
            'alter': int(s_r_alter),\
            'octave': s_r_octave}
    mode = {'modeName': s_m_name,\
            'modeNumber': int(s_m_number)}

    scale = {'root': root, 'mode': mode}

    response = generate_interval.diatonic_endpoint(rules, reference, scale)
    assert response == result






with open('test/test_fix_octave.csv') as f:
    data_fix_octave = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'start_point_root,start_point_octave,end,rules_octave,rules_direction,result',
        data_fix_octave
        )
def test_fix_octave(start_point_root, start_point_octave, end, rules_octave, rules_direction, result):

    rules = {'octave': int(rules_octave),\
            'direction':rules_direction}

    start_point = {'octave':int(start_point_octave),\
            'root':start_point_root}

    response = generate_interval.fix_octave(start_point, end, rules)
    assert response == result
    
