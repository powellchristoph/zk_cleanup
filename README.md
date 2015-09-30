# zk_cleanup

[Taskflow](https://wiki.openstack.org/wiki/TaskFlow) can be configured to use [Zookeeper](https://zookeeper.apache.org/) as a persistence backend but currently lacks any method of purging or aging out any entries it creates. This can lead to continually growing Zookeeper snapshots and extreme memory usage. This script will simply delete any older znodes under Taskflow's path.

```
usage: zk_cleanup.py [-h] [--dry-run] [--age AGE] [--server SERVER]
                     [--port PORT] [--zk-root-path ZK_ROOT_PATH]
                     [--zk-paths ZK_PATHS]

Taskflow znode cleanup.

optional arguments:
  -h, --help            show this help message and exit
  --dry-run             Dry run only, will not delete znodes. (default: False)
  --age AGE             Delete znodes older than X days (default: 7)
  --server SERVER       The zookeeper ip address. (default: localhost)
  --port PORT           The port zookeeper is listening. (default: 2181)
  --zk-root-path ZK_ROOT_PATH
                        Taskflow's root path in Zookeeper. (default:
                        /taskflow)
  --zk-paths ZK_PATHS   The taskflow paths in zookeeper that will be searched.
                        (default: ['flow_details', 'books', 'atom_details'])
```
