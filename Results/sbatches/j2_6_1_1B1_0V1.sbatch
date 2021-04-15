#!/bin/bash
#SBATCH --job-name=j2_6_1_1B1_0V1
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=200G
#SBATCH --time=04:00:00
#SBATCH --output=./stdouts/j2_6_1_1B1_0V1.out
#SBATCH --error=./stderrs/j2_6_1_1B1_0V1.err
#SBATCH --partition=all
#SBATCH --mail-user=stu223753@mail.uni-kiel.de
#SBATCH --mail-type=FAIL

~/IntOpt/V1/nfold ~/IntOpt/myCases/2_6_1_1/bound_1_0.in

jobinfo