#!/bin/bash
#SBATCH --job-name=stable
#SBATCH --output=%x_%j.out
#SBATCH --mail-user=""
#SBATCH --mail-type="ALL"
#SBATCH --partition="gpu-long"
#SBATCH --time=7-00:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40
#SBATCH --mem=160G
#SBATCH --gres=gpu:a100:1

# making sure we start with a clean module environment
module purge
echo "## Starting GPU test on $HOSTNAME"
echo "## Loading module"
module load ALICE/default
module load slurm
module load CUDA/12.1.1
module load GCC/11.3.0

echo "#### Starting Test"
export HF_HOME="$TMPDIR"
#export HF_API_TOKEN=""
#export MODEL_NAME="stabilityai/stable-diffusion-3.5-medium"
export MODEL_NAME="stabilityai/stable-diffusion-2-1-base"
export DATASET_NAME="retoe/image10k"
export DATASET="$TMPDIR""/temp"
#export WANDB_DIR="$TMPDIR""/wandb"

#export ACCELERATE_ENVIRONMENT="LOCAL_MACHINE"
#export ACCELERATE_DISTRIBUTED_TYPE="MULTI_GPU"
#export ACCELERATE_NUM_PROCESSES=2
#export ACCELERATE_MIXED_PRECISION="fp16"

huggingface-cli login --token ""
wandb login ""
accelerate config default
mkdir $DATASET
#mkdir $WANDB_DIR

CUDA_VISIBLE_DEVICES=0 accelerate launch train_text_to_image_lora_sdxl2.py \
  --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \
  --pretrained_vae_model_name_or_path="madebyollin/sdxl-vae-fp16-fix" \
  --dataset_name="Retoe/image8k" \
  --validation_prompt="A minecraft castle" \
  --instance_prompt="a minecraft building" \
  --caption_column="text" \
  --output_dir="$DATASET" \
  --num_validation_images=4 \
  --validation_epochs=1 \
  --resolution=512 \
  --center_crop \
  --random_flip \
  --train_text_encoder \
  --train_batch_size=4 \
  --num_train_epochs=10 \
  --gradient_accumulation_steps=4 --gradient_checkpointing \
  --learning_rate=1e-04 \
  --lr_warmup_steps=0 \
  --max_train_steps=4 --checkpointing_steps=2 --checkpoints_total_limit=2 \
  --use_8bit_adam \
  --seed="0" \
  --dataloader_num_workers=1 \
  --allow_tf32 \
  --mixed_precision="fp16" \
  --report_to="wandb" \
  --push_to_hub \
  --hub_model_id="sd8k3"

for (( i=8; i<=6000; i+=4 ))
do
  CUDA_VISIBLE_DEVICES=0 accelerate launch train_text_to_image_lora_sdxl2.py \
    --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \
    --pretrained_vae_model_name_or_path="madebyollin/sdxl-vae-fp16-fix" \
    --dataset_name="Retoe/image8k" \
    --validation_prompt="A minecraft castle" \
    --instance_prompt="a minecraft building" \
    --caption_column="text" \
    --output_dir="$DATASET" \
    --num_validation_images=4 \
    --validation_epochs=1 \
    --resolution=512 \
    --center_crop \
    --random_flip \
    --train_text_encoder \
    --train_batch_size=4 \
    --num_train_epochs=10 \
    --gradient_accumulation_steps=4 --gradient_checkpointing \
    --learning_rate=1e-04 \
    --lr_warmup_steps=0 \
    --max_train_steps=$i --checkpointing_steps=2 --checkpoints_total_limit=2 \
    --resume_from_checkpoint="latest" \
    --use_8bit_adam \
    --seed="0" \
    --dataloader_num_workers=1 \
    --allow_tf32 \
    --mixed_precision="fp16" \
    --report_to="wandb" \
    --push_to_hub \
    --hub_model_id="sd8k3"
done

echo "This is $SLURM_JOB_USER and my first job has the ID $SLURM_JOB_ID"
# get the current working directory
CWD=$(pwd)
echo "This job was submitted from $SLURM_SUBMIT_DIR and I am currently in $CWD"
# get the current time and date
DATE=$(date)
echo "It is now $DATE"
echo "Hello World from $HOSTNAME"
echo "#### Finished Test. Have a nice day"
