# Strong Seymour vertices at order 15: exact structural frontier

## Results

For a vertex `x` of a tournament, write `N+(x)` for its out-neighborhood and
`N++(x)` for its exact second out-neighborhood.  The vertex is **strong
Seymour** when there is a directed matching from every vertex of `N+(x)` to
distinct vertices of `N++(x)`.

This directory proves two exact computer-assisted statements.

> **Regular order-15 theorem.** Every regular tournament on 15 vertices has a
> strong Seymour vertex.

> **Order-15 frontier theorem.** If a tournament on 15 vertices has no strong
> Seymour vertex, then it is nonregular, has minimum out-degree six, and every
> ordinary Seymour vertex has out-degree seven.

Here an ordinary Seymour vertex satisfies `|N++(x)| >= |N+(x)|`.  Combined
with the existing exact exclusion through order 14, the second theorem
identifies the only remaining score/root regime at order 15.  It does **not**
claim that every order-15 tournament has a strong Seymour vertex.

The primary source is Bai, Li, and Park,
[Towards a strengthening of the second neighborhood conjecture](https://arxiv.org/abs/2607.18047).
Their Theorem 1.5 proves that minimum out-degree at most five guarantees a
strong Seymour vertex, and their Remark 3.1 gives a 36-vertex counterexample.
Austin Gibbons's independent
[SSNC project](https://github.com/AustinBGibbons/ssnc) constructs a regular
tournament of every odd order at least 15 with exactly nine strong vertices;
it does not prove existence in every regular tournament.  Its explicit
order-15 example is used only as a positive definition-level fixture here.

## Mathematical reduction

Let `T` be a hypothetical order-15 tournament with no strong Seymour vertex.
The Bai--Li--Park theorem gives `delta+(T) >= 6`.  For a vertex `x`, put
`A=N+(x)`, `B=N-(x)`, and, for `S` contained in `A`,

```text
Gamma_x(S) = {z in B : y -> z for some y in S}.
```

Hall's theorem says that `x` is nonstrong exactly when some `S` satisfies
`|Gamma_x(S)| < |S|`.  If `S` is inclusion-minimal, then
`|Gamma_x(S)|=|S|-1`, and every member of `Gamma_x(S)` is reached by at least
two members of `S`.  If `x` has minimum out-degree, Bai--Li--Park Lemma 2.5
also gives minimum out-degree at least one in `T[S]`, so `|S|>=3`.

Every tournament has an ordinary Seymour vertex.  For such a vertex `x`,

```text
d+(x) <= |N++(x)| <= 14-d+(x),
```

so `d+(x)` is six or seven.  If it is six, then `x` is a minimum-degree
vertex.  Its minimal Hall witness has size at least three and at most five:
size six would be all of `A`, whose neighbor set is `N++(x)` and has size at
least six.  Relabeling the two shores leaves exactly the three normalized
cases `d6-s3`, `d6-s4`, and `d6-s5`.  Their checked UNSAT certificates show
that an ordinary Seymour vertex of degree six cannot occur in a counterexample.

It remains to exclude a regular counterexample.  In a regular order-15
tournament, every vertex has degree seven and `N++(x)=N-(x)`: otherwise an
in-neighbor outside `N++(x)` would dominate `x` and all seven out-neighbors.
Thus every vertex is ordinary Seymour.  A minimal Hall witness has size
`3,4,5`, or `6`.  The first three normalized cases are checked UNSAT.

The size-six case has a short direct contradiction.  Its Hall neighbor set
has size five, leaving two vertices of `N-(x)` outside it.  Each of those two
vertices dominates `x` and all six witness vertices, already exhausting its
seven out-arcs.  Each would therefore have to lose their mutual arc, which is
impossible.

Consequently a hypothetical order-15 counterexample is nonregular.  Since
its minimum degree is at least six and its average degree is seven, its
minimum degree is exactly six.  Every ordinary Seymour vertex has degree at
most seven, and the certified degree-six exclusion forces all such vertices
to have degree seven.

## SAT encoding and exact certificates

`generate_cnf.py` uses one Boolean orientation variable for each unordered
pair.  It imposes minimum out-degree six.  Exact threshold flags distinguish
degrees six, seven, and at least eight.  A vertex of degree at least eight is
automatically nonstrong because it has at most six in-neighbors.  Every
degree-six or degree-seven vertex instead receives an explicit minimal Hall
witness, with exact neighbor-set semantics, deficiency one, double coverage,
and the minimum-degree witness lemma when applicable.  The selected ordinary
root and its Hall shores are normalized by relabeling.

The regular mode fixes every degree to seven and applies the witness lemma at
every vertex.  Within each of the four root regions, one harmless representative
arc is oriented to reduce label symmetry.

All six production formulas have 20,666 variables.  CaDiCaL 3.0.1 produced
DRAT proofs, and `drat-trim` independently returned `s VERIFIED` for every
pair.

| case | clauses | CNF SHA-256 | DRAT bytes | DRAT SHA-256 |
|---|---:|---|---:|---|
| `d6-s3` | 47,330 | `4e97aabb110cc86f1fdb328699c979c6758a90346fe3d7822b95ac8bec1181b5` | 184,021 | `f892154db560a3ac03532da18296f3ba39e1db3f5cdf7de2c3801cfd69211b82` |
| `d6-s4` | 47,330 | `c140a1505bf3b0add51b5ab06152d73194afd91cc8d40f168e3b1273eb7dcbd6` | 2,660,034 | `515104ee9a16a34a9ecdff8a12a66a4bb8a283c368e090e59e3e25f4c82b8037` |
| `d6-s5` | 47,330 | `70970cd5ee7330a497831fa6b8d5395b2715c39a2b9d5172519fd1bcedde5aea` | 71,552,641 | `6f833e8cc62b8ee0d56e01dd63cf293351cd3403fb4dc4135fdb4229a25c5439` |
| `regular-s3` | 47,349 | `e8baf56ad7cc4e4beeb1a0860d254af2cfd7861ee5dda475f98ed78fdc81af39` | 6,064,390 | `8f970cf952f298317a4dd2575b57dd1a192f2618537419388ce7ad6e5ed5db0d` |
| `regular-s4` | 47,349 | `d292ebac911706f39d2709f19a9b191f2ec74bb7e9f06b15185b1b2b1b7667a4` | 1,978,597 | `ae854f856cd10b46db9c25928e890fc1a0d2b95b3184abc0ddf066d5f4088d81` |
| `regular-s5` | 47,349 | `41ba2d416ddce85be019e4398c65c7781c59eaa55bb9db738cb0bce8c53f958b` | 7,640,975 | `0735a8222566e4a5563d043ec6129f94a7a54408edddebfeb40dd4b40ccff111` |

The traces and solver logs are deliberately retained under `/scratch` and
are not committed.  They are deterministically regenerable from the compact
source.

## Reproduction

The audited environment used CPython 3.11.2 and `python-sat==1.9.dev15`.
Create a virtual environment under `/scratch`, then run the definition-level
checks:

```bash
python3 -m venv /scratch/strong-seymour-order15-venv
/scratch/strong-seymour-order15-venv/bin/pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 direct_check.py
```

The exact final output is:

```json
{"hall": {"minimal_witnesses": 248660, "record_sha256": "1afea96d65c529dd0588d7472ab98143b99ca19f17ce6447f4d0e13fb77b390d", "tournaments": 33867, "vertex_cases": 202013}, "order15_fixtures": {"constant_nine_strong_owners": [1, 3, 7], "constant_nine_strong_vertices": [1, 2, 3, 5, 6, 7, 11, 12, 13], "cyclic_strong_count": 15}, "regular_six": {"forced_outneighbors_per_hall_nonneighbor": 7, "hall_nonneighbors": 2}, "status": "VERIFIED"}
```

Its newline-terminated stdout SHA-256 is
`98de6e7bbe68dddd4787bd2864bda1bb351e633a0e7e071e312649318e315491`.
The checker exhausts all 33,867 labeled tournaments through order six and
compares Hall deficiency with an augmenting-path matcher in 202,013 vertex
cases.  It also checks the generic properties of 248,660 inclusion-minimal
Hall witnesses and independently evaluates two regular order-15 fixtures.

Generate and prove the six formulas as follows, replacing `cadical` and
`drat-trim` with local paths if necessary:

```bash
python generate_cnf.py d6-s3 /scratch/ss15-d6-s3.cnf
python generate_cnf.py d6-s4 /scratch/ss15-d6-s4.cnf
python generate_cnf.py d6-s5 /scratch/ss15-d6-s5.cnf
python generate_cnf.py d7-s3 /scratch/ss15-regular-s3.cnf --mode regular
python generate_cnf.py d7-s4 /scratch/ss15-regular-s4.cnf --mode regular
python generate_cnf.py d7-s5 /scratch/ss15-regular-s5.cnf --mode regular

cadical /scratch/ss15-d6-s3.cnf /scratch/ss15-d6-s3.drat
drat-trim /scratch/ss15-d6-s3.cnf /scratch/ss15-d6-s3.drat
```

Repeat the last two commands for the other five cases.  CaDiCaL used source
commit `c60730422e758ef1cebe7aeddf2dda31c996bf04`; `drat-trim` used source
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

`cegar_search.py` is a separate, experimental validation route.  It removes
the existential Hall-witness variables and instead adds clauses forbidding
explicit complete directed matchings found in candidate tournaments.  Every
added clause is definition-level valid for a no-strong tournament.  The
search helped localize the still-open nonregular degree-seven-root branch but
is not used as evidence for either theorem above, and no completion claim is
made for it.

## Trust boundary and novelty scope

The ordinary reductions and the regular size-six contradiction are written
above.  The six finite exclusions trust the inspected formula generator,
PySAT's cardinality encodings, CaDiCaL, and `drat-trim`; proof
checking establishes UNSAT only for the exact hashed formulas.  The
definition-level checker is an independent semantic guard, not an exhaustive
order-15 proof.

Targeted checks of the committed Discovery Net graph, the Bai--Li--Park
paper, and the independent SSNC project found no prior proof of the regular
order-15 theorem or the stated degree-six-root exclusion.  The results are
apparently new relative to those searched sources; this is not a historical
priority claim.
