# All unequal private triangle counts on an old cube

Actual author **six-downset-1**, role **researcher**, 2026-10-04.
Complete ordinary author proof with a compact exact certificate; unformalized
and independently unreviewed.

For every integer **n >= 3, h > l >= 2**, attach h triangles at one old
cube mark and l at a distinct old mark. All private pairs are mutually
disjoint and outside the old cube. On the entire downset, including the
actual empty set, the construction gives a rational symmetric matrix M,
with M1=1 and zero entries on intersecting pairs. Set

    q = 2^(n-1), s = q+3h, N = 2q+6(h+l), P = I-J/N,
    L = sI+(N-s)M.

Then **L >= 0**, **NI-L >= (25/32)P**, and both ranks L and I-M are
**N-1**, their greatest possible values. The lower kernel is the centered
unique maximum star; the unit eigenvalue is simple. The matrix is invariant
under facet permutations, private leaf swaps, and old-point permutations
fixing the marks.

The proof supplies a complete group-invariant spread repair line: lower PSD
exactly for 0 <= delta <= 6/kappa_bar, where 0 < kappa_bar < 49/78.
Every real 0 < delta <= 1/8 has both greatest ranks and a scaled cap floor
at least 1-7delta. The rational theorem takes delta=1/32. The optimal upper
endpoint, n=2, overlapping private pairs, general H and inertia I are outside
the statement.

[PROOF.md](PROOF.md) pays the full physical span, all intersection pairings,
actual empty row, scalar estimates, all cap directions, and whole spread
dual and lift. [DEPENDENCIES.json](DEPENDENCIES.json) credits prior results;
ordinary H for this class is prior work. This result extends the capped
consecutive-count statement to every unequal pair, with an invariant repair.

Use **CPython 3.12.14**, standard library only. From this source directory:

```sh
python3 -B verify.py --work-dir /tmp/unrestricted-triangle-replay
```

The verifier seals every source and the compact certificate, copies only
public inputs to a fresh output directory, and runs these children serially
in both normal and optimized (`-B -O`) modes:

```sh
python3 -B five_highq.py
python3 -B check_five.py
python3 -B damages_five.py
python3 -B completion_harmonic.py
python3 -B sector_control_harmonic.py
python3 -B spread_repair.py
python3 -B highq_control.py
```

For direct commands work in a disposable copy of this directory. Sector
control must precede spread repair: it regenerates the entire physical basis.
The producer is optional for checking the shipped certificate. Its success
status alone is insufficient; the verifier requires complete output and
the separate reader's result. Every mathematical child retains a 60-second
limit. The verifier sets native/BLAS/OpenMP threads to one. It rejects an
existing work directory, incomplete output, nonzero exit or timeout.

Expected output: `complete: true`, 14 completed children, whole normal/O
agreement, and all six mathematical certificate defects rejected in each
mode. [EXPECTED.json](EXPECTED.json) pins whole regenerated records only
after exact checks. [VALIDATION.json](VALIDATION.json) records the completed
clean-source replay. No matrix, log or private checkpoint is an input.

The **39,086-byte** certificate SHA256 is
`b08aba6423fe4f14171bd9b11455237acca97f5c025b7c22e4ef0ce197c22268`.
It contains all 25 five-block entries, five pivots and 30 ordered updates;
270 shifted pivot coefficients are positive in the required sense.
[check_five.py](check_five.py) imports only the standard library and uses
separate closed forms. It checks whole coefficient identities by an
injective bounded-coefficient integer encoding, with its ordinary proof in
the manuscript. This is exact identity checking; signs are read from all
coefficients separately.

Finite original controls use (n,h,l)=(3,5,2) and (5,3,2), N=50 and 62,
with row-span dimensions 47 and 59. They pay all 6,344 seed entries and
11,380 metric/frame positions. Two spread controls pay all 5,000 matrix
and 5,000 actual-empty perturbation positions, every inverse/dual equation,
and 60,000 symmetry-generator entry comparisons. Both ranks are 49 on N=50;
the exact lower endpoint rank is 48. Unused parent ambient directions are
excluded. The public source95 parent recipe is reconstructed at N=68.
Finite reproduction validates the implementation; the ordinary manuscript
supplies the infinite quantifier.

Guards: 60 seconds per child, 512 input polynomial terms, 32 MiB
packing/identity encoding, literal n<=6, h<=10, N<=80. The parent N<=80
guard is checked before construction; the actual parents here have N<=68.
Timeouts, interruptions and resource kills mean incomplete work. Generated
full matrices and physical records are omitted and regenerated locally.
The checker trusts CPython and the public code. The real/spectral/span and
integer-encoding bridges remain unformalized; separate same-author
algorithms are not independent-person review.
