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

out_fa.write("libID\tAuthor\tBirth_Year\tDeath_Year\n")
out_fb.write("libID\tAlternative_names\tScript_of_alternative_name\n")
out_fc.write("libID\tViaf_no\n")


#def splityears()

 #   birthyear= re.compile(r'\d{4}-')#find regex to split and save the first 4 digits in one, the last in the other
  #  deathyear= re.compile(r'\d{4}-\d{4}')
   # return int(birthyear.group())
    #return int(deathyear.group())


def process_xml(f):
    tree = ET.parse(f)
    root= tree.getroot()
    
    for record in root.getchildren():
        libid= record.find('.//controlfield/[@tag="001"]').text 

        for fieldinrecord in record.getchildren(): 
            viaf=None
            if fieldinrecord.find('./[@tag="901"]') is not None:
                 viaf= fieldinrecord.find('./subfield/[@code="a"]')   
                 viaf= viaf.text   
                 #print (libid, viaf)
                 out_fc.write("{0}\t{1}\n".format(libid, viaf))
            
            if fieldinrecord.find('./[@tag="100"]') is not None:
                #tag= fieldinrecord.get('tag')
                lang= fieldinrecord.find('./subfield/[@code="9"]').text 
                if lang== 'heb':  
                    lifeyears = fieldinrecord.find('./subfield/[@code="d"]')
                    if lifeyears is not None:
                        life_years = lifeyears.text 
                        life_years = life_years.split('-')  
                        #print(life_years)
                        #print(life_years[0], life_years[1])
 
                    Cname= fieldinrecord.find('./subfield/[@code="a"]').text
                    #if Cname is not None:
                        #Cname=Cname.text
                                #print (libid, viaf, Cname, lifeyears)
                                    #out_fa.write("{0}\t{1}\t{2}\n".format(libid, Cname, lifeyears.text))
                                    #out_fa.write("{0}\t{1}\t{2}\n".format(libid, Cname, life_years))
                                    # try:
                    out_fa.write("{0}\t{1}\t{2}\t{3}\n".format(libid, Cname, life_years[0], life_years[1]))
                            
                    
                    #if tag== '100': 
                else:
                    altname= fieldinrecord.find('./subfield/[@code="a"]').text
                    out_fb.write("{0}\t{1}\t{2}\n".format(libid, altname, lang))
                 
            elif fieldinrecord.find('./[@tag="400"]') is not None:
                lang= fieldinrecord.find('./subfield/[@code="9"]').text 
                if lang is not None:
                    #print(libid, altname, lang.text) #just lang doesn't work
                    altname= fieldinrecord.find('./subfield/[@code="a"]').text
                    out_fb.write("{0}\t{1}\t{2}\n".format(libid, altname, lang))
                    
def main(argv=None):
    if argv is None:
        argv = sys.argv
        args = argv[1:]
        for arg in args:
            if os.path.exists(arg):
                process_xml(arg)

if __name__ == "__main__":
    main()