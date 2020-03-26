#! python3
# pdfParanoia.py - Add password in command line
# to every PDF in folder and subfolders.

import PyPDF2, os, sys

password = sys.argv[1]

for foldername, subfolders, filenames in os.walk(os.getcwd()):

	# Find each PDF after walking through given directory.
	for filename in filenames:
		if (filename.endswith('.pdf')):

			# Rewrite PDF to become encrypted.
			pdfPath = os.path.join(foldername, filename)
			pdfFile = open(pdfPath, 'rb')
			pdfReader = PyPDF2.PdfFileReader(pdfFile)
			pdfWriter = PyPDF2.PdfFileWriter()

			for pageNum in range(pdfReader.numPages):
				pdfWriter.addPage(pdfReader.getPage(pageNum))

			resultFilename = filename[:-4] + '_encrypted.pdf'
			resultPath = os.path.join(foldername, resultFilename)
			resultPdf = open(resultPath, 'wb')

			pdfWriter.encrypt(password)
			pdfWriter.write(resultPdf)
			
			# Close original and result PDFs.
			pdfFile.close()
			resultPdf.close()

			# Verify encryption.
			verifyReader = PyPDF2.PdfFileReader(open(resultPath, 'rb'))
			verifyReader.decrypt(password)

			if verifyReader.getPage(0):

				print('%s encrypted as %s. Deleting %s.' %
					(filename, resultFilename, filename))

				# Delete original.
				os.unlink(pdfPath)
				
			else:
				print('Encryption failed.')
