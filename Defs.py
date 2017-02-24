#Per aprire i files
import os
#Per usare le regex
import re
#Per dare il path della cartella con gli input
import sys
#glob per avere lista di file
import glob
#numpy per gli array
import numpy as np
#per avere data-frames
import pandas as pd
#per multithreding
import threading

#===========Function definition============#

# This Function will extract chromosome, position, reference and alternate allele
# And print them in a file

def Position_extractor(vcf_file):
    """Function that extract the position of called variables
    and report them in output files"""
    
    print ("You're analyzing: "+vcf_file)
    print ("The output file will "+vcf_file+".pos")

    #output file
    vcf_file_out=open(vcf_file+".pos",'w')
    #open input file in buffered mode and then do things
    with open(vcf_file,mode="r",buffering = 200000000 ) as vcf_file_in:
        for line in vcf_file_in:
            if line.startswith("##"):
                pass
            else:
                splitted_line = re.split(r'\t+',line)
                #it catches the position and the variants found
                vcf_file_out.write(splitted_line[0]+'\t'+splitted_line[1]+'\t'+splitted_line[2]+'\t'+splitted_line[3]+'\t'+splitted_line[4]+'\n')
    vcf_file_out.close()
    vcf_file_in.close()
    print ("Done, moving to the following \n")
    print ("========================================\n")
    return 1

#To find the number of lines in file

def file_len(fname):
    """Function that extract the number of lines in a file"""
    i=0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1    

#To create a set of the chromosomes considered
def chrom_set(File):
    """Number Set of chromosome in the studied organism """
    chrom_list = []
    original_file = open(File,r'r')
    lines_original_file = original_file.readlines()
    for line in lines_original_file:
        splitted_lines = line.split('\t')
        chrom_list.append(splitted_lines[0])
        chrom_set = set(chrom_list)
        return chrom_set


def Variants(File,List):
    """This Function write chromosome, position and bases
    of the called variants in a list"""
    with open(File,'r',buffering=20000000) as f:  
        lines_f=f.readlines()
        for line in lines_f:
            #splitted_f=line.split('\t')
            #if element == splitted_f[0]:
            List.append(line)
            #else:
                #pass
    return List

def CommonVariants2(File1,File2,OutFile,OutList):
    """Based on the lists from Variants(File,List), find the common
    variant in each list and wirte them down in a file"""
    #for 2 pos files
    #write the lines of variants in a List
    #Each file trated by a thread
    seq_f1 = [] 
    t1 = threading.Thread(target=Variants, args=(File1,seq_f1))
    seq_f2 = []
    t2 = threading.Thread(target=Variants, args=(File2,seq_f2))
    
    #Star the threads
    t1.start()
    t2.start()
    #Syncronize the threads
    t1.join()
    t2.join()

    #open a output file
    out_file=open(OutFile+'.txt','w',buffering=1000000)
    #I find the intersection between the two list with set.intersection
    Inter=list(set(seq_f1).intersection(seq_f2))
    #I print each element of the itersection in the output fil

    for i in Inter:
        OutList.append(i)
        out_file.write(i)
    out_file.close()
    return OutList

def TripleCommonVariants(list1,list2,list3):
    """Gets the output from CommonVariants2, intersect the results
    and write the variants common to 2 or all methods in a file
    called final.txt"""
    
    Inter0_1=list(set(list1).intersection(list2))
    Inter_all=list(set(Inter0_1).intersection(list3))

    diff1=list(set(list1)-set(Inter_all))
    diff2=list(set(list2)-set(Inter_all))
    diff3=list(set(list3)-set(Inter_all))

    final=open('final.txt','w',buffering=20000000)
    for i in diff1:
        final.write(i)

    for i in diff2:
        final.write(i)
   

    for i in diff3:
        final.write(i)
   
    
    for i in Inter_all:
        final.write(i)

    diffs=[diff1,diff2,diff3,Inter_all]        
    final.close
    return diff1,diff2,diff3,Inter_all


#===========End Functon definition=========#
