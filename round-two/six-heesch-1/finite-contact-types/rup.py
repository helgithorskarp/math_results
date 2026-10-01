"""Small forward RUP checker, independent of the discovery SAT solvers.

Deletion lines are ignored: keeping proved clauses only strengthens unit
propagation and is sound. RAT-only steps are unsupported and rejected.
"""
from collections import defaultdict, deque


class RupChecker:
    def __init__(self, clauses, nv):
        self.nv = nv
        self.clauses = []
        self.occurrences = defaultdict(list)
        self.units = []
        self.empty = []
        for clause in clauses:
            self.add(clause)
        self.base = len(self.clauses)

    def add(self, clause):
        clause = tuple(dict.fromkeys(clause))
        if any(type(p) is not int or not 1 <= abs(p) <= self.nv for p in clause):
            raise ValueError('literal outside variable domain')
        cid = len(self.clauses)
        self.clauses.append(clause)
        for p in clause:
            self.occurrences[p].append(cid)
        if len(clause) == 1:
            self.units.append((clause[0], cid))
        if not clause:
            self.empty.append(cid)
        return cid

    def rup(self, clause):
        """Return (is_RUP, sufficient previously proved clause IDs)."""
        if any(type(p) is not int or not 1 <= abs(p) <= self.nv for p in clause):
            raise ValueError('literal outside variable domain')
        values = bytearray(self.nv + 1)
        queue = deque()
        dependencies = set()

        def enqueue(p, cid=None):
            if cid is not None and cid >= self.base:
                dependencies.add(cid)
            want = 1 if p > 0 else 2
            old = values[abs(p)]
            if old:
                return old == want
            values[abs(p)] = want
            queue.append(p)
            return True

        for cid in self.empty:
            if cid >= self.base:
                dependencies.add(cid)
            return True, dependencies
        for p in clause:
            if not enqueue(-p):
                return True, dependencies
        for p, cid in self.units:
            if not enqueue(p, cid):
                return True, dependencies
        while queue:
            p = queue.popleft()
            for cid in self.occurrences.get(-p, ()):
                free = None
                several = False
                satisfied = False
                for z in self.clauses[cid]:
                    val = values[abs(z)]
                    if val == (1 if z > 0 else 2):
                        satisfied = True
                        break
                    if val == 0:
                        if free is None:
                            free = z
                        else:
                            several = True
                            break
                if satisfied or several:
                    continue
                if free is None:
                    if cid >= self.base:
                        dependencies.add(cid)
                    return True, dependencies
                if not enqueue(free, cid):
                    return True, dependencies
        return False, dependencies

    def verify(self, trace, capture=False):
        additions = deletions = 0
        dependencies = {}
        added = {}
        last = None
        for lineno, line in enumerate(trace.splitlines(), 1):
            words = line.split()
            if not words:
                raise ValueError(f'blank proof line {lineno}')
            deletion = words[0] == 'd'
            if deletion:
                words = words[1:]
            try:
                nums = list(map(int, words))
            except ValueError:
                raise ValueError(f'invalid proof line {lineno}') from None
            if not nums or nums[-1] != 0 or any(p == 0 for p in nums[:-1]):
                raise ValueError(f'invalid clause terminator at line {lineno}')
            clause = nums[:-1]
            if any(not 1 <= abs(p) <= self.nv for p in clause):
                raise ValueError(f'out-of-domain literal at line {lineno}')
            if deletion:
                deletions += 1
                continue
            ok, used = self.rup(clause)
            if not ok:
                raise ValueError(f'non-RUP step at line {lineno}')
            cid = self.add(clause)
            if capture:
                dependencies[cid] = used
                added[cid] = clause
            additions += 1
            last = cid
        if last is None or self.clauses[last]:
            raise ValueError('proof must end with an added empty clause')
        result = dict(additions=additions, ignored_deletions=deletions)
        if capture:
            needed = {last}
            pending = [last]
            while pending:
                cid = pending.pop()
                for dep in dependencies[cid]:
                    if dep not in needed:
                        needed.add(dep)
                        pending.append(dep)
            result['trimmed'] = ''.join(' '.join(map(str, added[cid])) +
                                       (' ' if added[cid] else '') + '0\n'
                                       for cid in sorted(needed))
        return result
