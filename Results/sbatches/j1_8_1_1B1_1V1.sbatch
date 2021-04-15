#!/bin/bash
#SBATCH --job-name=j1_8_1_1B1_1V1
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=200G
#SBATCH --time=04:00:00
#SBATCH --output=./stdouts/j1_8_1_1B1_1V1.out
#SBATCH --error=./stderrs/j1_8_1_1B1_1V1.err
#SBATCH --partition=all
#SBATCH --mail-user=stu223753@mail.uni-kiel.de
#SBATCH --mail-type=FAIL

~/IntOpt/V1/nfold ~/IntOpt/myCases/1_8_1_1/bound_1_1.in

jobinfo