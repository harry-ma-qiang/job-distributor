import sqlite3
from datetime import datetime

__DBNAME__ = ""


class Job:
    def __init__(self, job_id, status, lastUpdate, name):
        self.id = job_id
        self.status = status
        self.lastUpdate = lastUpdate
        self.name = name


class Option:
    def __init__(self, option_id, key, name, is_optional):
        self.id = option_id
        self.key = key
        self.name = name
        self.is_optional = is_optional


class JobOption:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Profile:
    def __init__(self, profile_id, name):
        self.id = profile_id
        self.name = name


def initDB(name):
    global __DBNAME__
    if not __DBNAME__:
        __DBNAME__ = name
    else:
        raise RuntimeError("Database name has already been set.")


def currentDatetime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def getOptions():
    options = []
    with sqlite3.connect(__DBNAME__) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Key, Name, Optional FROM Option")

        for option in cursor.fetchall():
            options.append(Option(option[0], option[1], option[2], option[3]))

    return options


def getJobs():
    jobs = []
    with sqlite3.connect(__DBNAME__) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Worker, LastUpdate, Name FROM Job")

        for job in cursor.fetchall():
            jobs.append(Job(job[0], job[1], job[2], job[3]))

    return jobs


def getProfiles():
    profiles = []
    with sqlite3.connect(__DBNAME__) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Name FROM Profile")

        for profile in cursor.fetchall():
            profiles.append(Profile(profile[0], profile[1]))

    return profiles


def getJobOptionsByProfileId(profileId):
    job_options = []
    with sqlite3.connect(__DBNAME__) as conn:
        cursor = conn.cursor()
        cursor.execute(""" SELECT A.Key, J.Value FROM ProfileOptionValues AS J
                            INNER JOIN Option AS A ON A.ID = J.OptionID
                            WHERE ProfileID = ? """, (profileId,))

        for job_option in cursor.fetchall():
            job_options.append(JobOption(job_option[0], job_option[1]))

    return job_options


def getJobOptionsByJobId(jobId):
    job_options = []
    with sqlite3.connect(__DBNAME__) as conn:
        cursor = conn.cursor()
        cursor.execute(""" SELECT A.Key, J.Value FROM JobOptionValues AS J
                            INNER JOIN Option AS A ON A.ID = J.OptionID
                            WHERE JobID = ? """, (jobId,))

        for job_option in cursor.fetchall():
            job_options.append(JobOption(job_option[0], job_option[1]))

    return job_options


def changeJobStatus(jobId, status):
    with sqlite3.connect(__DBNAME__) as conn:
        cursor = conn.cursor()
        now = currentDatetime()
        cursor.execute("UPDATE Job SET Worker = ?, LastUpdate = ? WHERE ID = ?", (status, now, jobId))
        conn.commit()


def addProfile(job_options, profile_name):
    with sqlite3.connect(__DBNAME__) as conn:
        try:
            cursor = conn.cursor()
            # add new job
            cursor.execute("INSERT INTO Profile (Name) VALUES(?)", (profile_name,))
            profile_id = cursor.lastrowid

            # add new job option
            options = getOptions()
            cursor.executemany("INSERT INTO ProfileOptionValues (OptionID, ProfileID, Value) VALUES (?,?,?)",
                               [(next(o.id for o in options if o.key == job_option.key), profile_id, job_option.value)
                                for job_option in job_options])
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()

        return profile_id


def addJob(job_options, name):
    with sqlite3.connect(__DBNAME__) as conn:
        try:
            now = currentDatetime()
            cursor = conn.cursor()
            # add new job
            cursor.execute("INSERT INTO Job (LastUpdate, Name) VALUES(?, ?)", (now, name))
            job_id = cursor.lastrowid

            # add new job option
            options = getOptions()
            cursor.executemany("INSERT INTO JobOptionValues (OptionID, JobID, Value) VALUES (?,?,?)",
                               [(next(o.id for o in options if o.key == job_option.key), job_id, job_option.value)
                                for job_option in job_options])
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()

        return job_id


def updateProfile(profile, job_options):
    with sqlite3.connect(__DBNAME__) as conn:
        try:
            cursor = conn.cursor()
            options = getOptions()
            cursor.executemany("INSERT OR REPLACE INTO ProfileOptionValues (OptionID, ProfileID, Value) VALUES (?,?,?)",
                               [(next(o.id for o in options if o.key == job_option.key), profile.id, job_option.value)
                                for job_option in job_options])
            cursor.execute("UPDATE Profile SET Name = ? WHERE ID = ?", (profile.name, profile.id))
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()


def updateJob(jobId, job_options):
    with sqlite3.connect(__DBNAME__) as conn:
        now = currentDatetime()
        try:
            cursor = conn.cursor()
            options = getOptions()
            cursor.executemany("INSERT OR REPLACE INTO JobOptionValues (OptionID, JobID, Value) VALUES (?,?,?)",
                               [(next(o.id for o in options if o.key == job_option.key), jobId, job_option.value)
                                for job_option in job_options])
            cursor.execute("UPDATE Job SET LastUpdate = ? WHERE ID = ?", (now, jobId))
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()


def deleteProfile(profile_id):
    with sqlite3.connect(__DBNAME__) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ProfileOptionValues WHERE ProfileID=?", (profile_id,))
            cursor.execute("DELETE FROM Profile WHERE ID=?", (profile_id,))
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()


def deleteJob(jobId):
    with sqlite3.connect(__DBNAME__) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM JobOptionValues WHERE JobID=?", (jobId,))
            cursor.execute("DELETE FROM Job WHERE ID=?", (jobId,))
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()
