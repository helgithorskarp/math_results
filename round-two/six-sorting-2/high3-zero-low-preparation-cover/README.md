# Native HIGH3: zero-prior-LOW preparation cover

Actual author: **six-sorting-2, researcher**. Scoped author proof with
separate same-author exact algorithms; external review/formalization pending.

For the literal HIGH3 prefix of length27, assume a size-at-most44 sorter
whose first strict LOW event is singleton with zero earlier LOW merges.
Arbitrary preparation words before that event reduce to **181 full
five-input functions**, represented by words of length at most7. The
complete pruned closure has374 states,193 certified all-suffix free-cut
exits and446 edges. Seven is an output; no word-depth cutoff is used.
The singleton/tail stage and whole target remain open.

[PROOF.md](PROOF.md) proves the normalization and scope.
[certificate.json](certificate.json) gives every full32-input function,
shortest word, edge and actual original-domain cut witness.
[checks.json](checks.json) stores entire normal/optimized records.
[SOURCE-CREDITS.md](SOURCE-CREDITS.md) credits9616/9525/9590 and source pins.

Run here with Python3.11.2, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 generate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O generate.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
```

Expected checker: `WHOLE_ORIGINAL_CUBES_AND_FULL_FUNCTION_CLOSURE_VERIFIED`,
374 functions,446 edges,193 cut exits,181 retained,maximum shortest7;
ten damaged controls reject for intended reasons. Every original clamped
free cube is retained. Producer and checker use distinct algorithms; the
checker imports no producer or profile.

Certificate91,009 bytes, SHA256
`bdfdc23f34cffe622f623d00f4b005d57de1388c307a9662ab93b351c1d37257`.
Producer .844/.867s; checker11.085/11.124s,56,556/58,048KiB.
External55s guards and1CPU2GiB remain unchanged, one serial native thread.
No large lower-bound corpus is needed or replayed; imported S11>=35 and
S12>=39, ordinary bridges and new cover proof remain unformalized.
The unrestricted thirteen-input44..45 gap remains open.
