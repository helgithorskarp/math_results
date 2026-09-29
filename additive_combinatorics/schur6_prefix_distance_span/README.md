# A Schur prefix forcing a sixth colour in every later 83-point interval

The explicit five-colouring `u` of `[1,77]` in [data.json](data.json) is
sum-free, including repeated summands. In any classical six-colour Schur
colouring extending this fixed prefix, **every interval of 83 consecutive
integers lying above 77 must contain colour 6**. The number 83 is sharp:
the same data supplies a complete valid 237-word with an 82-point terminal
interval avoiding colour 6. The statement is invariant under renaming the
five prefix colours.

This is a conditional obstruction for one explicit prefix. It does not
exclude all prefixes or the free interval construction at 537, and it gives
**no improvement** to the [published `S(6)>=536` bound](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32),
also used in the [2026 shifted-template paper](https://arxiv.org/abs/2607.15034).
The 237-word witnesses sharpness of this conditional statement only.

## Exact distance span

The fixed prefix, in colour labels 1 through 5, is

```
43322224341111111111332222335555555555555555555555555555532242111111111112232
```

For a word `b` of length `L`, indexed from 0, impose

    not (b[i] = b[i+d] = u[d])
    for 1 <= d <= 77 and 0 <= i < i+d < L.

Here `u` is indexed from 1. Let its distance span be the largest `L` for
which such a word over colours 1 through 5 exists. A compatible word of
length 82 is supplied in full. A proof-checked SAT refutation excludes
length 83, so the exact span is **82**. Larger lengths are excluded by
restricting any purported word to its first 83 positions.

This is a fixed edge-labelled instance of
[adapted vertex colouring](https://doi.org/10.1016/j.ejc.2007.11.015):
join positions at distances at most 77, and label an edge of distance `d`
by `u[d]`. No edge may have the same label as both endpoints. The general
colouring notion, its SAT encoding and proof checking are standard. No
historical priority is claimed for those methods or this particular
prefix-specific value.

## Why the span forces the sixth colour

Suppose a six-colour Schur word `C` agrees with `u` on `[1,77]`, and let
`I=[t,t+82]` lie in its domain, with `t>=78`. If `I` avoided colour 6,
then `b[i]=C(t+i)` would be a word over colours 1 through 5. For every
distance `d<=77`, the ordinary Schur equation

    d + (t+i) = t+i+d

forbids `b[i]=b[i+d]=u[d]`. Thus `b` would satisfy the length-83 distance
formula, contradicting the checked refutation. This argument applies at
any later location and makes no assumption about the intervening colours.

For sharpness, let `b` be the supplied compatible word of length 82 and
form

    u + [6]*78 + b.

This colours `[1,237]`, with colour 6 exactly on `[78,155]` and `b` on
`[156,237]`. The prefix is sum-free; `[78,155]` is sum-free; a sum of two
prefix points either stays in the prefix or enters colour 6. A sum of a
prefix point and a terminal point is exactly one of the distance
constraints. Two terminal points sum above 237. A triple meeting colour 6
and another colour cannot be monochromatic. These cases prove validity.
The literal checker also checks all **14,042** full Schur equations,
including **118** doublings, on the supplied complete 237-word.

Consequently this fixed prefix also has exact endpoint 237 in the family
that reserves colour 6 exactly on `[78,155]` and uses only colours 1
through 5 afterward. This is a restricted-family endpoint, not `S(6)`.

## Relevance to the 537 construction

The free interval construction reserves colour 6 exactly on
`[78,154] union [460,537]` and leaves all other positions independent.
The low prefix in this note arose in a joint assignment to
`U=[1,77]` and `V=[155,304]`. That complete 227-digit partial word is
included in the data. It has just two base violations, `(1,232,233)` and
`(3,231,234)`, and none of its 155 initial tail lists is empty.
It is **not** a full 537-position near-colouring.

Regardless of how V and the remaining tail are recoloured, keeping this U
cannot work: V itself contains an 83-point interval avoiding colour 6.
The obstruction therefore concerns U alone, rather than one failed middle
assignment. This explains why a small base-defect score was misleading.
The [earlier interval-tail reduction](../schur6_interval_tail_trades/README.md)
already contains these UWW rows; the new contribution here is the exact
prefix span and its checked gap consequence.

A different supplied valid 77-prefix has a compatible 155-word, checked
against all 8,932 relevant pairs. Thus a prefix must be tested; the
obstruction is not shared automatically by all valid five-colour prefixes.
Forty-eight bounded feedback iterations did not find a valid 537-word.
Their exploratory logs and solver cores are not used as proof here.
The construction search should preserve a compatible low/tail pair during
coordinated changes, rather than rely on a small number of base defects.

## Encoding and certificates

For length 83, use variables `X[i,c]` for 83 positions and five colours.
There is an at-least-one and pairwise at-most-one family at each position.
For `j-i=d<=77`, add `not X[i,u[d]] or not X[j,u[d]]`.
Decoding is exactly the displayed distance condition in both directions;
there is no symmetry breaking, omitted colour, or additional constraint.

The formula has **415 variables and 4,301 clauses**. Its SHA-256 is
`da79de45fb932edacfbaaa50b6528f118ca7da4d5462c6bca52375ccab7d18a9`.
The independent [audit.py](audit.py) imports neither generator nor solver
and matches every clause to a separate endpoint-first traversal. It also
checks both prefixes, the compatible blocks, the 237-word, the partial
word's two defects and nonempty lists, and rejection of a corrupted block.
Running that script alone does **not** verify the UNSAT upper bound.

[prove.py](prove.py) regenerates the formula and a Glucose 3 refutation,
runs the semantic audit, and requires `drat-trim` to report `VERIFIED`.
With Python 3.11.2 and `python-sat==1.9.dev15`, the proof has 1,087,155
bytes and SHA-256
`c414cc231592213f8eccad1e0149eafa9aeb7dc106e575f3d0a55daeba85df92`.
Generation and proof checking each took about 0.2 seconds in the recorded
run. The checker used 3,785 of 9,257 lemmas, 84,064 resolution steps and
no RAT lemmas. Runtime and proof bytes are provenance, not the theorem.
An accepted proof of the audited formula is the upper-bound gate.

The trust boundary is the explicit data, the finite translation, the
literal Python audit and the independent C proof checker. The solver's
UNSAT return alone supplies no proof. These are author-conducted independent
implementation checks, not external peer review. Proof traces, generated
CNFs, binaries and logs are regenerated locally and are not committed.

## Reproduce

The fixture audit uses only Python 3.11 or later and its standard library:

```sh
sha256sum -c SHA256SUMS
python3 -B audit.py > /tmp/prefix-span-audit.json
diff -u expected.json /tmp/prefix-span-audit.json
```

For the upper certificate, install the pinned Python dependency in a local
environment and build [drat-trim](https://github.com/marijnheule/drat-trim)
at commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, using for example
`cc -O2 drat-trim.c -o drat-trim`. Then run

```sh
python3 -B prove.py --drat-trim /path/to/drat-trim \
  --out-dir /tmp/schur-prefix-span-proof
```

The output directory contains the regenerated CNF, DRUP trace, checker log
and concise result. Success requires the full semantic audit, the explicit
82-position witness and the independently checked 83-position refutation.
