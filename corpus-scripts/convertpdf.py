#!/usr/bin/env jython
import sys

if __name__ == "__main__":
	from sys import argv
	try:
		pdffile = argv[1]
		sys.path.append("/usr/share/java/PDFBox.jar")
		sys.path.append("/usr/share/java/fontbox.jar")
		
		from org.pdfbox.util import PDFTextStripper
		from org.pdfbox.pdmodel import PDDocument
		from java.io import *
		
	except (IndexError, ImportError):
		print "Usage: jython convertpdf.py <PDF file name>"
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise
	else:
		doc = PDDocument.load(FileInputStream(pdffile));
		
		stripper = PDFTextStripper()
		text = stripper.getText(doc)
		print text
