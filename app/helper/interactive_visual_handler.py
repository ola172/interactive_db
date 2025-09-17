from abc import ABC, abstractmethod
from typing import Any, Dict
import uuid


class VisualDataHandler(ABC):
    """Abstract base class for visual data handlers"""

    @abstractmethod
    async def create(self, data: Dict[str, Any], repos: Dict[str, Any]) -> uuid.UUID:
        """Create visual data and return the ID"""
        pass

    @abstractmethod
    async def update(
        self, item_id: uuid.UUID, data: Dict[str, Any], repos: Dict[str, Any]
    ) -> bool:
        """Update visual data"""
        pass

    @abstractmethod
    async def delete(self, item_id: uuid.UUID, repos: Dict[str, Any]) -> bool:
        """Delete visual data"""
        pass


class TableDataHandler(VisualDataHandler):
    """Handler for table visual data"""

    async def create(self, data: Dict[str, Any], repos: Dict[str, Any]) -> uuid.UUID:
        table_dict = {
            "headers": data.get("headers", []),
            "rows": data.get("rows", []),
            "title": data.get("title", ""),
            "caption": data.get("caption", ""),
        }
        table = await repos["table_repo"].create(table_dict)
        return table.id

    async def update(
        self, item_id: uuid.UUID, data: Dict[str, Any], repos: Dict[str, Any]
    ) -> bool:
        table_update_data = {
            "headers": data.get("headers"),
            "rows": data.get("rows"),
            "title": data.get("title"),
            "caption": data.get("caption"),
        }
        # Remove None values
        table_update_data = {
            k: v for k, v in table_update_data.items() if v is not None
        }
        if table_update_data:
            result = await repos["table_repo"].update(item_id, table_update_data)
            return result is not None
        return True

    async def delete(self, item_id: uuid.UUID, repos: Dict[str, Any]) -> bool:
        return await repos["table_repo"].delete(item_id)


class ChartDataHandler(VisualDataHandler):
    """Handler for chart visual data"""

    async def create(self, data: Dict[str, Any], repos: Dict[str, Any]) -> uuid.UUID:
        chart_dict = {
            "chart_type_id": data.get("chart_type_id"),
            "labels": data.get("labels", []),
            "data": data.get("data", []),
            "title": data.get("title", ""),
        }
        chart = await repos["chart_repo"].create(chart_dict)
        return chart.id

    async def update(
        self, item_id: uuid.UUID, data: Dict[str, Any], repos: Dict[str, Any]
    ) -> bool:
        chart_update_data = {
            "chart_type_id": data.get("chart_type_id"),
            "labels": data.get("labels"),
            "data": data.get("data"),
            "title": data.get("title"),
        }
        # Remove None values
        chart_update_data = {
            k: v for k, v in chart_update_data.items() if v is not None
        }
        if chart_update_data:
            result = await repos["chart_repo"].update(item_id, chart_update_data)
            return result is not None
        return True

    async def delete(self, item_id: uuid.UUID, repos: Dict[str, Any]) -> bool:
        return await repos["chart_repo"].delete(item_id)


class ImageDataHandler(VisualDataHandler):
    """Handler for image visual data"""

    async def create(self, data: Dict[str, Any], repos: Dict[str, Any]) -> uuid.UUID:
        image_dict = {
            "url": data.get("url", ""),
            "alt_text": data.get("alt_text"),
            "title": data.get("caption", ""),
        }
        image = await repos["image_repo"].create(image_dict)
        return image.id

    async def update(
        self, item_id: uuid.UUID, data: Dict[str, Any], repos: Dict[str, Any]
    ) -> bool:
        image_update_data = {
            "url": data.get("url"),
            "alt_text": data.get("alt_text"),
            "title": data.get("caption"),
        }
        # Remove None values
        image_update_data = {
            k: v for k, v in image_update_data.items() if v is not None
        }
        if image_update_data:
            result = await repos["image_repo"].update(item_id, image_update_data)
            return result is not None
        return True

    async def delete(self, item_id: uuid.UUID, repos: Dict[str, Any]) -> bool:
        return await repos["image_repo"].delete(item_id)
