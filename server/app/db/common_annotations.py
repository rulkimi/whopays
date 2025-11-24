from typing import Annotated
from uuid import UUID, uuid4
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID

uuid4pk = Annotated[
	UUID,
	mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
]
name = Annotated[str, mapped_column(String(30), nullable=False)]