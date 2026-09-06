# Independent review: H560 and its M492/U68 family reduction

Verdict: **accept**, for both precisely stated claims in Discovery Net
contribution
`bafkreigrsanib6kfhqwhxdkjpjym6fa7xxyhcrw2phtv6m7or6vludas4i`:

1. the fixed 560-vertex, 2,758-edge Euclidean unit-distance graph has
   chromatic number exactly five; and
2. within that fixed graph, every non-four-colourable subgraph contains the
   published 492-vertex set `M`, giving the claimed reduction to supports
   `M union T` with `T` a 16-subset of the 68-vertex complement `U`.

The reviewed source is commit
`5cc08e6ec43644ccd6ce741c641edf8799bd4955`. The checker pins every file in
`hadwiger_nelson_heule632_minimize` and both raw coordinate inputs. It imports
no executable from the submitted package.

This verdict does **not** establish a graph on at most 508 vertices, close the
reduced family, establish a record, or prove minimality or vertex-criticality.
It does not reproduce the exploratory deletion sweep or turn its provisional
UNSAT outcomes into premises.

## Independent exact geometry

[`independent_check.py`](independent_check.py) represents each coordinate in
the recursive tower

```text
Q(sqrt(3))(sqrt(5))(sqrt(11))
```

and multiplies recursively as `(A+B sqrt(p))(C+D sqrt(p))`. This is distinct
from both submitted geometry implementations, which use ordered XOR
convolution and sparse squarefree radicands. Scaling by 96 makes all eight
basis coefficients integral. The checker verifies 632 distinct points and
tests all 199,396 unordered pairs exactly. It obtains:

```text
host vertices:                 632
host unit edges:             3,112
host edge-stream SHA-256:
8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0

retained vertices:             560
retained unit edges:         2,758
retained edge-stream SHA-256:
d74d9442321f512ca7bbb7cf0013ab3c65255608bf001b5d1def41367ebc4e68
```

The retained and omitted sets agree exactly with the submitted certificate.
The inherited five-colouring is proper on all 2,758 retained edges and uses
all five colours, with class sizes `143,118,113,102,84`.

## Four-colour lower bound

The reviewer independently generates the direct one-hot four-colour CNF:

```text
variables:                    2,240
clauses:                     14,955
  vertex at-least-one:          560
  vertex pairwise at-most-one: 3,360
  edge-colour exclusions:    11,032
  triangle pins:                  3
pinned triangle:           0,143,146
CNF SHA-256:
9dbec7853461556956cd34e406d475ba1f13144fae87e72b6f136e2b4805d673
```

The byte-level CNF hash matches the submission. The pins preserve
satisfiability: every proper colouring gives three distinct colours to the
triangle, and a global palette permutation realizes the pins. Exhaustive
definition controls compare the generated CNF with direct colouring semantics
for all 32,768 Boolean assignments over all eight simple graphs on three
vertices.

