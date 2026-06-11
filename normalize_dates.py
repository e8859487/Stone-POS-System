"""
一次性腳本：把 Firestore 'orders' collection 裡 shippingDate / arrivalDate
從 yyyy/mm/dd（含補零，例如 2026/06/12）統一轉成 yyyy/m/d（例如 2026/6/12）。

預設為 dry-run（只印出會修改的內容，不寫入）。
確認無誤後加上 --apply 參數才會真的更新 Firestore。
"""
import argparse
import datetime
import pathlib

import firebase_admin
from firebase_admin import credentials, firestore


def normalize(date_str):
    if not date_str:
        return date_str
    s = date_str.replace('-', '/')
    try:
        dt = datetime.datetime.strptime(s, "%Y/%m/%d")
    except ValueError:
        return date_str  # 格式不認得，跳過不處理
    return '{dt.year}/{dt.month}/{dt.day}'.format(dt=dt)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='實際寫入 Firestore（預設只 dry-run）')
    args = parser.parse_args()

    key_path = pathlib.Path(__file__).parent.joinpath('firebase-key.json')
    cred = credentials.Certificate(key_path.as_posix())
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    collection = db.collection('orders')

    changed = 0
    for doc in collection.stream():
        d = doc.to_dict()
        updates = {}
        for field in ('shippingDate', 'arrivalDate'):
            old = d.get(field, '')
            new = normalize(old)
            if new != old:
                updates[field] = new

        if updates:
            changed += 1
            print('[{}] {}'.format(doc.id, d.get('name', '')))
            for field, new in updates.items():
                print('    {}: {!r} -> {!r}'.format(field, d.get(field), new))
            if args.apply:
                doc.reference.update(updates)

    print('\n共 {} 筆需要更新{}'.format(changed, '' if args.apply else '（dry-run，未寫入，加 --apply 才會更新）'))


if __name__ == '__main__':
    main()
