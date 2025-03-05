from socket import *
import os 

serverName = "localhost" #server is set to local host
serverPort = 6789 #server port is set to 6789
serverSocket = socket(AF_INET,SOCK_STREAM) # create a socket
serverSocket.bind(('',serverPort)) #bind the socket to the port and specific address
serverSocket.listen(1) # server can handle one request at a time

print ('The server is ready to receive')

while True:
    # Establish the connection
    connectionSocket, addr = serverSocket.accept()
    print("Connection from ", addr, "established") 
    
    try:
        # Receive request
        request = connectionSocket.recv(1024).decode()
        print("Received request:\n", request) #server has recieved the request from the client

        # Extract file name from GET request
        # Parse the accepted requested file
        try: 
            fileName = request.split()[1][1:] if request.startswith("GET") else None
        except IndexError:
            fileName = None
     
        if fileName:
            if fileName == "HelloWorld":
                fileName = "HelloWorld.html"
            
            # Check if file exists
            if os.path.exists(fileName):
                print("File exists")
                print("Filename: ", fileName)

            if fileName == "favicon.ico":
                if fileName=="favicon.pnj":
                   print("favicon.ico or favicon.png request ignored")
                connectionSocket.close()
                continue
            
            # Determine content type
            if fileName.endswith(".html"):
                    content_type = "text/html"   
            elif fileName.endswith(".png"):
                    content_type = "image/png"                 
            elif fileName.endswith(".txt"):
                    content_type = "text/plain"                   
            elif fileName.endswith(".jpeg") or fileName.endswith(".jpg"):
                content_type = "image/jpeg"               
            else:
                content_type = "application/octet-stream"
                
            # Read file
            with open(fileName, "rb") as f:
                response = f.read()
                print("Response: ", response)

            # Construct HTTP response
            #HTTP header format with status and content type   
            responseHeaders = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Length: {len(response)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
                
            # Send headers and file content to client
            connectionSocket.sendall(responseHeaders.encode() + response)
            print("Response sent to the client")
        
        # if requested file is not in the system send 404 error
        else:
            # File not found - Send 404 response    
            errorMessage = "404 Not Found"
            responseHeaders = (
                 "HTTP/1.1 404 Not Found\r\n"
                 "Content-Type: text/html\r\n" 
                 f"Content-Length: " + str(len(errorMessage)) + "\r\n"                      
                 "Connection: close\r\n"
                     "\r\n")
            # Send headers and file content to client
            connectionSocket.sendall(responseHeaders.encode() + errorMessage.encode())

    # Handle exceptions         
    except Exception as e:
        print("Error :", e)
        
    finally:
        connectionSocket.close()
        print("Connection closed/n")