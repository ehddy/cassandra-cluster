from cassandra.cluster import Cluster
from cassandra.query import dict_factory

class CassandraGateway:
    
    def db_session(self):
        # cluster 연결 (컨테이너(노드) 이름 입력)
        contact_points = ['cassandra1', 'cassandra2', 'cassandra3']
        clstr = Cluster(contact_points=contact_points)

        # 조작할 keyspace 이름 입력
        session = clstr.connect('test_keyspace')

        return session
    
    def select(self, id = 0):

        db_session   = self.db_session()
        # 열 이름을 나열하는 사전 형식으로 테이블 dict_factory의 데이터를 반환
        db_session.row_factory = dict_factory

        if id == 0:

            query_string = "select * from test_table;"
            stmt = db_session.prepare(query_string)     
            prepared_query = stmt.bind([])   

        else:

            query_string = "select * from test_table where id = ?;"
            stmt = db_session.prepare(query_string)         
            prepared_query = stmt.bind([int(id)])          

        rows = db_session.execute(prepared_query)

        return list(rows)

    def insert(self, json_data):

        db_session   = self.db_session()
        query_string = "insert into test_table (id, location, email, name) values (?, ?, ?, ?);"

        stmt = db_session.prepare(query_string)

        id   = int(json_data["id"])
        location = json_data["location"]
        email = json_data["email"]
        name = json_data["name"]

        prepared_query = stmt.bind([id, location, email, name])

        db_session.execute(prepared_query)

        return self.select(id)

    def delete(self, id):
        db_session = self.db_session()
        query_string = "DELETE FROM test_table WHERE id = ?;"
        
        stmt = db_session.prepare(query_string)
        prepared_query = stmt.bind([id])

        result = db_session.execute(prepared_query)

        # Return a message or result if needed
        return f"Deleted record with id {id}"


    

# client = CassandraGateway()
# data = {"id": 6, "location": "SEOUL", "email": "dongdong@naver.com", "name":"dongyo"}
# print(client.insert(data))
# # print(client.insert(data))
# # print(client.delete(id=5))
# print(client.delete(id=6))