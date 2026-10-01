# Pair-parity ladders and derivative cuts for period 618

**six-vdw-3, researcher**, round two, 2026-10-01.

For the separable construction
`c(t)=u(t mod103) XOR 000111(t mod6)`, seven-AP avoidance is exactly a
four-edge not-all-equal condition on pair parities. The [proof](PROOF.md)
gives a complete graph-cut encoding and an infinite-family cyclic-run
obstruction. At 103 columns, every nonzero shift distance of a valid
orientation must be **even and between 28 and 76**, and both orientation
classes must have **at least 17 points**.

If the one-set has size 17, each nonzero difference occurs at most three
times, and at least 68 shifts attain distance 28. This is a precise
remaining cohort, not a classification or an existence assertion.

The model uses **5253 edge variables and 31110 CNF clauses**, or 5151 XOR
equations together with 10506 ordinary clauses. Its cut assignments cover
all `2^102` complement-normalized orientations; the ladder clauses impose
the full cyclic condition. Fewer clauses with more variables does not
promise a faster search.

This is a new structural restriction on an unresolved construction family.
The separable family at 618 remains open. No length-3704 witness, new lower
bound, exact value, or unrestricted exclusion for `W(2,7)` is claimed.
Here `W(2,7)` always means two colors and seven terms.

## Reproduce

Requires CPython 3.11 or newer, standard library only. From any directory:

```sh
python3 round-two/six-vdw-3/parity-ladders/reproduce.py \
  --workdir /tmp/parity-ladder-reproduction
```

Expected status: `VERIFIED_PARITY_LADDER_REPRODUCTION`, two successful
normal/optimized checks, model SHA256
`1a0e530403d4ec844d4988ba5e842a8a5582ed09f63a3e7eac6f595762fb659f`.
The work directory contains the regenerable DIMACS model and checked output;
they are omitted from Git. Each child runs serially with one thread and a
45-second bound. Timeout or failure halts reproduction and proves no
exclusion. The mathematical derivative cut is a written proof, not a
solver verdict.

To generate the model and run only the independent checker:

```sh
python3 round-two/six-vdw-3/parity-ladders/generate.py --output /tmp/ladder103.cnf
python3 round-two/six-vdw-3/parity-ladders/check.py \
  --model /tmp/ladder103.cnf \
  --fixture round-two/six-vdw-3/parity-ladders/q23.json
```

The checker imports neither the generator nor a solver. It compares every
model clause against a full-directed-step reconstruction; exhausts all 128
local seven-bit assignments; compares individual cyclic product words and
pair ladders on all **70720** normalized words at q=7,11,13,17; rejects six
corrupt models; and checks an actual interval obstruction to the extremal
103-column pattern. The [q23 fixture](q23.json) is a small positive control,
checked term by term on all 18906 cyclic pairs. The q=7 fixture shows why
the infinite-family extremal proof has a size hypothesis. These small
templates are validation, not improved records or claimed new constructions.

The classical length-3703 QR617 seed is independently reconstructed using
squares and checked on all 1140833 integer APs. Its canonical word, including
a newline, hashes to
`442f563bc6e1ae75d9666a3417e1246e413c83393777dd22ac0bc730d0f4759a`.
This reproduces existing mathematics.

## Prior work and scope

[Monroe, JCMCC128, Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
gives the located symmetric incumbent `>3703` and prime 617 without a
zipper marker. Monroe uses `W(length, colors)`. The primary construction
context also includes
[Herwig--Heule--van Lambalgen--van Maaren](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Heule's pre-partition methods](https://www.cs.utexas.edu/~marijn/publications/JOC_08_03_A01.pdf).
Bounded current searches did not locate a newer symmetric witness or this
specific derivative obstruction; no priority claim is made.

The application to the residual constant skeleton uses the existing
[period-618 normal form](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_phase_symmetry)
and [binary-fiber reduction](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_binary_fibers).
The [affine symmetry result](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_affine_reduction)
explains why this family is also the residual nontrivial symmetry case.
Exact graph references and the proof's dependencies appear in [PROOF.md](PROOF.md).
Reproduction needs no sibling directory or external evidence.

The trust boundary is the elementary unformalized proof and exact
standard-library source/interpreter checks. These separate implementations
are by the same researcher; no independent peer review or formalization is
claimed. The unrestricted target remains a binary coloring of `[1,3704]`
with no monochromatic nonconstant seven-term AP.
