import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import os
import dgl
import dgl.function as fn
from dgl.nn.pytorch.conv import GATConv
import dgl.data

dataset = dgl.data.CoraGraphDataset()
g = dataset[0]


class GCN(nn.Module):
    def __init__(self, in_feat, out_feat, num_classes, num_heads):
        super(GCN, self).__init__()
        self.conv1 = GATConv(in_feat, out_feat, num_heads)
        self.conv2 = GATConv(out_feat*num_heads, num_classes, 1,)

    def forward(self, g, in_feat):
        h = self.conv1(g, in_feat)
        h = h.view(-1, h.size(1) * h.size(2))  # (in_feat, num_heads, out_dim) -> (in_feat, num_heads * out_dim)
        # WHAT?
        h = F.elu(h)
        h = self.conv2(g, h)
        h = h.squeeze()  # (in_feat, 1, out_dim) -> (in_feat, out_dim)
        return h


def train(g, model):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    best_val_acc = 0
    best_test_acc = 0

    features = g.ndata['feat']
    labels = g.ndata['label']
    train_mask = g.ndata['train_mask']
    val_mask = g.ndata['val_mask']
    test_mask = g.ndata['test_mask']
    for e in range(1000):
        # Forward
        logits = model(g, features)

        # Compute prediction
        logp = F.log_softmax(logits, 1)
        pred=logits.argmax(1)
        loss = F.nll_loss(logp[train_mask], labels[train_mask])

        train_acc = (pred[train_mask] == labels[train_mask]).float().mean()
        val_acc = (pred[val_mask] == labels[val_mask]).float().mean()
        test_acc = (pred[test_mask] == labels[test_mask]).float().mean()

        if best_val_acc < val_acc:
            best_val_acc = val_acc
            best_test_acc = test_acc

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if e % 5 == 0:
            print('In epoch {}, loss: {:.3f}, val acc: {:.3f} (best {:.3f}), test acc: {:.3f} (best {:.3f})'.format(
                e, loss, val_acc, best_val_acc, test_acc, best_test_acc))



g = g.to('cuda')
model = GCN(g.ndata['feat'].shape[1], 16, dataset.num_classes, 3).to('cuda')
train(g, model)


