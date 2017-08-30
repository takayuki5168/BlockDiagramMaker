#!/bin/sh

SCRIPT_DIR=$(dirname $0)

mkdir -p ${SCRIPT_DIR}/../json
echo "{
 \"which_use\" : \"sample1\",

 \"sample1\" : {
  \"gain\" : {
   \"file_name\" : [1, 2, 3],
   \"freqency\" : [10, 20, 30],
   \"time_line\" : 5,
   \"gain_line\" : 13
  },
  \"phase\" : {
   \"file_name\" : [1, 2, 3],
   \"freqency\" : [10, 20, 30],
   \"time_line\" : 5,
   \"phase_line\" : 13
  }
 }
}" > ${SCRIPT_DIR}/../json/format.json
