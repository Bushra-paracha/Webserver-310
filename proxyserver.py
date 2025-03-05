from socket import *
import os

proxyServer = "localhost" #server is set to local host
proxyPort=8888            #server port is set to 8888
cacheDir = "cache"        #cache directory

# Create cache directory if it does not exist
if not os.path.exists(cacheDir):
     os.makedirs(cacheDir)

# Create a server socket, bind it to a port and start listening
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((proxyServer,proxyPort))
serverSocket.listen(5)

while True:
    # Establish the connection
    print('The server is ready to receive')
    connectionSocket, addr = serverSocket.accept()
    print("Connection from ", addr, "established") 
        
    # Receive request
    try:
        request=connectionSocket.recv(1024).decode()
        print("Request recieved:\n", request)

        # Extract file name from GET request
        try: 
            fileName = request.split()[1][1:] if request.startswith("GET") else None
        except IndexError:
            fileName = None

        if filename:
            if fileName == "HelloWorld":
                filename = "HelloWorld.html"

        if (fileName == "favicon.ico") & (fileName == "favicon.png"): #ignore favicon requests
            print ("Ignoring favicon request")
            connectionSocket.close()
            continue

        cacheFile = fileName.replace("/","_")
        cachePath=os.path.join(cacheDir,cacheFile)

        # check if file exists in cache
        if os.path.exists(cachePath):
            print("File exists")
            if cachePath.endswith(".html"):
                        content_type = "text/html"
            elif cachePath.endswith(".png"):
                        content_type = "image/png"
            elif cachePath.endswith(".txt"):
                        content_type = "text/plain"
            elif cachePath.endswith(".jpeg") or cacheFile.endswith(".jpg"):
                    content_type = "image/jpeg"
            else:
                    content_type = "application/octet-stream"
                
                # Read file
            with open(cachePath,"rb") as f:
                response = f.read()

            responseHeaders = (
                    "HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/html\r\n"
                    f"Content-Length: {len(response)}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )
            
            # Send headers and file content to client
            connectionSocket.sendall(responseHeaders.encode() + response)
            
        # IF file does not exist in cache, fetch it from the web
        else:
            print(f"Fetching {fileName} from the web")
            webSocket = socket(AF_INET, SOCK_STREAM)
            domain = fileName.split("/")[0]
            fileRequest = "/" + "/".join(fileName.split("/")[1:])
            
            try:
                webSocket.connect((domain, 80))
                requestHeaders = (
                    f"GET {fileRequest} HTTP/1.1\r\n"
                    f"Host: {domain}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )
                
                # Send request to web server
                webSocket.sendall(requestHeaders.encode())
                response = b""
            
                while True:
                    data = webSocket.recv(1024)
                    if not data:
                        break
                    response += data
                with open(cachePath, "wb") as tempFile:
                    tempFile.write(response)
                connectionSocket.sendall(response)
            
            # Handle exceptions and send 404 response
            except Exception as e:
                print("Error fetching file:", e)
                errorResponse = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "<html><body><h1>404 Not Found</h1></body></html>"
                )
                connectionSocket.sendall(errorResponse.encode())
            finally:
                webSocket.close()

    # Handle exceptions and close connection
    except Exception as e:
        print("Error:",e)

    finally:
        connectionSocket.close()
                