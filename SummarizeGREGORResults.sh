if [ ${#} != 1 ] ; then
	echo -e "\nUsage: outdir\n"
	echo -e "outdir:\tThe GREGOR output directory.\n"
	exit 1
fi

OUTDIR=$1

#################
#Combine Results#
#################

OUTFILE=${OUTDIR}/Results.txt
TMPFILE1=${OUTDIR}/tmpfile1.txt
TMPFILE2=${OUTDIR}/tmpfile2.txt
TMPFILE3=${OUTDIR}/tmpfile3.txt

rm -f ${TMPFILE1}
rm -f ${TMPFILE2}
rm -f ${TMPFILE3}

touch ${TMPFILE1}
touch ${TMPFILE2}
touch ${TMPFILE3}

ls ${OUTDIR}/*/StatisticSummaryFile.txt | while read LINE
do
	NUMLINES=$(cat $LINE | wc -l)

	PHENOTYPE=$(basename $(dirname $LINE))
	for i in $(seq 1 $NUMLINES);
	do 
		echo "$PHENOTYPE" >> ${TMPFILE1};
	done 

	cat $LINE >> ${TMPFILE2}
done

paste ${TMPFILE1} ${TMPFILE2} > ${TMPFILE3}

cat ${TMPFILE3} | grep -v "Bed_File" | sed -e '1i Phenotype\tBed_File\tObserved\tExpected\tPvalue\t' > ${OUTFILE}

rm ${TMPFILE1}
rm ${TMPFILE2}
rm ${TMPFILE3}

