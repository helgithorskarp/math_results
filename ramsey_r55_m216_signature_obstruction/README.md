# A vertex-minimal signature obstruction inside the M=216 pseudomodel

The fixed exceptional core and signature multiplicities of the published
M=216 aggregate-edge pseudomodel **cannot be completed to a Ramsey (5,5)
graph, even after changing every central-edge count**. A forbidden partial
coloring on just 18 of its vertices proves this. The obstruction uses no
degrees, deficiency inequalities, density bounds, automorphisms, or catalog.

This does **not** exclude the whole `19^2 20^5 21^36` degree profile, or even
every signature vector over its seven-vertex core. The campaign totals remain
66 profiles / 271 anchored splits. No 43-vertex target graph or improved
Ramsey lower bound is claimed.

## 1. The local theorem and reusable cut

Let E be seven ordered vertices `0,...,6`. Its red edges are exactly

```text
01 02 03 06 14 15 16 23 24 25 36 45.
```

All other pairs in E are blue. For a vertex outside E, its signature is the
set of its red neighbors in E. The following six disjoint signature cells
cannot simultaneously contain the indicated numbers of vertices:

| Signature mask | Red neighbors in E | Required vertices | Template labels |
|---:|:---|---:|:---|
| 49 | 0,4,5 | 1 | 7 |
| 50 | 1,4,5 | 2 | 8,9 |
| 60 | 2,3,4,5 | 1 | 10 |
| 73 | 0,3,6 | 2 | 11,12 |
| 116 | 2,4,5,6 | 2 | 13,14 |
| 120 | 3,4,5,6 | 3 | 15,16,17 |

Every root-to-cell edge is fixed by this table; **every edge between the
eleven outside vertices is free**. Nevertheless, every completion has a
red or blue K5 that meets E. This last assertion is an exact
computer-assisted lemma, certified below.

Writing y_X for the number of vertices of signature X, the reusable necessary
condition is the six-way disjunction

```text
y_49 = 0  OR  y_50 <= 1  OR  y_60 = 0  OR
y_73 <= 1 OR  y_116 <= 1 OR  y_120 <= 2.                 (1)
```

Equivalently, `sum_X min(y_X,t_X) <= 10`, for the six thresholds
`t=(1,2,1,2,2,3)`. This is a disjunctive/threshold cut, **not an ordinary
linear inequality**. Other cells and all edges to additional vertices are
irrelevant. If all thresholds held, choosing precisely the listed vertices
would induce the forbidden partial coloring. The theorem applies to any
graph order and any seven roots with the displayed coloring; roots need not
be exceptional-degree vertices. Relabeling or reversing both colors gives
the corresponding transported statement without imposing an automorphism.

The partial coloring is **vertex-minimal uncompletable**: for each of its
18 vertices, deleting that vertex permits a complete 17-vertex coloring
with neither a red nor a blue K5. The explicit completions are in
[DELETIONS.json](DELETIONS.json). Thus deleting a root or lowering any one
positive threshold produces a completable template. This does not claim
edge-minimality or the smallest possible uncompletable partial coloring.

## 2. Why the certificate proves the lemma

The 55 unordered pairs among vertices `7,...,17`, in lexicographic order,
are Boolean variables; true means red. There are no auxiliary variables or
symmetry-breaking clauses. For each five-set meeting E and each color,
discard the forbidden-monochromatic clause if a fixed edge already has the
opposite color. Otherwise the free central pairs must not all have that
color. Deduplication gives exactly

```text
5 unit clauses + 115 three-literal clauses + 401 six-literal clauses = 521.
```

These are necessary and sufficient for avoiding monochromatic five-sets
that meet E. Five-sets entirely outside E are deliberately omitted in the
negative proof. Their addition could only strengthen the obstruction.

[SUPPORT.cnf](SUPPORT.cnf) contains 146 of those clauses, using 43 of the 55
variables. [CERTIFICATE.rup](CERTIFICATE.rup) has 246 additions, including
the final empty clause, and is only 5,137 bytes. For every addition, the
standard-library verifier negates the proposed clause and performs literal
unit propagation on the available premises. A conflict proves the clause
by reverse unit propagation (RUP). Induction through all additions proves
the final contradiction. No general RAT step or external proof checker is
needed for this proof path.

The full formula is generated in two ways. `model.py` appends central
cliques to fixed monochromatic root cliques. `verify.py`, independently of
that construction, inspects each literal five-subset and its ten edges.
The complete clause sets agree; every support clause is justified by the
latter literal construction. The original SAT solver and DRAT trimmer are
discovery tools only, not theorem-verification dependencies.

