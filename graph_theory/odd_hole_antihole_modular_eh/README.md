# Sharp Erdős--Hajnal bounds for odd-hole/antihole modular graphs

For every integer `h>=2`, this directory proves sharp product and homogeneous
set bounds for the hereditary substitution class whose prime quotients are
perfect graphs or odd holes/antiholes of length at least `2h+1`.

Put

```text
q_h = log_(2h+1)(2h).
```

Every nonempty graph `G` in the class satisfies

```text
alpha(G) * omega(G) >= |V(G)|^q_h,
max(alpha(G), omega(G)) >= |V(G)|^(q_h/2).
```

Both exponents and the leading constant one are sharp.  The result strictly
extends the previously reviewed perfect-or-pentagon theorem from one
imperfect prime quotient to all odd holes and odd antiholes, and gives a
length-sensitive hierarchy when shorter holes/antiholes are excluded.

The mathematical proof is in [THEOREM.md](THEOREM.md), with literature and
scope in [SOURCES.md](SOURCES.md).  Reproduce the exact audit with:

```bash
./run_checks.sh
```

The checker uses only the Python standard library.  Its finite calculations
audit definitions, cycle incidence identities, extremal case reductions,
and equality recurrences.  Universal quantifiers rest on the written proof.

