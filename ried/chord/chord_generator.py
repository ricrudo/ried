from ried.notation import notation_analyzer
from ried.note.note_generator import Note

class Chord:

    nttnAnlzr = notation_analyzer.Chord()
    
    def __init__(self, name, sufix='none', alter='none', duration='none', key=None):
        predata = self.nttnAnlzr.generator_chord(name, sufix, alter)
        self.root = Note(predata['name'])
        self._set_types(predata)
        self.category = self._set_chord_category()
        self._set_notes()

    def _set_types(self, predata):
        self.type_third = predata['sufix']['third'] or predata['sufix']['fourth'] or 'major'
        self.type_fourth = predata['sufix']['fourth'] or 'no specified'
        self.type_fifth = predata['sufix']['fifth'] or 'perfect'
        self.type_sixth = predata['sufix']['sixth'] or 'no specified'
        self.type_seventh = predata['sufix']['seventh'] or 'no specified'
        self.type_ninth = predata['sufix']['ninth'] or 'no specified'
        self.type_eleventh = predata['sufix']['eleventh'] or 'no specified'
        self.type_thirteenth = predata['sufix']['thirteenth'] or 'no specified'

    def _set_chord_category(self):
        if self.type_third == 'major':
            if not self.type_seventh:
                if any(['add' in x for x in self.type_ninth]):
                    if self.type_fifth == ['#5']: return 'augmented add2'
                    return 'major add2'
                return 'major'
            if self.type_seventh == '7': return 'dominant'
            if self.type_seventh == 'maj7': return 'major seventh'
        if self.type_third == 'minor':
            if self.type_fifth == 'perfect':
                if not self.type_seventh: 
                    if any(['add' in x for x in self.type_ninth]): return 'minor add2'
                    return 'minor'
                if self.type_seventh == '7':
                    if self.type_sixth == 'b6': return 'minor seventh b6'
                    return 'minor seventh'
                if self.type_seventh == 'maj7': return 'minor major seventh'
            if self.type_fifth == ['b5']:
                if not self.type_seventh: 'diminished'
                if self.type_seventh == 'maj7': return 'diminished major seventh'
                if self.type_seventh == '7': return 'half diminished'
                if self.type_seventh == 'º7': return 'whole diminished'
        if any(['sus4' in self.type_third, 'sus4' in self.type_fourth]):
            if not self.type_seventh: return 'suspended'
            if self.type_seventh == '7': return 'suspended dominant'
            if self.type_seventh == 'maj7': return 'suspended maj7'
        #self.name_without_alter = predata['name_without_alter']
        #self.full_name = predata['full_name']
        #self.alter = predata['alter']
        #self.alter_str = predata['alter_str']
        #self.pitch_index_without_alter = predata['pitch_index_without_alter'] 
        #self.pitch_index = predata['pitch_index']
        #self.solfeo_without_alter = predata['solfeo_without_alter'].upper()
        #self.solfeo = predata['solfeo'].upper()
        #self.duration = self._duration(duration)
        #self.key = self._setKey(key)


    def _set_notes(self):
        self.third = self._set_third()
        self.fourth = self._set_fourth()
        self.fifth = self._set_fifth()
        self.sixth = self._set_sixth()
        self.seventh = self._set_seventh()
        self.ninth = self._set_ninth()
        self.eleventh = self._set_eleventh()
        self.thirteenth = self._set_thirteenth()
        self.second = self.ninth


    def _set_third(self):
        if self.type_third in ['major', 'add3']: return self.root + '3M'
        elif self.type_third in ['minor', 'addb3']: return self.root + '3m'

    def _set_fourth(self):
        if '4' in self.type_fourth:
            if not self.third:
                self.third = self.root + '4p'
            return self.root + '4p'

    def _set_fifth(self):
        if self.type_fifth == 'perfect': return self.root + '5p'
        if isinstance(self.type_fifth, list):
            fifth = []
            for x in self.type_fifth:
                if x == 'b5': fifth.append(self.root + '5d')
                elif x == '#5': fifth.append(self.root + '5a')
                elif x == 'omit5': fifth = None
            return fifth

    def _set_sixth(self):
        if self.type_sixth == 'b6': return self.root + '6m'
        if self.type_sixth == '6': return self.root + '6M'

    def _set_seventh(self):
        if self.type_seventh == 'maj7': return self.root + '7M'
        if self.type_seventh == '7': return self.root + '7m'
        if self.type_seventh == 'º7': return self.root + '7d'

    def _set_ninth(self):
        if isinstance(self.type_ninth, list):
            ninth = []
            for x in self.type_ninth:
                if x in ('9', 'add9', 'add2'): ninth.append(self.root + '2M')
                if x in ('b9', 'b2', 'addb2', 'addb9'): ninth.append(self.root + '2m')
                if x in ('#9', '#2', 'add#2', 'add#9'): ninth.append(self.root + '2a')
            return ninth

    def _set_eleventh(self):
        if self.type_eleventh == '11': return self.root + '4p'
        if self.type_eleventh == '#11': return self.root + '4a'

    def _set_thirteenth(self):
        if isinstance(self.type_thirteenth, list):
            thirteenth = []
            for x in self.type_thirteenth:
                if x == 'b13': thirteenth.append(self.root + '6m')
                elif x == '13': thirteenth.append(self.root + '6M')
                elif x == '#13': thirteenth.append(self.root + '6a')
            return thirteenth

