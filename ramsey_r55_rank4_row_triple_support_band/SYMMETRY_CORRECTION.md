# Prepublication inverse-transpose correction

An independent reduction audit found that the first exploratory support
partition applied a row-stabilizing linear map directly to column labels.
Factor equivalence instead applies its inverse transpose to the columns.  The
two groups both have order 192 and coincidentally give the same orbit-count
histogram, but they are different subgroups (intersection order 12) and only
72 of their 288 minimum representatives in support sizes 5--8 coincide.

The affected exploratory base formula had SHA-256
`724cbd9b1ddf80fb0c69a43cffa906075634128f3bb10a3753de063c5bfdf862`.
It and its partial proof replay are rejected as coverage evidence and are not
used in `RESULT.json` or the public combined manifest.

The corrected production enumerator computes the inverse-transpose action and
checks dot-product preservation on all 256 vector pairs.  The final formula
uses that corrected action in its support-symmetry clauses and tests the whole
support-size band at once.  Its independently audited orbit table agrees with
the formula's 475 canonical spanning supports before the size bound and 288 in
the tested band.  The final CNF and proof were regenerated after the correction.
