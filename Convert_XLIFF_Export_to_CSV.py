# -*- coding: utf-8 -*-
#This script takes a proposal export file generated with RS_TRANSLATION_EXPORT_PP (4 character language keys as input and outputs a CSV file containing all proposals, exclusing exceptions.
import os
import re
import codecs
import sys
import xml.etree.ElementTree as ET

#sys.argv  #sys.argv[1] is the file to upload


sourcelang = 0
targetlang = 0
objectname = 0
sourcetext = 0
targettext = 0
domain = 0
translation_units = []
transunit = 0
transunitparam = {'trans-unit'} # has to be escaped because of the minus sign

class Translation_Unit:

    def __init__(self, name):
        self.domain = domain
        self.objectname = objectname
        self.sourcelang = sourcelang
        self.targetlang = targetlang
        self.sourcetext = sourcetext
        self.targettext = targettext

#parse XLIFF and create an object for each translation and add it to a list
#!replace hard path
for filename in os.listdir(os.getcwd()+"/source"):
    with open("source/"+filename) as f:
        tree = ET.parse(f)
        root = tree.getroot()
        for file in root:
            for body in file:
                for trans_unit_parameter in body:
                    transunit = Translation_Unit("x")
                    transunit.objectname = str(re.sub(r'//...//...//......//.+?//', '', (re.search('//...//...//......//.+?//.+', file.get('original')).group(0))))
                    transunit.sourcelang = file.get('source-language')
                    transunit.targetlang = file.get('target-language')
                    transunit.domain = file.get('category')
                    transunit.sourcetext = trans_unit_parameter[0].text
                    transunit.targettext = trans_unit_parameter[1].text
                    #print repr(transunit.sourcelang)
                    #add to list
                    translation_units.append(transunit)
                    
#output CSV as UTF with BOM so MS Excel can read it
with codecs.open ("exported_text_pairs.csv", 'w', encoding='utf-8_sig') as f:
    #add header
    f.write ("SLang;TLang;Source Text;Target Text;Domain;Object Name;Collection\n")
    for i in translation_units:
        #prepend u
        f.write (u"{};{};{};{};{};{}\n".format(i.sourcelang, i.targetlang, i.sourcetext, i.targettext, i.domain, i.objectname))
        