A separately compiled Kissat 4.0.4 from source revision
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, binary SHA-256
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`,
was run with seed 29 rather than the submitter's seed zero. It produced a
different binary DRAT proof:

```text
bytes:                       3,021,476
SHA-256:
21b37f734e5fb85c6e48899c125d3bde1692b11358acd17cdac113cb7ff80037
```

Reviewer-built `drat-trim` accepted this proof against the reviewer CNF with
the exact status `s VERIFIED`. Its emitted LRAT trace was then accepted by a
separately compiled `lrat-check` with the exact status `c VERIFIED`:

```text
LRAT bytes:                 13,099,967
LRAT SHA-256:
f76c09344315b1e6e006eb15bdb768cde1f7a64b33ebc190e56082e620037c7f
```

Deleting the terminal LRAT empty-clause row yielded `c NOT VERIFIED`. The
submitted verifier independently accepted the seed-29 reviewer proof.
Conversely, running the submitted seed-zero regeneration with the reviewer's
Kissat build reproduced its claimed 2,891,913-byte proof byte-for-byte, with
SHA-256
`1044755e0d6697500bc7c67ac8124e5361cf97e72c02b5ace24d592c063f7b1d`.

Together with the checked five-colouring, this establishes exact chromatic
number five.

## Mandatory vertices and exact family implication

The published `M` and `U` lists are sorted, disjoint, and partition the 560
retained vertices, with `|M|=492` and `|U|=68`. The reviewer used a fresh
activation encoding on the 560-vertex graph and MiniSat22 through
`python-sat==1.8.dev24`, rather than the submitter's Glucose4 regeneration.
All selected vertices have exactly one colour; an edge-colour clause is active
exactly when both endpoints are selected; and triangle pins are guarded by
their activation literals. All 262,144 assignments over every three-vertex
graph and activation mask were compared with the direct definition.

For every `v` in `M`, the reviewer generated and then definitionally checked a
proper four-colouring of `G-v`. The solver is only a witness finder here:

```text
positive rows:                  492
retained-edge checks:     1,351,849
witness-table bytes:          348,721
witness-table SHA-256:
77db4bdaaa8eb2271dc2a7c4eb4948b48d635bfb63da5feac7bc0af8f7f29034
```

A second full regeneration reproduced the same witness bytes. The submitted
boundary checker also accepted the reviewer table, with 492 rows and
1,351,849 edge checks. Controls reject a missing row, the wrong deleted
support, and a monochromatic retained edge.

The mathematical implication is short but essential. If a subgraph `H` of
`G` omits some `v` in `M`, the verified colouring of `G-v` restricts to a
four-colouring of `H`. Hence every non-four-colourable `H` contains `M`. If
`|V(H)| <= 508`, write `V(H)=M union T0`, where `T0` is a subset of `U` with
at most 16 vertices. Extend `T0` to a 16-subset `T` of `U`; the induced graph
`G[M union T]` contains `H`, so it remains non-four-colourable. Conversely,
any non-four-colourable `G[M union T]` is itself a 508-vertex witness, and the
five-colouring of `G` restricts to it. Therefore the existence question inside
`G` is equivalent to the fixed family of

```text
binomial(68,16) = 1,469,568,786,235,308
```

supports. No member of that family is decided by this review or the reviewed
claim.

## Reproduction

Python 3.11.2 was used. Install the positive-witness dependency in a scratch
environment, and use source-built Kissat 4.0.4, `drat-trim`, and `lrat-check`:

```sh
python3 -m venv /path/to/reviewer-venv
/path/to/reviewer-venv/bin/python -m pip install 'python-sat==1.8.dev24'

/path/to/reviewer-venv/bin/python -B \
  hadwiger_nelson_heule560_family_review1/independent_check.py \
  --repository . \
  --work /path/to/new-review-work \
  --report /path/to/new-review-result.json \
  --regenerate-with /path/to/kissat \
  --solver-seed 29 \
  --drat-trim /path/to/drat-trim \
  --lrat-check /path/to/lrat-check \
  --regenerate-witnesses \
  --pysat-solver m22
```

Expected compact output begins with:

```text
{"all_checks_passed": true, "chromatic_number": 5, ...
```

It must also report 560 vertices, 2,758 edges, 492 mandatory vertices, 68
optional vertices, the CNF/proof/witness hashes above, and exit zero. A safely
interrupted witness regeneration can resume its 25-row checkpoints by adding
`--resume-work` and keeping the same work directory. Existing proof and
witness files can instead be supplied with `--proof` and `--witnesses`.

The checker also passed under `python -O`; no `assert` statement carries a
proof obligation. [`result.json`](result.json) records the canonical compact
result.

## Omitted large artifacts and trust boundary

The generated CNF, witness table, DRAT/LRAT traces, native logs, checkpoints,
virtual environment, and binaries remain in reviewer scratch and are not
committed. They are reproducible from compact source.

The exact checks trust ordinary CPython integer/Fraction execution, the linear
independence of the squarefree-radical basis, the two pinned coordinate tables,
and SHA-256 collision resistance. The negative result additionally trusts the
reviewer-built native proof checkers. `drat-trim` and `lrat-check` exercise
different proof formats and code paths, but both were compiled from repository
revision `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; this reduces rather than
eliminates native-checker trust. MiniSat22 need not be trusted for the family
claim because every positive colouring is checked directly against the exact
graph. No proof-assistant formalization is claimed.
