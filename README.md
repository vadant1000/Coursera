# Server for receiving metrics

## Tech Stack:
Python 3.9

asyncio

## Description
The server must be able to accept put and get commands from clients, parse them, and form a response according to the protocol.

The put request requires that metrics be stored in data structures in process memory. On a get request, the server must return the data in the correct sequence. When working with a client, the server must support sessions, the connection with the client between requests must not be "broken".

General client request format:`<command> <request data><\n>`

General format of server responses:`<response status><\n><response data><\n\n>`

For example:
```
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
> get test_key
< ok
< 
> got test_key
< error
< wrong command
< 
> put test_key 12.0 1503319740
< ok
< 
> put test_key 13.0 1503319739
< ok
< 
> get test_key 
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< 
> put another_key 10 1503319739
< ok
< 
> get *
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< another_key 10.0 1503319739
```

