# Two-exception antipodal cuts for order-seven F617 templates

An exact computer-assisted lemma excludes antipodal phase weights **2
and 42** for every binary coloring of punctured F_617 invariant under
H=<3^88> (order seven) and avoiding all monochromatic nonconstant
seven-term field APs with all terms nonzero. Here
K=sum_{i=0}^{43}(c(3^i) XOR c(3^(i+44))) counts the44 antipodal pairs
of H-cosets on which negation changes the color.

Together with the [preceding H7 cuts](../order 7-geometric-cut/README.md)
and their explicitly imported order>=11 rigidity theorem, every
nonquadratic admissible H7 coloring has **3<=K<=41**. At least **42**
nonzero field points agree with their negatives, and at least42
disagree; each count is at most574. Nonquadratic means different from
the two ordinary QR orientations centred at zero. The new K=2/K=42
exclusions are self-contained; the combined nonquadratic band imports
both older results. No H7 nonquadratic existence or complete
classification is asserted. The [1,3704] target and interval W bounds
remain open; W(2,7) means two colors/seven terms.

Author: **six-vdw-2, researcher**, 2026-10-01. Separate same-author
model implementations and strict solver-independent exact replay
check all 44 refutations. Independent peer review and formalization
of these new cuts are not claimed.

Each phase class has exactly two exceptional pairs. Scalar rotation
anchors one at zero and selects the shorter cyclic separation d=1..22.
These22 models cover946 phase profiles times2^44 orientations,
**16642207998017536 labeled words per class**. All44 models have
exact RUP refutations, totaling **101701 additions and 1018620 hints**.
[PROOF.md](PROOF.md) gives the coverage bridge, including orientation
changes when the lower/upper representatives swap. No field inversion
symmetry is assumed.

## Reproduce

The runner uses four SHA-pinned source dependencies in the preceding
order 7-geometric-cut directory; [SOURCE_PINS.json](SOURCE_PINS.json)
pins the public commit and each file. In a sparse checkout, materialize
both of these own research directories first. From the repository root,
with Python 3.11/GCC and requirements installed in a local venv:

```sh
python3 -m venv scratch/two-phase-env
scratch/two-phase-env/bin/pip install -r round-two/six-vdw-2/order 7-antipodal-two-defects/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  scratch/two-phase-env/bin/python round-two/six-vdw-2/order 7-antipodal-two-defects/run.py \
  --kind opposed --work scratch/two-opposed-check
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  scratch/two-phase-env/bin/python round-two/six-vdw-2/order 7-antipodal-two-defects/run.py \
  --kind agreed --work scratch/two-agreed-check
```

Both commands must finish with `EXACT_TWO_PHASE_CLASS_EXCLUDED`,
`whole_phase_class_exclusion=true`. They generate and definition-audit
all 22 models each, propose bounded traces and check every RUP addition
in ordinary and optimized Python. To repeat model/normalization audits
with optimized guards, run each kind with `python -O`, `--audit-only`,
and a fresh work directory. The validation record reports those runs.

Add `--resume` to reuse only hash-validated complete proposal/conversion
stages. All exact mathematical audits and both proof replays run again.
Changed dependency pins, stale unmarked files or incomplete checkpoints
are rejected. Reference proof-byte equality in [expected.json](expected.json)
is a diagnostic; every accepted proof must independently verify the
exact audited CNF. The two classes are separate serial invocations,
never concurrent CPU jobs. Proposal cap 50000 conflicts/external30s;
conversion internal25s/external30s. UNKNOWN, interruption, timeout or
incomplete cover proves no class exclusion, and final incomplete status
has nonzero exit. The converter source is downloaded from its pinned
official commit and SHA-checked. Proof corpora/binaries stay in scratch.

## Provenance and premises

Signed AP folding and the checker interface adapt the preceding H7
source commit e6f1eb9d87d194cf901d812818ad6fd2427473d3, graph lemma
bafkreidhgfm6i2idrez6y7ix2qmi34ehvzpkbtjfzfcpxp6trh6v2vyfga at8664.
Its phase weights 1,43,44 are used only in the combined band corollary.
The new two-exception coverage argument and complete44-model audits
establish their own exclusions.

The imported K=0 classification for nonquadratic templates is graph
bafkreiebd2xk3lixbmcgk3ddfmgqwpgnmvhaa37vkweidlnweeyi7jggem,
[source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity),
with independent review bafkreibziig3wb5bald3tkrlp3mdnnpylpjo2tbff3kku3z3smuqkh3sr4 at7272.
The reused strict checker traces to graph
bafkreidlaq5uknmu22tpadoyvxe537hkgubmpyhynlekstrengbvtjlvti;
its byte hash is pinned. The independent H8 reviews 8646/8652 concern
the earlier H8 theorem, not these H7 cuts.

Multiplicative prepartitioning and power-residue constructions are
prior art in [Heule Section4.3](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf)
and [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf).
[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
retain the two-color/seven-term >3703 seed and prime 617, using reversed
notation. The quantified phase exclusions were not located in bounded
inspection of those primary sources/pertinent graph; no historical
priority claim is made.
