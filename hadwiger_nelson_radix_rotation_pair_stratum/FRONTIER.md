# Residual interface after the complete rotation-only decision

The input is h4191's exact interface, canonical SHA-256
`8810828aa75a2d4a83cc18322d0312f58cb484b3683869eee38b63927d9246c1`.
Filtering all retained rows for a nonidentity stabilizer selects exactly the
four declared rows; all four already belonged to the at-least-six mode.

| mode | rows removed | allowance removed | rows remaining | allowance remaining |
|---|---:|---:|---:|---:|
| inherited exact-five flag | 0 | 0 | 121,480 | 3,590,760 |
| already requires at least six | 4 | 40 | 7,216 | 222,672 |
| whole frontier | 4 | 40 | 128,696 | 3,813,432 |

Every remaining global pair stabilizer is trivial. These allowances are
conservative bounds with multiplicities, not distinct-root or candidate counts.
Exact-five flags remain inherited from h4185 through h4191. There are no new
mode moves or pencil counts. The old 5,112 pencils / 128,871,936 lifts remain
prior upper bounds pending propagation of the accumulated pair exclusions.

The new interface contains eight additional forbidden pairs and the combined
list of 6,704 h4191 reflection and current rotation pair exclusions. The new
list hash is `ce5105cf3453b9ab6809589d0d3aa51174ae11025daa50233efdf861a6480760`;
the combined hash is
`e5d25c2f0ae10bf246afc4dc2fdb4fab8febdcb6b64ce44785fa1a167248f2de`.
The exact new interface has canonical SHA-256
`9da6cb1a32bbb5004b72bf2ac934dc05a44b5e2bf7705e7ec55498c3e7caabf9`.

Regenerate the h4191 input using its
[published handoff](../hadwiger_nelson_radix_reflection_pair_stratum/HANDOFF.md),
then run from the repository root:

```sh
python3 -B hadwiger_nelson_radix_rotation_pair_stratum/frontier.py \
  --frontier /tmp/hn-reflection-frontier.json \
  --export-interface /tmp/hn-rotation-frontier.json --check-expected
```

The output path must not exist. The larger interface is regenerated locally,
not committed. This frontier tool verifies the exact table transformation; the
physical validity of the exclusions is supplied by verify.py and PROOF.md.

HN2 now owns exact viability and geometry as well as construction, physical
realization and chromatic decisions. HN3 is parked and has not been contacted
or assigned work. Its durable h4187 reconciliation and earlier exact interfaces
remain historical inputs. The new milestone ends here; a later pass must start
from this residual and preserve all closed families. No record graph is found.
