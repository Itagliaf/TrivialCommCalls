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
import argparse
import shutil

import Defs
#====CREATE A PARSER====

parser = argparse.ArgumentParser(description='Options')
parser.add_argument("-i" ,"--input_folder",
                    type=str,
                    dest="input_folder",
                    help="Folder containig input vcfs")

parser.add_argument("-o" ,"--output_folder",
                    type=str,
                    dest="output_folder",
                    help="Folder that will contain the results")

#To show "How to use" when no arguments are given

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
#Add the arguments to the program
args = parser.parse_args()

#====Checking Arguments====
print "Checking Arguments...\n"

dir_file=args.input_folder
if os.path.exists(os.path.abspath(args.input_folder)):
    print "The folder containing the inputs is:"
    print os.path.abspath(args.input_folder)
else:
    raise NameError("No Input folder")


if os.path.exists(os.path.abspath(args.output_folder)):
    print "\n"
    print "The folder that will contain the output is:"
    print os.path.abspath(args.output_folder)
    out_folder=args.output_folder
else:
    raise NameError("No Output folder")

print "\nLook good here, moving on \n"
#====Check End====
vcf_list=glob.glob(str(dir_file)+'*.vcf')
print vcf_list

print "Your input files are: \n" 
for i in vcf_list:
    print i

#========================

#I get the current dir
Current_dir=os.getcwd()
print Current_dir
print '=================================================='

#====VA PARALLELIZZATA!!!!=====
for vcf in vcf_list:
     Defs.Position_extractor(vcf)
#====VA PARALLELIZZATA!!!!====

#move pos files
files = glob.iglob(os.path.join(dir_file, "*.pos"))
for file in files:
    if os.path.isfile(file):
        shutil.copy2(file, out_folder)

vcf_pos_list=glob.glob(out_folder+'*.vcf.pos')


print "Finding the Common calls between couples:"
print "=================================================="
print "Common between " + vcf_pos_list[0] + " and " + vcf_pos_list[1] 
Common_0_1_ls=[]
Defs.CommonVariants2(vcf_pos_list[0],vcf_pos_list[1],out_folder+'Common_0_1',Common_0_1_ls)

print "Common between " + vcf_pos_list[0] + " and " + vcf_pos_list[2] 
Common_0_2_ls=[]
Defs.CommonVariants2(vcf_pos_list[0],vcf_pos_list[2],out_folder+'Common_0_2',Common_0_2_ls)

print "Common between " + vcf_pos_list[1] + " and " + vcf_pos_list[2] 
Common_1_2_ls=[]
Defs.CommonVariants2(vcf_pos_list[1],vcf_pos_list[2],out_folder+'Common_1_2',Common_1_2_ls)
 
Common_list=glob.glob(out_folder+'/Common_*.txt')#harcoded

print '=================================================='
print "Finding common call betweel all the samples and the unique ones"

diffs1,diffs2,diffs3,Inter_all=Defs.TripleCommonVariants(Common_0_1_ls,Common_0_2_ls,Common_1_2_ls,out_folder)

Inter_All_Sort=sorted(Inter_all)


# with open(vcf_list[0],mode="r",buffering = 200000000 ) as vcf_file_in:
#     for line in vcf_file_in:
#         if line.startswith("##"):
#                 pass
#         else:
#             splitted_line = line.split('\t')
#             line_head=splitted_line[0]+'\t'+splitted_line[1]+'\t'+splitted_line[2]+'\t'+splitted_line[3]+'\t'+splitted_line[4]
#             #            print splitted_line[0]
#             for common_element in Inter_All_Sort:
#                 print line_head[0] + ' ' + common_element[0]
#                 print splitted_line[0]==common_element[0]
#                 # if splitted_line[0]==common_element[0]:
#                 #     if line_head==common_element:
#                 #         print line
#                 #         print line_head+common_element
#                 #         break
#                 #     else:
#                 #         print "Same Contig Different Sequence "+line_head+" "+common_element
#                 # else:
#                 #     print "Different Contig"+line_head+" "+common_element
                    
# vcf_file_in.close()
