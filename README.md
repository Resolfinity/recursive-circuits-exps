## Experiments with recursive pragma workers

## Inputs

These circtuits should be ran with same inputs, placed into the ./inputs folder of this repo.

Public input is empty array.
Private input is production size data, including 2\*\*21 fake validators data, and 1024 changed validators data with storage proofs.

Since private-input.json is too large to be put on Github, it is placed here in .zip format.

## What is these circuits about

### poseidon-8

Is a set of pragma-based code, to merkelize subtrees of poseidon merkle tree, split to produce tables with size up to 2\*\*20 rows. It consists of 8 workers.

### poseidon-8-bigtable

Same circuit, but split by 2\*\*21 tables rows.

### sha-8

Split to 8 pragma workers, each piece is responsible for sha256 validator leaf merkelization and merkle proof of validator set update verification. It generates tables with 2\*\*20 rows

### sha-8-bigtable

Same but with 2\*\*21 rows.

## How to run

Update proof producer:

```
apt remove proof-producer
apt update
apt install proof-producer
```

I've used assigner built from commit 11544ace39a1117674be0495a9cce7b0bd7f7092, as recommended by Lena.

Also i worked in the zkllvm-template directory.

### Prepare circtuit and inputs

- Place main.cpp file from one of 4 exp folders into ./src folder
- unzip private-input.json.zip into ./src folder
- place public-input.json into ./src folder

### Make circuit

`make -C ${ZKLLVM_BUILD:-build} template`

### Run assigner

```
date && python3 memory-check.py assigner -b build/src/template.ll          -i src/public-input.json          -p src/private-input.json          --circuit template.crct          --assignment-table template.tbl          -e pallas -f dec -s 40000000 --max-num-provers 100 && date
```

I use this command to print date before and after execution, to compute assigner time.
Also i've included memory-check.py, it prints memory peak during the assigner work.

Measure execution time and memory peak, write it into the google sheet.

### Run prover

At that moment, we should have set of files like .crct0(1,2,3...) and .tbl0(1,2,3...)

These files are supposed being used to generate recursive proofs and recursive verifiers .cpp code.

Most of generated tables have similar rows count.

Run prover to measure proof building time for table .tbl1

```
date && /root/zkll/build/bin/recursive_gen/recursive_gen -m gen-input -i ./src/public-input.json -t ./template.tbl1 -c ./template.crct1 -o ./recursive -e pallas -p 1 -s 3 --multi-prover && date
```

In the beginning, prover prints Tables rows info.
Save it into the google sheet.

After computation, save working time and memory peak into the google sheet.

Run this routine for all of 4 circuits, using same inputs.
