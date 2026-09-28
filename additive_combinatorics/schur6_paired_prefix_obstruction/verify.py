"""Definition-level checks, independent of the CNF generator and SAT solver."""
import json
from pathlib import Path


def schur(word, colours, modulus=None):
    assert word and all(type(c) is int and 0 <= c < colours for c in word)
    N = len(word)
    ordinary = 0
    for z in range(2, N + 1):
        for x in range(1, z // 2 + 1):
            assert not word[x - 1] == word[z - x - 1] == word[z - 1], (x, z-x, z)
            ordinary += 1
    modular = 0
    if modulus is not None:
        assert N == modulus - 1
        for x in range(1, modulus):
            for y in range(x, modulus):
                z = (x + y) % modulus
                if z:
                    assert not word[x - 1] == word[y - 1] == word[z - 1], (x,y,z)
                    modular += 1
    return dict(endpoint=N, class_sizes=[word.count(c) for c in range(colours)],
                ordinary_equations=ordinary, doublings=N//2, modular_equations=modular)


def paired(word, colours=5):
    result = schur(word, colours)
    for block in range(len(word)//5 + 1):
        for positions, special in [((5*block+1,5*block+2),(0,1)),
                                   ((5*block+3,5*block+4),(1,0))]:
            values = [word[x-1] for x in positions if x <= len(word)]
            if not values:
                continue
            assert all(c >= 2 for c in values) and len(set(values)) == 1 or values == list(special[:len(values)])
    return result


def full_shared(data):
    a, p, word = data['axis_factor'], data['short_factor'], data['word']
    assert p == 5 and a >= 3 and a % 2 == 1 and len(word) == 5*a-1
    result = schur(word, 6, 5*a)
    assert all(word[x-1] == word[5*a-x-1] for x in range(1,5*a))
    states = []
    for q in range(a):
        low = word[5*q:5*q+2]
        assert low == [0,1] or low[0] == low[1] >= 2
        states.append(low[0])
    assert states[0] == 0
    result['residual_size'] = states.count(0)
    return result


def scaffold(prefix_endpoint=110):
    a = 109
    A = set(range(39,73)) - {63}
    B = set(range(37,68)) | {77}
    E = set(range(41,69))
    D = A ^ B
    points = {5*q for q in E}
    for support,b in ((A,1),(B,2)):
        for q in support:
            points.update((5*q+b,5*a-5*q-b))
    assert len(points) == 158 and min(points) == 158
    assert all((x+y) % (5*a) not in points for x in points for y in points)
    # These are exactly the coordinates of complete low and reflected high
    # pairs seen in the prefix. No incomplete end pair needs equality.
    low = {q for q in range(a) if 5*q+2 <= prefix_endpoint}
    high = {a-1-r for r in range(a) if 5*r+4 <= prefix_endpoint}
    needed = low | high
    assert needed == set(range(22)) | set(range(87,109))
    assert D == {37,38,63,68,69,70,71,72,77} and D.isdisjoint(needed)
    return dict(class_points=len(points),first_point=min(points),
                mandatory_disagreements=sorted(D),
                additional_disagreement_required_in=sorted(needed),
                conditional_minimum_actual_disagreements=10,
                full_colouring_supplied=False)


def check_witnesses():
    data = json.loads((Path(__file__).parent/'witnesses.json').read_text())
    prefix = data['prefix109']['word']
    assert len(prefix) == 109
    first = paired(prefix)
    full = data['full334']; second = full_shared(full)
    assert full['axis_factor'] == 67 and second['endpoint'] == 334
    word = full['word']
    C = {q for q in range(67) if word[5*q] == 2}
    E = {q for q in range(1,67) if word[5*q-1] == 2}
    T = {22} | set(range(24,34))
    assert C == set(range(23,45)) and E == T | {67-q for q in T}
    assert word.index(2) + 1 == 110
    # The remaining five labels on [1,109] also give a second positive
    # prefix witness, obtained from a complete cyclic construction.
    relabel = {0:0,1:1,3:2,4:3,5:4}
    paired([relabel[c] for c in word[:109]])
    return dict(status='WITNESSES_AND_SCAFFOLD_VERIFIED',prefix109=first,
                full334=second,scaffold=scaffold(),new_s6_bound=False)


if __name__ == '__main__':
    print(json.dumps(check_witnesses(),indent=2))
