# Degree-stratified K4 contact theorem

Call a red/blue coloring of `K_43` **good** when neither color contains a
`K_5`. Fix a monochromatic `K_4`, denoted `Q`, and call its color `c`. For
`j=0,1,2,3`, let `n_j` be the number of the 39 outside vertices with exactly
`j` color-`c` neighbors in `Q`. No outside vertex has four such neighbors,
since it would extend `Q` to a color-`c` `K_5`. Put

```text
t = n_1+n_2+n_3 = 39-n_0.
```

Suppose the minimum color-`c` degree is at least `d`. Each member of `Q` has
three neighbors inside `Q`, so the total number of color-`c` incidences from
`Q` to the outside is at least

```text
n_1+2n_2+3n_3 >= 4(d-3).                         (1)
```

For each `i` in `Q`, consider the outside vertices adjacent in color `c` to
the other three members of `Q` and nonadjacent in color `c` to `i`. Any two
members of this class must have their mutual edge in the other color;
otherwise they and the three vertices `Q-{i}` form a color-`c` `K_5`.
The class therefore has order at most four, since five members would form a
`K_5` in the other color. The four classes partition the vertices counted by
`n_3`, giving

```text
n_3 <= 16.                                        (2)
```

Equations (1)--(2) now give

```text
4(d-3) <= n_1+2n_2+3n_3
         <= 2(n_1+n_2+n_3)+n_3
         <= 2t+16.
```

Hence every prescribed monochromatic `K_4` has at least

```text
t >= 2d-14                                        (3)
```

same-color contacts, or equivalently at most `53-2d` noncontacts. The
classical `R(4,5)=25` degree window gives `18<=d<=24`, producing the seven
exact strata

| lower bound on color minimum degree | maximum noncontacts | minimum contacts |
|---:|---:|---:|
| 18 | 17 | 22 |
| 19 | 15 | 24 |
| 20 | 13 | 26 |
| 21 | 11 | 28 |
| 22 | 9 | 30 |
| 23 | 7 | 32 |
| 24 | 5 | 34 |

The inequalities are sharp at the level of signature populations: the
extremal rows are `(n_0,n_1,n_2,n_3)=(53-2d,0,2d-30,16)`. They are not
asserted realizable as physical good43 graphs.

This argument is the clique-side mechanism already present in the accepted
h3657 nontrivial-separator theorem and explicitly confirmed by its h3667
review. Its application as a degree-stratified interface for every h3887 K4
block is new here. It improves h3899's unconditional contact floor from 19
to 22. On this particular K4 cut it also dominates the newer h3909
maximal-connectivity consequence `t>=d`: equation (3) is stronger by `d-14`
contacts. Thus no large generic connectivity encoding is needed to obtain
the stronger local rule.

## Exact encoding

For every physical vertex, the interface defines threshold variables for
red degree at least `j`, for `j<=25`, by a fully equivalent sequential
recurrence over its 42 incident physical literals. Fixed task edges use the
already true constant variable with the appropriate sign. Units enforce red
degree between 18 and 24; because blue degree is `42-red degree`, this is the
degree window in both colors.

For each color and `d=19,...,24`, a 42-gate conjunction defines whether all
43 color degrees are at least `d`. The blue predicate uses the exact identity

```text
blue degree >= d  iff  red degree < 43-d.
```

The existing h3899 counters define whether a block has at least `j`
noncontacts for every `j<=21`. Consequently equation (3) needs only one
unconditional unit per block at `d=18` and six guarded binary clauses for
the higher strata. All new clauses have width at most three, and every new
auxiliary is uniquely determined by the physical assignment.

The construction is generic in `(q,r)` and covers all 18 h3887 macro classes
and all 2,189,178 physical tasks. It adds 32,754 variables and
`127,717+7q` clauses. It preserves satisfiability and exact physical-model
projection; it does not decide any task.
