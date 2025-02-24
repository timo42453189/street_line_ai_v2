import tensorflow as tf
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Modell laden
model_path = "contrast_model/v0_contrast.h5"
model = tf.keras.models.load_model(model_path)

# Layer-Informationen extrahieren
layers = [layer for layer in model.layers if 'dense' in layer.name]
layer_sizes = [layer.input_shape[-1] for layer in layers] + [layers[-1].output_shape[-1]]

# Netzwerk-Graph erstellen
G = nx.DiGraph()
positions = {}
node_id = 0
layer_nodes = []

# Knoten platzieren
for layer_index, num_neurons in enumerate(layer_sizes):
    x_pos = layer_index * 2
    y_positions = np.linspace(-1, 1, num_neurons) if layer_index < len(layer_sizes) - 1 else [0]  # Mittig für letzte Schicht
    current_layer_nodes = [node_id + i for i in range(num_neurons)]
    for i, y in enumerate(y_positions):
        G.add_node(node_id + i, pos=(x_pos, y))
        positions[node_id + i] = (x_pos, y)
    layer_nodes.append(current_layer_nodes)
    node_id += num_neurons

# Kanten mit Gewichten hinzufügen
edge_colors = []
edge_widths = []
for i in range(len(layers)):
    weights, biases = layers[i].get_weights()
    for in_node, out_node in np.ndindex(weights.shape):
        weight = weights[in_node, out_node]
        G.add_edge(layer_nodes[i][in_node], layer_nodes[i+1][out_node], weight=weight)
        edge_colors.append(weight)
        edge_widths.append(abs(weight) * 2)  # Skalierung für bessere Sichtbarkeit

# Netzwerk zeichnen
plt.figure(figsize=(12, 8))
nx.draw(
    G, pos=positions, with_labels=False, node_size=300, 
    edge_color=edge_colors, edge_cmap=plt.cm.coolwarm, width=edge_widths, alpha=0.7
)
plt.title("Neuronales Netzwerk - Visualisierung der Verbindungsgewichte")
plt.show()