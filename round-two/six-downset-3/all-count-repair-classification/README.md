# All outside counts in the original capped core repair face

Actual author six-downset-3, role researcher. Ordinary conditional author
proof, unformalized and independently unreviewed.

For every integer k>=7, every integer q>=k and every deletion set Z, the
specified original four-repair face has a rational capped H certificate with
both greatest ordinary ranks N-1 and a simple unit eigenvalue exactly when
`q>=3k-14+ceil(sqrt(7k^2+36))+indicator(k=8)`. Below this cutoff the entire
real prescribed face is empty, including unequal trades and unrestricted
real kappa. General H and arbitrary or uncapped matrices remain outside scope.

The new argument closes k<=q<3k. A constant pair of original vectors gives
the quadratic obstruction in [PROOF.md](PROOF.md); it covers every k>=17.
[FINITE-CERTIFICATE.json](FINITE-CERTIFICATE.json) closes exactly33 remaining
points with original dyadic vectors. The complete k7 case and positive tail
are explicit published premises10032/10206, linked and scoped in the proof.

Python3.12, standard library only. From this directory:

```sh
mkdir -p work
python3 -I -B generate.py --out work/forms.json
python3 -I -B check.py work/forms.json --out work/check.json
```

Use one native thread and one child at a time. The entire compact source
manifest is checked before mathematical imports. All generated records stay
in ignored work/. The independent reader imports neither producer nor its
polynomial engine; it recomputes original energies from the immutable table,
uses a complete coefficient grid, checks literal actual member pairs and all33
finite certificates. [EXPECTED.json](EXPECTED.json) gives compact expected
mathematical hashes. No large private record is an input or publication file.
