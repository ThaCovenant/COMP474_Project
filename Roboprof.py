from Roboprof_functions import createGraphs


def main():
    graph = createGraphs()
    # print(graph.serialize(format='turtle'))

    # Loop through each triple in the graph (subj, pred, obj)
    for s, p, o in graph:
        # Print the subject, predicate and the object
        print(s, p, o)


if __name__ == '__main__':
    main()
