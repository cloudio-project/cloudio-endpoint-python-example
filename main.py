from cloudio.endpoint import CloudioEndpoint
import time

from cloudio.endpoint.interface import CloudioAttributeListener


class MyEndpoint(CloudioAttributeListener):
    def __init__(self, cloudio_endpoint_name='example'):
        super(MyEndpoint, self).__init__()
        self._i = 0

        # Give the .properties file name and directory location
        self._endpoint = CloudioEndpoint(cloudio_endpoint_name, locations='path:config/')

    def initialize(self):
        while not self._endpoint.is_online():
            time.sleep(0.2)

        self._create_model()

    def _create_model(self):
        from cloudio.endpoint.runtime import CloudioRuntimeNode, CloudioRuntimeObject

        # Create a node
        node = CloudioRuntimeNode()

        # Adds an object
        props = CloudioRuntimeObject()
        node.add_object('myObject', props)

        # Adds attributes
        self._my_measure = props.add_attribute('myMeasure', float, 'measure')
        self._my_setpoint = props.add_attribute('mySetPoint', float, 'setpoint')

        # Adds a listener on the setpoint
        self._my_setpoint.add_listener(self)

        # Finally adds the node to the endpoint
        self._endpoint.add_node('myNode', node)

    def exec(self):
        self._i = 0
        while True:
            print('Value is: ' + str(self._i))
            self._my_measure.set_value(self._i)

            self._i += 1
            self._i %= 100
            time.sleep(1)

    def attribute_has_changed(self, attribute, from_cloud: bool):
        self._i = attribute.get_value()


if __name__ == '__main__':
    e = MyEndpoint()
    e.initialize()
    e.exec()
