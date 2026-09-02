# Exact results

The one-element lattice is won by the empty sequence.  The production output
for every nontrivial order was:

```text
PASS order=2 total=1 winnable=1 max_states_before_goal=2
PASS order=3 total=1 winnable=1 max_states_before_goal=2
PASS order=4 total=2 winnable=2 max_states_before_goal=7
PASS order=5 total=5 winnable=5 max_states_before_goal=15
PASS order=6 total=15 winnable=15 max_states_before_goal=31
PASS order=7 total=53 winnable=53 max_states_before_goal=63
PASS order=8 total=222 winnable=222 max_states_before_goal=127
PASS order=9 total=1078 winnable=1078 max_states_before_goal=255
PASS order=10 total=5994 winnable=5994 max_states_before_goal=511
PASS order=11 total=37622 winnable=37622 max_states_before_goal=1023
PASS order=12 total=262776 winnable=262776 max_states_before_goal=2047
PASS order=13 total=2018305 winnable=2018305 max_states_before_goal=4095
PASS order=14 total=16873364 winnable=16873364 max_states_before_goal=8191
```

Thus 19,199,439 isomorphism classes, including the trivial order-one class,
were covered.

The compressed order-14 inputs used in the two complete runs had hashes

```text
b1e3fda190ef6e0493d4ae2be0b38301aaa0dfb1a067afb62519cf7963663e2d  unlabelled-14.cats.xz
eae91a0b3dff3c2b2104e1b5fa01e46e02271442b6ff099f1948ff131bac0b67  Lattice Cover Relations 14.txt.gz
```

The first is from the publisher-provided `unlabelled.sha256` manifest for the
Gebhardt--Tawn catalogue.  The second records the independently downloaded
Reading/Heitzig--Reinhold catalogue used in the replication.
