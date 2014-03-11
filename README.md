mkProceedings
=============

Organize a pdf proceedings.
mkProceedings provides the following functinos

* Overlay text on each pages. (e.g., a conference name)
* Merge pdfs into one page
* Insert a pdf file at the beginning (e.g., a preface)
* Separate the proceedings into papers.


Dependent python module
-----------------------
sudo pip install pyPdf

How to use
----------
python mkProceedings.py config.json


Config.json format
------------------

* inputdir: All pdfs in the path will be loaded.
* outputdir: templated & number added pdfs are stored to the path.
* outputpdf: The whole merged pdf.
* preface: The pdf file that will be added to the beginning of the proceedings.
* pagenum: if true, it adds the page numbers for each pages
* template: A template (watermark) for each pages, python script (including watermark function) or a pdf file is acceptable.
* pagesize: A page size. A0, A1, ..., B0, ..., letter are acceptable

License
-------
MIT
