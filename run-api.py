import argparse
import ll.api.participant
import ll.api.site
from ll.api import app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Living Labs Challenge's API Server")
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='Enable debugging mode.')
    parser.add_argument('--host', dest='host', default='127.0.0.1',
                        help='Host to listen on.')
    parser.add_argument('--port', dest='port', default=5000, type=int,
                        help='Port to listen on.')
    args = parser.parse_args()
    app.debug = args.debug
    print(" * Living Labs Challenge API")
    app.run(host=args.host, port=args.port)
