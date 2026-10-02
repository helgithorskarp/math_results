# Independent audit of the XOR618 character repair bound

six-reviewer-4, independent mathematical reviewer. [REVIEW.md](REVIEW.md)
confirms committed LEMMA9659's sixteen-column obstruction and103 root
cuts. Proved refinements: sufficient integer prefix2460, illegal phase
prefix2163, exact1685-representative parity catalogue, and the correlation
formula for every zero-to-three-hole mask. No repair optimum, sufficient
repair, unrestricted coloring exclusion or new numerical W bound.

CPython3.12.14, standard library only. From this directory:

```bash
python3 -B verify.py --work /tmp/character-parity-audit-normal
python3 -O -B verify.py --work /tmp/character-parity-audit-optimized
```

Use fresh work directories. All three independent kernels and six semantic
controls run serially, with native threads1 and fixed20-second guards.
Every generated mathematical byte is compared with [RESULTS.json](RESULTS.json),
[CONTROLS.json](CONTROLS.json) and [CORE.json](CORE.json).

Optional original source comparison and unchanged both-mode replay, from
an authorized repository checkout containing the sibling author packet:

```bash
python3 -B verify.py --work /tmp/character-parity-audit-complete \
  --author-packet ../../six-vdw-3/character-parity-repair618
python3 -O -B verify.py --work /tmp/character-parity-audit-complete-O \
  --author-packet ../../six-vdw-3/character-parity-repair618
```

[AUTHOR_SOURCE.json](AUTHOR_SOURCE.json) pins all11 expected author files
at41caf6cbc7670e15486da381059666c96df1dfe4. The optional branch reads these
files only after the independent work is complete and runs the unchanged
author reconstruction, which itself checks both modes. It compares the
entire [COMPARISON.json](COMPARISON.json) and [FINAL.json](FINAL.json).

[algebra.py](algebra.py) derives the inverse by binary cyclic polynomial
Euclid and covers all symmetry orbits. [full.py](full.py) repeats the
physical inverse product and all171802 inputs without importing the algebra
kernel. [physical.py](physical.py) checks actual APs, all64 phase rows,
all63036 affine/phase parameter sets, positive integer lifts and repeated
modular terms. [controls.py](controls.py) checks damaged inputs and all712
distance/correlation cases. Ordinary bridges are proved in REVIEW.md and
remain unformalized. Python and source execution are explicit trust.

Large generated orbit registries/transcripts and operational run data stay
in the specified work directory. Compact inverse, histogram, positive
parity witness and complete expected records are included here. Shared
signing identity does not establish separate mathematical authorship.
