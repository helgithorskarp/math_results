# Exact packing total chromatic numbers of all cycles of order at least 14

For every `n >= 14`, the packing total chromatic number of the cycle is

```text
chi''_rho(C_n) = 10,  if n is 14 or 16;
                 8,  if n = 27*a + 53*b for integers a,b >= 0;
                 9,  otherwise.
```

This closes the cycle problem posed by Jasmina Ferme and Daša Mesarič Štesl,
*On packing total coloring*, arXiv:2508.08691v2 (2026),
<https://arxiv.org/abs/2508.08691v2>, in the range `n >= 14` emphasized in
that paper.  The arXiv source was checked again on 2026-09-20 and was still at
version 2.

## New common-base construction

Order the elements of `V(C_n) union E(C_n)` as

```text
v_0, e_0, v_1, e_1, ..., v_(n-1), e_(n-1).
```

The total graph in this ordering is `C_(2n)^2`.  A word of length `2n` is
therefore a packing total coloring precisely when consecutive cyclic
occurrences of color `i` are separated by at least `2*i+1` word positions.

For colors `1,...,9`, record the capped ages since their last occurrences,
with caps

```text
(2,4,6,8,10,12,14,16,18).
```

The certificate uses the single state

```text
s = (2,3,6,8,7,12,1,4,0).
```

The words in `certificate.json` give closed walks from `s` back to `s` of
length `2n` for

```text
n = 17 and every n in {23,24,...,39}.
```

Closed walks based at the same state may be concatenated.  Consequently,
strong induction gives a common-base closed walk for every `n >= 23`: the
orders 23 through 39 are the base interval, and for `n >= 40` append the
order-17 loop to a loop for `n-17 >= 23`.  The five standalone cyclic words
for orders 18 through 22 complete the upper bound

```text
chi''_rho(C_n) <= 9 for every n >= 17.
```

This is an infinite construction, not a cutoff census.  The transfer search
used to discover the words is not part of the proof's trust boundary.

## Exactness

Two earlier independently checked results in this repository supply the lower
bounds:

- [`packing_total_cycles_c14_c26`](../packing_total_cycles_c14_c26/) proves
  `chi''_rho(C_14)=10`, `chi''_rho(C_15)=9`, and
  `chi''_rho(C_16)=10` (as part of its exact finite table).
- [`packing_total_cycles_8color_semigroup`](../packing_total_cycles_8color_semigroup/)
  proves that, for `n >= 14`, an 8-coloring exists exactly for
  `n in <27,53>`, and also proves the universal lower bound 8.

Thus a non-semigroup order `n >= 17` needs at least 9 colors and the new
construction uses 9.  Semigroup orders have exact value 8.  Together with the
three small exact values, this proves the displayed formula.

## Verification

Run

```bash
python3 verify.py
```

The checker reads the certificate, tests every cyclic separation directly,
checks every claimed common-base return, and constructs and rechecks all
orders from 17 through 2000 as a regression test of the induction.  Expected
output is

```text
verified 18 common-base loops and 5 standalone words
verified the common-base induction for every order 23 through 2000
therefore every C_n with n >= 17 has a 9-color packing total coloring
combined with the cited exact lower bounds: the n >= 14 formula follows
```

Only Python integer/list/dictionary operations and the JSON parser are used.
The mathematical trust boundary is the elementary reduction
`T(C_n)=C_(2n)^2`, direct word checking, common-base concatenation, strong
induction, and the two explicitly cited prior results.  No solver, random
choice, floating point, graph enumeration, or unverified external dataset is
used by the checker.

The formula appears new relative to the cited primary source and the
Discovery Net neighborhood checked through 2026-09-20; no claim of historical
priority is made.
