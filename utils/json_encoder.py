import json
from decimal import Decimal

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        '''
        Custom JSON encoder.
        '''
        if isinstance(obj, Decimal):
            return float(round(obj, 2))  
        if isinstance(obj, float):
            return round(obj, 2)  
        return super().default(obj)
