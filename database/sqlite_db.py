import sqlite3 as sq


async def sql_start():
    global base, cur
    base = sq.connect('anonim_bot.db')
    cur = base.cursor()

    if base:
        print("database conected ok")

    base.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY)')
    base.execute('CREATE TABLE IF NOT EXISTS room(room_number TEXT PRIMARY KEY ,enter_teacher_code TEXT ,enter_student_code TEXT ,teacher_id TEXT ,student_id TEXT ,room_status TEXT,chat_id TEXT,teacher_note TEXT)')
    base.commit()


async def sql_create_room(room_number, enter_code_for_teacher, enter_code_for_student, room_status, chat_id,teacher_note):
    cur.execute('INSERT OR IGNORE INTO room VALUES (?,?,?,?,?,?,?,?)',(room_number, enter_code_for_teacher, enter_code_for_student, 0, 0, room_status, chat_id,teacher_note))
    base.commit()


async def get_chat_id(room_number):
    tmp1 = cur.execute('SELECT chat_id FROM room WHERE room_number = ?', (room_number,)).fetchone()
    print("tmp1[0]", tmp1[0])
    return tmp1[0]


async def sql_add_user_id(user_id):
    cur.execute('INSERT OR IGNORE INTO users VALUES (?)', (user_id,))
    base.commit()


async def sql_show_all_rooms() -> object:
    """

    :rtype: object
    """
    return cur.execute('SELECT room_number FROM room').fetchall()


async def sql_show_enter_teacher_code_rooms():  # не треба
    return cur.execute('SELECT enter_teacher_code FROM room').fetchall()


async def check_id_for_teacher(id):
    teacher_id = cur.execute('SELECT teacher_id FROM room').fetchall()
    if id in teacher_id:
        return 1
    else:
        return 0


async def check_id_for_student(id):
    student_id = cur.execute('SELECT student_id FROM room').fetchall()
    print(student_id)
    if id in student_id:
        return 1
    else:
        return 0


async def check_user_id(id):
    user_id = cur.execute('SELECT user_id FROM users WHERE user_id == ?', (f'{id}',)).fetchone()
    if user_id:
        return 1
    else:
        return 0


async def check_teacher_id_exist(user_id):
    tmp = cur.execute('SELECT teacher_id FROM room WHERE teacher_id == ?', (f'{user_id}',)).fetchone()
    # print(user_id)
    return tmp


async def check_student_id_exist(user_id):
    tmp = cur.execute('SELECT student_id FROM room WHERE student_id == ?', (f'{user_id}',)).fetchone()
    tmp2 = cur.execute('SELECT teacher_id FROM room WHERE teacher_id == ?', (f'{user_id}',)).fetchone()
    if tmp:
        return 1
    if tmp2:
        return 2




async def check_teacher_or_student_code_for_enter(code):
    teacher_code = cur.execute('SELECT enter_teacher_code FROM room  WHERE enter_teacher_code == ?',
                               (f'{code}',)).fetchone()
    student_code = cur.execute('SELECT enter_student_code FROM room  WHERE enter_student_code == ?',
                               (f'{code}',)).fetchone()

    try:
        if teacher_code:
            return 'teacher'
        elif student_code:
            return 'student'
        else:
            return 'no in rooms'

    except Exception as err:
        return err


async def update_id_for_teacher_in_room(id, room_code_for_teacher):
    cur.execute('UPDATE room SET teacher_id = ? WHERE enter_teacher_code = ?', (id, room_code_for_teacher))
    base.commit()


async def update_id_for_student_in_room(id, room_code_for_student):
    cur.execute('UPDATE room SET student_id = ? WHERE enter_student_code = ?', (id, room_code_for_student))
    base.commit()


# ----------------------

async def check_which_room(id):
    tmp = cur.execute('SELECT room_number FROM room WHERE teacher_id OR student_id == ?', (f'{id}',)).fetchone()
    return tmp[0]


async def check_room_exist(room_number):
    tmp = cur.execute('SELECT room_number FROM room WHERE room_number == ?', (f'{room_number}',)).fetchone()
    if tmp:
        return 1
    else:
        return 0


