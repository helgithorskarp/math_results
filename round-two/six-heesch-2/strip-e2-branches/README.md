# Six strip-contact exclusions and an E2 cover reduction

Actual author: **six-heesch-2**, role **researcher**.

For every integer `k >= 6`, six explicit registered pair contacts of the
unmarked polyhex strip `T_k` are outside its local domain `E1`. Together with
the previously published forced half-turn, these leave exactly two possible
suppliers of one halo cell in any `E2` cover of the contact `(I;6,4-k)`.
See [the precise statement and ordinary reduction](proof.md).

From a checkout of this repository, using Python 3.11 or later:

```sh
python3 round-two/six-heesch-2/strip-e2-branches/verify.py
```

The command runs six **serial** jobs: two generators and a search-free reader
in normal and optimized Python. It verifies all parameter classes, including
the unbounded tails, and rejects 18 deliberately damaged certificates in each
reader mode. `expected.json` pins the seven published dependencies, the local
source, and the three mathematical output hashes. No solver or third-party
Python package is needed. Generated evidence stays in the ignored `generated/`
directory; no external proof corpus is required.

The three finite packing DAGs have 2, 3, and 3 nodes. The three supplier trees
have 4, 4, and 3 nodes. The two remaining E2 supplier poses are
`(-1,0,-1,1;7,5)` and `(2,-3,1,-2;3k+6,2k+5)` in the coordinates of `proof.md`.

This is an author-checked, unformalized local lemma, independently unreviewed.
The affine/height kernels are shared; endpoint sweeps, certificate replay, and
materialized point-alignment checks are separate implementations. Neither
remaining branch is excluded. A full E2 inclusion, a global Heesch upper bound,
and the finite unmarked polyhex Heesch-five target remain open.
