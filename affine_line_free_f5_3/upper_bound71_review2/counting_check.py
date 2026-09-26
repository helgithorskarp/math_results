"""Independent sparse reconstruction of the a_8+a_9 >= 5 certificate."""

from __future__ import annotations

from collections import Counter
from itertools import combinations_with_replacement
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add(column: dict[str, int], name: str, value: int) -> None:
    if value:
        column[name] = column.get(name, 0) + value


def spectra() -> tuple[tuple[int, ...], ...]:
    rows = []
    for line in (SOURCE / "low_planes72" / "spectra_expected.txt").read_text().splitlines():
        values = tuple(map(int, line.split()))
        require(len(values) == 7 and values[-1] > 0, "bad spectrum row")
        spectrum = values[:6]
        size, counts = spectrum[0], spectrum[1:]
        require(sum(counts) == 30, "plane line-count identity")
        require(sum(k * counts[k] for k in range(5)) == 6 * size, "point-line identity")
        require(sum(comb(k, 2) * counts[k] for k in range(5)) == comb(size, 2), "pair-line identity")
        require(not (size <= 11 and counts[4]), "small section contains four collinear points")
        rows.append(spectrum)
    require(len(rows) == 70 and len(set(rows)) == 70, "spectrum catalogue size")
    return tuple(rows)


def columns(spectrum_rows: tuple[tuple[int, ...], ...]):
    result = []
    for spectrum in spectrum_rows:
        size, counts = spectrum[0], spectrum[1:]
        column: dict[str, int] = {}
        add(column, "planes", 1)
        add(column, "plane_points", size)
        add(column, "plane_pairs", comb(size, 2))
        add(column, f"parallel_size_{size}", 1)
        for k, count in enumerate(counts):
            add(column, f"pencil_{k}_size_{size}", count)
        result.append((column, int(size <= 9)))

    parallel_profiles = [
        profile for profile in combinations_with_replacement(range(8, 17), 5)
        if sum(profile) == 72
    ]
    require(len(parallel_profiles) == 18, "parallel profile count")
    for profile in parallel_profiles:
        column = {"parallel_classes": 1}
        for size, count in Counter(profile).items():
            add(column, f"parallel_size_{size}", -count)
        result.append((column, 0))

    pencil_count = 0
    for k in range(5):
        for profile in combinations_with_replacement(range(max(8, 5 * k - 8), 17), 6):
            if sum(profile) != 72 + 5 * k:
                continue
            pencil_count += 1
            column = {"lines": 1, "line_points": k, "line_pairs": comb(k, 2)}
            for size, count in Counter(profile).items():
                add(column, f"pencil_{k}_size_{size}", -count)
            result.append((column, 0))
    require(pencil_count == 375 and len(result) == 463, "incidence column count")
    return result


def main() -> None:
    certificates = json.loads((SOURCE / "low_planes72" / "incidence_certificates.json").read_text())
    certificate = next(item for item in certificates if item["cutoff"] == 9)
    row_names = (
        "planes", "plane_points", "plane_pairs", "parallel_classes",
        *(f"parallel_size_{size}" for size in range(8, 17)),
        *(f"pencil_{k}_size_{size}" for k in range(5) for size in range(8, 17)),
        "lines", "line_points", "line_pairs",
    )
    require(len(row_names) == len(certificate["multipliers"]) == 61, "incidence row count")
    multipliers = dict(zip(row_names, certificate["multipliers"]))
    denominator = certificate["denominator"]
    slacks = []
    for column, objective in columns(spectra()):
        lhs = sum(multipliers[name] * value for name, value in column.items())
        slacks.append(denominator * objective - lhs)
    require(min(slacks) >= 0, "dual column inequality")

    rhs = {
        "planes": 155,
        "plane_points": 72 * 31,
        "plane_pairs": comb(72, 2) * 6,
        "parallel_classes": 31,
        "lines": 775,
        "line_points": 72 * 31,
        "line_pairs": comb(72, 2),
    }
    numerator = sum(multipliers[name] * value for name, value in rhs.items())
    require(numerator == certificate["bound_numerator"] == 440665, "dual numerator")
    require(4 * denominator < numerator <= 5 * denominator, "integer lower bound")
    result = {
        "status": "INDEPENDENT_LOW_PLANE_CERTIFICATE_VERIFIED",
        "spectra": 70,
        "incidence_rows": 61,
        "incidence_columns": 463,
        "minimum_slack": min(slacks),
        "tight_columns": sum(slack == 0 for slack in slacks),
        "bound_numerator": numerator,
        "bound_denominator": denominator,
        "integer_lower_bound": 5,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
