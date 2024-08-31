class DataRetrievalError(Exception):
    """Exception raised when data retrieval from the database fails."""

    def __init__(self, message="Failed to retrieve necessary data from the database"):
        self.message = message
        super().__init__(self.message)
