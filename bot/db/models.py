from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """
    Base model class for all database models.

    This class serves as the base for all models in the database, providing common functionality
    and allowing the use of SQLAlchemy's ORM features.
    """

    pass


class Category(BaseModel):
    """
    Model representing a category of items.

    Attributes:
        id (int): The primary key identifier for the category.
        name (str): The name of the category, which must be unique and not null.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<Category name={self.name}>"


class SubCategory(BaseModel):
    """
    Model representing a subcategory, linked to a parent category.

    Attributes:
        id (int): The primary key identifier for the subcategory.
        name (str): The name of the subcategory, which must not be null.
        category_id (int): Foreign key referencing the parent category.
    """

    __tablename__ = "sub_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    def __repr__(self) -> str:
        return f"<SubCategory name={self.name}>"


class Skin(BaseModel):
    """
    Model representing a skin, which belongs to a category and a subcategory.

    Attributes:
        id (int): The primary key identifier for the skin.
        name (str): The name of the skin, which must not be null.
        img (str): The URL or path to the skin's image, which must not be null.
        type (str): The type of skin, stored as a string up to 15 characters.
        descr (str): A text description of the skin, which is optional.
        ext (str): The exterior type of the skin, stored as a string up to 20 characters.
        category_id (int): Foreign key referencing the category the skin belongs to.
        sub_category_id (int): Foreign key referencing the subcategory the skin belongs to.
    """

    __tablename__ = "skins"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    img: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(String(15), nullable=False)
    descr: Mapped[str] = mapped_column(Text(), nullable=True)
    ext: Mapped[str] = mapped_column(String(20), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    sub_category_id: Mapped[int] = mapped_column(
        ForeignKey("sub_categories.id"), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Skin name={self.name}>"


class Exterior(BaseModel):
    """
    Model representing an exterior of a skin, with optional price references.

    Attributes:
        id (int): The primary key identifier for the exterior.
        ext (str): The exterior type, stored as a string up to 10 characters, which must not be null.
        img (str): The URL or path to the exterior's image, which is optional.
        price_id (int): An optional identifier linking to a specific price record.
        spec_price_id (int): An optional identifier linking to a special price record.
        skin_id (int): Foreign key referencing the skin the exterior belongs to.
    """

    __tablename__ = "exteriors"

    id: Mapped[int] = mapped_column(primary_key=True)
    ext: Mapped[str] = mapped_column(String(10), nullable=False)
    img: Mapped[str] = mapped_column(nullable=True)
    price_id: Mapped[int] = mapped_column(nullable=True)
    spec_price_id: Mapped[int] = mapped_column(nullable=True)
    skin_id: Mapped[int] = mapped_column(ForeignKey("skins.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Exterior ext={self.ext}>"
