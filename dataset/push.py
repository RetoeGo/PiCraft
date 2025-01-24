from datasets import load_dataset
dataset = load_dataset("imagefolder", data_dir="./image", drop_labels=True)
dataset.push_to_hub("Retoe/image8k")
