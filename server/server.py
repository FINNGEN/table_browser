from flask import Flask, jsonify, request, abort, render_template
from flask_compress import Compress
import imp, logging
import pandas as pd
import numpy as np
import re

from cloud_storage import CloudStorage

app = Flask(__name__, template_folder='../templates', static_folder='../static')
Compress(app)

config = {}
try:
    _conf_module = imp.load_source('config', 'config.py')
except Exception as e:
    print('Could not load config.py')
    raise
config = {key: getattr(_conf_module, key) for key in dir(_conf_module) if not key.startswith('_')}

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(config['log_level'])

cloud_storage = CloudStorage()

df = pd.read_csv(config['chipd_file'], encoding='utf8', sep='\t').fillna('NA')
# replace all . values with NA
df = df.replace(r'^\.$', 'NA', regex=True)
# find minimun p-value for each variant
df['is_top'] = 0
df.loc[df.groupby('variant')['pval'].idxmin(axis=0), 'is_top'] = 1
chipd = {
    'columns': df.columns.tolist(),
    'data': df.to_dict(orient='records')
}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route('/api/v1/chip_data')
def chip_data():
    return jsonify(chipd)

@app.route('/api/v1/cluster_plot/<variant>')
def cluster_plot(variant):
    cpra = variant.split(':')
    cpra[0] = 'X' if cpra[0] == '23' else cpra[0]
    data = cloud_storage.read_bytes(config['cluster_plot_bucket'], config['cluster_plot_loc'] + '_'.join(cpra) + '.png')
    if data is None:
        abort(404, 'Requested cluster plot not found!')
    return data

if __name__ == '__main__':
    app.run()
