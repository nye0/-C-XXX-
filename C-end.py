#!/anaconda3/bin/python
import xml.etree.cElementTree as et
import pandas as pd
import sys
def Reader(XML,ResultPath):
    result=[]
    parsedXML = et.parse(XML)
    for c in parsedXML.getroot():
        t=c.tag
        if t=='BlastOutput_iterations':
            for sc in c.getchildren():
                for s in sc.getchildren():
                    tt=s.tag
                    if tt=='Iteration_hits':
                        for h in s.getchildren():
                            for hs in h.getchildren():
                                if hs.tag=='Hit_id':
                                    ID=hs.text
                                if hs.tag=='Hit_len':
                                    P_length=hs.text
                                if hs.tag=='Hit_def':
                                    Name=hs.text
                                if hs.tag=='Hit_hsps':
                                    for hss in hs.getchildren():
                                        for hspuse in hss.getchildren():
#                                             print(hss.items)
                                            if hspuse.tag=='Hsp_hit-from':
                                                Hit_from=hspuse.text
                                            if hspuse.tag=='Hsp_hit-to':

                                                Hit_end=hspuse.text
                                                if Hit_end==P_length:
                                                    result.append({'ID':ID,'Name':Name,
                                                                   'P_length':P_length,
                                                                   'From':Hit_from,
                                                                   'End':Hit_end})
                                           
                                            
    Df=pd.DataFrame(result)
    Df.to_excel(ResultPath)
    return Df
XML=sys.argv[1]
ResultPath=sys.argv[2]
Reader(XML,ResultPath)
