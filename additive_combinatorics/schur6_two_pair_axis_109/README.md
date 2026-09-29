# Two colour classes of size two in a symmetric axis modulo 109

**Exact computer-assisted classification.** Let
`E : (Z/109Z) \ {0} -> {0,1,2,3,4,5}` satisfy `E(x)=E(-x)` and have no
monochromatic modular equation `x+y=z` with `x,y,z` nonzero, including
`x=y`. If two distinct colour classes have size two, write them as
`{s,-s}` and `{t,-t}`. Then

```
t/s belongs to {2, -2, 2^(-1), -2^(-1)} = {2, 107, 55, 54} modulo 109.
```

Conversely, all four ratios occur, by the supplied witness, scaling,
reflection and interchange of the two colour names. Thus the two pairs
must occupy a doubling position. At most **two** colour classes have size
two. This classification allows every axis run order and every interval
separation choice; it imposes no column conditions.

This is a constraint on axes, **not** an exclusion of a full 544-colouring
and **not** a new Schur-number lower bound. The witness below has length
108 and certifies the admissible axis case only. Completion by independent
columns is a separate open task. No external peer review or historical
priority is claimed here.

## Proof

Since 109 is prime, multiply all residues by `s^(-1)`, rename the two
classes 0 and 1, and choose the sign of `d=t/s` so `2 <= d <= 54`.
The distinguished classes are then exactly `{1,108}` and `{d,109-d}`.

For 45 of these 53 values of `d`, `data.json` supplies a unit `u` such that
the 45 residues `u,2u,...,45u` avoid all four distinguished residues.
The map `j -> uj (mod 109)` is injective on `[1,45]` and respects every
integer equation `i+j=k` with `k<=45`. Restricting `E` to this progression
would therefore give a four-colouring of `[1,45]` with no monochromatic
Schur triple. This contradicts the known theorem `S(4)=44`, in the
largest-colourable-endpoint convention. That theorem is an explicit
external input, not reproved by this package; it is recorded in
[Fredricksen and Sweet, *Symmetric Sum-Free Partitions and Lower Bounds
for Schur Numbers* (2000), p. 2](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf/).
The same source includes equal summands in the definition.

Precisely eight ratios remain:
`2,4,27,28,35,37,53,54`. Interchanging the two pairs replaces `d` by
`d^(-1)`, up to sign, giving the four orbits

```
{2,54}, {4,27}, {28,35}, {37,53}.
```

For each representative `d=4,28,37`, an exact SAT model colours the other
52 positive-half positions with four colours and reflects them. Three
DRAT-verified UNSAT proofs exclude these cases. For `d=2`, the complete
108-entry axis in `data.json` is directly checked against every nonzero
modular sum; its six class sizes are `2,2,20,22,26,36`. Inverting and
swapping the two colours gives the other normalized admissible ratio 54.

For the final assertion, normalize two pairs to `{±1}` and `{±2}`.
A third pair, if present, must be `{±54}` by its ratio to the first pair.
Its ratio to the second pair is 27 up to sign, which has already been
excluded. Thus three size-two classes are impossible.

## Exact encoding and trust boundary

Let `P=[1,54] \ {1,d}`, in increasing order. For `q=P[j]` and `c=0,1,2,3`,
variable `4j+c+1` means that both `q` and `109-q` have colour `c+2`.
Each position has exactly one colour, encoded by one four-literal clause
and all six pair exclusions. For each nonzero modular equation whose
three residues avoid the distinguished pairs, add the clause forbidding
them from having each of the four remaining colours. Equal variables
collapse, so doublings and other repeated reflected positions are retained.
The two fixed classes themselves are sum-free; equations meeting a fixed
class and its complement cannot be monochromatic.

Finally order the four remaining colours by their first appearance on `P`:
using colour `c>0` at position `j` requires some earlier use of `c-1`.
Any colouring, including one with unused colours, admits this relabelling,
so this removes no case. Each resulting formula has **208 variables and
4056 clauses**.

