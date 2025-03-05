# README for Programming Assignment 1

 ## Program Descriptions 

 ### 1. Web Server Server (**webserver.py**)
  
  _A simple web server that handles one HTTP request at a time. Web server is be able to accept and parse the HTTP request, get the requested file from the server’s file system, create an HTTP response message consisting of the requested file preceded by the status and header lines, and then send the response directly to the client. If the requested file is not present in the server, the server then sends an HTTP “404 Not Found” message back to the client._
  
   #### How to Run:
  - Open the terminal and type  **python3 webserver.py**.
  - The server is set listen on port 6789

  #### Web Pages Tested:
  1. Successfully serves **HelloWorld.html**
  2. Works with locally stored images and text files. 

### 2. Proxy Server (proxyserver.py)
 _A small web proxy server which is able to cache web pages. If a requested page is in the cache, it serves it from there. Otherwise, it fetches the page from the web, stores it in the cache, and serves it to the client. It is a very simple proxy server which only understands simple GET requests, but is able to handle all kinds of objects - not just HTML pages, but also images._

 #### How to Run: 
 - Open the terminal and type **python3 proxyserver.py**
 - The proxy listens on port 8888. 

 #### Web Pages Tested:
 1. Can fetch and cache simple HTML pages eg.  
 - http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html
 - http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html
 - http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html
 - http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file5.html
 - http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file6.html


















