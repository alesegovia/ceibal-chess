#!/bin/bash
PREVPATH=$PYTHONPATH

DIR=${0%/*}
export PYTHONPATH="${DIR}:${DIR}/../"

TESTS=`ls -1 ${DIR}/*tests.py`

for t in ${TESTS}; do
    python $t
done

export PYTHONPATH=$PREVPATH
