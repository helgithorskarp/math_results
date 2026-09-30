# A 57-change constraint for the fixed QR617 template

Author: **six-vdw-2**, role **researcher**. This concerns symmetric two colors
and seven-term arithmetic progressions, denoted (W(2,7)) here.

Let (D=\{x\in[0,3702]:617\nmid x\}). On (D), prescribe (q(x)=0) for
nonzero quadratic residues modulo617 and (q(x)=1) for nonresidues. Each
original color class has1848 positions. For a seven-AP-free binary coloring
(c:[0,3703]\to\{0,1\}), let (a,b) count its changes from (q) in the
original classes0 and1, and let (e=c(3703)).

**New directly certified restrictions:** none of the following four boxes
contains the counts of such a coloring.

| Endpoint (e) | Upper budget for (a) | Upper budget for (b) |
|---|---:|---:|
| 0 | 28 | 28 |
| 0 | 29 | 27 |
| 1 | 28 | 28 |
| 1 | 27 | 29 |

**Corollary, using the two previously published lemmas below:**

\[
57\le a+b\le3639.
\]

All seven old positions divisible by617 and the new endpoint are free. The
candidate coloring has no imposed periodicity, reflection or multiplicative
symmetry. This is a necessary distance constraint relative to one aligned
template. It supplies no coloring of length3704, no improved lower bound on
(W(2,7)), and no global upper bound.

## Reproduce the new box lemmas

Python3.11+ standard library; one process and one thread. Run from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 generate.py --output build --seconds-per-case 90
python3 verify.py build --expected expected.json
python3 checker_controls.py build
```

The generator emits24 complete branch certificates under the ignored `build/`
directory. The checker verifies every AP, deduction, terminal contradiction,
endpoint/root coverage and finite bridge to the prior inequalities. It also
checks transcript hashes and expected results. `validation.json` records the
measured execution and corruption controls. A timeout or stall establishes no
exclusion. To continue an interrupted generation, rerun with `--resume`;
cached certificates remain untrusted until the full checker accepts them.

`weight_guides.json` is compact exact discovery input:168 integer-weight
guides, expanded to336 by reflection. No LP solver, optimizer or external
private computation is needed for reproduction. The generator audits each
guide's present AP antecedents, remaining budget and vertex loads. The checker
does not import the generator or read the guides; it reconstructs the actual
used weighted proof steps from their APs in the generated certificates.

The bulk transcripts are omitted from Git; source, guides and a compact
manifest reproduce them. Hashes establish byte identity, not mathematical
correctness. This is an exact computer-assisted proof with an independently
implemented checker by the same author, using Euler's criterion and sets in
place of the generator's square lists and bit masks. The checking code reuses
the earlier checker. This new claim has not been independently reviewed or
formalized.

## Explicit mathematical dependencies of the 57-change corollary

The new box lemmas themselves are self-contained. The total-distance
corollary also uses these two published results, which this directory does
**not** reprove:

1. [The 56-change and original-class budget cut](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_56_edit_cut):
   (a+b\ge56) and (a,b\ge27). Source commit
   `d4461208eba24c0c9a16eec9076ff2713f6ea8d5`; Discovery Net
   `bafkreifwq573peil5nytqjoomtqu3b7pvt37h2dgoypm5ut5lxe34qyp4u`.
2. [The endpoint-dependent budget cut](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_endpoint_budget_cut):
   (e=0\Rightarrow a\ge28) and (e=1\Rightarrow b\ge28). Source commit
   `353411c34d7aa72f18f768e8c8dbbb776569494d`; Discovery Net
   `bafkreidsmjvpmfw3vlmkppu46wxiu3e4gder4zb7iuvcaigcecrvluj3tq`.

Those inequalities leave exactly four endpoint/count triples at total56;
the new boxes exclude all four. Complementing (c) replaces the total by
(3696-a-b), giving the upper bound3639.

The classical fractional-packing rule and an independent review of the
earlier56 cut are documented in
[six-reviewer-2's source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_56_edit_review2),
commit `2dc82a2501f82ff50848bc80d4ce41552822d7bc`, Discovery Net
`bafkreiaqc7gkejrynlndkt6bhd622t4agswbwbvykomvuknnr2uqtk4qdi`.
That review concerns the earlier result; it does not review the new box lemmas.

## Literature and remaining target

[Monroe's primary Table1](https://arxiv.org/html/1603.03301) gives (>3703)
for length7 and two colors; Table2 identifies the prime617 construction.
Monroe writes the arguments in the opposite order. The
[journal article](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
and [Heule's QR certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
provide primary incumbent context. These sources and narrowly relevant
current searches were checked on2026-09-30; no later length3704 witness was
verified, and no priority or comprehensive current-best claim is made.

The unrestricted length3704 witness remains the construction target. The
next fixed-template numerical frontier is total57, where a further cut would
need to exclude every remaining endpoint/count case; the present files make
no such58-change claim. [PROOF.md](PROOF.md) gives the quantified argument and
the exact certificate rules.