`audit.py` imports neither the encoder nor a SAT solver. It reconstructs
all six-colour modular constraints using **all ordered residue pairs**,
substitutes constants for the fixed pairs, and compares the complete
resulting clause set with the DIMACS file. It also checks the valid
first-appearance clauses, exact file hashes, AP coverage, inverse orbits,
the positive witness, and the three-pair deduction. Checks remain active
under `python -O`.

The three exclusions use CaDiCaL 1.9.5 to generate binary DRAT proofs and
DRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` to check them.
The checker, the reduction and elementary symmetry argument, the Python
runtime, and the external theorem `S(4)=44` are the trust boundary. This
is not a proof-assistant formalization; a SAT solver verdict alone is not
accepted as an exclusion.

| Representative | CNF bytes | Reference DRAT bytes |
| ---: | ---: | ---: |
| 4 | 71609 | 16637367 |
| 28 | 71622 | 42047020 |
| 37 | 71622 | 24149985 |

Full SHA-256 values appear in `data.json`. The 82,834,372 proof bytes and
verbose logs are deliberately not stored in the repository. Regenerate
them with the commands below. A valid regenerated proof may have a different
hash; the auditor reports this without substituting a hash comparison for
DRAT verification. `verified.json` records the reference certificate audit;
it is evidence metadata, not a substitute for rerunning the checker.

## Reproduce

Requirements: Python 3.11+ with the standard library. Proof regeneration
additionally needs a POSIX system, [CaDiCaL](https://github.com/arminbiere/cadical)
and [DRAT-trim](https://github.com/marijnheule/drat-trim). The reference run
used Python 3.11.2. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 audit.py
python3 encode.py --output /tmp/schur-two-pair-109
python3 audit.py --cnf-dir /tmp/schur-two-pair-109
python3 prove.py --output /tmp/schur-two-pair-109 \
  --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

The first audit checks compact data only and explicitly reports
`proofs_checked: false`. The second also checks all three CNF encodings.
Only the last command regenerates and verifies every exclusion proof;
it must report `CLASSIFICATION_CERTIFICATES_VERIFIED` and
`all_three_exclusion_proofs_checked: true`.

`prove.py` limits each solver/checker stage to 120 seconds by default
(`--seconds` changes this) and each generated proof to 128 MiB. Failure,
timeout or incomplete checking makes the command fail; it is not an
exclusion. Allow about 100 MiB of output space for the reference proofs.
To check already generated proofs without repeating SAT search:

```sh
python3 audit.py --cnf-dir /tmp/schur-two-pair-109 \
  --proof-dir /tmp/schur-two-pair-109 --drat-trim /path/to/drat-trim
```

`--ratios 4` selects a single-case smoke test; its output explicitly labels
partial checking and does not certify the whole classification.

## Relevance to the constructive S(6) route

A full reflected Schur colouring of `[1,544]` is a modular sum-free
colouring of `(Z/545Z)\{0}`. Indeed, a modular wraparound equation
`x+y=545+z` reflects to the ordinary equation
`(545-x)+(545-y)=545-z`. Restriction to multiples of 5 gives an axis `E`
modulo 109 satisfying this lemma. Consequently the result is necessary
for every such reflected full colouring, including the independent-column
construction, without any assumptions about its off-axis colours.
Here “class size two” always means size **within the axis**.

This differs from the earlier
[35 fixed axis-chamber result](../schur6_axis_chamber_barrier/README.md),
which kept seed-selected interval inequalities. The present classification
fixes no intervals, but concerns the two-size-two-class condition instead.
Neither result settles the unrestricted six-colouring problem. The
[2026 shifted-template paper](https://arxiv.org/abs/2607.15034) still records
the established bound `S(6)>=536`; the first new-bound target remains a
complete, independently verified colouring of `[1,537]` or longer.
