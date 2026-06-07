"""
One-time migration script: Google Sheets → Firestore

Usage:
    python3 migrate_sheets_to_firestore.py [--dry-run]
"""
import sys
from ReadGoogleExcel import getSpreadSheetData, initService
from DataParser import GoogleSpreadDataParser
from firestore_repository import FirestoreRepository


def migrate(dry_run=False):
    print("=== Google Sheets → Firestore Migration ===")

    # Step 1: Read from Google Sheets
    if not initService():
        print("ERROR: Cannot connect to Google Sheets. Run OAuth first.")
        sys.exit(1)

    raw = getSpreadSheetData()
    print("Found {} rows in Google Sheets".format(len(raw)))

    # Step 2: Parse each row
    parser = GoogleSpreadDataParser()
    orders = []
    skipped = 0
    for row in raw[GoogleSpreadDataParser.interestColumn].iterrows():
        try:
            parser.setData(row)
            dp = parser.parse()
            if dp.name:
                orders.append(dp)
            else:
                skipped += 1
        except Exception as e:
            skipped += 1
            print("  SKIP row {}: {}".format(row[0], e))

    print("Parsed {} orders ({} skipped)".format(len(orders), skipped))

    if dry_run:
        print("\n[DRY RUN] Would write {} orders to Firestore:".format(len(orders)))
        for i, dp in enumerate(orders[:5]):
            print("  {}: {} / {} / {}箱 / {}".format(
                i + 1, dp.name, dp.arrivalDate, dp.numbers, dp.shippingDate))
        if len(orders) > 5:
            print("  ... and {} more".format(len(orders) - 5))
        return

    # Step 3: Write to Firestore
    repo = FirestoreRepository()
    success = 0
    for i, dp in enumerate(orders):
        try:
            repo.add_order(dp, source="migrated")
            success += 1
            if (i + 1) % 10 == 0:
                print("  Written {}/{}...".format(i + 1, len(orders)))
        except Exception as e:
            print("  FAIL order {}/{} ({}): {}".format(i + 1, len(orders), dp.name, e))

    print("\nDone! {} / {} orders migrated to Firestore.".format(success, len(orders)))


if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    migrate(dry_run=dry_run)
