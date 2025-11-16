import math

from app.schemas.pagination import PaginationMeta


class PaginationFactory:
    @staticmethod
    def create_pagination_meta(page: int, size: int, total: int) -> PaginationMeta:
        pages = math.ceil(total / size)
        return PaginationMeta(
            page=page,
            size=size,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )
