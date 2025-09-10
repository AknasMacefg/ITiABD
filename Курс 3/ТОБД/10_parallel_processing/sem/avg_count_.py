import pandas as pd
def avg_count(filename, output):
    tags_dictionary = {}
    data = pd.read_csv(filename, decimal=';')
    for i, k in zip(data['tags'], data['n_steps']):
        tags_clean = i.strip('[]').split(', ')
        for j in tags_clean:
            if j not in tags_dictionary:
                tags_dictionary[j] = [1, k, 0]
            else:
                tags_dictionary[j][0] = tags_dictionary[j][0] + 1
                tags_dictionary[j][1] = tags_dictionary[j][1] + k
                tags_dictionary[j][2] = tags_dictionary[j][1] / tags_dictionary[j][0]

    output.put(tags_dictionary)
