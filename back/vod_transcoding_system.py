from threading import Lock

import db_management
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Program settings and additional information
Version = 1.0
DATABASE = "JobManagement"
JobStatuses = ["todo", "doing", "processed"]
lock = Lock()

db_management.initDB(DATABASE)

app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def is_job_exist(jobId):
    jobs = db_management.getJobs()
    jobsId = [job.id for job in jobs]

    return int(jobId) not in jobsId


def is_profile_exist(profileId):
    profiles = db_management.getProfiles()
    profilesId = [profile.id for profile in profiles]

    return int(profileId) not in profilesId


@app.route('/api/setJobStatus', methods=['POST'])
def set_job_status():
    job_status = request.get_json(force=True)
    jobsId = [job.id for job in db_management.getJobs()]

    if not int(job_status.get("id")) in jobsId:
        return {"code": 404, "msg": "Job with such id:{} doesn't exist."
            .format(job_status.get("id")), "result": True}, 404

    if not job_status.get("status") in JobStatuses:
        return {"code": 404, "msg": "Status {} isn't correct. Allowed statuses: {}"
            .format(job_status.get("status"), JobStatuses), "result": True}, 404

    db_management.changeJobStatus(job_status.get("id"), job_status.get("status"))

    return {"code": 200, "msg": "Status has been set.", "result": True}, 200


@app.route('/api/fetchJob', methods=['GET'])
def fetch_job():
    global lock
    with lock:
        job = next((j for j in db_management.getJobs() if j.status == JobStatuses[0]), None)
        if not job:
            result = {'code': 400, 'msg': "The queue is empty.", "result": False}
            return jsonify(result), result['code']
        else:
            job_options = db_management.getJobOptionsByJobId(job.id)
            result = dict((j.key, j.value) for j in job_options)

            result.update({'jobId': job.id})
            result.update({'service': 'encode'})
            result.update({'name': job.name})
            result.update({'enable': '1'})
            result.update({'version': Version})
            result.update({'config': request.host_url + 'api/getAttributes'})
            result.update({'status': request.host_url + 'api/updateJob'})

            db_management.changeJobStatus(job.id, JobStatuses[1])

            return jsonify(result), 200


@app.route('/api/job', methods=['POST'])
def add_job():
    job = request.get_json(force=True)
    db_management.addJob([db_management.JobOption(key, job["Options"][key]) for key in job["Options"]], job["Name"])

    return jsonify({"code": 200, "msg": "Job has been added.", "result": True})


@app.route('/api/profile/<profile_name>', methods=['GET', 'POST'])
def add_profile(profile_name):
    job_options = request.get_json(force=True)
    db_management.addProfile([db_management.JobOption(key, job_options[key]) for key in job_options], profile_name)

    return jsonify({"code": 200, "msg": "Profile has been added.", "result": True})


@app.route('/api/job/<jobId>', methods=['DELETE'])
def delete_job(jobId):
    if is_job_exist(jobId):
        return jsonify({"code": 404, "msg": "Job with such id:{} doesn't exist."
            .format(jobId), "result": True}), 404
    else:
        db_management.deleteJob(jobId)
        return jsonify({"code": 200, "msg": "Job has been deleted.", "result": True}), 200


@app.route('/api/profile/<profileId>', methods=['DELETE'])
def delete_profile(profileId):
    if is_profile_exist(profileId):
        return jsonify({"code": 404, "msg": "Profile with such id:{} doesn't exist."
            .format(profileId), "result": False}), 404
    else:
        db_management.deleteProfile(profileId)
        return jsonify({"code": 200, "msg": "Profile has deleted.", "result": True}), 200


@app.route('/api/getJobs', methods=['GET'])
def get_jobs():
    index = request.args.get('index', default=None, type=int)
    count = request.args.get('count', default=None, type=int)
    jobs = db_management.getJobs()

    if index is not None and count is not None:
        jobs = jobs[index * count:(index + 1) * count]
    job_dict = [ob.__dict__ for ob in jobs]

    return jsonify(job_dict), 200


@app.route('/api/getProfiles', methods=['GET'])
def get_profiles():
    profiles = db_management.getProfiles()
    profile_dict = [ob.__dict__ for ob in profiles]

    return jsonify(profile_dict), 200


@app.route('/api/getOptions/<job_id>', methods=['GET'])
def get_job_options(job_id):
    job_options = db_management.getJobOptionsByJobId(job_id)
    result = dict((j.key, j.value) for j in job_options)

    return jsonify(result), 200


@app.route('/api/getProfileOptions/<profile_id>', methods=['GET'])
def get_profile_options(profile_id):
    job_options = db_management.getJobOptionsByProfileId(profile_id)
    result = dict((j.key, j.value) for j in job_options)

    return jsonify(result), 200


@app.route('/api/updateJob/<job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    job_options = request.get_json(force=True)
    options = [db_management.JobOption(key, job_options[key]) for key in job_options]
    db_management.updateJob(job_id, options)

    return jsonify({"code": 200, "msg": "Job has been updated.", "result": True}), 200


@app.route('/api/updateProfile', methods=['POST'])
def update_profile():
    profile = request.get_json(force=True)
    options = [db_management.JobOption(key, profile["Options"][key]) for key in profile["Options"]]
    db_management.updateProfile(db_management.Profile(profile["Id"], profile["Name"]), options)

    return jsonify({"code": 200, "msg": "Profile has been updated.", "result": True}), 200


@app.route('/api')
def start():
    return jsonify({'Name': 'VOD Transcoding system', 'Version': Version})


@app.route('/')
def get_page():
    return render_template("index.html")


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        app.run(port=int(argv[1]))
    elif len(argv) == 3:
        app.run(port=int(argv[1]), host=argv[2])
    else:
        app.run()
