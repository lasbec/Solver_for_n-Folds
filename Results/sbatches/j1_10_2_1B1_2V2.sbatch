#!/bin/bash
#SBATCH --job-name=j1_10_2_1B1_2V2
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=200G
#SBATCH --time=04:00:00
#SBATCH --output=./stdouts/j1_10_2_1B1_2V2.out
#SBATCH --error=./stderrs/j1_10_2_1B1_2V2.err
#SBATCH --partition=all
#SBATCH --mail-user=stu223753@mail.uni-kiel.de
#SBATCH --mail-type=FAIL

~/IntOpt/V2/nfold ~/IntOpt/myCases/1_10_2_1/bound_1_2.in

jobinfo