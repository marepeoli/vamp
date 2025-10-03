from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    perfil_id = Column(Integer, ForeignKey("perfil_usuario.id"))
