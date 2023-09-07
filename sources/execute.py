#import os
#import sys
#import lci
#import frinfo
#import fr02
#import fr03
#import fr04


#file_lci = "lci.py"
#file_frinfo = "sh ${GITHUB_WORKSPACE}sources/frinfo.py"
file_frinfo = "frinfo.py"
#file_fr02 = "fr02.py"
#file_fr03 = "fr03.py"
#file_fr04 = "fr04.py"


content = """
#open(file_lci).read()
open(file_frinfo).read()
#open(file_fr02).read()
#open(file_fr03).read()
#open(file_fr04).read()
"""
exec(content)
