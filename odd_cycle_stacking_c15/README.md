# Exploratory odd-cycle stacking recurrence

`enumerate_stacking.cpp` implements the exact parent/child recurrence for
non-stackable pebbling configurations on an odd cycle, quotienting by the
dihedral group.

It independently reproduces the published values

```text
stack(C_7)  = 17
stack(C_11) = 77
```

and was used to assess whether the next unreported frontier could be reached
with a direct recurrence.  A run for `C_13` exactly completed the levels
through weight 23 (12,843,740 non-stackable dihedral orbits at that level),
but was deliberately stopped because this representation does not make a
`C_15` computation realistic on the available resources.  No incomplete run
is used as a mathematical result, and no graph contribution depends on this
directory.

The source is preserved because it was part of the research process.  Run,
for example:

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  enumerate_stacking.cpp -o /tmp/enumerate_stacking
/tmp/enumerate_stacking 7
```

Primary context: Tamás Csernák and Lajos Soukup, *Stacking and clearing in
graph pebbling*, arXiv:2604.22341v1.
