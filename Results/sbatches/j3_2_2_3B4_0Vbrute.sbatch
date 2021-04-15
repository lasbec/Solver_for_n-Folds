#!/bin/bash
#SBATCH --job-name=j3_2_2_3B4_0Vbrute
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=10G
#SBATCH --time=04:00:00
#SBATCH --output=./stdouts/j3_2_2_3B4_0Vbrute.out
#SBATCH --error=./stderrs/j3_2_2_3B4_0Vbrute.err
#SBATCH --partition=all
#SBATCH --mail-user=stu223753@mail.uni-kiel.de
#SBATCH --mail-type=FAIL

~/IntOpt/V1/brute ~/IntOpt/myCases/3_2_2_3/bound_4_0.in

jobinfo