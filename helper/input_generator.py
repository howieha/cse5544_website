from itertools import combinations
from random import sample, randint
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

    def remove_node(self, id, group):
        for node in self.input['nodes']:
            if node['id'] == id:
                self.input['nodes'].remove(node)
        self.latest_group = max(group, self.latest_group)
        for link in self.input['links']:
            if link['source'] == id:
                self.remove_link(link['source'], link['target'])

    def add_link(self, sourceID, targetID):
        self.input['links'].append({'source': sourceID, 'target': targetID})

    def remove_link(self, sourceID, targetID):
        self.input['links'].remove({'source': sourceID, 'target': targetID})

    def change_node_color(self, node_ID, group, value, new_color):

        for node in self.input['nodes']:
            if node['id'] == node_ID:
                self.input['nodes'].remove(node)
        self.input['nodes'].append({'id': node_ID, 'group': group, 'val': value, 'color': new_color})

    def add_connected_cluster(self, node_ID, val=1, remove_num=0, default_col=None, diff_num=2,  diff_col='blue'):
        self.latest_group += 1

        for id in node_ID:
            if default_col is None:
                self.add_node(id, self.latest_group, val)
            else:
                self.add_node(id, self.latest_group, val, color=default_col)

        temp_id = sample(node_ID, diff_num)
        for i in range(len(temp_id)):
            self.change_node_color(temp_id[i], self.latest_group, val, diff_col)

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

    generator.add_node(0, 0, 100, color='yellow')

    for i in range(30):
        generator.add_connected_cluster(list(range(i*8, (i+1)*8)), remove_num=2, diff_num=2, diff_col='pink')
        generator.add_link(0, i*8)




    with open('../data/input.json', 'w') as out_file:
        json.dump(generator.get_input(), out_file)

    print(generator.get_input())
