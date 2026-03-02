#!/usr/bin/env python3
"""
Build the FR watershed seed manifest from nou-techne/watershed-data-collection/docs/data.json.

Selects a curated subset of Colorado SNOTEL stations, stream gauges, and the
Lake Powell reservoir for seeding the Front Range KOI node.

Selection criteria:
- Colorado SNOTEL stations only (state == "CO")
- Prioritize stations near Boulder/Front Range corridor (lat 39.0-41.0, lon -107.0 to -105.0)
- Diverse elevation range (selected stations span 6280-10560 ft)
- Target: 12-15 stations + 3 stream gauges + Lake Powell = ~20 Location entities

Usage:
    python3 build-fr-watershed-manifest.py [path/to/data.json]

Outputs: fr-watershed-seed-manifest.json in the same directory as this script.
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Repo-relative: script is at BioregionalKnowledgeCommoning/pilots/front-range-cascadia-2026/
# Go up 4 levels to reach the projects/ directory, then into sibling clone
DEFAULT_DATA_PATH = os.path.normpath(os.path.join(
    SCRIPT_DIR, "..", "..", "..", "..",
    "nou-techne", "watershed-data-collection", "docs", "data.json"
))


def select_snotel_stations(stations):
    """Select ~15 Colorado SNOTEL stations near the Front Range with diverse elevations."""
    co_stations = [s for s in stations if s.get("state") == "CO"]

    # Front Range corridor: lat 39.5-40.5, lon -106.5 to -105.0
    front_range = [
        s for s in co_stations
        if 39.0 <= (s.get("latitude") or 0) <= 41.0
        and -107.0 <= (s.get("longitude") or 0) <= -105.0
    ]

    # Sort by elevation for diverse range selection
    front_range.sort(key=lambda s: s.get("elevation_ft") or 0)

    # Pick stations at diverse elevations (sample every N to spread across range)
    if len(front_range) > 15:
        step = max(1, len(front_range) // 15)
        selected = front_range[::step][:15]
    else:
        selected = front_range[:15]

    return selected


def select_gauges(gauges):
    """Select 3 representative stream gauges from the Colorado River Basin."""
    co_gauges = [g for g in gauges if g.get("state") in ("CO", None)]
    # Take first 3 (they're all relevant — Colorado River Basin)
    return co_gauges[:3]


def build_manifest(data_path):
    with open(data_path) as f:
        data = json.load(f)

    stations = select_snotel_stations(data.get("snowpack_stations", []))
    gauges = select_gauges(data.get("gauges", []))
    reservoirs = data.get("reservoirs", [])[:1]  # Lake Powell

    manifest = {
        "source": "nou-techne/watershed-data-collection",
        "data_fetched_at": data.get("fetched_at"),
        "basin": data.get("basin"),
        "selection_criteria": {
            "snotel": "Colorado stations, lat 39-41 / lon -107 to -105, diverse elevation",
            "gauges": "First 3 from Colorado River Basin",
            "reservoirs": "Lake Powell"
        },
        "snotel_stations": [
            {
                "triplet": s["triplet"],
                "name": s["name"],
                "state": s["state"],
                "elevation_ft": s.get("elevation_ft"),
                "latitude": s.get("latitude"),
                "longitude": s.get("longitude"),
                "swe_in": s.get("swe_in"),
                "swe_median_in": s.get("swe_median_in"),
                "pct_of_median": s.get("pct_of_median"),
            }
            for s in stations
        ],
        "stream_gauges": [
            {
                "site_id": g["site_id"],
                "name": g["name"],
                "state": g.get("state"),
                "latitude": g.get("latitude"),
                "longitude": g.get("longitude"),
                "median_discharge_cfs": g.get("median_discharge_cfs"),
                "pct_of_median": g.get("pct_of_median"),
            }
            for g in gauges
        ],
        "reservoirs": [
            {
                "site_id": r["site_id"],
                "name": r["name"],
                "elevation_ft": r.get("elevation_ft"),
                "fill_pct": r.get("fill_pct"),
                "latitude": r.get("latitude"),
                "longitude": r.get("longitude"),
            }
            for r in reservoirs
        ],
    }

    output_path = os.path.join(SCRIPT_DIR, "fr-watershed-seed-manifest.json")
    with open(output_path, "w") as f:
        json.dump(manifest, f, indent=2)

    total = len(manifest["snotel_stations"]) + len(manifest["stream_gauges"]) + len(manifest["reservoirs"])
    print(f"Manifest written to {output_path}")
    print(f"  SNOTEL stations: {len(manifest['snotel_stations'])}")
    print(f"  Stream gauges:   {len(manifest['stream_gauges'])}")
    print(f"  Reservoirs:      {len(manifest['reservoirs'])}")
    print(f"  Total locations:  {total}")

    return manifest


if __name__ == "__main__":
    data_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA_PATH
    if not os.path.exists(data_path):
        print(f"Error: data.json not found at {data_path}", file=sys.stderr)
        print("Usage: python3 build-fr-watershed-manifest.py [path/to/data.json]", file=sys.stderr)
        sys.exit(1)
    build_manifest(data_path)
