from typing import Dict
from app.exceptions.service_exception import ServiceException
from .interactive_visual_handler import VisualDataHandler, TableDataHandler, ChartDataHandler, ImageDataHandler


class VisualDataRegistry:
    """Registry for visual data handlers using the registry pattern"""

    def __init__(self):
        self._handlers: Dict[str, VisualDataHandler] = {
            "table": TableDataHandler(),
            "chart": ChartDataHandler(),
            "image": ImageDataHandler(),
        }

    def get_handler(self, visual_type: str) -> VisualDataHandler:
        """Get the appropriate handler for a visual type"""
        handler = self._handlers.get(visual_type.lower())
        if not handler:
            raise ServiceException(
                status_code=400,
                detail=f"Unsupported visual type: {visual_type}",
                additional_info={"supported_types": list(self._handlers.keys())},
            )
        return handler

    def register_handler(self, visual_type: str, handler: VisualDataHandler):
        """Register a new visual data handler"""
        self._handlers[visual_type.lower()] = handler