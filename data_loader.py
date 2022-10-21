import os
import random
import torch
import numpy as np
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import data_preprocess
#load saved dataset from local disk

class Datamanager(object):
    def __init__(self, data_name):
        self.data_name=data_name

    def data_load(self):
        data_name=self.data_name
        if data_name=='orlendo':

            data=data_preprocess.OrlendoDataset()
            return data
        else:
            print("invalid data name")
