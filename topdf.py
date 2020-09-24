#!/usr/bin/python2.7


from prettytable import from_csv
from PDFWriter import PDFWriter

def topdf(csv_file):

    fp = open(csv_file, "r")
    mytable = from_csv(fp,sep='|')
    fp.close()
    lines = mytable.get_string()



    pw = PDFWriter('/home/selvaprakash/BillD/Latta2.pdf')
    pw.setFont('Courier', 12)
    pw.setHeader('Demo of PrettyTable to PDF')
    pw.setFooter('Demo of PrettyTable to PDF')
    for line in lines.split('\n'):
        pw.writeLine(line)
    pw.close()