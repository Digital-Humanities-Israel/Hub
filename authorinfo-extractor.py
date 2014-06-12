#!/usr/bin/env python3
# -*- coding: utf-8 -*-
### this code is intended to extract information about authors from the MARCXml file of the NLI catalogue (רשומות זיהוי) and output them to a txt file
import sys, re, os, time
from xml.etree import ElementTree as ET

out_fna = "authors_info%s" % time.strftime('%Y%m%d_%H%M%S')#gives filename to outputfile a
out_fnb = "authors_altnames%s" % time.strftime('%Y%m%d_%H%M%S')
out_fa = open(out_fna + '.txt', 'w')
out_fb = open(out_fnb + '.txt', 'w')

#def splityears()
 #   birthyear= re.compile(r'\d{4}-\d{4}')#find regex to split and save the first 4 digits in one, the last in the other
  #  deathyear= re.compile(r'')
   # return int(birthyear.group())
    #return int(deathyear.group())


def process_xml(f):
    tree = ET.parse(f)##enter file name
    root= tree.getroot()
    
    for record in root.getchildren():
        libid= record.find('.//controlfield/[@tag="001"]').text 

#Element.findall() finds only elements with a tag which are direct children of the current element. 
#Element.find() finds the first child with a particular tag, and Element.text accesses the element’s text content. 
#Element.get() accesses the element’s attributes:
#rank = country.find('rank').text
# name = country.get('name')
       
        for datafield in record.getchildren(): #change getchildren to grandchildren
            viaf=None
            if datafield.find('./[@tag="901"]') is not None:
                 viaf= datafield.find('./subfield/[@code="a"]')   
                 viaf= viaf.text   
                 print (libid, viaf)#also make it write it into a file
            
            for subfield in datafield.getchildren():
                altname= datafield.find('./subfield/[@code="a"]') 
                if altname is not None:
                    altname=altname.text
                    #print(altname)#just to check. works (but gets false positives from fields other than 100 and 400)
                lang='nolang'
                tag= datafield.get('tag')
                #print(tag)#just to check.works.
                if tag is '100': #here starts the problem
                    print('trial')
                    #print(tag)#just to check - does not work!
                    lang= subfield.find('./[@code="9"]').text
                    if lang is 'heb':  
                        print(lang)
                        lifeyears = subfield.find('./[@code="d"]').text  
                        #birthanddeath = splityears(lifeyears.text) ? at some point?    
                        Cname= altname.text
                        print (libid, viaf, Cname, lifeyears)
                        out_fa.write("{0}, {1}, {2}, {3}\n".format(libid, viaf, Cname, lifeyears))
                elif tag is 400:
                    print(libid, altname, lang)
                    out_fb.write("{0}, {1}, {2}\n".format(libid, altname, lang))
                
#do we really need the argv business? 
def main(argv=None):
    if argv is None:
        argv = sys.argv
        args = argv[1:]
        for arg in args:
            if os.path.exists(arg):
                process_xml(arg)

if __name__ == "__main__":
    main()