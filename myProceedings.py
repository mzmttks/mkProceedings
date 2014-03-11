#!/usr/bin/env python

import glob
import sys
import json
import StringIO
import os.path

from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
import reportlab.lib.pagesizes

import procTemplate

# load config
if len(sys.argv) != 2:
    print "usage: myProceedings.py config.json"
    sys.exit()
with open(sys.argv[1]) as handle:
    config = json.loads("".join(handle.readlines()))

# prepare output pdf
proceedings = PdfFileWriter()
preface = PdfFileReader(file(config["preface"], "rb"))
for p in range(preface.numPages):
    proceedings.addPage(preface.getPage(p))

# setup canvas
pdfsize = getattr(reportlab.lib.pagesizes, config["pagesize"])


def makeWatermark(func, localpage, globalpage):
    packet = StringIO.StringIO()  # a buffer
    can = canvas.Canvas(packet, pagesize=pdfsize)

    can = func(can, localpage, globalpage)
    can.save()
    packet.seek(0)
    return PdfFileReader(packet)


numpagelist = []


# merge pdfs
pagecount = preface.numPages

for pdf in glob.glob(os.path.join(config["inputdir"], "*.pdf")):
    print "Combining", pdf, "..."

    # read your existing PDF
    existing_pdf = PdfFileReader(file(pdf, "rb"))

    st = pagecount
    # add the "watermark" (which is the new pdf) on the existing page
    for p in range(existing_pdf.numPages):
        # make a watermark
        watermark = makeWatermark(procTemplate.template, p+1, pagecount+1)

        page = existing_pdf.getPage(p)
        page.mergePage(watermark.getPage(0))

        pagenum = makeWatermark(procTemplate.pagenum, p+1, pagecount+1)
        page.mergePage(pagenum.getPage(0))

        proceedings.addPage(page)
        pagecount += 1
    ed = pagecount
    numpagelist.append((st, ed))


# finally, write "output" to a real file
stream = file(config["outputpdf"], "wb")
proceedings.write(stream)
stream.close()
print 
print "Proceedings is created at"
print "    %s" % (os.path.abspath(config["outputpdf"]))


# separate proceedings
proc = PdfFileReader(file(config["outputpdf"], "rb"))
for inum, numpage in enumerate(numpagelist):
    pdfobj = PdfFileWriter()
    for i in range(numpage[0], numpage[1]):
        pdfobj.addPage(proc.getPage(i))
    pdfname = os.path.join(config["outputdir"], "pdf%05d.pdf" % inum)
    stream = file(pdfname, "wb")
    pdfobj.write(stream)
    stream.close()

    print "A separated paper is created at"
    print "    %s" % (os.path.abspath(pdfname))
