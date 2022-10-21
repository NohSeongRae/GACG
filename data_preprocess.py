import pandas as pd
import dgl
from dgl.data import DGLDataset
from dgl import save_graphs, load_graphs
from dgl.data.utils import makedirs, save_info, load_info
import torch
import os

members = pd.read_csv('./SCG_Dataset/OSMNode/Node_Orlando.csv', low_memory=False, encoding='cp949')  # low_memory=false due to mixed data type
# print(members.head())  # check node csv file

interactions = pd.read_csv('./SCG_Dataset/OSMEdge/Edge_Orlando.csv', low_memory=False, encoding='cp949')
# print(interactions.head())  # check edge csv file

# print('num_nodes: ', members.shape[0])
# node_features = torch.tensor(members['lat'].to_numpy())
node_labels=torch.tensor(members['lon'].to_numpy())
# print("node_features: ", node_features)
# print("len of node_features: ", len(node_features))
# print("node_labels: ", node_labels)
# print("len of node_labels: ", len(node_labels))
#
edges_src = torch.tensor(interactions['src_id'].to_numpy()).int()
edges_dst = torch.tensor(interactions['dst_id'].to_numpy()).int()
print("src_id: ", edges_src)
print("dst_id: ", edges_dst)

class OrlendoDataset(DGLDataset):
    def __init__(self):
        super().__init__('orlendo')

    def process(self):
        nodes_data = pd.read_csv('./SCG_Dataset/OSMNode/Node_Orlando.csv', low_memory=False,encoding='cp949')
        edges_data = pd.read_csv('./SCG_Dataset/OSMEdge/Edge_Orlando.csv', low_memory=False,encoding='cp949')
        node_features = torch.tensor(nodes_data['lat'].to_numpy())
        # node_labels = torch.from_numpy(nodes_data['Club'].astype('category').cat.codes.to_numpy())
        node_labels=torch.tensor(nodes_data['lon'].to_numpy())
        edge_features = torch.tensor(edges_data['distance'].to_numpy())
        edges_src = torch.tensor(edges_data['src_id'].to_numpy()).int()
        edges_dst = torch.tensor(edges_data['dst_id'].to_numpy()).int()

        self.graph = dgl.graph(data=(edges_src, edges_dst), num_nodes=nodes_data.shape[0])
        self.graph.ndata['feat'] = node_features
        self.graph.ndata['label'] = node_labels
        self.graph.edata['weight'] = edge_features

        # If your graph_dataset is a node classification graph_dataset, you will need to assign
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
print("len of graph_dataset: ", len(dataset))
print(graph)
nC={'num_classes': 10}
file_name='orlendo_test'

graph_path=os.path.join('./graph_dataset',  file_name +'_dgl_graph.bin')
save_graphs(graph_path, graph, {'labels':node_labels })
info_path = os.path.join('./graph_dataset', file_name + '_info.pkl')
save_info(info_path, {'num_classes': nC})
def save(self):
    graph_path = os.path.join(self.save_path, self.mode + '_dgl_graph.bin')
    save_graphs(graph_path, self.graphs, {'labels': self.labels})
    # save other information in python dict
    info_path = os.path.join(self.save_path, self.mode + '_info.pkl')
    save_info(info_path, {'num_classes': self.num_classes})

