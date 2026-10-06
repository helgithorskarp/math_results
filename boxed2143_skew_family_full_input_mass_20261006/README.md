# Exponentially small full-input mass of a recursive skew family

Lyra / literature-researcher-2, with a complete different internal check
by Quinn / literature-researcher-3, 2026-10-06. This is a partial result
inside the boxed2143 growth problem. The author/checker exchange was
completed as864/869/874/877/890/913. These are internal team checks.

For boxed2143, positions i<j<k<l have values p[j]<p[i]<p[l]<p[k],
and no unselected point lies in the open rectangle (i,l) x (p[j],p[k]).
The upper value is the THIRD selected point. Let P_h be the FULL avoiding
fiber of the perfect ordered maximum-Cartesian tree of height h,
m_h=2^h-1, and w_h=|P_h|. The source law is uniform on EVERY ordered pair
in P_h x P_h, each of probability1/w_h^2, without output reweighting.

Set F_2={132,231} and, with d=2^(h-1)-1, define

    F_h={(d+alpha),2d+1,beta : alpha,beta in F_(h-1)}, h>=3.

The full descending-band join preserves boxed avoidance, perfect shape
and the ordered source decoder. Thus w_(h+1)>=w_h^2 for every h>=1.
The included43 distinct valid size-seven seed words give w_3>=43,
hence w_h>=43^(2^(h-3)). The family has exact cardinality
f_h=2^(2^(h-2)), and consequently, for EVERY h>=3,

    Pr_(uniform P_h x P_h)(F_h x F_h)
       = f_h^2 / w_h^2
      <= (4/43)^(2^(h-2))
       = (4/43)^((m_h+1)/4).

The complement therefore has mass at least1833/1849. Membership of43
distinct seed words is enough for these uniform bounds; completeness of
the seed list is not required. If using the previously established exact
w_3=43, the boundary family mass is16/1849. The finite verifier here
checks LOWER supply only and does not verify that old completeness claim.

This pays for excluding this specified family. It supplies no distinct
recoverable gain on the complement, growing full-input mean, exponential
upper bound for all avoiding permutations, or proof of unbounded roots.
The full target is to decide whether one finite C>0 satisfies a_n<=C^n
for all n>=1, or limsup a_n^(1/n)=infinity. It remains unsolved in this
campaign. No ordinary growth limit, novelty or external peer review is
asserted by this source publication.

## Proofs and exact scope

`author/author_proof864.md` is the immutable original full argument.
`review/uniform_proof_before_control.md` and `review/entire_review877.md`
contain Quinn's complete independent all-size reconstruction and whole
verdict. `author/acceptance890.md` records the actual whole author reading.
Their historical pending labels describe those files' writing stages;
the completed exchange above supersedes the author-acknowledgement stage.

The additional mean-contribution formula in those documents is explicitly
an implication ASSUMING the separate ALL-family join upper
N(alpha,beta)<=3*2^(h^2+3h). That upper theorem is not supplied or certified
by this directory, and a single fixed-pair bound would not suffice.
The unconditional mass/complement theorem needs none of that premise.
Its proof depends on the full-box join injection and the finite43-member
lower supply documented here; no omitted1903-record threshold certificate
or1849-pair join table is needed to establish those two conclusions.

## Reproduce the compact seed check

Use CPython3.11.2 and its standard library, one process/native thread.
From this directory run once with a fresh output path:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B verify_seed43.py --out /tmp/boxed2143-mass-seed43-replay
```

This portable entry point calls the UNCHANGED mathematical functions from
Quinn's original6385-byte `check_seed43_mass864_v1.py`. It removes only
the need for private campaign packet/receipt files at the entry-point
layer. `check_seed43_mass864_v1.py` itself is preserved verbatim as proof
computation provenance; its original `--packet` entry needs that omitted
campaign metadata and is not the public reproduction command.

The command checks precisely43 existing length-seven words, all1505
four-index choices, complete literal box lists, perfect heights and leaf
sets. Every43 corresponding record field must match the included compact
certificate. It verifies the four F_3 words are in the same supply and
the exact rational bounds16/1849 and1833/1849. There is no5040-permutation
recensus,1849-pair/old-DP replay or larger input domain. The internal cap
is10 seconds; cap/failure is explicit, never a partial success.

Expected canonical certificate:5107 bytes, SHA256
bef94fd6d7f955914196dc811d893f6fe67939d783cd2024fa58e4a2e460dd61.
`evidence/original_quinn_report.json` preserves the old complete independent
control's observations. The portable replay report has new source/entry
provenance and its own timing; it does not reproduce the original clocks.

Run `python3 -B verify_source.py` for source-file SHA256/size integrity.
That command is metadata only and does not prove any mathematical theorem.
The infinite-height proof needs checking separately from the1505-test
certificate. Bulky cumulative receipts, checkpoints, raw1903-output data,
keys and private node state are deliberately outside this public package.
