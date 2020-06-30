import os
import requests
from cprint import cprint
from unipath import Path

from genome import VisualGenomeData


PROJECT_ROOT = Path(__file__).absolute().parent
RESULTS_DIR = PROJECT_ROOT.child('results')

visual_genome = VisualGenomeData()
visual_genome.load()

results = visual_genome.fetch_results()

good = 0
i = 0
while good < 10:
    i += 1
    cprint.info(f"Parsing result {i} / goods {good}...")
    test_data = next(results)
    response = requests.get(test_data.img_url)
    if response.ok:
        graph = test_data.get_graph()


        img_names = []
        for node in graph.nodes():
            node_data = graph.nodes[node]
            if not node_data:
                continue

            names = ' - '.join(node_data['names']) + '\n'
            img_names.append(names)

        rels_desc = []
        for subject_id, object_id in graph.edges():
            subject = graph.nodes[subject_id]
            rel_object = graph.nodes[object_id]

            if not (subject and rel_object):
                continue

            subjects = ' - '.join(subject['names'])
            objects = ' - '.join(rel_object['names'])
            predicate = graph.edges[subject_id, object_id]['predicate']
            rels_desc.append(f"{subjects} {predicate} {objects}\n")


        IMG_DIR = RESULTS_DIR.child(str(test_data.img_id))
        if not IMG_DIR.exists():
            os.mkdir(IMG_DIR)

        with open(IMG_DIR.child('results.txt'), 'w') as fd:
            fd.writelines(img_names)

            fd.write('\n')
            fd.write('----------------------\n')
            fd.write('\n')

            fd.writelines(rels_desc)

        format = Path(test_data.img_url).name.split('.')[-1]

        with open(IMG_DIR.child(f'{test_data.img_id}.{format}'), 'wb') as fd:
            fd.write(response.content)

        good += 1
