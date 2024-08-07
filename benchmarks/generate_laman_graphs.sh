#!/bin/bash

# This script generates laman graphs using nauty and nauty laman plugin:
# https://pallini.di.uniroma1.it/
# https://github.com/martinkjlarsson/nauty-laman-plugin

if [[ -z "$EXECUTABLE" ]]; then
    EXECUTABLE=../nauty-laman-plugin/gensparseg
    echo Using generator: ${EXECUTABLE}
fi
if [[ -z "$OUTPUT_DIR" ]]; then
    OUTPUT_DIR="./graphs_store/nauty-laman"
    echo Using output dir: ${OUTPUT_DIR}
fi

if [[ ! -d "${OUTPUT_DIR}" ]]; then
    mkdir -p "${OUTPUT_DIR}"
fi

for n in {5..30} # 32 40 64 my computer cannot generate more in reasonable time
do
    "$EXECUTABLE" $n -K2 | head -n 128 > "${OUTPUT_DIR}/laman_${n}.g6"
done

