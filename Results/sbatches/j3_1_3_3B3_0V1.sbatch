#!/bin/bash
#SBATCH --job-name=j3_1_3_3B3_0V1
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=200G
#SBATCH --time=04:00:00
#SBATCH --output=./stdouts/j3_1_3_3B3_0V1.out
#SBATCH --error=./stderrs/j3_1_3_3B3_0V1.err
#SBATCH --partition=all
#SBATCH --mail-user=stu223753@mail.uni-kiel.de
#SBATCH --mail-type=FAIL

~/IntOpt/V1/nfold ~/IntOpt/myCases/3_1_3_3/bound_3_0.in

jobinfo