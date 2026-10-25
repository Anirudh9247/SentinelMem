"""Owner-run smoke check for write provenance, quarantine, and restart persistence."""

from __future__ import annotations

import argparse
from pathlib import Path

from sentinelmem.backends import EmulatedMem0Backend
from sentinelmem.models import MemoryRecord
from sentinelmem.storage import SQLiteLedger


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=Path("results/manual_storage_check.sqlite3"))
    args = parser.parse_args()

    ledger = SQLiteLedger(args.database)
    backend = EmulatedMem0Backend(audit_ledger=ledger)
    record = MemoryRecord(
        record_id="manual-synthetic-check",
        text="Synthetic placeholder for checking local storage persistence.",
        provenance="manual_synthetic_fixture",
        label="benign",
    )
    backend.write(record, session_id="manual-check", agent_id="owner-review")
    ledger.quarantine_record(record, "Manual persistence check fixture", 0.5)

    reopened = SQLiteLedger(args.database)
    provenance = reopened.get_provenance(record.record_id)
    quarantine = reopened.list_quarantine()
    if provenance is None or not quarantine or not reopened.verify_audit_chain():
        raise SystemExit("FAIL: inspect the database and logs before continuing")
    print(f"PASS provenance: record={provenance['record_id']} hash={provenance['content_hash']}")
    print(f"PASS quarantine: records={len(quarantine)} status={quarantine[0]['status']}")
    print(f"PASS audit chain: events={len(reopened.list_audit_events())} valid=true")
    print(f"Evidence database: {args.database}")


if __name__ == "__main__":
    main()
