import hashlib


class AddressSource:
    """
    superclass for a address data source
    """

    def get_addresses_results(self, query) -> list:
        """
        must return an array of dicts
        """
        pass

    def get_suggestions(self, query) -> list:
        """
        returns list of suggestions
        """
        pass

    @staticmethod
    def _get_address_hash(address_title) -> str:
        """
        compute a unique reply hash
        """
        return hashlib.md5(address_title.encode()).hexdigest()