import mysql.connector


# create a class for populating mysql values
class mysql_connector:

    # initializing the host, user, password and database
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cursor = self.init_mysql_conn()

    # initialize database_connection
    def init_mysql_conn(self):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            print("successfully_connected")
            self.db = mydb
            return mydb.cursor()
        except:
            print("error occured in setting connection with database")


    def toppers_table(self):

        semester = [2, 4]
        map = {}
        for sem in semester:
            query_det = f"""
            SELECT s.st_name, c.c_code, c.marks
            FROM student s
            JOIN certificate c ON s.email_id = c.email_id
            JOIN set_course sc on sc.c_code = c.c_code
            WHERE sc.sem = {sem} and c.marks = (select max(marks) from certificate where c_code = c.c_code);
            """
            self.cursor.execute(query_det)
            toppers_table = self.cursor.fetchall()
            map[sem] = toppers_table
        print(map)
        return map

    def course_name(self):

        query_det = f"""
        SELECT DISTINCT(c_name) 
        FROM course c 
        """
        self.cursor.execute(query_det)
        course_available = self.cursor.fetchall()
        return course_available

    def course_details(self, c_code):

        query_det = f"""
        select c_name,c_code,weeks,nptel_link
        from course where c_code =  '{c_code}';
        """

        self.cursor.execute(query_det)
        course_details = self.cursor.fetchall()
        print(course_details)
        return course_details

    # statistics db query
    def all_set_course(self):
        print("")
        print("this is the data for all the set courses id 1")
        print("")
        query_det = f"""
        SELECT DISTINCT(c.c_name),c.c_code
        FROM course c;
        """

        self.cursor.execute(query_det)
        course_details = self.cursor.fetchall()
        print(course_details)
        return course_details

    def get_details_course(self, c_code):
        print("")
        print("This is the data for available courses id 2")
        print("")
        query_det = f"""
        select * from course
        where c_code = '{c_code}';
        """

        self.cursor.execute(query_det)
        course_details = self.cursor.fetchall()
        print(course_details)
        return course_details

    def tot_avg_max(self, c_code):
        print("")
        print("This is the data for tot average mark id 3")
        print("")
        query_det = f"""
        SELECT COUNT(regno),AVG(verified_marks),MAX(verified_marks) AS total_students
        FROM NPTEL_MARKS
        WHERE c_code = '{c_code}';
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def toppers(self, c_code):
        print("")
        print("This is the data for toppers given sem and course code id 4")
        print("")
        query_det = f"""
        SELECT nm.regno,s.st_name, nm.verified_marks,nm.acc_year, nm.sem_type
        FROM NPTEL_MARKS nm
        join student s on nm.regno = s.regno
        WHERE nm.c_code = '{c_code}' -- Replace 'noc24-cs47' with your desired course code
        ORDER BY nm.verified_marks DESC
        LIMIT 10;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def convert_to_dicts(self, input_list):
        output = [
            {"year": str(year), "odd_semester": odd, "even_semester": even}
            for year, even, odd in input_list
        ]
        return output

    def enrollment_graph(self, c_code):
        print("")
        print("This is the data for double line graph chart id 5")
        print("")
        query_det = f"""
        SELECT 
            acc_year AS Year,
            COUNT(CASE WHEN sem_type = 'even' THEN regno END) AS Even_Sem_Enrollment_Count,
            COUNT(CASE WHEN sem_type = 'odd' THEN regno END) AS Odd_Sem_Enrollment_Count
        FROM 
            NPTEL_MARKS
        where c_code = '{c_code}'
        GROUP BY 
            acc_year;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        records = self.convert_to_dicts(records)
        print("@@@@@@@")
        print(records)
        return records

    def pie_chart(self, c_code):
        print("")
        print("This is the data for pie chart id 6")
        print("")
        query_det = f"""
        SELECT 
            sem, 
            COUNT(DISTINCT regno) AS num_students_enrolled 
        FROM NPTEL_MARKS 
        WHERE c_code = '{c_code}' 
        GROUP BY sem;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def silver_score_graph(self, c_code):
        print("")
        print("This is the data for slacked bar graph id 7")
        print("")
        query_det = f"""
        SELECT 
            acc_year AS Year,
            COUNT(CASE WHEN sem_type = 'even' AND verified_marks BETWEEN 50 AND 80 THEN regno END) AS Even_Sem_Marks_Count,
            COUNT(CASE WHEN sem_type = 'odd' AND verified_marks BETWEEN 50 AND 80 THEN regno END) AS Odd_Sem_Marks_Count
        FROM 
            NPTEL_MARKS
            
        where c_code = '{c_code}'
        GROUP BY 
            acc_year;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def gold_score_graph(self, c_code):
        print("")
        print("This is the data for multiple line chart id 8")
        print("")

        query_det = f"""
        SELECT 
            acc_year AS Year,
            COUNT(CASE WHEN sem_type = 'even' AND verified_marks BETWEEN 80 AND 100 THEN regno END) AS Even_Sem_Marks_Count,
            COUNT(CASE WHEN sem_type = 'odd' AND verified_marks BETWEEN 80 AND 100 THEN regno END) AS Odd_Sem_Marks_Count
        FROM 
            NPTEL_MARKS
            
        where c_code = '{c_code}'
        GROUP BY 
            acc_year;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def ins_std_table(self, records: list):

        try:
            query_ins = " "
            for record in records:
                # get the reg no and name and popullate the database
                query_ins += f"""
                        insert into student (regno, st_name) values ('{record[1]}', '{record[2]}');
                        """
                print(query_ins)
            self.cursor.execute(query_ins)

            self.db.commit()

        except Exception as e:
            # Handle the error, print a message, and optionally rollback the transaction
            print("Error:", e)
            # self.db.rollback()

    def many_std_insert(self, data: list):
        print("student DATTAAAA")
        print(data)
        regno = []
        values = []
        query_det = f"""
        select regno from student;
        """
        self.cursor.execute(query_det)
        old_course = [course[0] for course in self.cursor.fetchall()]
        print(old_course)
        for record in data:
            if record[1] not in regno:
                regno.append(record[1])
                tup = (record[1], record[2])
                if record[1] not in old_course:
                    values.append(tup)
        insert_st = "INSERT INTO STUDENT(regno,st_name) values (%s,%s)"
        # print(values)
        for value in values:
            print(value)
            self.cursor.execute(insert_st, value)
        self.db.commit()
        # self.db.close()
        return True

    def many_course_insert(self, data):
        print("DATTAAAA")
        print(data)
        regno = []
        values = []
        query_det = f"""
        select c_code from course;
        """
        self.cursor.execute(query_det)
        old_course = [course[0] for course in self.cursor.fetchall()]
        print(old_course)
        for record in data:
            # record[4] => code record[5] => c_name
            if record[4] not in regno:
                regno.append(record[4])
                tup = (record[4], record[5])
                if record[4] not in old_course:
                    values.append(tup)
        insert_st = "INSERT INTO COURSE(c_code,c_name) values (%s,%s)"
        self.cursor.executemany(insert_st, values)
        self.db.commit()
        # self.db.close()
        return True

    def many_nptelmark_ins(self, data, sem, year):
        print("DATTAAAA")
        print(data)
        regno_c_code = []
        values = []
        for record in data:
            print(
                type(record[1]), type(record[4]), type(record[7]), type(sem), type(year)
            )
            print(record[1], record[4], record[7], sem, year)
            # record[1] => regno record[4] => c_code
            if record[1] not in regno_c_code:
                regno_c_code.append((record[1], record[4]))
                tup = (record[1], record[4], record[7], record[3], year, sem)
                values.append(tup)
        # print(values)
        insert_st = "INSERT INTO nptel_marks(regno,c_code,verified_marks,sem,acc_year,sem_type) values (%s,%s,%s,%s,%s,%s)"
        for value in values:
            print(value)

            self.cursor.execute(insert_st, value)
        self.db.commit()
        # self.db.close()
        return True

    def facade_insert(self, data, sem, year):
        """
        inserts the values into student table,course and nptel_marks table
        """
        a = self.many_std_insert(data.copy())
        if a:
            b = self.many_nptelmark_ins(data.copy(), sem, year)
        if b:
            c = self.many_course_insert(data.copy())
        print(a, b, c)
        return True

    def getUniqueRegnoCountBySemTypeAndYear(self, acc_year, sem_type):
        print("")
        print("This is the data for the unique regno count")
        print("")

        query_det = f"""
        SELECT COUNT(DISTINCT regno) AS unique_regno_count
        FROM NPTEL_MARKS
        WHERE sem_type = '{sem_type}' AND acc_year = '{acc_year}';
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getUniqueCourseCodeCountBySemTypeAndYear(self, acc_year, sem_type):
        print("")
        print("This is the data for the unique course code given year and sem type")
        print("")

        query_det = f"""
        SELECT COUNT(DISTINCT c_code) AS unique_course_code_count
        FROM NPTEL_MARKS
        WHERE sem_type = '{sem_type}' AND acc_year = '{acc_year}';
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getEnrolledCountGroupedByYearAndSemType(self):
        print("")
        print("This is the data for the unique enrolled count given year and sem_type")
        print("")

        query_det = f"""
        SELECT 
            acc_year,
            SUM(CASE WHEN sem_type = 'odd' THEN count ELSE 0 END) AS odd_sem_count,
            SUM(CASE WHEN sem_type  = 'even' THEN count ELSE 0 END) AS even_sem_count
        FROM 
            (SELECT 
                acc_year,
                sem_type,
                COUNT(DISTINCT regno) AS count
            FROM 
                NPTEL_MARKS
            GROUP BY 
                acc_year, 
                sem_type) AS subquery
        GROUP BY 
            acc_year
        ORDER BY 
            acc_year;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getSemesterWiseCountByYearAndSemType(self, acc_year, sem_type):
        print("")
        print("This is the data for unique year given year and sem_type")
        print("")

        query_det = f"""
        SELECT 
            sem,
            COUNT(distinct(regno)) AS count
        FROM 
            NPTEL_MARKS
        WHERE 
            acc_year = '{acc_year}' 
            AND sem_type = '{sem_type}'
        GROUP BY 
            sem
        ORDER BY 
            sem;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getDistinctAcademicYears(self):
        print("")
        print("This is the data for distinct accademic years available")
        print("")

        query_det = f"""
        select distinct(acc_year) from nptel_marks;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getDistinctSemesterTypes(self):
        print("")
        print("This is the data for different sem types available")
        print("")

        query_det = f"""
        select distinct(sem_type) from nptel_marks;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records

    def getToppersgivenSemandYear(self, sem, year):
        print("")
        print("This is the data for different toppers")
        print("")
        print(sem, year)
        query_det = f"""
        SELECT 
    nm.regno,
    s.st_name,
    c.c_name,
    nm.verified_marks,
    nm.acc_year,
    nm.sem_type
FROM 
    NPTEL_MARKS nm 
    JOIN student s ON nm.regno = s.regno
    JOIN course c ON c.c_code = nm.c_code
WHERE 
    nm.acc_year = '{year}' -- Specify the desired academic year
    AND nm.sem_type = '{sem}' -- Specify the desired semester type
ORDER BY
    nm.verified_marks desc
LIMIT 5;
        """

        self.cursor.execute(query_det)
        records = self.cursor.fetchall()
        print(records)
        return records


my_db_connect = mysql_connector("localhost", "root", "password", "nptel_management")


my_db_connect.getToppersgivenSemandYear("odd", "2021-22")
