# job-distributor
A simple job distribution
## Installation
Run one of those command (depend on your OS system):  
  * `sudo bash installation_for_ubuntu.bash` (for Ubuntu).  
  * `sudo bash installlation_for_amazon_lin.bash` (for Amazon Linux).
  
  
## Running system
Run command in folder ./back:  `python vod_transcoding_system.py <port> <host>`.  
Where:
  * `<port>` — port through which system will be working (default value 5000).
  * `<host>` — host on which system will be hosting (default value localhost). 
    
    
## Usage
### Get start page
Return frontend page that uses the API system.
  * **URL**  
    /
  * **Method:**  
    `GET`
  * **Success Response:**  
    HTML page
  
### Show system information
Return information about system (version, name of the system).
  * **URL**  
    /api
  * **Method:**  
    `GET`  
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ Name: "VOD Transcoding system", Version: 1.0 }`

### Add job
Add job to the job queue (for further processing). 
  * **URL**  
    /api/job  
  * **Method:**  
    `POST`  
  * **Data Params**    
    `{ Options: { <Key:string>: <Value:string>...}, Name: <name:string>}`  
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ code: 200, msg: "Job has been added.", result: True }`  
    
### Edit job
Edit job from the job queue (change or add new options). 
  * **URL**  
    /api/updateJob/:id    
  * **Method:**  
    `POST`  
  * **URL Params**  
      **Required:**    
      `id=[integer]`
  * **Data Params**    
    `{ Options: { <Key:string>: <Value:string>...}, Name: <name:string>}`  
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ code: 200, msg: "Job has been updated.", result: True }`  
    
 ### Delete job
Delete job from the job queue. 
  * **URL**  
    /api/job/:id    
  * **Method:**  
    `DELETE`  
  * **URL Params**  
      **Required:**    
      `id=[integer]` 
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ code: 200, msg: "Job has been deleted.", result: True }`
  * **Error Response:**
    * **Code:** 404  
    **Content:** `{ code: 404, msg: "Job with such id:<id> doesn't exist.", result: False }`  
    
 ### Get jobs
Return list of all jobs.
  * **URL**  
    /api/getJobs
  * **Method:**  
    `GET`  
  * **Success Response:**
    * **Code:** 200  
    **Content:** `[{job Object}, {job Object}...]`  
    
 ### Get job options  
Return job options by job id.
  * **URL**  
    /api/getOptions/:id
  * **Method:**  
    `GET`  
  * **URL Params**  
    **Required:**    
    `id=[integer]` 
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ <Key:string>: <Value:string>,... }`
    
 ### Pop job from the queue 
Remove (set status 'doing') the next job from the queue and return it.
  * **URL**  
    /api/fetchJob
  * **Method:**  
    `GET`  
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ jobId: <id:integer>, name: <jobName:string>, service: 'encode', enable: '1', version: <version:integer>, config:  <host:string>/api/getAttributes, status: <host:string>/api/updateJob, <Key:string>: <Value:string> ... }`  
   * **Error Response:**  
    * **Code:** 400  
    **Content:** `{ code: 400, msg: "The queue is empty.", result: False }`
    
### Set job status
Set job status. 
  * **URL**  
    /api/setJobStatus    
  * **Method:**  
    `POST`  
  * **Data Params**  
      `{id: 1, status: 'todo' }`  
      `id` - job id.  
      `status` - status of job. Possible statuses: 'todo', 'doing', 'processed'.  
      todo - job waiting for processing in the job queue.  
      doing - job has been already picked from the queue, but hasn't been processed yet.   
      processed - job has been picked from the queue and already processed.    
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ code: 200, msg: "Status has been set.", result: True }`
  * **Error Response:**
    * **Code:** 404  
    **Content:** `{ code: 404, msg: "Job with such id:<id> doesn't exist.", result: False }`  
  OR  
    * **Code:** 404  
    **Content:** `{ code: 404, msg: "Status id:<id> isn't correct. Allowed statuses: ['todo', 'doing', 'processed']", result: False }`

 ### Get options
Return list of available options.
  * **URL**  
    /api/getOptions
  * **Method:**  
    `GET`  
  * **Success Response:**
    * **Code:** 200  
    **Content:** `[{option Object}, {option Object}...]`  
    
### Add profile
Add profile with job options (options will be using to fill out job information automatically). 
  * **URL**  
    /api/profile/:profile_name  
  * **Method:**  
    `POST`  
  * **URL Params**  
    **Required:**    
    `profile_name=[string]`  
  * **Data Params**    
    `{ <Key:string>: <Value:string>... }`  
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ code: 200, msg: "Profile has been added.", result: True }` 
    
 ### Delete profile
Delete profile from db. 
  * **URL**  
    /api/profile/:id    
  * **Method:**  
    `DELETE`  
  * **URL Params**  
      **Required:**    
      `id=[integer]` 
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ code: 200, msg: "Profile has been deleted.", result: True }`
  * **Error Response:**
    * **Code:** 404  
    **Content:** `{ code: 404, msg: "Profile with such id:<id> doesn't exist.", result: False }` 
    
 ### Get profiles
Return list of all profiles.
  * **URL**  
    /api/getProfiles
  * **Method:**  
    `GET`  
  * **Success Response:**
    * **Code:** 200  
    **Content:** `[{profile Object}, {profile Object}...]` 
    
 ### Get profile options  
Return profile options by profile id.
  * **URL**  
    /api/getProfileOptions/:id
  * **Method:**  
    `GET`  
  * **URL Params**  
    **Required:**    
    `id=[integer]` 
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ <Key:string>: <Value:string>,... }`
  
  ### Edit profile
Edit profile. Change or add new options, change the name of the profile.
  * **URL**  
    /api/updateProfile    
  * **Method:**  
    `POST`  
  * **Data Params**    
    `{ Id: 1, Name: "Profile1" ,Options: { <Key:string>: <Value:string>... } }`  
  * **Success Response:**
    * **Code:** 200  
    **Content:** `{ code: 200, msg: "Profile has been updated.", result: True }`  
