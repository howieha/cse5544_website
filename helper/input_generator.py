from itertools import combinations
from random import sample
import json

class input_generator():
    def __init__(self):
        self.input = {'nodes': [], 'links': []}
        self.latest_group = 0

    def add_node(self, id, group, val, color=None):

        if color is not None:
            self.input['nodes'].append({'id': id, 'group': group, 'val': val, 'color': color})
        else:
            self.input['nodes'].append({'id': id, 'group': group, 'val': val})
        self.latest_group = max(group, self.latest_group)

    def remove_node(self, id, group, val):
        self.input['nodes'].remove({'id': id, 'group': group, 'val': val})
        self.latest_group = max(group, self.latest_group)
        for link in self.input['links']:
            if link['source'] == id:
                self.remove_link(link['source'], link['target'])

    def add_link(self, sourceID, targetID):
        self.input['links'].append({'source': sourceID, 'target': targetID})

    def remove_link(self, sourceID, targetID):
        self.input['links'].remove({'source': sourceID, 'target': targetID})

    def add_connected_cluster(self, node_ID, val=1, remove_num=0):
        self.latest_group += 1
        for id in node_ID:
            self.add_node(id, self.latest_group, val)
        comb = combinations(node_ID, 2)
        comb = list(comb)
        for link in comb:
            self.add_link(link[0], link[1])
        if remove_num > 0:
            temp_links = sample(comb, remove_num)
            for link in temp_links:
                self.remove_link(link[0], link[1])


    def get_input(self):
        return self.input


if __name__ == "__main__":
    generator = input_generator()

    generator.add_node(0, 0, 100, color='red')

    for i in range(50):
        generator.add_connected_cluster(list(range(i*5, (i+1)*5)))
        generator.add_link(0, i*5)

    with open('../data/input.json', 'w') as out_file:
        json.dump(generator.get_input(), out_file)

    print(generator.get_input())
