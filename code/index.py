import http.server
from http import HTTPStatus
import socketserver

import json
import cassandra_gateway

class HttpHandler(http.server.SimpleHTTPRequestHandler): 

    def do_POST(self):
        # HTTP 응답 상태 코드를 200 (OK)로 설정
        self.send_response(HTTPStatus.OK)
        # 응답 헤더에 'Content-type'을 설정하여 응답이 JSON 형식임을 클라이언트에게 전달
        self.send_header('Content-type','application/json')
        # 헤더 설정이 끝났음을 나타냄
        self.end_headers()
        # 전송된 데이터의 길이를 추출 = POST 요청의 본문 크기
        content_length = int(self.headers['Content-Length'])
        # POST 요청의 본문
        post_data = self.rfile.read(content_length)
        # Json으로 변환 
        json_data = json.loads(post_data)  
        #  CassandraGateway 클래스의 인스턴스를 생성
        db_gateway =  cassandra_gateway.CassandraGateway()
        #  insert 메서드를 호출
        db_resp = db_gateway.insert(json_data)  

        resp = {                   
            "data": db_resp
        }           
        # 응답 데이터를 JSON 형식으로 인코딩하고 바이트로 변환한 후, 클라이언트에게 응답을 전송 
        self.wfile.write(bytes(json.dumps(resp, indent = 2) + "\r\n", "utf8")) 

    def do_GET(self):

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        product_id = 0

        if len(self.path.split("/")) >= 3:
             product_id = self.path.split("/")[2] 

        db_gateway = cassandra_gateway.CassandraGateway()

        db_resp = db_gateway.select(int(product_id))  

        resp = {                   
             "data": db_resp
        }           

        self.wfile.write(bytes(json.dumps(resp, indent = 2) + "\r\n", "utf8"))
    
    def do_DELETE(self):

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        product_id = 0

        if len(self.path.split("/")) >= 3:
             product_id = self.path.split("/")[2] 
        

        db_gateway = cassandra_gateway.CassandraGateway()

        db_resp = db_gateway.delete(int(product_id))  

        resp = {                   
             "data": db_resp
        }           

        self.wfile.write(bytes(json.dumps(resp, indent = 2) + "\r\n", "utf8"))
     
    
#  TCP 서버를 생성
httpd = socketserver.TCPServer(('', 8080), HttpHandler)
print("HTTP server started at port 8080...")

try:
    # 서버가 계속해서 클라이언트의 요청을 수락하고 처리(무한루프)
    httpd.serve_forever()
# 사용자가 키보드로 인터럽트 (Ctrl+C)를 입력하면 http 서버 종료
except KeyboardInterrupt: 

    httpd.server_close()

print("You've stopped the HTTP server.")