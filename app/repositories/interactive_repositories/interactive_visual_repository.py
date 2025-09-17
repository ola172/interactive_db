from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.interactive_models.visual_models import (
    VisualItemModel,
    VisualTypeModel,
    TableDataModel,
    ChartDataModel,
    ChartTypeModel,
    ImageModel,
)
from app.repositories.base_repo import BaseRepository
from app.exceptions.repo_exception import RepoException


class VisualItemRepository(BaseRepository[VisualItemModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(VisualItemModel, db)

    async def get_visual_by_paragraph_id(
        self, paragraph_id: UUID
    ) -> VisualItemModel | None:
        try:
            stmt = (
                select(VisualItemModel)
                .where(VisualItemModel.paragraph_id == paragraph_id)
                .options(
                    selectinload(VisualItemModel.visual_type),
                    selectinload(VisualItemModel.table),
                    selectinload(VisualItemModel.chart),
                    selectinload(VisualItemModel.image),
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving visual by paragraph_id",
                additional_info={"error": str(e), "paragraph_id": str(paragraph_id)},
            )

    async def get_visuals_by_type(
        self, visual_type_name: str
    ) -> Sequence[VisualItemModel]:
        try:
            stmt = (
                select(VisualItemModel)
                .join(VisualTypeModel)
                .where(VisualTypeModel.name == visual_type_name)
                .options(
                    selectinload(VisualItemModel.visual_type),
                    selectinload(VisualItemModel.table),
                    selectinload(VisualItemModel.chart),
                    selectinload(VisualItemModel.image),
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving visuals by type",
                additional_info={"error": str(e), "visual_type_name": visual_type_name},
            )


class VisualTypeRepository(BaseRepository[VisualTypeModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(VisualTypeModel, db)

    async def get_by_name(self, name: str) -> VisualTypeModel | None:
        try:
            stmt = select(VisualTypeModel).where(VisualTypeModel.name == name)
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving visual type by name",
                additional_info={"error": str(e), "name": name},
            )


class TableDataRepository(BaseRepository[TableDataModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(TableDataModel, db)

    async def get_table_with_visual(self, table_id: UUID) -> TableDataModel | None:
        try:
            stmt = (
                select(TableDataModel)
                .where(TableDataModel.id == table_id)
                .options(selectinload(TableDataModel.visual_item))
            )
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving table with visual",
                additional_info={"error": str(e), "table_id": str(table_id)},
            )


class ChartDataRepository(BaseRepository[ChartDataModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ChartDataModel, db)

    async def get_chart_with_type_and_visual(
        self, chart_id: UUID
    ) -> ChartDataModel | None:
        try:
            stmt = (
                select(ChartDataModel)
                .where(ChartDataModel.id == chart_id)
                .options(
                    selectinload(ChartDataModel.chart_type),
                    selectinload(ChartDataModel.visual_item),
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving chart with type and visual",
                additional_info={"error": str(e), "chart_id": str(chart_id)},
            )

    async def get_charts_by_type(
        self, chart_type_name: str
    ) -> Sequence[ChartDataModel]:
        try:
            stmt = (
                select(ChartDataModel)
                .join(ChartTypeModel)
                .where(ChartTypeModel.name == chart_type_name)
                .options(selectinload(ChartDataModel.chart_type))
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving charts by type",
                additional_info={"error": str(e), "chart_type_name": chart_type_name},
            )


class ChartTypeRepository(BaseRepository[ChartTypeModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ChartTypeModel, db)

    async def get_by_name(self, name: str) -> ChartTypeModel | None:
        try:
            stmt = select(ChartTypeModel).where(ChartTypeModel.name == name)
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving chart type by name",
                additional_info={"error": str(e), "name": name},
            )

    def validate_chart_data(
        self, chart_type_name: str, labels: list, data: list
    ) -> dict:
        """
        Validate chart data based on chart type requirements.
        Returns validation result with error details if any.
        """
        validation_result = {"valid": True, "errors": []}

        if chart_type_name == "pie":
            # Pie charts require equal number of labels and data points
            if len(labels) != len(data):
                validation_result["valid"] = False
                validation_result["errors"].append(
                    "Pie charts require equal number of labels and data points"
                )

            # Pie chart data should be positive numbers
            if not all(isinstance(d, (int, float)) and d >= 0 for d in data):
                validation_result["valid"] = False
                validation_result["errors"].append(
                    "Pie chart data must be positive numbers"
                )

        elif chart_type_name in ["bar", "line"]:
            # Bar and line charts require equal number of labels and data points
            if len(labels) != len(data):
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"{chart_type_name.title()} charts require equal number of labels and data points"
                )

            # Data should be numeric
            if not all(isinstance(d, (int, float)) for d in data):
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"{chart_type_name.title()} chart data must be numeric"
                )

        elif chart_type_name == "radar":
            # Radar charts require at least 3 data points
            if len(labels) < 3 or len(data) < 3:
                validation_result["valid"] = False
                validation_result["errors"].append(
                    "Radar charts require at least 3 data points"
                )

            # Radar charts require equal number of labels and data points
            if len(labels) != len(data):
                validation_result["valid"] = False
                validation_result["errors"].append(
                    "Radar charts require equal number of labels and data points"
                )

            # Data should be numeric and positive
            if not all(isinstance(d, (int, float)) and d >= 0 for d in data):
                validation_result["valid"] = False
                validation_result["errors"].append(
                    "Radar chart data must be positive numbers"
                )

        return validation_result


class ImageRepository(BaseRepository[ImageModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ImageModel, db)

    async def get_image_with_visual(self, image_id: UUID) -> ImageModel | None:
        try:
            stmt = (
                select(ImageModel)
                .where(ImageModel.id == image_id)
                .options(selectinload(ImageModel.visual_item))
            )
            result = await self.db.execute(stmt)
            return result.scalars().first()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving image with visual",
                additional_info={"error": str(e), "image_id": str(image_id)},
            )
