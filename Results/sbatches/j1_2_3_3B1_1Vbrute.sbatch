#!/bin/bash
#SBATCH --job-name=j1_2_3_3B1_1Vbrute
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=10G
#SBATCH --time=04:00:00
#SBATCH --output=./stdouts/j1_2_3_3B1_1Vbrute.out
#SBATCH --error=./stderrs/j1_2_3_3B1_1Vbrute.err
#SBATCH --partition=all
#SBATCH --mail-user=stu223753@mail.uni-kiel.de
#SBATCH --mail-type=FAIL

~/IntOpt/V1/brute ~/IntOpt/myCases/1_2_3_3/bound_1_1.in

jobinfo