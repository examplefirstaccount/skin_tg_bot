from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


class Category(BaseModel):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f'<Category name={self.name}>'


class SubCategory(BaseModel):
    __tablename__ = 'sub_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    def __repr__(self) -> str:
        return f'<SubCategory name={self.name}>'


class Skin(BaseModel):
    __tablename__ = 'skins'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    img: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(String(15), nullable=False)
    descr: Mapped[str] = mapped_column(Text(), nullable=True)
    ext: Mapped[str] = mapped_column(String(20), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    sub_category_id: Mapped[int] = mapped_column(ForeignKey('sub_categories.id'), nullable=False)

    def __repr__(self) -> str:
        return f'<Skin name={self.name}>'


class Exterior(BaseModel):
    __tablename__ = 'exteriors'

    id: Mapped[int] = mapped_column(primary_key=True)
    ext: Mapped[str] = mapped_column(String(10), nullable=False)
    img: Mapped[str] = mapped_column(nullable=True)
    price_id: Mapped[int] = mapped_column(nullable=True)
    spec_price_id: Mapped[int] = mapped_column(nullable=True)
    skin_id: Mapped[int] = mapped_column(ForeignKey('skins.id'), nullable=False)

    def __repr__(self) -> str:
        return f'<Exterior ext={self.ext}>'
