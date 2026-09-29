"""Sufficient-certificate rejection controls; no generator is imported."""
import copy
import json
from verify import ROOT, verify_certificate


def main():
    original = json.loads((ROOT / "certificate.json").read_text())
    bad = []
    c = copy.deepcopy(original)
    c["capacity_rows_m_t_holes_C"].pop()
    bad.append(c)
    c = copy.deepcopy(original)
    c["capacity_rows_m_t_holes_C"][0][3] += 1
    bad.append(c)
    c = copy.deepcopy(original)
    c["tower_cases"]["3"].pop()
    bad.append(c)
    c = copy.deepcopy(original)
    c["tower_cases"]["3"][0][3] = []
    bad.append(c)
    for c in bad:
        try:
            verify_certificate(c)
        except ValueError:
            continue
        raise ValueError("A corrupted certificate was accepted")
    print("4 corrupted certificates rejected")


if __name__ == "__main__":
    main()
