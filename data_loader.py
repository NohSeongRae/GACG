import pandas as pd
import dgl
from dgl.data import DGLDataset
import torch
import os

members = pd.read_csv('./SCG_Dataset/OSMNode/Node_Orlando.csv', low_memory=False, encoding='cp949')  # low_memory=false due to mixed data type
print(members.head())  # check node csv file

interactions = pd.read_csv('./SCG_Dataset/OSMEdge/Edge_Orlando.csv', low_memory=False, encoding='cp949')
print(interactions.head())  # check edge csv file


class OrlendoDataset(DGLDataset):
    def __init__(self):
        super().__init__('orlendo')

    def process(self):
        nodes_data = pd.read_csv('./SCG_Dataset/OSMNode/Node_Orlando.csv', low_memory=False,encoding='cp949')
        edges_data = pd.read_csv('./SCG_Dataset/OSMEdge/Edge_Orlando.csv', low_memory=False,encoding='cp949')
        node_features = torch.from_numpy(nodes_data['lat'].to_numpy())
        # node_labels = torch.from_numpy(nodes_data['Club'].astype('category').cat.codes.to_numpy())
        node_labels=torch.from_numpy(nodes_data['lon'].to_numpy())
        edge_features = torch.from_numpy(edges_data['distance'].to_numpy())
        edges_src = torch.from_numpy(edges_data['src_id'].to_numpy())
        edges_dst = torch.from_numpy(edges_data['dst_id'].to_numpy())

        self.graph = dgl.graph((edges_src, edges_dst), num_nodes=nodes_data.shape[0])
        self.graph.ndata['feat'] = node_features
        self.graph.ndata['label'] = node_labels
        self.graph.edata['weight'] = edge_features

        # If your dataset is a node classification dataset, you will need to assign
        # masks indicating whether a node belongs to training, validation, and test set.
        n_nodes = nodes_data.shape[0]
        n_train = int(n_nodes * 0.6)
        n_val = int(n_nodes * 0.2)

        train_mask = torch.zeros(n_nodes, dtype=torch.bool)
        val_mask = torch.zeros(n_nodes, dtype=torch.bool)
        test_mask = torch.zeros(n_nodes, dtype=torch.bool)

        train_mask[:n_train] = True
        val_mask[n_train:n_train + n_val] = True
        test_mask[n_train + n_val:] = True

        self.graph.ndata['train_mask'] = train_mask
        self.graph.ndata['val_mask'] = val_mask
        self.graph.ndata['test_mask'] = test_mask

    def __getitem__(self, i):
        return self.graph

    def __len__(self):
        return 1


dataset = OrlendoDataset()
graph = dataset[0]

print(graph)
