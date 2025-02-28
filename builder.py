import random
from reportlab.lib.pagesizes import A4 
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PIL import Image
import streamlit as st
import os

# Predefined Career Objectives
OBJECTIVES = [
    "Seeking a challenging position to utilize my skills and contribute to organizational growth.",
    "Aspiring to work in a dynamic environment that fosters creativity and professional growth.",
    "Dedicated professional aiming to enhance my skills and make a meaningful impact.",
    "Motivated individual seeking opportunities to learn and grow in a professional setting.",
    "Passionate about technology and innovation, looking for opportunities to contribute effectively.",
    "Eager to leverage my expertise in a challenging role to drive company success.",
]

def generate_cv(name, email, phone, objective, skills, experience, education, profile_pic):
    file_name = f"{name}_CV.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    # Header Section
    c.setFillColor(colors.HexColor("#2C3E50"))  # Dark Blue
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(30, height - 50, name)
    
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 70, f"Email: {email} | Phone: {phone}")

    # Profile Picture
    if profile_pic:
        try:
            img = Image.open(profile_pic)
            img = img.resize((100, 100))
            img.save("temp_profile.jpg")
            c.drawImage("temp_profile.jpg", width - 130, height - 130, width=100, height=100)
            os.remove("temp_profile.jpg")
        except Exception as e:
            st.error(f"Error loading image: {e}")

    # Section Styling
    y = height - 120
    c.setStrokeColor(colors.HexColor("#2980B9"))  # Blue line separator
    c.line(30, y, width - 30, y)

    # Function to Add Sections with Bullet Points
    def add_section(title, content, y_offset):
        nonlocal y
        y -= y_offset
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.HexColor("#2980B9"))  # Blue color for section titles
        c.drawString(30, y, title)
        y -= 20
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        
        # Split content into bullet points
        content_list = content.split("\n")
        for line in content_list:
            if line.strip():
                c.drawString(40, y, f"• {line.strip()}")  # Bullet point
                y -= 20

    # Adding Sections
    add_section("Objective:", objective, 40)
    add_section("Skills:", skills, 40)
    add_section("Experience:", experience, 60)
    add_section("Education:", education, 60)

    # Save PDF
    c.save()
    return file_name

# Streamlit UI
st.set_page_config(page_title="CV Builder", page_icon="📝", layout="centered")
st.title("📄 Professional CV Builder")

# User Input Fields (Now in Main Page)
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
profile_pic = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"])

# Predefined Career Objective (Randomly Selected)
default_objective = random.choice(OBJECTIVES)
objective = st.text_area("Career Objective (Customize if needed)", value=default_objective)

skills = st.text_area("Skills (Enter each skill on a new line)")
experience = st.text_area("Work Experience (Enter each experience on a new line)")
education = st.text_area("Education (Enter each qualification on a new line)")

# Generate CV Button
if st.button("Generate CV", help="Click to generate your professional CV"):
    if name and email and phone and skills and experience and education:
        cv_file = generate_cv(name, email, phone, objective, skills, experience, education, profile_pic)

        # Display success message and preview
        st.success("✅ Your CV has been generated successfully!")
        
        # Display CV Preview
        st.write("📄 **CV Preview:** (Download Below)")
        
        with open(cv_file, "rb") as file:
            st.download_button(label="📥 Download CV", data=file, file_name=cv_file, mime="application/pdf")
    else:
        st.error("⚠️ Please fill in all required fields.")
