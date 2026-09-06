"""Physical six-neighborhood system and its exact degree-block projection.

No SAT solver is called. The output CNF is ONLY the neighborhood part;
projection.json side conditions are indispensable for the complete model.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
from flow import obstruction, lift, need

HERE = Path(__file__).resolve().parent
H_SHA = '926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466'


def write(path, data):
    with path.open('x') as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write('\n')


class Model:
    def __init__(self):
        path = HERE/'H92.json'
        need(hashlib.sha256(path.read_bytes()).hexdigest() == H_SHA, 'H identity')
        self.h = {tuple(e) for e in json.loads(path.read_text())['red_edges']}
        self.stars = {0: {10,11,12,13,18,19}|set(range(29,38))|set(range(38,43)),
                      1: set(range(14,20))|set(range(20,29))|set(range(38,43)),
                      38: set(range(20))}
        self.fixed = {}
        for e in it.combinations(range(43), 2):
            colors = []
            if e[1] < 20:
                colors.append(e in self.h)
            for root, neighbors in self.stars.items():
                if root in e:
                    colors.append((e[1] if e[0] == root else e[0]) in neighbors)
            if colors:
                need(len(set(colors)) == 1, 'consistent fixed colors')
                self.fixed[e] = colors[0]
        self.free = [e for e in it.combinations(range(43), 2) if e not in self.fixed]
        self.blocks = [(list(range(39,43)), list(range(2,10))),
                       (list(range(10,14)), list(range(20,29))),
                       (list(range(14,18)), list(range(29,38)))]
        self.removed = {tuple(sorted((u,v))) for L,R in self.blocks for u in L for v in R}
        need(len(self.removed) == 104 and self.removed <= set(self.free), '104 free removed pairs')
        self.visible = [e for e in self.free if e not in self.removed]
        self.index = {e: i+1 for i,e in enumerate(self.visible)}
        self.old_index = {e: i+1 for i,e in enumerate(self.free)}
        self.neighborhoods = [(root, color, sorted(neighbors if color else set(range(43))-{root}-neighbors))
                              for root, neighbors in self.stars.items() for color in (True,False)]
        self.clauses = set()
        for root, root_color, vertices in self.neighborhoods:
            for color,k in ((True,4 if root_color else 5),(False,5 if root_color else 4)):
                for subset in it.combinations(vertices,k):
                    pairs = list(it.combinations(subset,2))
                    if any(e in self.fixed and self.fixed[e] != color for e in pairs):
                        continue
                    variables = [e for e in pairs if e not in self.fixed]
                    need(not set(variables)&self.removed, 'removed edge in neighborhood clause')
                    row = tuple(sorted((-1 if color else 1)*self.index[e] for e in variables))
                    need(row, 'fixed forbidden clique')
                    self.clauses.add(row)
        self.clauses = sorted(self.clauses, key=lambda x: (len(x),x))
        self.residuals = []
        for v in range(43):
            target = 20 if v in self.stars else 21
            self.residuals.append({'vertex': v, 'constant': target-sum(c for e,c in self.fixed.items() if v in e),
                                   'subtract_variables': [self.index[e] for e in self.visible if v in e]})
        covered = {v for L,R in self.blocks for v in L+R}
        need(sum(len(L)+len(R) for L,R in self.blocks) == len(covered), 'vertex-disjoint blocks')
        self.outside = sorted(set(range(43))-covered)
        self.densities = []
        for root in (0,1):
            Q = set(range(43))-{root}-self.stars[root]
            pairs = list(it.combinations(sorted(Q),2))
            need(not set(pairs)&self.removed, 'removed edge in Q edge count')
            self.densities.append({'root': root, 'sum_variables': [self.index[e] for e in pairs if e in self.index],
                                   'equals': 124-sum(self.fixed[e] for e in pairs if e in self.fixed)})

    def descriptor(self):
        return {'format': 'ramsey-six-neighborhood-degree-projection-v1',
                'warning': 'Neighborhood CNF alone is not the complete model; all side conditions are required.',
                'H_sha256': H_SHA, 'variables': len(self.visible), 'visible_pairs': self.visible,
                'removed_pairs': sorted(self.removed), 'residuals': self.residuals,
                'residual_zero_vertices': self.outside, 'density_equalities': self.densities,
                'blocks': [{'left': L, 'right': R, 'row_bounds': [0,len(R)], 'column_bounds': [0,len(L)],
                            'equal_margin_totals': True,
                            'subset_cuts': [[L[i] for i in range(len(L)) if mask >> i & 1]
                                            for mask in range(1,1 << len(L))],
                            'cut_semantics': 'sum residuals on S <= sum min(residual at j, size(S)) over right j'}
                           for L,R in self.blocks]}

    def residual(self, values):
        need(len(values) == len(self.visible) and all(type(x) is bool for x in values), 'visible Boolean vector')
        return [row['constant']-sum(values[i-1] for i in row['subtract_variables']) for row in self.residuals]

    def evaluate(self, values):
        residual = self.residual(values)
        bad = [obstruction([residual[i] for i in L], [residual[j] for j in R]) for L,R in self.blocks]
        clause_violations = sum(not any(values[abs(x)-1] == (x>0) for x in row) for row in self.clauses)
        density_values = [sum(values[i-1] for i in row['sum_variables']) for row in self.densities]
        valid = (clause_violations == 0 and not any(bad) and
                 all(residual[v] == 0 for v in self.outside) and
                 all(value == row['equals'] for value,row in zip(density_values,self.densities)))
        return {'satisfies_complete_projected_system': valid, 'neighborhood_clause_violations': clause_violations,
                'residuals': residual, 'block_obstructions': bad, 'density_values': density_values,
                'outside_residuals': {str(v):residual[v] for v in self.outside}}

    def complete_degrees(self, values):
        """Only the degree projection is checked here; evaluate() checks all conditions."""
        residual = self.residual(values)
        need(all(residual[v] == 0 for v in self.outside), 'outside degree equations')
        red = {e for e,c in self.fixed.items() if c}|{e for e,x in zip(self.visible,values) if x}
        for L,R in self.blocks:
            rows,columns = [residual[i] for i in L], [residual[j] for j in R]
            need(obstruction(rows,columns) is None, 'projected degree obstruction')
            matrix = lift(rows,columns)
            need(matrix is not None, 'flow must realize admitted margins')
            red |= {tuple(sorted((i,j))) for a,i in enumerate(L) for b,j in enumerate(R) if matrix[a][b]}
        need([sum(v in e for e in red) for v in range(43)] == [20 if v in self.stars else 21 for v in range(43)],
             'full lifted degree sequence')
        return {'n':43, 'red_edges': [list(e) for e in sorted(red)]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work',type=Path,required=True)
    a = p.parse_args(); a.work.mkdir(exist_ok=False)
    model = Model(); path = a.work/'neighborhood_clauses.cnf'
    with path.open('x') as f:
        f.write(f'p cnf {len(model.visible)} {len(model.clauses)}\n')
        for row in model.clauses:
            f.write(' '.join(map(str,row))+' 0\n')
    descriptor = model.descriptor()
    descriptor['neighborhood_cnf_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    write(a.work/'projection.json',descriptor)
    print(json.dumps({'variables':len(model.visible), 'neighborhood_clauses':len(model.clauses),
                      'removed_pairs':len(model.removed), 'subset_cuts':45,
                      'neighborhood_cnf_sha256':descriptor['neighborhood_cnf_sha256'],
                      'scope':'exact projected subsystem, no SAT/UNSAT verdict'}),flush=True)


if __name__ == '__main__':
    main()
