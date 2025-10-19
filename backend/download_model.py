from huggingface_hub import snapshot_download


model_name = "sentence-transformers/all-MiniLM-L6-v2"

local_dir = "./all-MiniLM-L6-v2"

print(f"Starting download of model '{model_name}'...")
print(f"This will be saved to a folder named '{local_dir}'")
print("This may take a few minutes depending on your internet connection.")

snapshot_download(
    repo_id=model_name,
    local_dir=local_dir,
    local_dir_use_symlinks=False,
    ignore_patterns=["*.pt", "*.bin"], 
)

print("\n Download complete!")
print(f"The model has been saved in the '{local_dir}' folder.")