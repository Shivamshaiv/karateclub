import numpy as np
import networkx as nx
from karateclub.estimator import Estimator

class NetLSD(Estimator):
    r"""An implementation of `"FGSD" <https://papers.nips.cc/paper/6614-hunt-for-the-unique-stable-sparse-and-fast-feature-learning-on-graphs>`_
    from the NeurIPS '17 paper "Hunt For The Unique, Stable, Sparse And Fast Feature Learning On Graphs".
    The procedure calculates the Moore-Penrose spectrum of the normalized Laplacian.
    Using this spectrum the histogram of the spectral features is used as a whole graph representation. 

    Args:
        hist_bins (int): Number of histogram bins. Default is 200.
        hist_range (int): Histogram range considered. Default is 20.
    """
    def __init__(self, hist_bins=200, hist_range=20):

        self.hist_bins = hist_bins
        self.hist_range = (0, hist_range)



    def _calculate_heat_kernel_trace(self, eivals):
        timescales = np.logspace(-2, 2, 250)
        nodes = eivals.shape[0]
        heat_kernel_trace = np.zeros(timescales.shape)
        for idx, t in enumerate(timescales):
            heat_kernel_trace[idx] = np.sum(np.exp(-t * eivals))
        heat_kernel_trace = heat_kernel_trace / nodes
        return heat_kernel_trace

    def _calculate_netlsd(self, graph):
        """
        Calculating the features of a graph.

        Arg types:
            * **graph** *(NetworkX graph)* - A graph to be embedded.

        Return types:
            * **hist** *(Numpy array)* - The embedding of a single graph.
        """
        mat = sps.coo_matrix(nx.normalized_laplacian_matrix(graph, nodelist = range(graph.number_of_nodes())))
        eivals = eigenvalues_auto(mat)
        heat_kernel_trace = self._calculat_heat_kernel_trace(eivals)
        return heat_kernel_trace

    def fit(self, graphs):
        """
        Fitting a FGSD model.

        Arg types:
            * **graphs** *(List of NetworkX graphs)* - The graphs to be embedded.
        """
        self._embedding = [self._calculate_netlsd(graph) for graph in graphs]


    def get_embedding(self):
        r"""Getting the embedding of graphs.

        Return types:
            * **embedding** *(Numpy array)* - The embedding of graphs.
        """
        return np.array(self._embedding)