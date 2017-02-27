# -*- coding: utf-8 -*-

""" TrivialCommonCalls.py
Aka Trivial extraction of Common genetic variant Calls in different vcfs

Run this script in a folder containing ONLY the vcf file you want to analyze.
It will search any .vcf file and extract Position (chromosome, numbero of base),
the allele in the reference and in the alternate allele.

The results will be stored in output files
"""

import os
import re
import sys
import glob
import threading
import Defs

#I get the current dir
Current_dir=os.getcwd()
print Current_dir

#Read frome sys.argv[1] the folder containing the 

dir_file=str(sys.argv[1])
vcf_list=glob.glob(dir_file+'*.vcf')
# print '=================================================='


#====VA PARALLELIZZATA!!!!=====
for vcf in vcf_list:
    Defs.Position_extractor(vcf)
#====VA PARALLELIZZATA!!!!====
vcf_pos_list=glob.glob(dir_file+'*.vcf.pos')

print "Finding the Common calls between couples:"
print "=================================================="
print "Common between " + vcf_pos_list[0] + " and " + vcf_pos_list[1] 
Common_0_1_ls=[]
Defs.CommonVariants2(vcf_pos_list[0],vcf_pos_list[1],'Common_0_1',Common_0_1_ls)

print "Common between " + vcf_pos_list[0] + " and " + vcf_pos_list[2] 
Common_0_2_ls=[]
Defs.CommonVariants2(vcf_pos_list[0],vcf_pos_list[2],'Common_0_2',Common_0_2_ls)

print "Common between " + vcf_pos_list[1] + " and " + vcf_pos_list[2] 
Common_1_2_ls=[]
Defs.CommonVariants2(vcf_pos_list[1],vcf_pos_list[2],'Common_1_2',Common_1_2_ls)
 
Common_list=glob.glob(Current_dir+'/Common_*.txt')#harcoded

print '=================================================='
print "Finding common call betweel all the samples and the unique ones"

diffs1,diffs2,diffs3,Inter_all=Defs.TripleCommonVariants(Common_0_1_ls,Common_0_2_ls,Common_1_2_ls)

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
