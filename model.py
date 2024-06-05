from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BusinessCard(Base):
    __tablename__ = "business_cards"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    card_holder_name = Column(String)
    designation = Column(String)
    mobile_number = Column(String)
    email_address = Column(String)
    website_url = Column(String)
    area = Column(String)
    city = Column(String)
    state = Column(String)
    pin_code = Column(String)
    image = Column(LargeBinary)
