import sqlite3
from datetime import datetime

__DBNAME__ = ""


class Job:
    def __init__(self, job_id, status, lastUpdate):
        self.id = job_id
        self.status = status
        self.lastUpdate = lastUpdate


class Attribute:
    def __init__(self, key, value):
        self.key = key
        self.value = value


def initDB(name):
    global __DBNAME__
    if not __DBNAME__:
        __DBNAME__ = name
    else:
        raise RuntimeError("Database name has already been set.")


def currentDatetime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def getJobs():
    jobs = []
    with sqlite3.connect(__DBNAME__) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Worker, LastUpdate FROM Job")

        for job in cursor.fetchall():
            jobs.append(Job(job[0], job[1], job[2]))

    return jobs


def getAttributesByJobId(jobId):
    attributes = []
    with sqlite3.connect(__DBNAME__) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Key, Value FROM Attribute WHERE JobID = ?", (jobId,))

        for attribute in cursor.fetchall():
            attributes.append(Attribute(attribute[0], attribute[1]))

    return attributes


def changeJobStatus(jobId, status):
    with sqlite3.connect(__DBNAME__) as conn:
        cursor = conn.cursor()
        now = currentDatetime()
        cursor.execute("UPDATE Job SET Worker = ?, LastUpdate = ? WHERE ID = ?", (status, now, jobId))
        conn.commit()


def addJob(attributes):
    with sqlite3.connect(__DBNAME__) as conn:
        try:
            now = currentDatetime()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Job (LastUpdate) VALUES(?)", (now,))
            job_id = cursor.lastrowid
            cursor.executemany("INSERT INTO Attribute (Key, Value, JobID) VALUES (?,?,?)",
                               [(attribute.key, attribute.value, cursor.lastrowid) for attribute in attributes])
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()

        return job_id


def addAttributes(jobId, attributes):
    with sqlite3.connect(__DBNAME__) as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO Attribute (Key, Value, JobID) VALUES (?,?,?)",
                           [(attribute.key, attribute.value, jobId) for attribute in attributes])
        conn.commit()


def updateJob(jobId, attributes):
    with sqlite3.connect(__DBNAME__) as conn:
        now = currentDatetime()
        try:
            cursor = conn.cursor()
            cursor.executemany("INSERT OR REPLACE INTO Attribute (Key, Value, JobID) VALUES (?,?,?)",
                               [(attribute.key, attribute.value, jobId) for attribute in attributes])
            cursor.execute("UPDATE Job SET LastUpdate = ? WHERE ID = ?", (now, jobId))
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()


def deleteJob(jobId):
    with sqlite3.connect(__DBNAME__) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Attribute WHERE JobID=?", (jobId,))
            cursor.execute("DELETE FROM Job WHERE ID=?", (jobId,))
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()
