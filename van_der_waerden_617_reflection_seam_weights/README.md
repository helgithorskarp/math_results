Author: six-vdw-3, researcher. This directory gives an exact weighted AP
packing bound for all617 partial affine QR617 references
(s,1-s,1) on{0,...,3703}, seam1852. Every arbitrary binary coloring with
no monochromatic nonconstant seven-term integer AP must change at least
196 nonpoles of EACH reference color, hence at least392 nonpoles in total.
All pole colors are free. The candidate need satisfy no reflection condition.
The all-incompatible-key domain has760761 keys; this result covers the617
reflection-antisymmetric references specified above. It does not give a
length3704 witness or a new bound for W(2,7), and it claims no edit optimum.

Read [the proof](PROOF.md), [checked counts](expected.json), and the
[independent verifier](verify.py). The verifier uses only the Python standard
library and trusts no solver. The generator uses Python3.12.14,
highspy1.11.0 and numpy2.2.6; the exact checker also runs on Python3.11.2.

For a complete fresh reproduction, create a work directory outside source
publication paths and run one CPU job with all numerical threads set to one:

```sh
python3.12 -m venv /path/to/scratch/work/venv
/path/to/scratch/work/venv/bin/pip install highspy==1.11.0 numpy==2.2.6
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /path/to/scratch/work/venv/bin/python reproduce.py --work /path/to/scratch/work/certificates
python3 verify.py /path/to/scratch/work/certificates --require-complete
```

The native guidance limit is15 seconds per phase, with sequential child
processes and no nested worker pool. No host, account or resource limits
are changed. `--budget 60` produces a bounded resumable prefix; run the same
command without a budget to resume. A prefix is marked incomplete and
proves bounds only for its explicit phase set. The directory verifier with
`--require-complete` fails unless all617 exact phase certificates are present
and pass. It checks every listed AP, not just aggregate counts.

For a short check without installing a solver:

```sh
python3 verify.py example.json
python3 controls.py example.json
python3 arithmetic.py
```

These commands check one compact phase certificate, sixteen rejection
controls, and all 617 reference reflections and class counts. The complete fresh run took 795.474 seconds with 53696 KiB peak child RSS.
The complete 9,855,886-byte generated proof collection is deliberately omitted;
generation code and compact expected counts are published. See provenance.json
for dependencies and validation.json for measured resource use. `expected.json`
describes the validated run rather than proving optimality of the LP or edit
problem. On another numerical platform, newly regenerated weights must pass
the exact checker and meet the stated integer bound. A failing or weaker
regeneration is not a nonexistence theorem.

The previous all-incompatible-key132-edit transfer is complementary:
https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_seam_dilation_transfer
The present proof imports no numerical packing premise from it. The
fixed aligned QR617 repair-distance family and the period618 construction
family studied nearby quantify different words and have separate bounds.

The primary seed is Monroe's Table1, length7/two colors>3703, with prime617
in Table2; that paper writes W(length,colors), reversing our W(colors,length).
This is a bounded primary-source check, not a claim of exhaustive current-best
status. A coloring on3704 points would establish W(2,7)>=3705, not its exact value.
Primary source:
https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/
