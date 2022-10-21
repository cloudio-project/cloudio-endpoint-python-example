from cloudio.endpoint import CloudioEndpoint
import time

from cloudio.endpoint.interface import CloudioAttributeListener


class MyEndpoint(CloudioAttributeListener):
    def __init__(self, cloudio_endpoint_name='example'):
        super(MyEndpoint, self).__init__()
        self._i = 0
        self._endpoint = CloudioEndpoint(cloudio_endpoint_name, locations='path:config/')

    def initialize(self):
        while not self._endpoint.is_online():
            time.sleep(0.2)

        self._create_model()

    def _create_model(self):
        from cloudio.endpoint.runtime import CloudioRuntimeNode, CloudioRuntimeObject

        node = CloudioRuntimeNode()

        props = CloudioRuntimeObject()
        node.add_object('properties', props)

        self._datapoint = props.add_attribute('datapoint', float, 'measure')
        self._setValue = props.add_attribute('setValue', float, 'setpoint')

        self._setValue.add_listener(self)

        self._endpoint.add_node('myNode', node)

        self._endpoint.get_node('')

    def exec(self):
        self._i = 0
        while True:
            print('Value is: ' + str(self._i))
            self._datapoint.set_value(self._i)

            self._i += 1
            self._i %= 100
            time.sleep(0.5)

    def attribute_has_changed(self, attribute, from_cloud: bool):
        self._i = attribute.get_value()


if __name__ == '__main__':
    e = MyEndpoint()
    e.initialize()
    e.exec()
