#import os
#import sys
#import lci
import sh ${GITHUB_WORKSPACE}sources/frinfo.py
#import fr02
#import fr03
#import fr04


#file_lci = "lci.py"
file_frinfo = "frinfo.py"
#file_fr02 = "fr02.py"
#file_fr03 = "fr03.py"
#file_fr04 = "fr04.py"


content = """
#open(file_lci).read()
open(file_frinfo).read()
"""
exec(content)
