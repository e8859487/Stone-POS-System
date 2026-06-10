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

    def update_order(self, order_id, data_pack):
        """Update an existing order. Returns True on success."""
        raise NotImplementedError

    def delete_order(self, order_id):
        """Delete an order. Returns True on success."""
        raise NotImplementedError

    def mark_orders_exported(self, shipping_date_str):
        """Mark all orders for a shipping date as exported. Returns count."""
        raise NotImplementedError
