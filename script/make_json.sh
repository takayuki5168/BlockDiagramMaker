#!/bin/sh

SCRIPT_DIR=$(dirname $0)

mkdir -p ${SCRIPT_DIR}/../json
echo "{
  \"which_use\" : \"sample1\",
 
  \"sample1\" : {
    \"cycle_sec\" : 0.001,
    \"freqency\" : [1, 7, 10],
    \"input\" : {
      \"file_name\" : [\"log/10.log\", \"log/70.log\", \"log/100.log\"],
      \"time_line\" : 5,
      \"gain_line\" : 15,
      \"phase_line\" : 10
    },
    \"output\" : {
      \"file_name\" : [\"log/10.log\", \"log/70.log\", \"log/100.log\"],
      \"time_line\" : 5,
      \"gain_line\" : 15,
      \"phase_line\" : 10
    }
  }
}" > ${SCRIPT_DIR}/../json/format.json
