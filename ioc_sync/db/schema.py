from typing import List

from sqlalchemy import DateTime, func, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship, declared_attr, Mapped, mapped_column


class BaseEntity(DeclarativeBase):
    pass


class DataSource(BaseEntity):
    __tablename__ = "data_source"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alias: Mapped[str] = mapped_column(String, unique=True)
    url: Mapped[str] = mapped_column(String)
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now(), insert_default=func.now())
    ip_ioc: Mapped[List["IpIoc"]] = relationship("IpIoc",
                                                 back_populates="data_source"
                                                 )
    url_ioc: Mapped[List["UrlIoc"]] = relationship("UrlIoc",
                                                   back_populates="data_source"
                                                   )


class Ioc:
    __tablename__ = 'ioc'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now(), insert_default=func.now())

    @declared_attr
    def data_source_id(cls):
        return mapped_column(ForeignKey("data_source.id"))

    @declared_attr
    def data_source(cls):
        return relationship("DataSource", back_populates=cls.__tablename__)


class IpIoc(BaseEntity, Ioc):
    __tablename__ = "ip_ioc"
    ip: Mapped[str] = mapped_column(String)
    __table_args__ = (UniqueConstraint('ip', 'data_source_id', name='ip_data_source_uc'),)


class UrlIoc(BaseEntity, Ioc):
    __tablename__ = "url_ioc"
    url: Mapped[str] = mapped_column(String)
    __table_args__ = (UniqueConstraint('url', 'data_source_id', name='url_data_source_uc'),)
