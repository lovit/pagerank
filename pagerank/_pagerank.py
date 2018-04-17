def pagerank(G, bias=None, df=0.15,
             max_iter=50, converge_error=0.001,verbose=0):
    """
    Arguments
    ---------
    G: Inbound graph, dict of dict
        G[to_node][from_node] = weight (float)
    df: damping factor, float. default 0.15
    """
    
    A, nodes = _normalize(G)
    N = len(nodes) # number of nodes
    sr = 1 - df # survival rate (1 -  damping factor)
    ir = 1 / N # initial rank

    # Initialization
    rank = {n:ir for n in nodes}

    # Initialization of bias
    if not bias:
        bias = {node:ir for node in nodes}

    # Iteration
    for _iter in range(1, max_iter + 1):
        rank_new = {}

        # t: to node, f: from node, w: weight
        for t in nodes:
            f_dict = A.get(t, {})
            rank_t = sum((w*rank[f] for f, w in f_dict.items())) if f_dict else 0
            rank_t = sr * rank_t + df * bias.get(t, 0)
            rank_new[t] = rank_t

        # convergence check
        diff = sum((abs(rank[n] - rank_new[n]) for n in nodes))
        if diff < converge_error:
            if verbose:
                print('Early stopped at iter = {}'.format(_iter))
            break

        if verbose:
            sum_ = sum(rank_new.values())
            print('Iteration = {}, diff = {}, sum = {}'.format(_iter, diff, sum_))

        rank = rank_new

    return rank


def _normalize(G):
    """It returns outbound normalized graph
    Arguments
    ---------
    G: inbound graph dict of dict
    """
    # Sum of outbound weight
    # t: to node, f: from node, w: weight
    W_sum = {}    
    for t, f_dict in G.items():
        for f, w in f_dict.items():
            W_sum[f] = W_sum.get(f, 0) + w
    A = {t:{f:w/W_sum[f] for f,w in f_dict.items()} for t, f_dict in G.items()}    
    nodes = set(G.keys())
    nodes.update(W_sum)
    return A, nodes