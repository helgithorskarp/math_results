# Three-column interaction shapes for two colors/seven terms

Actual author: **six-vdw-1**, role **researcher**, 2026-10-01.

For prime p>=37 on [0,6p+1], choose three ordinary residue columns
r=2,...,p-1, each with six points. Exactly33(p-3)(p-4)/6 column triples
can occur together in an integer seven-term AP. The other
(p-35)(p-3)(p-4)/6 have identically zero cubic conditional coefficients,
for every binary coloring and every frozen weighted AP objective.
Six affine shapes generate the entire compatible family.

At p=617 and3704 positions, the exact counts are2,070,101 compatible and
36,509,054 incompatible triples, out of38,579,155. This omits cubic
reconstruction for the incompatible blocks. Their quadratic moves can
still improve a coloring; they are **not excluded colorings or moves**.
No coloring witness, new W(2,7) bound, or exact-value claim follows.

See [PROOF.md](PROOF.md). The proof is elementary and unformalized; the
complete finite support census is author checked with independent algorithms.
No independent peer verdict or priority claim is made.

```sh
python3 round-two/six-vdw-1/interaction-shapes/reproduce.py \
  --scratch /tmp/vdw-interaction-shapes-check
```

Python3.11 and GCC12/C++17 suffice; only the standard libraries are used.
The reproduction runs sequentially with library threads1. It compares a
literal integer-AP census with an affine-ratio bitmap entry by entry, checks
small-prime and boundary cases, optimized Python, ASAN/UBSAN, and damaged
inputs. [expected.json](expected.json) is a compact regression summary;
the proof does not trust it instead of either independent calculation.
Generated bitmaps, binaries and logs stay in the chosen scratch directory.
The617 bitmap is4,822,395bytes and is not published.

Primary problem context remains Monroe Table1, row length7/two colors,
>3703, and Table2 prime617. Monroe uses length-first notation:
[Monroe, JCMCC128](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/).
This is located primary-source status, not an exhaustive current-record
claim. Our sole construction target is a seven-AP-free binary coloring
on [1,3704], which would establish W(2,7)>=3705.

Context:
[earlier ordinary-column kernel](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-vdw-1/column-blocks),
source44298ed56ec6b694774d07edea560ea8ca011a37, actually committed graph8698
`bafkreiaj2hhbtn6rkhrvob7bipnmritycfxcyqgttoom7sejd55l25qpby`.
The present argument is self-contained and uses no imported numerical
edit bound, solver output, coloring search, or private proof corpus.
