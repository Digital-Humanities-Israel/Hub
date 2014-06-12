#!/usr/bin/env python3
# -*- coding: utf-8 -*-
### this code is intended to extract information about authors from the MARCXml file of the NLI catalogue (רשומות זיהוי) and output them to a txt file
import sys, re, os, time
from xml.etree import ElementTree as ET

out_fna = "authors_info%s" % time.strftime('%Y%m%d_%H%M%S')#gives filename to outputfile a
out_fnb = "authors_altnames%s" % time.strftime('%Y%m%d_%H%M%S')
out_fnc = "lib_to_viaf%s" % time.strftime('%Y%m%d_%H%M%S')
out_fa = open(out_fna + '.txt', 'w')
out_fb = open(out_fnb + '.txt', 'w')
out_fc = open(out_fnc + '.txt', 'w')


#def splityears()
 #   birthyear= re.compile(r'\d{4}-\d{4}')#find regex to split and save the first 4 digits in one, the last in the other
  #  deathyear= re.compile(r'')
   # return int(birthyear.group())
    #return int(deathyear.group())


def process_xml(f):
    tree = ET.parse(f)
    root= tree.getroot()
    
    for record in root.getchildren():
        libid= record.find('.//controlfield/[@tag="001"]').text 

        for datafield in record.getchildren(): 
            viaf=None
            if datafield.find('./[@tag="901"]') is not None:
                 viaf= datafield.find('./subfield/[@code="a"]')   
                 viaf= viaf.text   
                 #print (libid, viaf)
                 out_fc.write("{0}\t{1}\n".format(libid, viaf))
            for subfield in datafield.getchildren():
                 altname= datafield.find('./subfield/[@code="a"]') 
                 if altname is not None:
                    altname=altname.text
                 tag= datafield.get('tag')
                 lang= datafield.find('./subfield/[@code="9"]') 
                 if tag== '100': 
                        if lang.text== 'heb':  
                            lifeyears = datafield.find('./subfield/[@code="d"]')  
                        #birthanddeath = splityears(lifeyears.text) ? at some point?    
                            Cname= altname
                            if lifeyears is not None:
                                #print (libid, viaf, Cname, lifeyears)
                                out_fa.write("{0}\t{1}\t{2}\n".format(libid, Cname, lifeyears.text))
                 elif tag== '400':
                        if lang is not None:
                            #print(libid, altname, lang.text) #just lang doesn't work
                            out_fb.write("{0}\t{1}\t{2}\n".format(libid, altname, lang.text))
                
def main(argv=None):
    if argv is None:
        argv = sys.argv
        args = argv[1:]
        for arg in args:
            if os.path.exists(arg):
                process_xml(arg)

if __name__ == "__main__":
    main()