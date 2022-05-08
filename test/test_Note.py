import pytest

from ried.note.note_generator import Note

import csv

with open('test/test_Note_onlyName.csv') as f:
    noteOnlyName = [tuple(x) for x in csv.reader(f)]

@pytest.mark.parametrize(
        'inputNote,respOctave,respAlter,respNoteWAlter,respNote,respPitchIndex,respMidiNumber,respDuration,solfeo',
        noteOnlyName
        )
def test_NoteOnly(inputNote,respOctave,respAlter,respNoteWAlter,respNote,respPitchIndex,respMidiNumber,respDuration,solfeo):
    note = Note(inputNote)
    assert note.octave == respOctave
    assert note.alter == int(respAlter)
    assert note.name_without_alter == respNoteWAlter
    assert note.name == respNote
    assert note.pitch_index == int(respPitchIndex)
    assert note.midi_number == respMidiNumber
    assert note.duration == respDuration
    assert note.solfeo == solfeo



with open('test/test_Note_octave.csv') as f:
    noteOctave = [tuple(x) for x in csv.reader(f)]
@pytest.mark.parametrize(
        'inputNote,octave,respOctave,respAlter,respNoteWAlter,respNote,respPitchIndex,respMidiNumber,respDuration,solfeo',
        noteOctave
        )
def test_note_octave(inputNote,octave,respOctave,respAlter,respNoteWAlter,respNote,respPitchIndex,respMidiNumber,respDuration,solfeo):
    note = Note(inputNote, octave=int(octave))
    assert note.octave == int(respOctave)
    assert note.alter == int(respAlter)
    assert note.name_without_alter == respNoteWAlter
    assert note.name == respNote
    assert note.pitch_index == int(respPitchIndex)
    assert note.midi_number == int(respMidiNumber)
    assert note.duration == respDuration
    assert note.solfeo == solfeo


with open('test/test_Note_alter.csv') as f:
    noteAlter = [tuple(x) for x in csv.reader(f)]
@pytest.mark.parametrize(
        'inputNote,alter,respOctave,respAlter,respNoteWAlter,respNote,respPitchIndex,respMidiNumber,respDuration,solfeo',
        noteAlter
        )
def test_note_alter(inputNote,alter,respOctave,respAlter,respNoteWAlter,respNote,respPitchIndex,respMidiNumber,respDuration,solfeo):
    note = Note(inputNote, alter=int(alter))
    assert note.octave == respOctave
    assert note.alter == int(respAlter)
    assert note.name_without_alter == respNoteWAlter
    assert note.name == respNote
    assert note.pitch_index == int(respPitchIndex)
    assert note.midi_number == respMidiNumber
    assert note.duration == respDuration
    assert note.solfeo == solfeo

with open('test/test_NoteWithOctave.csv') as f:
    NoteWithOctave = [tuple(x) for x in csv.reader(f)]
@pytest.mark.parametrize(
        'inputNote,respOctave,respAlter,respNoteWAlter,respNote,respPitchIndex,respMidiNumber,respDuration,solfeo',
        NoteWithOctave
        )
def test_NoteWithOctave(inputNote,respOctave,respAlter,respNoteWAlter,respNote,respPitchIndex,respMidiNumber,respDuration,solfeo):
    note = Note(inputNote)
    assert note.octave == int(respOctave)
    assert note.alter == int(respAlter)
    assert note.name_without_alter == respNoteWAlter
    assert note.name == respNote
    assert note.pitch_index == int(respPitchIndex)
    assert note.midi_number == int(respMidiNumber)
    assert note.duration == respDuration
    assert note.solfeo == solfeo

