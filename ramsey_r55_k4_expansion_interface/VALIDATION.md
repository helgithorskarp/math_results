# Validation record

The compact replay has status `VERIFIED_K4_EXPANSION_INTERFACE`. It checks:

- separate literal reconstruction of all 18 `(q,r)` suffixes;
- all 64 truth-table cases for the contact and recurrence gadgets;
- 7,172 complete assignments across every threshold for n=2 through 9;
- 64 n=39 boundary propagation controls, covering 32 placements at 20 and
  21 noncontacts;
- exact physical numbering, signed red/blue block literals, auxiliary range
  disjointness, clause counts, widths, bytes, and SHA-256;
- identical compact output under normal and assertion-disabled Python.

The complete shared-triangle example was freshly produced at
`bo1-q7-r7-c000000`. An independent stream rebuilt the base physical and
triangle clauses, the h3887 ordering suffix, and then this interface without
importing its producer. Normal and `-O` audits agree exactly:

```json
{
  "variables": 10868,
  "clauses": 923269,
  "ordered_variables": 6332,
  "ordered_clauses": 905265,
  "expansion_variables": 4536,
  "expansion_clauses": 18004,
  "max_width": 8,
  "bytes": 35503067,
  "sha256": "755dbcd5677bbc57a0865637dbce19fa72084c4846b3996b8697bf1485070178"
}
```

The 35.5 MB formula and 6.6 MB downloaded catalog cache are omitted from the
repository. They are deterministic scratch outputs reproducible from the
pinned public source and author inputs. No SAT executable, model, DRAT stream,
or solver log enters this result.

The implementation controls are not an external review or formal proof. The
universal mathematical scope rests on the proof in `PROOF.md` and h3897's
separator classification. The external-review status of h3897 and this new
interface is pending. The h3887 cover continues to import the completeness of
the McKay Ramsey(4,4) catalogs.
