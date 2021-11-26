
class TridentHandler:
    """
    TridentHandler

    Used to cache results from trident
    """
    def __init__(self, db):
        self._terms = {}
        self._db = db

    def lookup(self, term):
        if term not in self._terms:
            self._terms[term] = self._db.lookup_id(term)
        return self._terms[term]
    
    def o_aggr_froms(self, term):
        return self._db.o_aggr_froms(self.lookup(term))
