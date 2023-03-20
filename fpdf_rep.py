# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 21:01:07 2023

@author: diego
"""

from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
import plots as p
import functions_diego as f
import fmpsdk as fmp
apikey='cdcb171caeb7cc3ab258fb24c77918a1'


# Initialize the PDF object
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.set_margins(left=20, top=20, right=20)

def header():
    pdf.set_xy(20, 10)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(190, 10, 'GreenField Capital', 0, 1, 'C')

header()

def footer():
    pdf.set_xy(20, -15)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(190, 10, 'Page %s' % pdf.page_no(), 0, 1, 'C')



# Title
pdf.set_font("Arial", style='U', size=16)
pdf.cell(190, 10, txt="Google: A Leader in AI and Search Engine Business", ln=1, align='C')

# Subtitle
pdf.set_font("Arial", size=14)
pdf.cell(190, 10, txt="An Overview of the Company's Key Business Units", ln=1, align='C')

# Paragraph 1
pdf.set_font("Arial", size=12)
pdf.multi_cell(190, 10, txt="Google, a subsidiary of Alphabet Inc., is a multinational technology company that specializes in Internet-related services and products. These include search engines, online advertising technologies, cloud computing, software, and hardware. With its roots dating back to the late 1990s, Google has grown to become one of the largest and most influential technology companies in the world. The company's mission is to organize the world's information and make it universally accessible and useful.", align='L')

# Paragraph 2
pdf.set_font("Arial", size=12)
pdf.multi_cell(190, 10, txt="One of the key business units of Google is its search engine. Google's search engine is the most widely used search engine in the world, handling billions of searches every day. The company's search engine is known for its accuracy and relevancy, and it has become an indispensable tool for people around the world who are looking for information on the Internet.", align='L')
# Graph

p.linep([f.clean_financials(fmp.historical_price_full(apikey, 'GOOGL'))['close']], 'linear', ['google'], (6.8,4.6), False, 'Google performance in the past year', 'In USD', 'FMP')
from PIL import Image

def add_image(pdf, image_path, width, margin=20):
    y = pdf.get_y()
    remaining_space = pdf.h - y - margin
    image = Image.open(image_path)
    aspect_ratio = image.height / image.width
    image_height = aspect_ratio * width
    
    if image_height > remaining_space:
        pdf.add_page()
        pdf.image(image_path, x=30, y=pdf.get_y(), w=width)
    else:
        pdf.image(image_path, x=30, y=y, w=width)
        pdf.set_y(y + image_height)

# Example usage:
add_image(pdf, "google.png", 150)


# Paragraph 3
pdf.set_font("Arial", size=12)
pdf.multi_cell(190, 10, txt="Another important business unit of Google is its artificial intelligence (AI) technology. Google has made significant investments in AI research and development, and the company is now at the forefront of AI technology. Google's AI technology is used in a variety of applications, including image and speech recognition, natural language processing, and autonomous vehicles. With its cutting-edge AI technology, Google is well positioned to continue its leadership in the AI industry.", align='L')

footer()


pdf.output("Google_AI_and_Search_Engine_Report.pdf", "F")