## 3. Relation to the published aggregate witness

Input: [the M=216 edge-lift pseudomodel](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m216_edge_lift),
Discovery Net `bafkreibzeqyc7jymyz6c3se3x6adj57xg7dzelih2xc5fa5m2flfwtmffm`
at height 2703. Its verified source commit is
`36cdd7fdd7d6227e77a1252634408cd1f7b53703`.

[INPUT_EDGE_LIFT.json](INPUT_EDGE_LIFT.json) is the unchanged 7,063-byte
numerical input, with SHA256
`61c0953591ffe94ee2d61efeeab5f9d60cbc5f6278f1cc4fa7ab468a66968372`.
Its source numbering embeds the obstruction on vertices

```text
0,1,2,3,4,5,6,22,23,24,25,27,28,38,39,40,41,42.
```

The verifier checks both this embedding and the exact input hash. All six
thresholds are attained, so (1) fails. Consequently **no change of the
central-edge counts can repair this particular core/signature record**.
Changing the signature multiplicities or core is still allowed by the
whole-profile problem and is not excluded here.

There is also a much smaller reason why the original *edge counts* alone
do not lift: its size-three signature-3 cell has three red internal edges,
and root edge 01 is red. The forced triangle plus 0 and 1 is a red K5.
That observation alone would allow an edge-count repair; the new 18-vertex
obstruction rules out every such repair while the core and cell sizes stay
fixed.

The source claimed only an aggregate pseudomodel, explicitly not individual
edge realizability. Therefore this result **does not contradict its theorem**.
The source author's normal and optimized verifiers and all seven manifest
entries were replayed successfully before this continuation. That replay is
input validation, not an independent review of its whole reduction. The
new local theorem does not depend on the correctness of that reduction,
the external-root lifting lemma, or inherited local Ramsey extrema.

The general method of completing partial Ramsey colorings is standard;
no priority claim is made. The contribution is this exact localized
obstruction, its vertex-minimality witnesses, and the resulting cut on the
previously published feasible aggregate record.

## 4. Reproduction and validation

Proof verification uses CPython 3.11.2 and only its standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --report /tmp/m216-obstruction.json
cmp report.json /tmp/m216-obstruction.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py --report /tmp/m216-obstruction-O.json
cmp report.json /tmp/m216-obstruction-O.json
sha256sum -c SHA256SUMS
```

Expected: 521 independently reconstructed clauses, 146 supported premises,
246 RUP additions, and 18 valid deletion completions. The checker directly
tests all 111,384 five-sets in those completions, **including the entirely
central five-sets omitted from the negative proof**. It also exhausts all
1,024 five-vertex colorings with six choices of root prefix (6,144 full
truth-table comparisons) and rejects four deliberate certificate mutations.
Checks remain active under `python3 -O`.

Certificate SHA256:
`9ec2e2416a6d3e9783c996a1f5bdd2da0082c7c02cf9641fef6f984a05686094`.
The compact expected output is [report.json](report.json).

Optional rediscovery uses Kissat 4.0.4, source
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim source
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`:

```bash
python3 generate.py --work /tmp/m216-obstruction-fresh \
  --output /tmp/m216-obstruction-certificates \
  --kissat /path/to/kissat/build/kissat --drat-trim /path/to/drat-trim
python3 verify.py --certificate-dir /tmp/m216-obstruction-certificates
```

The work directory must be new. There is one negative solve and 18 deletion
solves, each with a 10-second solver limit and a 30-second process safety
limit. Missing conclusions abort instead of claiming exclusion. The recorded
production run took 0.664 seconds; largest child peak RSS was 64,188 KiB.
Binary hashes and the full formula/proof hashes are in
[discovery_report.json](discovery_report.json). A regenerated proof may differ;
its logical validity is established by `verify.py`, not hash agreement alone.
Large logs and exploratory outputs are not required and are not published.

Remaining trust: the unformalized graph-to-clause argument, the small exact
Python verifier, Python integer/Boolean semantics, SHA256 for input
provenance, and ordinary hardware. This is internal certificate validation,
not independent peer review or formal proof-assistant verification.

This bounded milestone is complete. Next, apply the new signature cut at a
fresh coordinated boundary; do not count this one-core/one-vector exclusion
as a global profile closure or reopen the finished `19^2 20^3 21^38` profile.
