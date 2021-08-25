if [ ${#} != 1 ] ; then
	echo -e "\nUsage: runGREGOR.sh configfile\n"
	echo -e "configfile:\tConfiguration file to run.\n"
	exit 1
fi

configfile=$1

perl "/GREGOR/script/GREGOR.pl" -conf "${configfile}" > "${configfile}.out"
