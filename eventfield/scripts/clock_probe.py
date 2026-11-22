#!/usr/bin/env python3
"""Propagate saved aperture differences through the local slope of Lee et al. Eq. 2."""
import csv
import math
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[2] / "research"
SLOPE = 0.52  # Gyr per unit d/R500c
INTERCEPT = -0.24  # Gyr
R500_KPC = 1000.0  # Stated example scale, never fitted to an observed system.


def main():
    cases = {}
    for experiment in ("two-cluster-physical-beam", "g099-paired-positions"):
        with (RESEARCH / experiment / "variants.csv").open() as stream:
            for row in csv.DictReader(stream):
                if row["image"] == "T50" and row["relic"] == "N" and float(row["threshold_mjy_per_beam"]) == 0.2:
                    key = (row["cluster"], int(row["radius_kpc"]))
                    if key in cases:
                        raise ValueError(f"Duplicate aperture case {key}")
                    cases[key] = float(row["pair_difference_kpc"])
    if len(cases) != 9:
        raise ValueError("Expected three radii for each of three fields")
    print("field,aperture_kpc,t50_minus_t50sub_kpc,illustrative_shift_myr")
    for (field, aperture), delta in sorted(cases.items()):
        normalized_shift = delta / R500_KPC
        print(f"{field},{aperture},{delta:.6f},{1000 * SLOPE * normalized_shift:.6f}")
    angle = math.radians(30)
    reference, projected = (SLOPE * x + INTERCEPT for x in (2.4, 2.4 * math.cos(angle)))
    print(f"30 degree toy projection: {reference:.6f} and {projected:.6f} Gyr; shift {(projected - reference) * 1000:.3f} Myr")


if __name__ == "__main__":
    main()
