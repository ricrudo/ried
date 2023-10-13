import pytest

from ried.scale.scale_generator import Scale

def test_scale_generator():
    sc = Scale()
    assert sc.generate_scale('Ab', mode='harmonic_minor') == ['Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'G']
