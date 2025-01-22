from rest_framework.renderers import JSONRenderer
from decimal import Decimal

class CustomJSONRenderer(JSONRenderer):
    """
    Custom JSON Renderer to handle Decimal properly.
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):
            data = self._convert_decimals(data)
        return super().render(data, accepted_media_type, renderer_context)

    def _convert_decimals(self, obj):
        """
        Recursively convert Decimal to float in dictionaries and lists.
        """
        if isinstance(obj, dict):
            return {key: self._convert_decimals(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_decimals(item) for item in obj]
        elif isinstance(obj, Decimal):
            return float(round(obj, 2))  
        return obj
