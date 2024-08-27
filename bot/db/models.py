from sqlalchemy import ForeignKey, String, Text, DateTime
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


# class BaseModel(DeclarativeBase):
#     __abstract__ = True
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     created_at: Mapped[str] = mapped_column(DateTime(timezone=True), default=datetime.datetime.utcnow)
#     updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), default=datetime.datetime.utcnow)
#
#     def before_save(self, *args, **kwargs):
#         pass
#
#     def after_save(self, *args, **kwargs):
#         pass
#
#     def save(self, commit=True):
#         self.before_save()
#         db.session.add(self)
#         if commit:
#             try:
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 raise e
#
#         self.after_save()
#
#     def before_update(self, *args, **kwargs):
#         pass
#
#     def after_update(self, *args, **kwargs):
#         pass
#
#     def update(self, *args, **kwargs):
#         self.before_update(*args, **kwargs)
#         db.session.commit()
#         self.after_update(*args, **kwargs)
#
#     def delete(self, commit=True):
#         db.session.delete(self)
#         if commit:
#             db.session.commit()
#
#     @classmethod
#     def eager(cls, *args):
#         cols = [orm.joinedload(arg) for arg in args]
#         return cls.query.options(*cols)
#
#     @classmethod
#     def before_bulk_create(cls, iterable, *args, **kwargs):
#         pass
#
#     @classmethod
#     def after_bulk_create(cls, model_objs, *args, **kwargs):
#         pass
#
#     @classmethod
#     def bulk_create(cls, iterable, *args, **kwargs):
#         cls.before_bulk_create(iterable, *args, **kwargs)
#         model_objs = []
#         for data in iterable:
#             if not isinstance(data, cls):
#                 data = cls(**data)
#             model_objs.append(data)
#
#         db.session.bulk_save_objects(model_objs)
#         if kwargs.get('commit', True) is True:
#             db.session.commit()
#         cls.after_bulk_create(model_objs, *args, **kwargs)
#         return model_objs
#
#     @classmethod
#     def bulk_create_or_none(cls, iterable, *args, **kwargs):
#         try:
#             return cls.bulk_create(iterable, *args, **kwargs)
#         except exc.IntegrityError as e:
#             db.session.rollback()
#             return None
