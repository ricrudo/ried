from ried.note.note_generator import Note, Silence
import copy
from typing import Union

class Beat:

    def __init__(self, pattern, content=None, bar_position=None, clef=None, centralLine=None):
        self.clef = clef
        self.centralLine =centralLine
        self.pattern = self._check_pattern(pattern)
        self.content = self.pairing_content_pattern(content)
        self._set_joiners()

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
                if not isinstance(content[i], Note):
                    if centralLine:
                        content[i] = Note(content[i], duration=duration, centralLine=centralLine)
                    else:
                        content[i] = Note(content[i], duration=duration)
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
            response = self._define_groups(value, joiners['silence'])
            self._joiners_to_notes(key, response)
        del joiners
        breakpoint()


    def _mk_joiners_by_figure(self):
        joiners = {}
        joiners['noJoin'] =  [i for i, x in enumerate(self.pattern) if x >= 1]
        joiners['join8ths'] = [i for i, x in enumerate(self.pattern) if 1 > x > 0]
        joiners['join16ths'] = [i for i, x in enumerate(self.pattern) if 0.5 > x > 0]
        joiners['join32ths'] = [i for i, x in enumerate(self.pattern) if 0.25 > x > 0]
        joiners['join64ths'] = [i for i, x in enumerate(self.pattern) if 0.125 > x > 0]
        joiners['join128ths'] = [i for i, x in enumerate(self.pattern) if 0.0625 > x > 0]
        joiners['silence'] = [i for i, x in enumerate(self.pattern) if x < 0]
        return joiners

    def _define_groups(self, value, silences):
        if all(list(map(lambda x: x-1 == value[value.index(x) - 1], value[1:]))):
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
                if not index in value and not index in silences:
                #if not index in value:
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
        for starter in response['start']:
            if not hasattr(self.content[starter], 'joiner'):
                self.content[starter].joiner = {}
            if not key in self.content[starter].joiner:
                self.content[starter].joiner[key] = []
            self.content[starter].joiner[key].append('start')
        for grupos in response['middle']:
            for index in grupos:
                if not hasattr(self.content[index], 'joiner'):
                    self.content[index].joiner = {}
                self.content[index].joiner[key] = ['middle']
        for ender in response['end']:
            if not hasattr(self.content[ender], 'joiner'):
                self.content[ender].joiner = {}
            if not key in self.content[ender].joiner:
                self.content[ender].joiner[key] = []
            self.content[ender].joiner[key].append('end')


