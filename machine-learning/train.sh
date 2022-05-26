#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --time=72:00:00
#SBATCH --mem=4000

module load CUDA/10.0.130 
module load GCC/7.3.0-2.30
module load cuDNN/7.4.2.24-CUDA-10.0.130

source virtualHanabi/bin/activate

echo RainbowDQN

python -u ~/rainbowToM/train.py --base_dir=~/hanabi_rainbow_experiment --checkpoint_dir=checkpoints --gin_files='rainbowToM/configs/hanabi_rainbow.gin'

mv *.out slurm/
