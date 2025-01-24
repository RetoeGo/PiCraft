from datasets import load_dataset
dataset = load_dataset("imagefolder", data_dir="./images", drop_labels=True)
dataset.push_to_hub("Retoe/image8k") #replace with your own dataset name
