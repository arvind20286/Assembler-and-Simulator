import matplotlib.pyplot as plt
def graph_plot(x, y):
    plt.scatter(x,y)
    plt.xlabel('Cycle number')
    plt.ylabel('Memory address acessed')
    plt.savefig("graph.jpg")

