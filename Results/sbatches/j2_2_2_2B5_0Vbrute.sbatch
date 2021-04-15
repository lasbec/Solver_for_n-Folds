#!/bin/bash
#SBATCH --job-name=j2_2_2_2B5_0Vbrute
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=10G
#SBATCH --time=04:00:00
#SBATCH --output=./stdouts/j2_2_2_2B5_0Vbrute.out
#SBATCH --error=./stderrs/j2_2_2_2B5_0Vbrute.err
#SBATCH --partition=all
#SBATCH --mail-user=stu223753@mail.uni-kiel.de
#SBATCH --mail-type=FAIL

~/IntOpt/V1/brute ~/IntOpt/myCases/2_2_2_2/bound_5_0.in

jobinfo