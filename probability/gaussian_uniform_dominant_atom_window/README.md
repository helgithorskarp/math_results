# A uniform dominant-atom middle certificate

At unit Gaussian variance, let a law have an atom of mass at least
`1-2^(-21)`, with its whole support within unit distance of that atom.
For **every** contraction of that law,
the [author proof](PROOF.md) signs all normalized thresholds
`u>=2^(-11)` and proves

```
H_target(u)-H_source(u) >= (mean squared-distance loss)/2^24
                         for 1/2048 <= u <= 1/4.
```

The remaining mass may have any bounded atomic or nonatomic law. There
is no minimum rare weight, covariance condition or lower loss floor.
The radius-to-noise ratio is one, outside the prior radius-only window's
hypothesis. A general explicit mass budget is given for any fixed finite
radius and any finite logarithmic threshold interval.

The new ingredient is uniform control of the coarea kernel by its actual
loss, with positivity obtained **after angular averaging**. This makes the
earlier fixed-configuration small-mass result effective uniformly over the
entire bounded rare packet. It covers cases whose first mass variation
vanishes. The exact seven-site control has that property and paired rank
six.

The mass restriction is small and essential to the proof. Thresholds
below `1/2048` remain open, so this does not establish unrestricted full
majorisation or a new Kneser--Poulsen case. Independent review is pending.

Reproduce with Python 3.11 or later, standard library only:

```bash
python3 probability/gaussian_uniform_dominant_atom_window/verify.py
python3 -O probability/gaussian_uniform_dominant_atom_window/verify.py
```

Both commands print [EXPECTED.json](EXPECTED.json), with status
`EXACT_MIDDLE_CONSTANTS_PASS`. All computations use rational arithmetic.
The script verifies the constant chain, perturbation controls and the
finite control; it does not replace the continuum coarea/Abel proof or
claim to sample all thresholds. [SOURCES.md](SOURCES.md) gives the
dependencies and the exact distinction from prior results.
