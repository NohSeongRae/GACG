import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import os
import dgl
import dgl.function as fn
from dgl.nn.pytorch.conv import EGATConv
import args
import dgl.data
from dgl.nn.pytorch.conv import EGATConv

dataset = dgl.data.TUDataset('AIDS')
print('Number of categories:', dataset.num_classes)
print(len(dataset))

class GCN(nn.Module):
    def __init__(self, in_node_feats, in_edge_feats, out_node_feats, out_edge_feats, num_heads, num_classes):
        super(GCN, self).__init__()
        self.conv1 = EGATConv(in_node_feats, in_edge_feats, out_node_feats, out_edge_feats, num_heads)
        self.conv2 = EGATConv(out_node_feats, out_edge_feats,num_classes,1,num_heads)

    def forward(self, g, in_feat):
        h = self.conv1(g, in_feat)
        h = F.relu(h)
        h = self.conv2(g, h)
        return h

# Create the model with given dimensions
# model = GCN(g.ndata['feat'].shape[1], 16, dataset.num_classes)