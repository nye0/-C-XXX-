#!/anaconda3/bin/python
import xml.etree.cElementTree as et
import pandas as pd
import sys
import re
def IDTrans(IDList,From='ACC+ID',To='GENENAME'):
    import urllib.parse
    import urllib.request

    url = 'https://www.uniprot.org/uploadlists/'
    IDs=' '.join(IDList)


    params = {
    'from': From,
    'to': To,
    'format': 'tab',
    'query': IDs,
    }

    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
           response = f.read()
    Raw=response.decode('utf-8')
    Use=[i.split('\t') for i in Raw.strip().split('\n')[1:]]
#     RawID=[i[0] for i in Use]
#     TransID=[i[1] for i in Use]
    return Use

def Reader(XML):
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
                                                    result.append({'ID':ID,
                                                                   'ID_FullVersion':Name,
                                                                   'P_length':P_length,
                                                                   'From':Hit_from,
                                                                   'End':Hit_end})
                                           
                                            
    Df=pd.DataFrame(result)
    return Df
def IDprepare(ID,ID_FullVersion):
    Pair={'gb':'EMBL','dbj':'EMBL','emb':'EMBL','ref':'P_REFSEQ_AC','pdb':'PDB_ID'}
    F0,IDUse,NoteUse,Warning=None,None,'',0
    temp=ID.strip('|').split('|')
    temp_notelist=[]
    FullVersionContain_sp=re.findall('\>sp\|(.*?)\|',ID_FullVersion)
    if temp[0]=='sp':
        IDFormat='ACC+ID'
        IDUse=temp[1]
        Warning=0
    else:
        if len(FullVersionContain_sp)==1:
            IDFormat='ACC+ID'
            IDUse=FullVersionContain_sp[0]
        else:
            if len(FullVersionContain_sp)>1:
                Warning+=1
                Note=':'.join(['More Than one ACC found!','|'.join(FullVersionContain_sp)])
                temp_notelist.append(Note)
                IDFormat='ACC+ID'
                IDUse=FullVersionContain_sp[0]

            else:
                if len(temp)==2:
                    F0,IDUse=temp
                else:
                    if len(temp)!=2:
                        if len(temp)>2:
                            F0,IDUse=temp[0],temp[1]
                            Warning+=1
                            Note=':'.join(['IDUse may not be correct, ID have more contains than expect!',ID])
                            temp_notelist.append(Note)
                if F0 in Pair.keys():
                    IDFormat=Pair[F0]
                else:
                    Warning+=1
                    Note=':'.join(['ID do not contain the needed format, search format among ID_FullVersion',ID])
                    temp_notelist.append(Note)
                    Patterns=[(k,'\>%s\|.*?\|',Pair[k]) % k for k in Pair.keys()]
                    # bug, if format if gb|111|1, id will be 111, without warning!
                    for f,p,IDFormat0 in Patterns:
                        R=re.findall(p,ID_FullVersion)
                        lR=len(R)
                        if lR>0:
                            if len(R)==1:
                                IDFormat=IDFormat0
                                IDUse=R[0]
                            else:
                                Warning+=1
                                Note=':'.join(["ID_FullVersion contain more than one '%s' format" % f,'|'.join(R)])
                                temp_notelist.append(Note)
                        else:
                            continue



    NoteUse=';'.join(temp_notelist)
    return {'RawFormat':IDFormat,'RawFormatID':IDUse,
            'ID':ID,'ID_FullVersion':ID_FullVersion,
            'IDPrepWarning':Warning,'IDPrepNote':NoteUse}
def Main(XMLPath,ResultPath):
    Df0=Reader(XMLPath)
    IDPreparedDf=pd.DataFrame([IDprepare(ID,Full) for ID,Full in Df0.loc[:,['ID','ID_FullVersion']].values])

    FormatsRaw=set(IDPreparedDf.loc[:,'RawFormat'])-{'ACC+ID'}
    Df1=IDPreparedDf.loc[IDPreparedDf.loc[:,'RawFormat']=='ACC+ID',:]
    Df1.loc[:,'UniProtKB_ACC']=Df1.loc[:,'RawFormatID'].map(lambda x:x.split('.')[0])

    for f in FormatsRaw:
        Dftemp=IDPreparedDf.loc[IDPreparedDf.loc[:,'RawFormat']==f,:]
        IDList=Dftemp.loc[:,'RawFormatID'].dropna().values
        f2ACC=IDTrans(IDList=IDList,From=f,To='ACC')
        Dftemp.loc[:,'UniProtKB_ACC']=Dftemp.loc[:,'RawFormatID'].map(dict(f2ACC))
        Df1=pd.concat([Df1,Dftemp])

    ACC2GENENAME=IDTrans(IDList=Df1.loc[:,'UniProtKB_ACC'].dropna().values,
                         From='ACC',To='GENENAME')
    ACC2ENSEMBL_ID=IDTrans(IDList=Df1.loc[:,'UniProtKB_ACC'].dropna().values,
                         From='ACC',To='ENSEMBL_ID')
    Df1.loc[:,'GENENAME']=Df1.loc[:,'UniProtKB_ACC'].map(dict(ACC2GENENAME))
    Df1.loc[:,'ENSEMBL_ID']=Df1.loc[:,'UniProtKB_ACC'].map(dict(ACC2ENSEMBL_ID))

    DfFinial=pd.merge(Df0,Df1,on=['ID','ID_FullVersion'],how='outer')
    DfFinial.to_excel(ResultPath)
    return DfFinial

XML=sys.argv[1]
ResultPath=sys.argv[2]
Main(XML,ResultPath)
