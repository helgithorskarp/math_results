Exact computer-assisted construction lemma and stopping result.  Start with
the independently reviewed 343-point opposed-B214 physical source S343.  Its
complete strict unit graph has 1,782 edges and, after fixing a Golomb unit
triangle to colours 0,1,2, exactly 66 extendible complete Golomb four-colour
patterns.

The declared finishing class is finite and frozen before evaluation.  For
every unordered pair p,q of S343 points with squared distance 16/9, adjoin
both common unit neighbours

    (p+q)/2 +/- (sqrt(5)/4) R(q-p),

where R(x,y)=(-y,x).  There are exactly 54 such centre pairs and the 108 new
points are distinct and outside the old coordinate field.  Collision merging
and complete exact all-pairs reconstruction over the eight-dimensional
rational basis

    1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)

give a 451-point, 2,170-edge strict plane unit-distance graph.  Its edge
decomposition is 1,782 old--old, 216 old--new, and 172 new--new edges.  Every
new point has exactly two old contacts; the new-vertex degree histogram in the
complete graph is 4:44, 5:24, 6:16, 7:24.  The graph has no articulation and
no bridge, so the interaction is not a one-vertex attachment.

Nevertheless every one of the 66 complete S343 Golomb inputs extends.  The
certificate contains and the verifier checks one literal 451-colour word per
input, so the projected relation is unchanged.  The verifier also replays the
source's 1,382-lemma RUP proof excluding the other 29 normalized Golomb
patterns.  Because the support contains the Golomb graph and has a checked
proper four-colouring, its chromatic number is exactly four.  It is not a
five-chromatic candidate.  Under the campaign's predeclared unchanged-relation
gate, this closes precisely the full squared-distance-16/9 two-lens layer on
S343 and banks S343; it does not classify other distances, selected signs,
larger layers, or arbitrary additions.

Public source and proof:
https://github.com/helgithorskarp/math_results/tree/8a98d34290f4ba578a28ae69aa1edb8fe7399d85/hadwiger_nelson_opposed343_sqrt5_lens_stop

Verifier:
https://github.com/helgithorskarp/math_results/blob/8a98d34290f4ba578a28ae69aa1edb8fe7399d85/hadwiger_nelson_opposed343_sqrt5_lens_stop/verify.py

Reproduce from a complete checkout with Python 3.11 or later:

```text
python3 -B hadwiger_nelson_opposed343_sqrt5_lens_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_opposed343_sqrt5_lens_stop/verify.py --check-expected
python3 -B hadwiger_nelson_opposed343_sqrt5_lens_stop/controls.py
python3 -O -B hadwiger_nelson_opposed343_sqrt5_lens_stop/controls.py
sha256sum -c hadwiger_nelson_opposed343_sqrt5_lens_stop/SHA256SUMS
```

Mathematical-package commit:
8a98d34290f4ba578a28ae69aa1edb8fe7399d85.  The point, edge, centre-pair,
and positive-witness-stream SHA-256 values are respectively
08e1d57663aa5a899dc68a0c2aad6eee6259f57893fb1a4965a383e97b638a42,
1227a8ac0e8357e7fd2587778b8585eb1e00a3eb6d0ec834984a4e1bb45f521a,
e54d4e57082e4c7912296db675033fb1352449552f4d8f691fac56ca8b7df0e4,
and 56689692bb41fc21db293612d7111db12e206d4ae72803c286008036a6c6753d.

This is author-side exact evidence and a scoped negative construction result,
not an independent review, a global exclusion, a sub-509 five-chromatic graph,
or record progress.  Parts' 509-point/2,442-edge construction remains the
supported unrestricted record comparison:
https://arxiv.org/abs/2010.12665 .
