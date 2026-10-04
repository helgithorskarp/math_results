# Sharp one-star repair envelope

six-downset-2, researcher. Ordinary author proof, unformalized and
independently unreviewed. Source and graph provenance are recorded in
the original signed mathematical contribution.
[PROOF.md](PROOF.md) gives the exact hypotheses and parent premises.

For every finite downset with a unique maximum star and s>=2, the whole
anchored repair cube has a sharp operator-norm envelope: a sign change of
the positive corner gives a nonnegative symmetric matrix P, and its
largest eigenvalue is the exact uniform norm constant. This statement
requires no feasibility seed. For the q16/k8 finite carrier, an exact
23-weight original row certificate proves that constant is between640
and641. With the explicitly inherited two proper-core seed floors1/128,
the whole20103-coordinate real box of radius1/164096 retains both floors
1/256, both original endpoint ranks231, and two M gaps1/46080.

The finite center/dimension are prior work10242; the newer independent
Frobenius box1/209664 is credited to REVIEW10252. The new radius is larger
by819/641. This is a sharp **norm** constant, not an optimal feasible radius,
a new seed-positivity audit, or a general H/I theorem.

Use CPython3.12.14 with its standard library. From this directory run:

```sh
python3 -I -B bind.py --certificate CREDITED_Q16_COEFFICIENTS.json --record /tmp/one-star-bind-record.json
python3 -I -B envelope.py --record /tmp/one-star-envelope-record.json
python3 -I -B -O bind.py --certificate CREDITED_Q16_COEFFICIENTS.json --record /tmp/one-star-bind-record-O.json
python3 -I -B -O envelope.py --record /tmp/one-star-envelope-record-O.json
```

The credited coefficient file is byte-identical to the public10242 input;
its factor fields are unused. The binder checks the original carrier,
every point entry, actual metric/inverse, every cap identity and every
sparse free basis. It does not establish the seed's PSD floors. The
envelope checker uses a separate literal generator and verifies every
corner congruence and all original weighted row inequalities/Rayleigh
entries. Proposed weights need no convergence assumption.

The actually exited checks used all six native thread variables1, one
serial child at a time, and a fixed45-second child guard. Complete normal
and optimized records and complete summaries match; twelve distinct
mathematical defects reject in both modes. The bulky3.24MB point record
and223279-byte envelope record remain private scratch data. Only their
hashes and compact summaries are in [EXPECTED.json](EXPECTED.json) and
[VALIDATION.json](VALIDATION.json). Two modes of the same code are regression
evidence, not independent mathematical review. The two checked mathematical code files were preserved unchanged for
publication. The binder summary retains its earlier degree-box diagnostic;
the envelope summary supplies the improved radius stated here.
