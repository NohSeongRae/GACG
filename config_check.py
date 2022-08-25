import sys
import torch
import numpy as np
import torch_geometric

print("----------------------------------------------------")
print(f"python version: {sys.version}")
print("----------------------------------------------------")
print(f"torch version: {torch.__version__}")
print("----------------------------------------------------")
print(f"is cuda available: {torch.cuda.is_available()}")
print(f"cuda device count: {torch.cuda.device_count()}")
print(f"cuda current device: {torch.cuda.current_device()}")
print(f"cuda device: {torch.cuda.device(0)}")
print(f"cuda device properties: {torch.cuda.get_device_properties(0)}")
print("----------------------------------------------------")
print(f"numpy version: {np.__version__}")
print("----------------------------------------------------")
print(f"PyG version: {torch_geometric.__version__}")
