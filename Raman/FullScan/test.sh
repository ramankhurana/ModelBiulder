for (( i=600; i <= 4000; i=i+50 )); do
    for (( j=300; j <= 1025; j=j+25 )); do
	
	mh=125
	ma0=$j
	mzp=$i
	
	mt=$(($mh+$ma0))
	echo "mass ="$mt
	if [[ $mzp -ge $mt ]]
	    then 
	    echo "found"  $mzp, $ma0
	fi 
	
    done
done