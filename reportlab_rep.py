# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 02:01:34 2023

@author: diego
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report():
    # create a canvas
    c = canvas.Canvas("report.pdf", pagesize=letter)

    # add header
    c.setTitle("Google Stock Price Report")
    c.setAuthor("Author Name")
    c.setSubject("Google Stock Price Report")
    c.setKeywords("Google, Stock Price, Report")

    # add header and footer
    c.setHeader("Google Stock Price Report")
    c.setFooter("Page %s of %s" % (c.getPageNumber(), c.getNumPages()))

    # add text
    c.drawString(72, 720, "Google Stock Price Report")
    c.drawString(72, 700, "The past 2 years of Google's stock price performance")

    # add graph
    c.drawImage("google.png", 36, 500, 500, 375)

    # save the PDF
    c.save()

# if __name__ == "__main__":
#     generate_report()
