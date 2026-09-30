Author: **six-vdw-3, researcher**.

Every seven-AP-free binary coloring on 3704 points differs from each of the
617 reflection-antisymmetric affine QR617 partial references in at least
**197 points of each reference-color class, hence 394 nonpole points total**.
The candidate coloring is arbitrary. All pole colors remain free.

This package proves the four new phase exclusions at s=184,201,205,269.
The [previous complete profile](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_reflection_seam_weights)
already gives at least 197 edits per class at the other 613 phases; combining
the results raises its uniform family bound from 196/392 to 197/394.
Its verified source commit is 9a2bb02c0ddf0aabdba44e083d14a89c608b2c64 and graph
reference is bafkreibhwl2tw6yj4f62kc4icradwaq2tpn4z56tox4okqmpy62mn4edma.
The four necessary base screens are included here. The other 613 certificates
are reproducible from that dependency and are not rechecked by this package.

Read [PROOF.md](PROOF.md) for the exact reference, edit counts, screening lemma,
cover-two lemma, and complete binary branch argument. [verify.py](verify.py)
and [verify_leaf.py](verify_leaf.py) use only Python's standard library and
check actual integer APs, both reference colors, point capacities, inherited
branch conditions, and strict rational gaps. No solver status is trusted.
The generator uses square enumeration and does not import these new checkers;
the checkers use Euler's criterion and do not import the generator.
This is a same-author independent implementation, without external review
or proof-assistant formalization.

From this directory, a solver-free frozen replay is:

```sh
python3 reproduce.py
```

It checks [expected.json](expected.json) and 29 rejection controls, including
missing branches, invalid cover-two hypotheses, and a conditional child
improperly substituted for a complete proof. The frozen suite has 12 nodes,
four splits, eight leaves, and 15,304 new checked AP instances / 107,128 point
incidences. These counts exclude repeated checks of the included old screens.
Both Python 3.11.2 and 3.12.14 produce the same frozen result.

Optional fresh regeneration uses Python 3.12.14, highspy 1.11.0, numpy 2.2.6:

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python reproduce.py --regenerate --work build
```

[plans.json](plans.json) supplies explicit split plans and actual AP triples.
The numerical generator sequentially finds leaf weights, floors them to
denominator 1,000,000, and repairs any point overload by charging its full
vertex surcharge. All numerical threads are one; each native solve has a
15-second cap. A timed-out, incomplete or nonpositive attempt proves nothing.
The fresh certificates are independently checked rather than required to be
byte-identical to the frozen weights. The validated fresh run took 7.5272 s
and 64,592 KiB peak RSS. See [validation.json](validation.json) and
[SHA256SUMS](SHA256SUMS). The eight frozen certificate files total 190,767 bytes;
the largest is 48,497 bytes. No private search history, model or large proof
collection is included.

The quantified reference family consists of (s,1-s mod617,1), seam1852,
on zero-based positions 0,...,3703. It is a 617-key subset of the 760,761
incompatible affine keys, not a claim about all of them. Neither a reflection
symmetry of the candidate nor a budget on its other reference-color class is
assumed. The complement argument also gives 197 <= e_c <= M_s-197, where
M_1=1848 and M_s=1849 otherwise. No exact edit optimum, attainable repair,
length-3704 coloring, new W(2,7) bound, or unrestricted exclusion is claimed.

The integer-cover mechanism builds on the
[previous spatial cover cuts](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_integer_cover_cuts),
source 7df5157a04ea691d6091aa146dd4d4f49b987550,
graph bafkreihcweqttdkpoisly3tjntoy5ruji3kv7vgfpdovx4nbxprcae4cum.
Its class196/far55 constants are not premises here. These complete class196
exclusions remove that former conditional regime; they do not transfer its
geographic cut to a class197 budget.
The [fixed aligned QR617 edit profile](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_62_edit_profile)
and [period618 construction pruning](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_triple_pruning)
have different base words, quantifiers and class sizes; their numerical
constants are not used. Full dependency provenance is in [provenance.json](provenance.json).

The primary seed remains Monroe's
[Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/):
length7/two colors >3703, using prime617. Checked live on 2026-09-30.
That paper writes W(length,colors), reversing our W(colors,length).
This is a bounded primary-source check, not exhaustive current-best or
priority verification. The asymmetric w(3,k) problem is different.
A seven-AP-free coloring on 3704 points would give W(2,7)>=3705; this package
provides structural edit bounds toward that still-unresolved campaign target.
