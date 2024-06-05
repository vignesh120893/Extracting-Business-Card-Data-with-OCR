import streamlit as st
from PIL import Image
import easyocr
from models import BusinessCard, Base
from db import SessionLocal, engine
from sqlalchemy.orm import sessionmaker
import io

# Create the database tables
Base.metadata.create_all(bind=engine)

def extract_info_from_image(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(np.array(image))
    
    # Process results to extract specific information
    info = {
        "company_name": "",
        "card_holder_name": "",
        "designation": "",
        "mobile_number": "",
        "email_address": "",
        "website_url": "",
        "area": "",
        "city": "",
        "state": "",
        "pin_code": ""
    }
    
    for detection in result:
        text = detection[1]
        # Implement regex or string matching to fill info dictionary
        # Example for email:
        if "@" in text:
            info["email_address"] = text
        # Add further processing logic here
    
    return info

def display_extracted_info(info):
    st.write("Extracted Information:")
    for key, value in info.items():
        st.write(f"{key.replace('_', ' ').title()}: {value}")

def save_to_database(image, info):
    db = SessionLocal()
    card = BusinessCard(
        company_name=info["company_name"],
        card_holder_name=info["card_holder_name"],
        designation=info["designation"],
        mobile_number=info["mobile_number"],
        email_address=info["email_address"],
        website_url=info["website_url"],
        area=info["area"],
        city=info["city"],
        state=info["state"],
        pin_code=info["pin_code"],
        image=image.read()
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    db.close()
    st.success("Information saved successfully!")

def main():
    st.title("BizCardX: Business Card Data Extractor")
    uploaded_file = st.file_uploader("Upload a business card image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Business Card', use_column_width=True)

        if st.button("Extract Information"):
            extracted_info = extract_info_from_image(image)
            display_extracted_info(extracted_info)

        if st.button("Save to Database"):
            save_to_database(uploaded_file, extracted_info)
    
    if st.button("Show Database Entries"):
        show_database_entries()

def show_database_entries():
    db = SessionLocal()
    cards = db.query(BusinessCard).all()
    for card in cards:
        st.write(f"ID: {card.id}")
        st.write(f"Company Name: {card.company_name}")
        st.write(f"Card Holder Name: {card.card_holder_name}")
        st.write(f"Designation: {card.designation}")
        st.write(f"Mobile Number: {card.mobile_number}")
        st.write(f"Email Address: {card.email_address}")
        st.write(f"Website URL: {card.website_url}")
        st.write(f"Area: {card.area}")
        st.write(f"City: {card.city}")
        st.write(f"State: {card.state}")
        st.write(f"Pin Code: {card.pin_code}")
        st.image(Image.open(io.BytesIO(card.image)), caption='Business Card Image', use_column_width=True)
        if st.button(f"Delete ID {card.id}"):
            delete_entry(card.id)
    db.close()

def delete_entry(card_id):
    db = SessionLocal()
    card = db.query(BusinessCard).filter(BusinessCard.id == card_id).first()
    db.delete(card)
    db.commit()
    db.close()
    st.success(f"Entry ID {card_id} deleted successfully!")

if __name__ == "__main__":
    main()
