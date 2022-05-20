import essentia.standard as es

if __name__ == '__main__':
    any(["OnsetDetection" in algo for algo in es.algorithmNames()])
    es.__spec__()
