from database.DB_connect import DBConnect
from model.sightings import Sighting
from model.state import State
class DAO():
   @staticmethod
   def getAllSightings():
      conn = DBConnect.get_connection()
      result = []
      cur = conn.cursor(dictionary=True)
      cur.execute("SELECT * from sighting")
      for row in cur:
         result.append(Sighting(**row))
      cur.close()
      conn.close()
      return result

   @staticmethod
   def getAllStates():
      conn = DBConnect.get_connection()
      result = []
      cur = conn.cursor(dictionary=True)
      cur.execute("select * from state")
      for row in cur:
         result.append(State(**row))
      cur.close()
      conn.close()
      return result

   @staticmethod
   def getConnessioni(shape, anno, idMap):
      conn = DBConnect.get_connection()
      result = []
      cur = conn.cursor(dictionary=True)
      query = """SELECT n.state1 as s1, n.state2 as s2, count(*) as avv
                    FROM sighting s , neighbor n 
                    where year(s.`datetime`) = %s
                    and s.shape = %s
                    and (s.state = n.state1 or s.state = n.state2 )
                    and n.state1 < n.state2
                    group by n.state1 , n.state2 """
      cur.execute(query, (anno, shape))
      for row in cur:
            result.append((idMap[row['s1']], idMap[row['s2']], row['avv']))
      cur.close()
      conn.close()
      return result

