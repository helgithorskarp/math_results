# Uniform blow-ups cannot create a first Erdős–Szekeres counterexample

For Baek–Balko's uniform $x$-blow-up, with $x\ge1$ and
$k=m+2x$, any output exceeding $2^{k-2}$ points yields a subset of its
seed that already violates the conjectured bound at some polygon size
$q\le m<k$. An exact identity expresses the output excess as a sum of
seed and endpoint-layer excesses with strictly positive coefficients.

This closes the uniform construction as a route to the **smallest-size**
counterexample. It also gives the sharp bound and an exact equality
profile whenever the relevant smaller Erdős–Szekeres bounds hold.
The general nonuniform $(X,Y)$ construction remains outside this result.

- [Full proof and scope](PROOF.md)
- [Prior sources and novelty limitations](REFERENCES.md)
- [Exact supplemental verifier](verify.py)
- [Small geometric fixtures](fixtures.json)
- [Expected deterministic output](expected.json)

The construction and its cardinality formula are Baek–Balko's. The
contribution here is the positive excess decomposition, smaller-witness
extraction, and equality criterion. No historical-priority claim is made;
the 2026 journal full text could not be checked.

From this directory, run:

```sh
python3 verify.py
```

Tested with CPython 3.11.2; standard library only. The verifier compares
convex-subset enumeration with a separate cap/cup dynamic program, checks
all thresholds of the supplied seeds, and tests the identity on arbitrary
formal profiles, including deliberately unrealizable profiles with
positive excess. It also checks the binary-word partition directly.
These finite checks supplement the proof; they establish neither the
general conjecture nor exhaustive coverage of planar order types.

Source files and compact results only. No solver, floating point, private
data, downloaded paper, or large certificate is required.
