class DataRepository:
    """Abstract interface for order data storage."""

    def add_order(self, data_pack):
        """Persist a single order. Returns True on success."""
        raise NotImplementedError

    def get_orders_by_shipping_date(self, shipping_date_str):
        """Returns list of DataPack objects for the given shipping date."""
        raise NotImplementedError

    def get_available_shipping_dates(self):
        """Returns sorted list of unique shipping date strings."""
        raise NotImplementedError

    def get_all_orders(self):
        """Returns list of all DataPack objects."""
        raise NotImplementedError
