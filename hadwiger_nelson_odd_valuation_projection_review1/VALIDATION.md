# Validation record

- Verdict: **ACCEPT with high confidence**.
- Mathematical target: `bb69773f6a25827ea035c65978ad5a19303136ac`.
- Target release: normal and optimized exact replays of `verify.py`,
  `controls.py`, and `filter.py` passed; the target manifest passed.
- Independent release: normal and optimized replays passed byte-for-byte.
- Physical realization: 474 distinct points, 1,953 complete unit edges,
  112,101 unordered pairs, two independent exact metrics agreeing everywhere.
- Proper colouring: regenerated four-colour word checked on every unit edge.
- Placement inputs: 646 source edges and 16 nonzero base bridges; their stated
  arithmetic product is 41,344 raw oriented/chiral placements.
- General controls: 450 norm-one vectors, 450 projection-norm checks, 1,350
  translated colour checks, six odd-valuation field presentations.
- Negative control: the even-valuation `D=5` projection failure is reproduced.
- Frontier: all 1,490 classes independently regenerated; complete normalized
  inventory hash matches; 1,406 sufficient whole-field exclusions and 84
  undecided classes reproduced.
- Environment: CPython 3.11.2, standard library only.

Limitations: no five-chromatic construction, sub-509 record, or global bound
is produced. The 84 survivors belong only to the archived A159 origin-pencil
family and have no certified non-four significance. The infinite theorem is
an unformalized written proof. One hash-pinned prior independent arithmetic
module and the shared source-coordinate data remain in the trust boundary.
