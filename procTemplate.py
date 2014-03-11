#!/usr/bin/env python
#-*- coding: utf8 -*-
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# you can specify you font 
fontPath = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
pdfmetrics.registerFont(TTFont('MyFont', fontPath))


def template(can, localpage, globalpage):
    """A function that generates a tempmlate pdf"""
    can.setFont('MyFont', 20)

    if localpage == 1:
        can.drawString(10, 800, "A title given to the first page")
        can.drawString(10, 820, u"日本語")
    else:
        can.drawString(10, 800, "A text given to the rest pages")
        can.drawString(10, 820, u"日本語")
    return can


def pagenum(can, localpage, globalpage):
    can.drawString(10, 10, "-%d-" % globalpage)
    return can
