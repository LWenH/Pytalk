import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    db='Chat',
)


def get_cursor():
    return conn.cursor()


def safe_execute(sql):
    c = get_cursor()
    try:
        c.execute(sql)
    except Exception:
        return False
    conn.commit()
    return True


def safe_query(sql, num=0):
    c = get_cursor()
    c.execute(sql)
    if num is 1:
        return c.fetchone()
    else:
        return c.fetchall()


def check_login(account, passwd):
    sql = 'SELECT passwd,user_id,name from Users WHERE account = "%s"' % account
    try:
        res = safe_query(sql)[0]
    except Exception:
        return [False]
    if passwd == res[0]:
        return [True, res[1], res[2]]
    return [False]


def do_register(account, passwd, name):
    sql = 'INSERT INTO Users(account,passwd,name,user_id) VALUES ("%s","%s","%s",null)' % (account, passwd, name)
    return safe_execute(sql)


def add_friend(from_id, to_id):
    sql = 'INSERT INTO Friend(user_id,friend_id,accepted) VALUES (%d,%d,false)' % \
          (from_id, to_id)
    return safe_execute(sql)


def get_friend_list(id):
    sql = 'SELECT name,user_id from Users WHERE user_id IN (SELECT friend_id from Friend WHERE user_id = %d and accepted = true)' % id
    return safe_query(sql)


def get_group_list(user_id):
    sql = 'SELECT room_id,identity from RoomUser WHERE user_id = %d' % user_id
    return safe_query(sql)


def add_friend_chat_history(from_id, to_id, text, path=''):
    if path == '':
        text = pymysql.escape_string(text)
        sql = 'INSERT INTO FriendHistory(user_id,friend_id,message,extra_address,create_time) VALUES (%d,%d,"%s",NULL,NOW())' % (
        from_id, to_id, text)
    else:
        sql = 'INSERT INTO FriendHistory(user_id,friend_id,message,extra_address,create_time) VALUES (%d,%d,NULL,"%s",NOW())' % (
        from_id, to_id, path)
    safe_execute(sql)


def query_all_history(from_id, to_id):
    sql = 'SELECT user_id,message,extra_address,create_time from FriendHistory WHERE user_id = %d and friend_id = %d  OR user_id = %d and friend_id = %d ORDER BY create_time ASC' % (
    from_id, to_id, to_id, from_id)
    return safe_query(sql)


def set_all_read(from_id, to_id):
    sql = 'UPDATE FriendHistory SET accepted = 1 WHERE accepted = 0 and user_id = %d and friend_id = %d' % (
    from_id, to_id)
    safe_execute(sql)


def createGroup(room_id, user_id):
    sql = 'INSERT INTO Room(room_id,name) VALUES (%d,"%s")' % (room_id, "群" + str(room_id))
    res = safe_execute(sql)
    if res is True:
        return joinGroup(room_id, user_id, "群主")
    else:
        return False


def joinGroup(room_id, user_id, status):
    sql = 'INSERT INTO RoomUser(room_id,user_id,identity) VALUES (%d,%d,"%s")' % (room_id, user_id, status)
    return safe_execute(sql)


def getRoomPeople(room_id, use_id, status):
    updateStatus(room_id, use_id, status)
    sql = 'SELECT name,identity from users,roomuser WHERE users.user_id = roomuser.user_id and roomuser.room_id = %d' % room_id
    return safe_query(sql)


def updateStatus(room_id, user_id, status):
    sql = 'UPDATE RoomUser SET identity = "%s" where room_id = %d and user_id = %d' % (status, room_id, user_id)
    return safe_execute(sql)


def getRoomUserId(room_id):
    sql = 'SELECT user_id FROM RoomUser where room_id = %d' % room_id
    return safe_query(sql)


def queryUserName(user_id):
    sql = 'SELECT name FROM Users WHERE user_id = %d' % user_id
    return safe_query(sql)


def add_room_chat_history(room_id, user_id, text, path=''):
    if path == '':
        text = pymysql.escape_string(text)
        sql = 'INSERT INTO RoomHistory(room_id,user_id,message,create_time) VALUES(%d,%d,"%s",NOW())' % (
        room_id, user_id, text)
    else:
        sql = 'INSERT INTO RoomHistory(room_id,user_id,extra_address,create_time) VALUES(%d,%d,"%s",NOW())' % (
        room_id, user_id, path)
    safe_execute(sql)


def query_room_history(room_id):
    sql = 'SELECT m1.user_id,name,message,extra_address,create_time FROM RoomHistory m1,Users WHERE room_id = %d and m1.user_id = Users.user_id' % room_id
    return safe_query(sql)


def set_room_all_read(room_id, user_id):
    sql = 'UPDATE RoomHistory SET accepted = true where room_id = %d and user_id = %d' % (room_id, user_id)
    safe_execute(sql)


def updateFriendStatus(user_id, friend_id):
    sql = 'UPDATE Friend SET accepted = true where user_id = %d and friend_id = %d OR user_id = %d and friend_id = %d' % (
    user_id, friend_id, friend_id, user_id)
    safe_execute(sql)


def remove_friend(user_id, friend_id):
    sql = 'DELETE FROM Friend where user_id = %d and friend_id = %d OR user_id = %d and friend_id = %d' % (user_id, friend_id, friend_id, user_id)
    safe_execute(sql)


def get_unaccepted_friend(user_id):
    sql = 'SELECT name,user_id from Users WHERE user_id IN (SELECT friend_id from Friend WHERE user_id = %d and accepted = false)' % user_id
    return safe_query(sql)
