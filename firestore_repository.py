import pathlib
import firebase_admin
from firebase_admin import credentials, firestore

import GlobalSettings
from data_repository import DataRepository
from DataPack import DataPack

_app_initialized = False


def _init_firebase():
    global _app_initialized
    if _app_initialized:
        return
    key_path = GlobalSettings.FIREBASE_KEY_PATH
    if key_path and not pathlib.Path(key_path).is_absolute():
        key_path = pathlib.Path(__file__).parent.joinpath(key_path).as_posix()
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)
    _app_initialized = True


class FirestoreRepository(DataRepository):

    def __init__(self):
        _init_firebase()
        self.db = firestore.client()
        self.collection = self.db.collection('orders')

    def add_order(self, data_pack, source="web"):
        doc = data_pack.toFirestoreDict(source=source)
        self.collection.add(doc)
        return True

    def get_orders_by_shipping_date(self, shipping_date_str):
        query = self.collection.where('shippingDate', '==', shipping_date_str)
        docs = query.stream()
        orders = []
        for doc in docs:
            dp = DataPack.from_firestore_dict(doc.to_dict())
            orders.append(dp)
        return orders

    def get_available_shipping_dates(self):
        docs = self.collection.stream()
        dates = set()
        for doc in docs:
            d = doc.to_dict()
            sd = d.get('shippingDate', '')
            if sd:
                dates.add(sd.replace('-', '/'))
        return sorted(dates, key=lambda d: tuple(map(int, d.split('/'))))

    def get_all_orders(self):
        query = self.collection.order_by('timestamp', direction=firestore.Query.DESCENDING)
        docs = query.stream()
        orders = []
        for doc in docs:
            d = doc.to_dict()
            dp = DataPack.from_firestore_dict(d)
            dp._doc_id = doc.id
            dp._timestamp = d.get('timestamp')
            orders.append(dp)
        return orders

    def update_order(self, order_id, data_pack):
        doc = data_pack.toFirestoreDict()
        doc.pop('timestamp', None)
        self.collection.document(order_id).update(doc)
        return True

    def delete_order(self, order_id):
        self.collection.document(order_id).delete()
        return True

    def get_shipping_date_summary(self):
        import datetime
        today = datetime.date.today()
        docs = self.collection.stream()
        summary = {}
        for doc in docs:
            d = doc.to_dict()
            if d.get('exported', False):
                continue
            sd = d.get('shippingDate', '').replace('-', '/')
            if not sd:
                continue
            try:
                parts = sd.split('/')
                date = datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
            except (ValueError, IndexError):
                continue
            if date < today:
                continue
            summary[sd] = summary.get(sd, 0) + int(d.get('numbers', 0))
        return sorted(
            [{'date': k, 'total_boxes': v} for k, v in summary.items()],
            key=lambda x: tuple(map(int, x['date'].split('/')))
        )

    def mark_orders_exported(self, shipping_date_str):
        import datetime
        query = self.collection.where('shippingDate', '==', shipping_date_str)
        docs = query.stream()
        count = 0
        now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
        for doc in docs:
            doc.reference.update({'exported': True, 'exportedAt': now})
            count += 1
        return count
