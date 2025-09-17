#Подсчёт символов в тексте
def counter(filename, output):
    with open(filename, 'r') as file:
        text = file.read().replace('\n', '').replace('\xa0', ' ')
    dictionary = {}
    for i in text:
        if i.lower() not in dictionary:
            dictionary[i.lower()] = 1
        else:
            dictionary[i.lower()] = dictionary[i.lower()] + 1 
    output.put(dictionary)
