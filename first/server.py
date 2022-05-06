import asyncio


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    storage = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        if data.startswith('put'):
            return self.put(data)
        elif data.startswith('get'):
            return self.get(data)
        else:
            return 'error\nwrong command\n\n'

    def put(self, data):
        try:
            assert data.endswith('\n')
            assert len(data.split()) == 4
            float(data.split()[2])
            assert int(data.split()[3])
        except(AssertionError, ValueError):

            return 'error\nwrong command\n\n'

        if data.split()[1] not in self.storage:
            self.storage[data.split()[1]] = []

        values = self.storage[data.split()[1]]
        for value in values:
            if int(data.split()[3]) in value:
                values.remove(value)
        ClientServerProtocol.storage[data.split()[1]].append((float(data.split()[2]), int(data.split()[3])))

        return 'ok\n\n'

    def get(self, data):

        try:
            assert data.endswith('\n')
            assert len(data.split()) == 2
        except(AssertionError, ValueError):
            return 'error\nwrong command\n\n'

        output = 'ok\n'
        if data.split()[1] == '*':
            for key, value in self.storage.items():
                for metric in value:
                    output += (key + ' ' + str(metric[0]) + ' ' + str(metric[1]) + '\n')
            output += '\n'
            return output
        elif data.split()[1] in self.storage:
            value = self.storage[data.split()[1]]
            for metric in value:
                output += (data.split()[1] + ' ' + str(metric[0]) + ' ' + str(metric[1]) + '\n')
            output += '\n'
            return output
        else:
            return 'ok\n\n'


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
