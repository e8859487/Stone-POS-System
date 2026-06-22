"""
One-time migration script: reads all documents from the 'orders' collection
and copies them into per-year collections (orders_2024, orders_2025, etc.)
based on the shippingDate field.

Does NOT delete from 'orders'. Verify the migrated data, then delete manually.

Usage:
    python3 migrate_to_yearly_collections.py
"""

import pathlib
import firebase_admin
from firebase_admin import credentials, firestore

import GlobalSettings


def _init_firebase():
    key_path = GlobalSettings.FIREBASE_KEY_PATH
    if key_path and not pathlib.Path(key_path).is_absolute():
        key_path = pathlib.Path(__file__).parent.joinpath(key_path).as_posix()
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)


def _extract_year(shipping_date):
    """Extract year from 'YYYY/M/D' or 'YYYY-MM-DD' format. Returns str or None."""
    if not shipping_date:
        return None
    date_str = shipping_date.replace('-', '/')
    parts = date_str.split('/')
    if parts and parts[0].isdigit() and len(parts[0]) == 4:
        return parts[0]
    return None


def main():
    _init_firebase()
    db = firestore.client()

    source = db.collection('orders')
    docs = list(source.stream())
    print("Found {} documents in 'orders' collection.".format(len(docs)))

    year_counts = {}
    skipped = 0

    for doc in docs:
        data = doc.to_dict()
        shipping_date = data.get('shippingDate', '')
        year = _extract_year(shipping_date)

        if not year:
            # Fall back to timestamp year
            ts = data.get('timestamp')
            if ts:
                year = str(ts.year)
            else:
                print("  SKIP (no year): doc {} shippingDate='{}'".format(doc.id, shipping_date))
                skipped += 1
                continue

        target_col = db.collection('orders_{}'.format(year))
        target_col.document(doc.id).set(data)
        year_counts[year] = year_counts.get(year, 0) + 1

    print("\nMigration complete.")
    for year, count in sorted(year_counts.items()):
        print("  orders_{}: {} documents".format(year, count))
    if skipped:
        print("  Skipped (no year): {} documents".format(skipped))
    print("\nNOTE: Original 'orders' collection was NOT deleted.")
    print("After verifying, delete it manually in the Firebase console.")


if __name__ == '__main__':
    main()
