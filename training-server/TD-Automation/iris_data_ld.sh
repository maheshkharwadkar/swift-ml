#!/bin/ksh
##########
#########
#-- call to TPT --#

tbuild -f /opt/iris_data_ld.tpt -j iris_ld

lzreturncode=$?

if [ $lzreturncode -ne 0 ]
then
echo "TPT load step failed."
else
echo "TPT load completd successfully."
fi

. /opt/iris_data_exprt.bteq

if [ $lzreturncode -ne 0 ]
then
echo "TPT export step failed."
else
echo "TPT export completd successfully."
fi
