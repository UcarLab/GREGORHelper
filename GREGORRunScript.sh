#!/bin/bash 

case $1 in
    BuildGWAS) 
        python3 /GREGOR/ProcessGWASForGREGOR.py "${@:2}" ;;
    ConfigureGREGOR) 
        /GREGOR/ConfigureGREGOR.sh "${@:2}" ;;
    RunGREGOR) 
        /GREGOR/RunGREGOR.sh "${@:2}" ;;
    SummarizeGREGOR) 
        /GREGOR/SummarizeGREGORResults.sh "${@:2}" ;;
    *) echo "Commands: BuildGWAS ConfigureGREGOR RunGREGOR SummarizeGREGOR" ;;
esac



