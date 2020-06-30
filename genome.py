import itertools
import json
import networkx as nx
import requests
from cprint import cprint
from unipath import Path

PROJECT_ROOT = Path(__file__).absolute().parent
DATA_DIR = PROJECT_ROOT.child('data')


def read_json_data(json_filename):
    path = Path(DATA_DIR.child(f'{json_filename}.json'))

    if not path.exists():
        cprint.err(f"JSON file {path} does not exists.", True)

    with open(path) as fd:
        return json.load(fd)


class VisualGenomeData:

    def __init__(self):
        self._objects = None
        self._relationships = None
        self._obj_synsets = None
        self._rel_synsets = None
        self._attr_synsets = None

    @property
    def objects(self):
        if not self._objects:
            self._objects = read_json_data('objects')
        return self._objects

    @property
    def relationships(self):
        if not self._relationships:
            self._relationships = read_json_data('relationships')
        return self._relationships

    @property
    def rel_synsets(self):
        if not self._rel_synsets:
            self._rel_synsets = read_json_data('relationship_synsets')
        return self._rel_synsets
        self._rel_synsets = None

    @property
    def obj_synsets(self):
        if not self._obj_synsets:
            self._obj_synsets = read_json_data('object_synsets')
        return self._obj_synsets

    @property
    def attr_synsets(self):
        if not self._attr_synsets:
            self._attr_synsets = read_json_data('attribute_synsets')
        return self._attr_synsets
        self._attr_synsets = None

    def load_synsets(self):
        cprint.info("Loading relationship synsets...")
        self.rel_synsets
        cprint.info("Loading object synsets...")
        self.obj_synsets
        cprint.info("Loading attribute synsets...")
        self.attr_synsets

    def load(self):
        self.load_synsets()

        cprint.info("Loading objects...")
        self.objects
        cprint.info("Loading relationships...")
        self.relationships

    def fetch_results(self):
        for objs, rels in zip(self.objects, self._relationships):
            yield(GenomeImageData(objs, rels))


class GenomeImageData():

    def __init__(self, objects, relationships):
        self.img_id = objects['image_id']
        self.img_url = objects['image_url']
        self.objects = objects['objects']
        self.relationships = relationships['relationships']

    def get_graph(self):
        graph = nx.Graph()

        for obj in self.objects:
            graph.add_node(obj['object_id'], **obj)
        for rel in self.relationships:
            graph.add_edge(
                rel['subject']['object_id'],
                rel['object']['object_id'],
                **rel
            )

        return graph
