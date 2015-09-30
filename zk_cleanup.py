#!/srv/poppy/bin/python

import argparse
import logging

from kazoo.client import KazooClient
from datetime import datetime as dt

DEFAULTS = {
        'age'           : 7,
        'server'        : 'localhost',
        'port'          : '2181',
        'zk_root_path'  : '/taskflow',
        'zk_paths'      : ['flow_details', 'books', 'atom_details'],
}

def cleanup(args):
    now = dt.utcnow()
    server = '{server}:{port}'.format(server=args.server, port=args.port)
    logging.info('Connecting to {}'.format(server))
    zk = KazooClient(hosts=server)
    zk.start()

    for path in args.zk_paths:
        zk_path = '{}/{}'.format(args.zk_root_path, path)
        nodes = zk.get_children(zk_path)
        logging.info("Found {} nodes under {}".format(len(nodes), zk_path))

        deleted = 0
        for node in nodes:
            node_path = '{}/{}'.format(zk_path, node)
            data, stat = zk.get(node_path)
            last_modified = dt.fromtimestamp(stat.mtime/1000.0)
            if (now - last_modified).days > args.age:
                if not args.dry_run:
                    # Kazoo does not support recursive async deletes
                    if stat.children_count == 0:
                        res = zk.delete_async(node_path)
                    else:
                        zk.delete(node_path, recursive=True)
                deleted += 1

        logging.info("Deleted {} nodes".format(deleted))

    zk.stop()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(description='Taskflow znode cleanup.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dry-run', action='store_true', dest='dry_run',
            default=False, help='Dry run only, will not delete znodes.')
    parser.add_argument('--age', action='store', dest='age',
            default=DEFAULTS['age'], type=int, help='Delete znodes older than X days')
    parser.add_argument('--server', action='store', dest='server',
            default=DEFAULTS['server'], help='The zookeeper ip address.')
    parser.add_argument('--port', action='store', dest='port',
            default=DEFAULTS['port'], help='The port zookeeper is listening.')
    parser.add_argument('--zk-root-path', action='store', dest='zk_root_path',
            default=DEFAULTS['zk_root_path'], help='Taskflow\'s root path in Zookeeper.')
    parser.add_argument('--zk-paths', action='store', dest='zk_paths',
            default=DEFAULTS['zk_paths'], help='The taskflow paths in zookeeper that will be searched.')

    cleanup(parser.parse_args())
