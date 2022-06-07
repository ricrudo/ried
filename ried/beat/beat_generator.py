from ried.note.note_generator import Note, Silence
from ried.chord.chord_generator import Chord

import copy
from typing import Union

class Beat:

    def __init__(self, pattern, content=None, bar_position=None, clef=None, centralLine=None, bar_subdivision=None):
        self.clef = clef
        self.centralLine = centralLine
        self.bar_subdivision = bar_subdivision
        self.bar_position = bar_position
        self.pattern = self._check_pattern(pattern)
        self.silence_in_between = False
        self.content = self.pairing_content_pattern(content)
        self._set_joiners()
        self.beam_direction = self._set_beam_direction()

    def __repr__(self):
        if self.content:
            return f'Beat({self.content})'

    def _check_pattern(self, pattern):
        if pattern:
            try:
                if isinstance(pattern, (list, tuple)):
                    return [float(x) for x in pattern]
                elif isinstance(pattern, str):
                    sep = {x for x in pattern if x in ',-'}
                    if sep:
                        return [float(x) for x in pattern.split(list(sep)[0])]
                    else:
                        return [float(pattern)]
                else:
                    return [float(pattern)]
                    raise ValueError()
            except ValueError:
                raise ValueError(f'{pattern} is not a valid pattern to create a beat.')
   
    def pairing_content_pattern(self, content):
        if content or all([x < 0 for x in self.pattern]):
            if content:
                content = self._check_content(content)
            content = self._pairing(content)
            return content
        return

    def _check_content(self, content):
        if not isinstance(content, list):
            if isinstance(content, tuple):
                content = list(content)
            else:
                content = [content]
        if len([x for x in self.pattern if x > 0]) == len(content):
            for i, first in enumerate(content):
                for other in range(i+1, len(content)):
                    if content[other] is first:
                        content[other] = copy.deepcopy(content[other])
            return content
        return IndexError(f'The amount in "content" must be equal to the amout of positive values un "pattern"')

    def _pairing(self, content):
        for i, duration in enumerate(self.pattern):
            if duration > 0:
                if not isinstance(content[i], (Note, Chord)):
                    if isinstance(content[i], str):
                        content[i] = Note(content[i], duration=duration, centralLine=self.centralLine)
                    elif isinstance(content[i], (list, tuple)):
                        content[i] = Chord(content=content[i], duration=duration, centralLine=self.centralLine)
                    else:
                        raise ValueError(f'{content[i]} in not valid to create a Note() or Chord()')
                else:
                    content[i].set_duration(duration)
                    content[i].set_line_pos(self.centralLine)
            else:
                content.insert(i, Silence(abs(duration)))
        return content

    def _set_joiners(self):
        if not self.content or len(self.pattern) == 1:
            return
        joiners = self._mk_joiners_by_figure()
        if len(joiners['join8ths']) < 2:
            return
        for key, value in joiners.items():
            if key in ('noJoin', 'silence'):
                continue
            if not value:
                continue
            response = self._define_groups(value, joiners['silence'][key])
            if key != 'join8ths':
                response = self._unique_joiner(response)
            response = self._clean_joiner(response, key)
            self._joiners_to_notes(key, response)
        self._check_silence_between()
        del joiners

    def _mk_joiners_by_figure(self):
        joiners = {}
        joiners['noJoin'] =  [i for i, x in enumerate(self.pattern) if x >= 1]
        joiners['join8ths'] = [i for i, x in enumerate(self.pattern) if 1 > x > 0]
        joiners['join16ths'] = [i for i, x in enumerate(self.pattern) if 0.5 > x > 0]
        joiners['join32ths'] = [i for i, x in enumerate(self.pattern) if 0.25 > x > 0]
        joiners['join64ths'] = [i for i, x in enumerate(self.pattern) if 0.125 > x > 0]
        joiners['join128ths'] = [i for i, x in enumerate(self.pattern) if 0.0625 > x > 0]
        joiners['silence'] = self._silence_arranged()

        return joiners

    def _silence_arranged(self):
        silences = {}
        silences['noJoin'] =  [i for i, x in enumerate(self.pattern) if x <= -1]
        silences['join8ths'] = [i for i, x in enumerate(self.pattern) if -0.5 >= x > -1]
        silences['join16ths'] = [i for i, x in enumerate(self.pattern) if -0.25 >= x > -0.5]
        silences['join32ths'] = [i for i, x in enumerate(self.pattern) if -0.125 >= x > -0.25]
        silences['join64ths'] = [i for i, x in enumerate(self.pattern) if -0.0625 >= x > -0.125]
        silences['join128ths'] = [i for i, x in enumerate(self.pattern) if 0 > x > -0.0625]
        return silences

    def _define_groups(self, value, silences):
        if all(list(map(lambda x: x-1 == value[value.index(x) - 1], value[1:]))):# or not silences:
            response = {'start':[value[0]]}
            if len(value) > 1:
                response['middle'] = [[x for x in range(value[1], value[-1])]]
            else:
                response['middle'] = [[]]
            response['end'] =[value[-1]]
        else:
            groups = [[value[0]]]
            index = value[0] + 1
            while index <= value[-1]:
                if not index in value:# and index in silences:
                    if groups[-1]:
                        groups[-1].append(index-1)
                        groups.append([])
                else:
                    if not groups[-1]:
                        groups[-1].append(index)
                index += 1
            groups[-1].append(value[-1])
            for i, val in enumerate(value[1:-1]):
                if not val - 1 == value[i]:
                    groups[-1].append(value[i])
                    groups.append([val])
            groups[-1].append(value[-1])
            response = {}
            response['start'] = {x[0] for x in groups}
            response['middle'] =[[j for j in range(x[0], x[1]) if j not in response['start'] and j not in silences] for x in groups]
            response['end'] = {x[1] for x in groups}
            del groups
        return response

    def _joiners_to_notes(self, key, response):
        if 'unique' in response:
            for place, indexList in response['unique'].items():
                if indexList:
                    for index in indexList:
                        if not hasattr(self.content[index], 'joiner'):
                            self.content[index].joiner = {}
                        self.content[index].joiner[key] = place
        for starter in response['start']:
            if not hasattr(self.content[starter], 'joiner'):
                self.content[starter].joiner = {}
            self.content[starter].joiner[key] = 'start'
        for grupos in response['middle']:
            for index in grupos:
                if not hasattr(self.content[index], 'joiner'):
                    self.content[index].joiner = {}
                self.content[index].joiner[key] = 'middle'
        for ender in response['end']:
            if not hasattr(self.content[ender], 'joiner'):
                self.content[ender].joiner = {}
            self.content[ender].joiner[key] = 'end'

    def _unique_joiner(self, response):
        if all([x in response for x in ('start', 'end')]):
            for x in response['start']:
                if x in response['end']:
                    if 'unique' not in response:
                        response['unique'] = {'unique_start': [], 'unique_end':[]}
                    if not hasattr(self, 'subdivision_pairs'):
                        self._gen_subdivision_pairs()
                    if x in self.subdivision_pairs['start']:
                        response['unique']['unique_start'].append(x)
                    elif x in self.subdivision_pairs['end']:
                        response['unique']['unique_end'].append(x)
        return response
    
    def _clean_joiner(self, response, key):
        if key == 'join8ths' and isinstance(response['start'], set) and isinstance(response['end'], set):
            if 'middle' in response:
                for i, x in enumerate(response['middle']):
                    if not x:
                        del response['middle'][i]
            response['end'].discard(min(response['start']))
            response['start'].discard(max(response['end']))
            while len(response['start']) > len(response['end']):
                if 'middle' in response:
                    if response['middle']:
                        response['middle'][-1].append(max(response['start']))
                    else:
                        response['middle'].append([max(response['start'])])
                response['start'].remove(max(response['start']))
            while len(response['start']) < len(response['end']):
                if 'middle' in response:
                    if response['middle']:
                        response['middle'][-1].append(min(response['end']))
                    else:
                        response['middle'].append([min(response['end'])])
                response['end'].remove(min(response['end']))
        if 'unique' in response:
            for value in response['unique'].values():
                for index in value:
                    response['start'].remove(index)
                    response['end'].remove(index)
        return response

    def _gen_subdivision_pairs(self):
        size_beat = self.bar_subdivision.beat_grouping[self.bar_position] * (4/self.bar_subdivision.figure_subidivision)
        self.subdivision_pairs = {'start':[0], 'end':[len(self.pattern)-1]}
        avance = 0
        for i, x in enumerate(self.pattern):
            if i == 0 or i == len(self.pattern) - 1:
                avance += abs(x)
                continue
            if avance % (4 / self.bar_subdivision.figure_subidivision) == 0:
                self.subdivision_pairs['start'].append(i)
            else:
                self.subdivision_pairs['end'].append(i)
            avance += abs(x)

    def _check_silence_between(self):
        silences = [i for i, x in enumerate(self.pattern) if x < 0]
        if not silences:
            return
        for x in silences:
            pre = [x for x in self.pattern[:x] if x > 0]
            pos = [x for x in self.pattern[x:] if x > 0]
            if pre and pos:
                self.silence_in_between = True
                return

    def _set_beam_direction(self):
        sorte = []
        for x in self.content:
            if isinstance(x, Note) and x.duration < 4:
                inter = self.centralLine ^ x
                sorte.append(inter.steps + (inter.octaves*7))
            elif isinstance(x, Chord) and x.duration < 4:
                for note in x.content:
                    inter = self.centralLine ^ note
                    sorte.append(inter.steps + (inter.octaves*7))
        if not sorte:
            return None
        self.border_notes = {'lowest': min(sorte), 'highest': max(sorte)}
        beam_up = [abs(x) for x in sorte if x <= 0]
        beam_down = [x for x in sorte if x > 0]
        if beam_up and not beam_down:
            return 'up'
        elif beam_down and not beam_up:
            return 'down'
        elif beam_up and beam_down:
            if max(beam_up) > max(beam_down):
                return 'up'
            elif max(beam_up) < max(beam_down):
                return 'down'
            elif len(beam_up) >= len(beam_down):
                return 'up'
            elif len(beam_up) < len(beam_down):
                return 'down'
        return None
