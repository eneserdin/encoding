#!/home/eneserdin/anaconda2/bin/python

import zlib


letter_freq={}
with open('GoodFETMAXUSB.py','rb') as openfileobject:
    for line in openfileobject:
        IreadIt=line
        IreadIt=IreadIt.replace('\n','')
        if '#' not in IreadIt:
            if '"""' not in IreadIt:
                if "'''" not in IreadIt:
                    print(IreadIt)
                    for letter in IreadIt:
                        try:
                            letter_freq[letter]+=1
                        except:
                            letter_freq[letter]=1



print('=======================================================')
print('=======================================================')
print('=======================================================')
print('Below are the frequency of the letters')
print('=======================================================')
print('=======================================================')
print('=======================================================')
print('=======================================================')

letter_freq_list=[]

for ii in letter_freq:
    print(ii, letter_freq[ii])
    letter_freq_list.append([ii,letter_freq[ii]])

def bubble_sort(my_list):
    for jj in range(0,len(my_list)-1):
        for ii in range(0,len(my_list)-1):
            if my_list[ii][1]<my_list[ii+1][1]:
                tmp=my_list[ii]
                tmp1=my_list[ii+1]
                my_list[ii]=tmp1
                my_list[ii+1]=tmp
    return my_list


letter_freq_list=bubble_sort(letter_freq_list)




#~ ============================================================
#~ ============================================================
#~ ============================================================
#~ ============================================================
#~ ============================================================

def deflate(data, compresslevel=9):
    compress = zlib.compressobj(
            compresslevel,        # level: 0-9
            zlib.DEFLATED,        # method: must be DEFLATED
            -zlib.MAX_WBITS,      # window size in bits:
                                  #   -15..-8: negate, suppress header
                                  #   8..15: normal
                                  #   16..30: subtract 16, gzip header
            zlib.DEF_MEM_LEVEL,   # mem level: 1..8/9
            0                     # strategy:
                                  #   0 = Z_DEFAULT_STRATEGY
                                  #   1 = Z_FILTERED
                                  #   2 = Z_HUFFMAN_ONLY
                                  #   3 = Z_RLE
                                  #   4 = Z_FIXED
    )
    deflated = compress.compress(data)
    deflated += compress.flush()
    return deflated

def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


def huffman_codeword_generator():
    depth =[0,1,2,3,4,5]

    
    myset=[]
    
    for ii in depth:
        for jj in depth:
            for kk in depth:
                for ll in depth:
                    print(ii,jj,kk,ll)
                    var=ii*1000+jj*100+kk*10+ll
                    strvar=str(var)
                    if strvar[-1]=='0':
                        if '0' not in strvar[0:-1]:
                            print(var)
                            myset.append(var)

                    #~ while(var%100==0 and not var==0):
                        #~ var=var/10
                        
    print(list(set(myset)))
    return myset



def CalculateMonetaryCostOfMyCode(mycode):
    print(mycode)
    ss=0
    for kk in str(mycode):
        ss+=(int(kk)+1)
    print(ss)

def CalculateTimeCostOfMyCode(mycode):
    print(mycode)
    print(len(str(mycode)))


def CalculateMonetaryCostOfMyCodeword(myset):
    for ii in myset:
        CalculateMonetaryCostOfMyCode(ii)
        
        
def CalculateTimeCostOfMyCodeword(myset):
    for ii in myset:
        CalculateTimeCostOfMyCode(ii)
            
def CalculateCostOfMyCodeword(myset):
    for ii in myset:
        CalculateMonetaryCostOfMyCode(ii)
        CalculateTimeCostOfMyCode(ii)

def InversePointerMyCodewordTable(mydict):
    Inverse={}
    for ii in mydict:
        Inverse[mydict[ii]]=ii
    #~ for ii,jj in enumerate(myset):
        #~ Inverse[jj]=ii
    return Inverse

import os

def AssignCharsToCodewords(myset,letter_freq_list):
    MyCodeWordSet={}
    #Letters should be orderes letters
    if len(myset)<len(letter_freq_list):
        print("Length Error")
        os._exit(1)
    else:
        for jj in range(0,len(letter_freq_list)-1):
            #~ MyCodeWordSet[myset[jj]]=letter_freq_list[jj][0]
            MyCodeWordSet[letter_freq_list[jj][0]]=myset[jj]
    return MyCodeWordSet


myset=huffman_codeword_generator()
mystr="hello World"
compressed=deflate(mystr)


CalculateMonetaryCostOfMyCodeword(myset)
CalculateTimeCostOfMyCodeword(myset)

CalculateCostOfMyCodeword(myset)


MyCodeWordSet=AssignCharsToCodewords(myset,letter_freq_list)
#~ AssignCharsToCodewords(letter_freq_list,myset)

def EncodeItNow(mystr,MyCodeWordSet):
    atput=''
    for ss in mystr:
        atput+=str(MyCodeWordSet[ss])
    return atput


atput=EncodeItNow(mystr,MyCodeWordSet)

InverseCodeWordSet=InversePointerMyCodewordTable(MyCodeWordSet)

print(atput)
def DecodeItNow(atput,InverseCodeWordSet):
    ptr1=0
    for ptr in range(0,len(atput)):
        if atput[ptr]=='0':
            print('THIS')
            found=atput[ptr1:ptr+1]
            print(found)
            print(InverseCodeWordSet[int(found)])
            ptr1=ptr+1

DecodeItNow(atput,InverseCodeWordSet)

import ipdb;ipdb.set_trace()

