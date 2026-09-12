"""Read-only original-task adapter. Never touches physical queues or verdicts."""
from functools import cache
import hashlib
import importlib
import json
from pathlib import Path
import sys
from receiver import from_graph, edges

HERE = Path(__file__).resolve().parent


@cache
def parent():
    data = json.loads((HERE/'DEPENDENCIES.json').read_text())
    for record in data['files']:
        if hashlib.sha256((HERE.parent/record['path']).read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('changed dependency: '+record['path'])
    folder = HERE.parent/'ramsey_r55_maximal_block_order'
    sys.path.insert(0, str(folder))
    module = importlib.import_module('carrier')
    if Path(module.__file__).resolve().parent != folder:
        raise ValueError('wrong carrier module')
    return module


class OriginalTask:
    def __init__(self, name, cache_dir):
        self.old = parent().Carrier(name, cache_dir)
        self.name = name
        self.star_states = 15**len(self.old.old.stars)
        self.frame_count = self.old.size//self.star_states
        first = self.frame(0)
        self.chains_per_frame = first.product.size
        self.size = self.frame_count*self.chains_per_frame

    def frame(self, index):
        if type(index) is not int or not 0 <= index < self.frame_count:
            raise ValueError('frame index')
        graph = self.old.unrank(index*self.star_states)
        return from_graph(43, self.old.q, self.old.r, int(graph['red_hex'], 16))

    def decide(self, index):
        if type(index) is not int or not 0 <= index < self.size:
            raise ValueError('new task code')
        frame_index, chain_index = divmod(index, self.chains_per_frame)
        return dict(task=self.name, task_chain_code=index, frame_index=frame_index,
                    packet=self.frame(frame_index).decide(chain_index))

    def check(self, wrapper):
        from check import check
        code = wrapper['task_chain_code']
        if wrapper['task'] != self.name or type(code) is not int or not 0 <= code < self.size:
            raise ValueError('original obligation identity')
        fi, ci = divmod(code, self.chains_per_frame)
        packet = wrapper['packet']
        if (wrapper['frame_index'] != fi or packet['chain_index'] != ci or
                packet['frame'] != self.frame(fi).data()):
            raise ValueError('original frame/index mismatch')
        return check(packet)

    def address_old(self, graph):
        old_code = self.old.rank(graph)
        frame_index = old_code//self.star_states
        frame = self.frame(frame_index)
        word = int(graph['red_hex'], 16)
        state = tuple(sum((word >> e & 1) << j for j, e in enumerate(star))
                      for star in frame.star_edges)
        chain, position = frame.product.address(state)
        return frame_index*self.chains_per_frame+chain, position


def physical_guard(packet, literals):
    """Check an arbitrary M_r core cylinder; not only catalog graph cores."""
    frame = packet['frame']
    if (frame['n'], frame['q']) != (43, 8) or frame['r'] not in range(5, 9):
        raise ValueError('physical M_r scope')
    pairs = list(edges(43))
    variable = {e: i+2 for i, e in enumerate(e for e in pairs
                if not (e[1] < 32 and e[0]//4 == e[1]//4))}
    inverse = {v: e for e, v in variable.items()}
    if len(variable) != 855 or set(variable[e] for e in pairs if e[0] >= 32) != set(range(802, 857)):
        raise ValueError('physical core variable bridge')
    if len({abs(x) for x in literals}) != len(literals):
        raise ValueError('duplicate guard variable')
    index = {e: k for k, e in enumerate(pairs)}
    word = int(frame['fixed_hex'], 16)
    for lit in literals:
        if type(lit) is not int or not 802 <= abs(lit) < 857:
            raise ValueError('guard must use only actual core variables')
        if (word >> index[inverse[abs(lit)]] & 1) != int(lit > 0):
            raise ValueError('wrong physical guard cylinder')
    return True


class PhysicalCohort:
    """Complete M_r AND guard coordinates, including all unlisted core words.

    The adapter reads pinned block-domain source only. It does not read or
    write a queue, and it does not require a Ramsey core catalog.
    """
    def __init__(self, r, guard, require_edge119=False):
        from chains import ways
        from counts import fixed_factor
        if type(r) is not int or r not in range(5, 9):
            raise ValueError('M_r value')
        if len({abs(x) for x in guard}) != len(guard) or any(
                type(x) is not int or not 802 <= abs(x) < 857 for x in guard):
            raise ValueError('distinct actual core literals required')
        if type(require_edge119) is not bool or (require_edge119 and r != 8):
            raise ValueError('edge119 branch is only defined for M8')
        self.require_edge119 = require_edge119
        self.block_start = 0
        self.r = r
        self.guard = tuple(sorted(guard, key=abs))
        self.assigned = {abs(x)-802: int(x > 0) for x in guard}
        self.unset = [i for i in range(55) if i not in self.assigned]
        self.core_volume = 2**len(self.unset)
        self.block_frames = fixed_factor(8, r)
        if require_edge119:
            from math import comb
            domains = parent().dependencies.load()['family'].parent()['domains']
            roots = domains.root_states('R4')
            if len(roots) != 1998 or sum(x < 4096 for x in roots) != 213:
                raise ValueError('edge119 root-domain threshold')
            self.block_start = comb(219, 7)*37823**21
            self.block_frames -= self.block_start
        self.chains_per_frame = ways(88)
        self.size = self.block_frames*self.core_volume*self.chains_per_frame

    def frame(self, block_index, core_index):
        from itertools import combinations
        from receiver import Frame
        if type(block_index) is not int or not 0 <= block_index < self.block_frames:
            raise ValueError('block-frame code')
        if type(core_index) is not int or not 0 <= core_index < self.core_volume:
            raise ValueError('core-cylinder code')
        block_index += self.block_start
        module = parent()
        family = module.dependencies.load()['family']
        domains = family.parent()['domains']
        a, b = self.r-1, 8-self.r
        rest = list(combinations(range(1, 8), 2))
        def domain(i, j):
            return domains.states('R4' if i < self.r else 'B4',
                                  'R4' if j < self.r else 'B4')
        radices = [module.multiset_count(1998, a), module.multiset_count(1931, b)]
        radices += [len(domain(i, j)) for i, j in rest]
        digits = []
        for radix in reversed(radices):
            block_index, d = divmod(block_index, radix)
            digits.append(d)
        digits.reverse()
        roots = module.unrank_multiset(digits[0], 1998, a)+module.unrank_multiset(digits[1], 1931, b)
        lookup = {e: k for k, e in enumerate(edges(43))}
        word = 0
        for block in range(8):
            if block < self.r:
                for e in combinations(range(4*block, 4*block+4), 2):
                    word |= 1 << lookup[e]
        matrices = [((0, j), domains.root_states('R4' if j < self.r else 'B4')[d])
                    for j, d in enumerate(roots, 1)]
        matrices += [((i, j), domain(i, j)[d]) for (i, j), d in zip(rest, digits[2:])]
        for (i, j), value in matrices:
            for u in range(4):
                for v in range(4):
                    word |= (value >> (4*u+v) & 1) << lookup[4*i+u, 4*j+v]
        values = dict(self.assigned)
        values.update({v: core_index >> j & 1 for j, v in enumerate(self.unset)})
        for j, e in enumerate(combinations(range(32, 43), 2)):
            word |= values[j] << lookup[e]
        if self.require_edge119 and not (word >> lookup[3, 4] & 1):
            raise ValueError('edge119 positive frame range')
        return Frame(43, 8, self.r, format(word, 'x'))

    def decide(self, index):
        if type(index) is not int or not 0 <= index < self.size:
            raise ValueError('cohort chain code')
        fixed_index, chain = divmod(index, self.chains_per_frame)
        block, core = divmod(fixed_index, self.core_volume)
        packet = self.frame(block, core).decide(chain)
        physical_guard(packet, self.guard)
        return dict(base='M'+str(self.r), guard=list(self.guard),
                    require_edge119=self.require_edge119,
                    cohort_chain_code=index, block_frame=block, core_code=core, packet=packet)

    def check(self, wrapper):
        from check import check
        code = wrapper['cohort_chain_code']
        if (wrapper['base'] != 'M'+str(self.r) or wrapper['guard'] != list(self.guard)
                or wrapper['require_edge119'] != self.require_edge119
                or type(code) is not int or not 0 <= code < self.size):
            raise ValueError('physical obligation identity')
        fi, ci = divmod(code, self.chains_per_frame)
        bi, co = divmod(fi, self.core_volume)
        packet = wrapper['packet']
        if (wrapper['block_frame'] != bi or wrapper['core_code'] != co or
                packet['chain_index'] != ci or packet['frame'] != self.frame(bi, co).data()):
            raise ValueError('physical frame/index mismatch')
        physical_guard(packet, self.guard)
        return check(packet)
