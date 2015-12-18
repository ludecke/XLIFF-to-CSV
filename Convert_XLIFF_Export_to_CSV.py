# -*- coding: utf-8 -*-
#This script takes XLIFF exports from a Unicode SAP system and outputs a CSV containing source text, target text, and domain.
#Duplicates (source *and* target text are the same) are removed, but duplicates for target texts shorter than 5 characters are
#only removed within domains, so one instance remains per domain.

import os
import re
import codecs
import sys
import xml.etree.ElementTree as ET

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
                    #set target text for red lines to standard value
                    for target in trans_unit_parameter:
                        if target.text is None:
                            transunit.targettext = "this is actually a red line, don't add it"
                        else:
                            transunit.targettext = target.text
                        
                    #exlude supplemented lines and red lines
                    if not transunit.sourcetext == transunit.targettext:
                        if transunit.targettext != "this is actually a red line, don't add it":
                    #exclude duplicates
                    #if the source text is very short, allow 1 duplicates for each domain, since they will be created as exceptions in PP.
                    #Modify the numer to change minimum length
                            if len(transunit.sourcetext) > 4:
                                if not any (s.targettext == transunit.targettext and s.sourcetext == transunit.sourcetext for s in translation_units):
                                    translation_units.append(transunit)
                    #if the source text longer, allow no duplicates, ignoring domains
                            else:
                                if not any (s.targettext == transunit.targettext and s.sourcetext == transunit.sourcetext and s.domain == transunit.domain for s in translation_units):
                                    translation_units.append(transunit)

#output CSV as UTF with BOM so MS Excel can read it
with codecs.open ("exported_text_pairs.csv", 'w', encoding='utf-8_sig') as f:
    #add header
    f.write ("SLang;TLang;Source Text;Target Text;Domain;Object Name;Collection\n")
    for i in translation_units:
        #prepend u
        f.write (u"{};{};{};{};{};{}\n".format(i.sourcelang, i.targetlang, i.sourcetext, i.targettext, i.domain, i.objectname))