#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --time=22:00:00
#SBATCH --mem=4000

module load CUDA/10.0.130 
module load GCC/7.3.0-2.30
module load cuDNN/7.4.2.24-CUDA-10.0.130

source /home/s2843013/virtualHanabi/bin/activate

echo RainbowZero Batch

python -u /home/s2843013/hanabi-theory-of-mind/machine-learning/tom-rainbow/train.py --base_dir=/home/s2843013/experimentZero --checkpoint_dir=checkpoints --gin_files='machine-learning/tom-rainbow/configs/hanabi_rainbow_zero.gin'

mv *.out slurm/
