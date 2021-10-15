import json
import re
from main import DataHandler
from datetime import datetime, timedelta

class Aggregator(DataHandler):
    """Aggregates parking data by daily, weekly, and hourly metrics."""

    def __init__(self):
        super().__init__()
    
    def _row_to_numerical_data(self, row):
        """Helper function that takes a row and converts numerical data to ints."""
        timestamp = row[0]
        availabilities = [int(x) for x in row[1:]]
        return [timestamp, *availabilities]

    def last_n(self, n):
        """Returns the last N datapoints from the moment this method is called."""
        self._ensure_sheet_is_uptodate()

        # Get the bounds of the last N datapoints
        now = datetime.now() - timedelta(minutes=1)  # exclude current minute
        hhmm = now.strftime("%H:%M")
        cell = self.curr_sheet.find(hhmm)
        row_ub = cell.row
        row_lb = cell.row - n 

        last_n_rows = self.curr_sheet.get(f"A{row_lb}:F{row_ub}")

        # Convert availabilites to ints
        rv = [self._row_to_numerical_data(row) for row in last_n_rows]
        print(json.dumps(rv))
        return rv

agg = Aggregator()
agg.last_n(5)
