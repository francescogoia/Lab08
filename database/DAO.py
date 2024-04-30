from database.DB_connect import DBConnect
from model.nerc import Nerc
from model.powerOutages import Event


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNerc():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from nerc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Nerc(row["id"], row["value"]))


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEvents(nerc):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from poweroutages
                    where nerc_id = %s
                    """

        cursor.execute(query, (nerc.id,))

        for row in cursor:
            e = Event(row["id"], row["event_type_id"],
                      row["tag_id"], row["area_id"],
                      row["nerc_id"], row["responsible_id"],
                      row["customers_affected"], row["date_event_began"],
                      row["date_event_finished"], row["demand_loss"],
                      )
            e.set_durata()
            result.append(e)



        cursor.close()
        conn.close()
        return result


if __name__ == "__main__":
    d = DAO()
    d.getAllNerc()

