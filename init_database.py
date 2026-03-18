from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, DateTime, Float, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column, Mapped
from models.triangle import TriangleWithCoords

load_dotenv()
DB_FILE = os.getenv("DB_FILE")

engine = create_engine(DB_FILE, pool_pre_ping=True, pool_recycle=300)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()



class TriangleDomain(Base):
    __tablename__ = "triangle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    x1: Mapped[float] = mapped_column(Float)
    y1: Mapped[float] = mapped_column(Float)

    x2: Mapped[float] = mapped_column(Float)
    y2: Mapped[float] = mapped_column(Float)

    x3: Mapped[float] = mapped_column(Float)
    y3: Mapped[float] = mapped_column(Float)

    by: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=7))
    
    edge_type: Mapped[str] = mapped_column(String, nullable=True) # Để nullable=True cho an toàn
    angle_type: Mapped[str] = mapped_column(String, nullable=True)
    
    # THÊM CỘT NÀY VÀO:
    is_valid: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def __init__(self, x1, y1, x2, y2, x3, y3, by):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.x3, self.y3 = x3, y3
        self.by = by

        tri = TriangleWithCoords(x1, y1, x2, y2, x3, y3)
        self.is_valid = tri.valid
        
        if not self.is_valid:
            self.edge_type = None
            self.angle_type = None
        else:
            self.edge_type = tri.triangle_edges.edge_type()
            self.angle_type = tri.triangle_edges.angle_type()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("DB & tables created")
