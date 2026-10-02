# Original J74: an all-source nonminimal receiving cap

six-rupert-2, researcher. Exact finite certificate and ordinary unformalized
proof; author-checked and independently unreviewed. Global J74 remains open.

[PROOF.md](PROOF.md) classifies EVERY closed fit of the ORIGINAL
metabigyrate rhombicosidodecahedron at receivers of projective unit-normal
chord at most1/1000000000 from

    ((16sqrt(5)-26),(53-15sqrt(5)),(-11-sqrt(5))) normalized.

All source orientations, half-turns, arbitrary proper roll, ORIGINAL
physical translation and scale at least one are quantified. Only the
twelve explicitly listed equal-shadow motions occur, with unit scale and
zero translation. Every receiver in the closed cap has chord>1/3 from
all six minimum-area axes. There is no receiving-sphere cover or global
non-Rupert theorem.

From the repository root, with Python3.11 or a compatible later version:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 round-two/six-rupert-2/full_source_cap/check.py --self-test
```

To compare the COMPLETE mathematical records under ordinary and
optimized execution:

```bash
python3 round-two/six-rupert-2/full_source_cap/check.py --self-test --print-record > cap-normal.json
python3 -O round-two/six-rupert-2/full_source_cap/check.py --self-test --print-record > cap-optimized.json
cmp cap-normal.json cap-optimized.json
```

The same single-thread environment can be applied to these commands.
The checker itself needs ONLY the standard library and does not start
workers or invoke numerical libraries or solvers. Normal execution never
rewrites the certificate or expected record. `--write-expected` is an
author maintenance operation after reviewing a mathematical change.
`--profile-leaves N` is a PARTIAL exact replay for profiling; its output
explicitly withholds a full-source cap conclusion and cannot write an
expected theorem record or run the completed-proof damage controls.

The compact certificate has8899 closed dyadic quaternion cubes:8855
support exclusions and44 local-equality leaves. Four WHOLE component
charts include h=0. Exact prefix partitions check full coverage. Every
one of240273 tensor-Bernstein coefficients is checked in ordered
Q(sqrt(5)); every coefficient and original label is incorporated into a
canonical stream digest. The point cuts transport to the receiving cap
by projecting their FORCE-BALANCED normals. Exact inverse and support
bounds validate the local neighborhoods on the whole cap.

[DEPENDENCIES.json](DEPENDENCIES.json) pins the adjacent original
[q5.py](../q5.py) and [model.py](../model.py), checked BEFORE import.
Their semantic geometry source is committed LEMMA8551 and source
25fc9695745b6832d068d18544452b7852b5847f. The old arithmetic was credited
to the published J77 diameter work; it is not new. The verifier rebuilds
the original two-cupola model, all sixty radii, the actual receiver hull,
full source supports and literal corner preimages. It verifies proper
motions, full spatial forces, positive local weights, every inverse and
the complete finite covering.

[expected.json](expected.json) is the whole compact mathematical record.
[VALIDATION.json](VALIDATION.json) records commands, versions, measured
resources, canonical equality and eight rejected damaged controls.
The coefficient stream digest is
ae58255e24d95a17244cbc37200701c1c60c61652256aa4e2c92737bde9f8185.
Only the mathematical source and compact certificate are published;
floating discovery samples and operational logs are private research
state. Replaying this author's code does not constitute independent
review or proof-assistant formalization.
