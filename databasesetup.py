from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sys
Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'

    name = Column(
        String(100),
        nullable=False
    )
    id = Column(
        Integer,
        primary_key=True
    )


class MenuItem(Base):
    __tablename__='menu'

    name = Column(
        String(150),
        nullable=True
    )
    id = Column(
        Integer,primary_key=True
    )
    course = Column(
        String(80)
    )
    restaurant = relationship(Restaurant)
    restaurant_id = Column(
        Integer,
        ForeignKey("restaurant.id")
    )
    price = Column(
        String(8),
        nullable=False
    )
    description = Column(
        String(250)
    )




engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.create_all(engine)