async def get_enter_teacher_code_using_room_number(room_number):
    tmp1 = cur.execute('SELECT enter_teacher_code FROM room WHERE room_number = ?', (room_number,)).fetchone()
    return tmp1[0]


async def get_enter_student_code_using_room_number(room_number):
    tmp1 = cur.execute('SELECT enter_student_code FROM room WHERE room_number = ?', (room_number,)).fetchone()
    return tmp1[0]


async def get_teacher_user_id(room_number):
    tmp1 = cur.execute('SELECT teacher_id FROM room WHERE room_number = ?', (room_number,)).fetchone()
    return tmp1[0]


async def get_room_status(room_number):
    tmp1 = cur.execute('SELECT room_status FROM room WHERE room_number = ?', (room_number,)).fetchone()
    return tmp1[0]


#   cur.execute('UPDATE room SET student_id = ? WHERE enter_student_code = ?',(id,room_code_for_student))


async def check_room_status(room_number):
    tmp1 = cur.execute('SELECT teacher_id FROM room WHERE room_number = ?', (room_number,)).fetchone()
    tmp2 = cur.execute('SELECT student_id FROM room WHERE room_number = ?', (room_number,)).fetchone()

    if tmp1[0] and tmp2[0]:
        print("2")
        cur.execute('UPDATE room SET room_status = "Active" WHERE room_number == ?', (room_number,))
        base.commit()
        return 1

    else:
        print("3")
        return 0


async def check_active_status_room(room_number):
    tmp1 = cur.execute('SELECT room_status FROM room WHERE room_number = ?', (room_number,)).fetchone()
    if tmp1[0] == 'Active':
        print("active")
        return 1
    else:
        return 0



async def get_student_user_id(room_number):
    tmp1 = cur.execute('SELECT student_id FROM room WHERE room_number = ?', (room_number,)).fetchone()
    print(tmp1[0])
    return tmp1[0]


async def get_teacher_user_id(room_number):
    tmp1 = cur.execute('SELECT teacher_id FROM room WHERE room_number = ?', (room_number,)).fetchone()
    return tmp1[0]


async def get_user_id(user_id):
    tmp1 = cur.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return tmp1[0]


async def sql_delete_room(room_number):
    cur.execute('DELETE FROM room WHERE room_number = ?', (room_number,))
    base.commit()


async def check_teacher_or_student_kick(user_id):
    teacher_id = cur.execute('SELECT teacher_id FROM room  WHERE teacher_id == ?', (f'{user_id}',)).fetchone()
    student_id = cur.execute('SELECT student_id FROM room  WHERE student_id == ?', (f'{user_id}',)).fetchone()

    try:
        if teacher_id:
            return 'teacher'
        elif student_id:
            return 'student'
        else:
            return 'no in rooms'

    except Exception as err:
        return err


async def kick_teacher_from_room(teacher_id):
    cur.execute('UPDATE room SET teacher_id = 0 WHERE teacher_id == ?', (teacher_id,))
    base.commit()


async def kick_student_from_room(student_id):
    cur.execute('UPDATE room SET student_id = 0 WHERE student_id == ?', (student_id,))
    base.commit()


async def update_enter_teacher_code(new_enter_code_for_teacher, data):
    cur.execute('UPDATE room SET enter_teacher_code = ? WHERE teacher_id == ?', (new_enter_code_for_teacher, data))
    base.commit()


async def update_enter_student_code(new_enter_code_for_student, data):
    cur.execute('UPDATE room SET enter_student_code = ? WHERE student_id == ?', (new_enter_code_for_student, data))
    print("updated")
    base.commit()

# ----------------------------------------------------------------------


async def get_teacher_note(room_number):
    tmp1 = cur.execute('SELECT teacher_note FROM room WHERE room_number = ?', (room_number,)).fetchone()
    return tmp1[0]



async def set_note_to_room(data,room_number):
    cur.execute('UPDATE room SET teacher_note = ? WHERE room_number = ?', (data,room_number,))

    print('data',data)
    base.commit()


async def get_all_rooms_for_teacher():  # не треба
    return cur.execute('SELECT enter_teacher_code FROM room').fetchall()