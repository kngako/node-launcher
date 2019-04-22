import os

from node_launcher.node_set.lnd.lnd import (
    LndNode
)
from node_launcher.port_utilities import is_port_in_use


class TestDirectoryConfiguration(object):
    def test_lnd_data_path(self, lnd: LndNode):
        assert os.path.isdir(lnd.lnddir)

    def test_multi_property(self, lnd: LndNode):
        lnd.file['multi_property'] = [
            'test1',
            'test2'
        ]
        assert len(lnd.file['multi_property']) == 2

    def test_multi_listen(self, lnd: LndNode):
        lnd.file['listen'] = [
            '127.0.0.1:9835',
            '192.168.1.1:9736',
        ]
        assert lnd.node_port == '9835'

    def test_rest(self, lnd: LndNode):
        assert not is_port_in_use(lnd.rest_port)

    def test_node(self, lnd: LndNode):
        assert not is_port_in_use(lnd.node_port)

    def test_grpc(self, lnd: LndNode):
        assert not is_port_in_use(lnd.grpc_port)

    def test_bitcoin_file_changed(self, lnd: LndNode):
        lnd.bitcoind_node.file['rpcport'] = 8338
        lnd.bitcoind_node.running = False
        lnd.bitcoind_node.config_file_changed()
        lnd.bitcoin_config_file_changed()
        new_config = lnd.file.snapshot
        lnd.running = False
        assert lnd.file['bitcoind.rpchost'] == new_config['bitcoind.rpchost'] == '127.0.0.1:8338'
        assert lnd.restart_required == False
        lnd.bitcoind_node.running = True
        lnd.bitcoind_node.config_snapshot = lnd.bitcoind_node.file.snapshot
        assert lnd.bitcoind_node.config_snapshot['rpcport'] == 8338
        lnd.bitcoind_node.file['rpcport'] = 8340
        lnd.bitcoind_node.config_file_changed()
        lnd.bitcoin_config_file_changed()
        new_config = lnd.file.snapshot
        assert lnd.file['bitcoind.rpchost'] == new_config['bitcoind.rpchost'] == '127.0.0.1:8340'
        assert lnd.restart_required == False
        lnd.running = True
        assert lnd.bitcoind_node.restart_required == True
        assert lnd.restart_required == True

    def test_file_changed(self, lnd: LndNode):
        lnd.file['listen'] = '127.0.0.1:9739'
        lnd.config_file_changed()
        lnd.running = False
        new_config = lnd.file.snapshot
        assert lnd.node_port == new_config['listen'].split(':')[-1] == '9739'
        assert lnd.restart_required == False
        lnd.running = True
        lnd.file['listen'] = '127.0.0.1:9741'
        lnd.config_file_changed()
        new_config = lnd.file.snapshot
        assert lnd.node_port == new_config['listen'].split(':')[-1] == '9741'
