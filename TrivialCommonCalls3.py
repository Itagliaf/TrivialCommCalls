#!/pico/scratch/userinternal/itagliaf/pipelineMarco/MultipleCall2/venv/bin/python
#prendo il python della virtualenv
# -*- coding: utf-8 -*-

""" TrivialCommonCalls.py
Aka Trivial extraction of Common genetic variant Calls in different vcfs

Run this script in a folder containing ONLY the vcf file you want to analyze.
It will search any .vcf file and extract Position (chromosome, numbero of base),
the allele in the reference and in the alternate allele.

The results will be stored in output files

"""
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

#Mi tengo da parte la directory di lavoro
Current_dir=os.getcwd()
print Current_dir

# #impostare la cartella dove sono i campioni
# #legge dal primo argomeno
# #NB: sistmare lo slash

dir_file=str(sys.argv[1])
vcf_list=glob.glob(dir_file+'*.vcf')
# print '=================================================='


# #====VA PARALLELIZZATA!!!!=====
# for vcf in vcf_list:
#     Position_extractor(vcf)
# #====VA PARALLELIZZATA!!!!====
vcf_pos_list=glob.glob(dir_file+'*.vcf.pos')

#I open a vcf file and read all lines

#f2 = open(vcf_pos_list[0],'r')
#lines_f2=f2.readlines()

#I will create a list of cromosomes as set of the first elemen of each line
# chrom_list = []
# for line in lines_f2:
#     splitted_lines_f2 = line.split('\t')
#     chrom_list.append(splitted_lines_f2[0])

# chrom_set = set(chrom_list)

# f2.close()

print "Finding the Common calls between couples:"
print "=================================================="
print "Common between " + vcf_pos_list[0] + " and " + vcf_pos_list[1] 
Common_0_1_ls=[]
CommonVariants2(vcf_pos_list[0],vcf_pos_list[1],'Common_0_1',Common_0_1_ls)

print "Common between " + vcf_pos_list[0] + " and " + vcf_pos_list[2] 
Common_0_2_ls=[]
CommonVariants2(vcf_pos_list[0],vcf_pos_list[2],'Common_0_2',Common_0_2_ls)

print "Common between " + vcf_pos_list[1] + " and " + vcf_pos_list[2] 
Common_1_2_ls=[]
CommonVariants2(vcf_pos_list[1],vcf_pos_list[2],'Common_1_2',Common_1_2_ls)
 
Common_list=glob.glob(Current_dir+'/Common_*.txt')#harcoded

print '=================================================='
print "Finding common call betweel all the samples and the unique ones"

diffs1,diffs2,diffs3,Inter_all=TripleCommonVariants(Common_0_1_ls,Common_0_2_ls,Common_1_2_ls)

Inter_All_Sort=sorted(Inter_all)

with open(vcf_list[0],mode="r",buffering = 200000000 ) as vcf_file_in:
    for line in vcf_file_in:
        if line.startswith("##"):
                pass
        else:
            splitted_line = line.split('\t')
            line_head=splitted_line[0]+'\t'+splitted_line[1]+'\t'+splitted_line[2]+'\t'+splitted_line[3]+'\t'+splitted_line[4]
            #            print splitted_line[0]
            for common_element in Inter_All_Sort:
                print line_head[0] + ' ' + common_element[0]
                print splitted_line[0]==common_element[0]
                # if splitted_line[0]==common_element[0]:
                #     if line_head==common_element:
                #         print line
                #         print line_head+common_element
                #         break
                #     else:
                #         print "Same Contig Different Sequence "+line_head+" "+common_element
                # else:
                #     print "Different Contig"+line_head+" "+common_element
                    
vcf_file_in.close()
