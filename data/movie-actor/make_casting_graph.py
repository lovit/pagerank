def make_graph(casting_csv_path):
    # load file
    with open(casting_csv_path, encoding='utf-8') as f:
        next(f)
        graph = {line.split('\t')[0]:line.split('\t')[1].strip().split() for line in f if len(line.split('\t'))==2}
    
    # weighting
    # casting order (n-i)^2/ sum (i^2 for i = 1 to n)
    def weight(casting_order):
        if not casting_order:
            return {}
        n = len(casting_order)        
        weights = [(n-i) ** 2 for i in range(n)]
        sum_ = sum(weights)
        return {actor:w/sum_ for actor, w in zip(casting_order, weights)}
    
    graph = {movie:weight(actors) for movie, actors in graph.items() if actors}
    return graph

def oneway_to_bidirected_graph(graph):
    """Input: graph[movie][actor] = weight graph"""
    # bi-directed graph
    # graph has only one-way link: movie -> actor
    actor_weight_sum = {}

    # cumulate actor weights
    for movie, actors in graph.items():
        for actor, weight in actors.items():
            actor_weight_sum[actor] = actor_weight_sum.get(actor, 0) + weight

    # make bi-directed graph
    from collections import defaultdict
    g = defaultdict(lambda: {})
    for movie, actors in graph.items():
        g['movie {}'.format(movie)] = {'actor {}'.format(a):w for a,w in actors.items()}
        for actor, weight in actors.items():
            g['actor {}'.format(actor)]['movie {}'.format(movie)] = weight / actor_weight_sum[actor]

    g = dict(g)
    return g

def main():
    casting_csv_path = 'casting.txt'
    graph_path = 'casting_graph.pkl'

    graph = make_graph(casting_csv_path)

    import pickle
    with open(graph_path, 'wb') as f:
        pickle.dump(graph, f)

if __name__ == '__main__':
    main()