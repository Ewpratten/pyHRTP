from wrapper import HRTPServer

def call(name:str, client_id:int, data:list)->list:
    print(f"Got data from: {name} ({client_id})")
    output = []
    for line in data:
        output.append(line.decode())
        print(line)
    return output

server = HRTPServer(port=8089, callback=call)
server.start(True)