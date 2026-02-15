from supabase import create_client, Client


def connect():
    SUPABASE_URL= 'https://kowiztmshzyngqsjabtv.supabase.co'#link for program to send a request to
    SUPABASE_KEY='sb_publishable_GndDzAqshC7SlvqDooQKFw_WW49ETzH'# used for authentication and gaining a valid request
    #Creates and returns a PostgreSQL connection.
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        return -1


def Read(connection, table, filters=None):
    try:
        query = connection.table(table).select("*")
        if filters:
            for column, value in filters.items():
                #filters is a dictionary which will have conditions e.g {'UserID': 3}
                query = query.eq(column, value)
                #each iteration refines the query statement here, .eq adds the query on to make a refined query
        response = query.execute()#searches the table for the data that satisfies the queries
        if response.data == []:
            return -1
        return response.data
    except:
        return -1
        

def Create(connection, Table, data):
    try:
        response = connection.table(Table).insert(data).execute()
        #Creates a record in a specified table using the data given
        return response.data
    except Exception as e:
        print(e)    
        return -1

def Update(connection, Table, filters, NewValues):
    try:
        query = connection.table(Table).update(NewValues)
        #prepares a statement to update a record e.g if NewValues = {"WinProb": 0.7} Then query is basically UPDATE table SET WinProb = 0.7, 
        #but this is not executed yet as the filters have not been added
        for column, value in filters.items():
            query = query.eq(column, value)
            #this adds the filter statements to the query variable, this poses the same function as in the read function
        response = query.execute()#sends a request to update the data in the database
        if response == []:
            return -1
        return response.data

    except:
        return -1

def Delete(connection, table, filters):
    try:
        query = connection.table(table).delete()
    #prepares a delete statement
        for column, value in filters.items():
            query = query.eq(column, value)
            #adds the filter statements 
        response = query.execute()#sends a request to delete the data
        if response == []:
            return 0
    except:
        return -1

