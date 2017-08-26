#!/bin/bash
file="$@"
. ./constants.sh
mkdir -p $TMP_PATH
tmp_file=`mktemp -p $TMP_PATH`
hash=`dd if="$file" bs=4k 2>>$SPEED_FILE | tee $tmp_file | sha256sum | awk -F" " '{print $1}'`
index_path=$ROOT_PATH/`echo $hash|perl -pe "s/(.{2})(.{2}).*/\1\/\2\//"`
mkdir -p $index_path
final_path="$index_path/$hash"
if ! [ -a "$final_path" ]
then
	echo "add: $final_path"
	mv $tmp_file $index_path/$hash
	file -s -z -i -k "$final_path" |tee ${final_path}.meta
	file -s -z -k "$final_path" |tee -a ${final_path}.meta
	echo "path:" "$file" |tee -a ${final_path}.meta
else
	echo "file: $hash exists"
	echo "path: $file" |tee -a ${final_path}.meta
	rm $tmp_file
fi
