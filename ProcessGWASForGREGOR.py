import numpy as np
import pandas as pd
import sys
from pathlib import Path
import re

import argparse

parser = argparse.ArgumentParser(description='Program for compiling GWAS catalog associations for GREGOR.')
parser.add_argument("associationfile")
parser.add_argument("outputdirectory")

#Optional arguments
parser.add_argument('-m', dest='excludemultiple', action='store_const', default=False, const=True,
                    help='Exclude multiple SNP associations (rsid1; rsid2; etc.).')
parser.add_argument('-x', dest='excludeinteractions', action='store_const', default=False, const=True,
                    help='Exclude snp interactions (rsid1 x rsid2).')


args = parser.parse_args()
infile = args.associationfile
outfile = args.outputdirectory

includemult = not args.excludemultiple
includeinter = not args.excludeinteractions



#Check inputs
if not Path(infile).is_file:
    print("Gwas trait file does not exit.")
    sys.exit(0)

if Path(outfile).is_dir():
    print("Output directory exists.")
    sys.exit(0)

    
Path(outfile).mkdir(exist_ok=False)
Path(outfile+"/traits/").mkdir()

#Read gwasdata and initialize dictionary for assigning SNPs to traits
gwasdata = pd.read_csv(infile, sep="\t")

traits = list(np.unique(gwasdata["DISEASE/TRAIT"]))

traitdictinit = []
for curtrait in traits:
    traitdictinit.append((curtrait, []))
traitdict = dict(traitdictinit)


#Parse the GWAS catalog file based on optional parameters
singlesnpc = 0
multisnpc = 0
intersnpc = 0
notreadc = 0


for index, currow in gwasdata.iterrows():
    trait = currow['DISEASE/TRAIT']
    snps = currow['SNPS'].strip()
    
    if re.match('rs[0-9]+$', snps):
        traitdict[trait].append(snps)
        singlesnpc += 1
    elif ";" in snps:
        if includemult:
            multisnps = snps.split(";")
            for curmsnp in multisnps:
                curmsnp_stripped = curmsnp.strip()
                if re.match('rs[0-9]+$', curmsnp_stripped):
                    traitdict[trait].append(curmsnp_stripped)
        multisnpc += 1
    elif "x" in snps:
        if includeinter:
            intersnps = snps.split("x")
            for curisnp in intersnps:
                curisnp_stripped = curisnp.strip()
                if re.match('rs[0-9]+$', curisnp_stripped):
                    traitdict[trait].append(curisnp_stripped)
        intersnpc += 1
    else:
        notreadc += 1    


#Write stats
stattable = [["Single SNP association:", singlesnpc],
             ["Multi SNP assocoation ("+("included" if includemult else "excluded")+"):", multisnpc],
             ["SNP interaction assocation ("+("included" if includeinter else "excluded")+"):", intersnpc],
             ["Not read (no rsId, excluded):", notreadc]]

pd.DataFrame(np.array(stattable)).to_csv(outfile+"/stats.txt", sep="\t", index=None, header=None)

#Map new ids for traits that can be used for directories, but only traits with at least 1 rsid
traitmapping = []

index = 1
for curkey in traitdict.keys():
    cursnplist = traitdict[curkey]
    
    if len(cursnplist) > 0:
        traitmapid = "Trait_"+str(index)
        traitmapping.append([traitmapid, curkey])
        pd.DataFrame(np.unique(cursnplist)).to_csv(outfile+"/traits/"+traitmapid+".txt", sep="\t", index=None, header=None)
        index += 1
        
pd.DataFrame(np.array(traitmapping), columns=["TraitId", "Trait Label"]).to_csv(outfile+"/traitmapping.txt", sep="\t", index=None)

