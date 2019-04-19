# sample-python-api

This is a backend engineer assessment. Here I built:
- a customer data model
- an Basic JSON API perform CRUD functions on the customer data model
- authentication using JWT Token.
- and how to deploy on AWS Amazon Lightsail (80% completed).

## Getting-started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a cloud hosting, i.e. AWS LightSail.

### Prerequisites

You need to install on your local machine 
- a virtual environment of **Python 3.6.x** via virtual_env or pipenv (there is some issues with conda in the deployment stage at the moment)
- [**PostgreSQL**](http://www.postgresqltutorial.com/install-postgresql/), remember to save value of `Database Port`(5432 by default), `Database Superuser`(postgres by default), and `Password` when you first install it
- [**Postman**](https://www.getpostman.com/downloads/)
- and the following packages:
```sh
pip install psycopg2
pip install flask
pip install flask_restful
pip install flask_jwt
```

### Installing

In the terminal, clone this repository to your local machine
```sh
git clone https://github.com/hovinh/sample-python-api
```

Modify the line 16-19 in *postgresql_database.py* file with saved value of `Database Port`, `Database Superuser`, and `Password`. Mine is:
```python
                user="postgres",
                password="HoXu2nv!nh",
                host="localhost",
```

Open Postman application, go to Import >> Import From Link, and enter "https://www.getpostman.com/collections/0098fe53a825ad757fd6" to import my Postman collection. Once done, you will have the **Customers** collection on the left containing all the test queries.

![](img/postman_collection.png)

### Running the test

In the terminal, run the JSON API
```sh
python app.py
```
It will be fine if the terminal outputs similarly to below
```sh
* Serving Flask app "settings" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 109-851-098
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Now in Postman, you can test with requests stored in **Customers** collection. I will explain 4 test cases, and the others work similarly. All required parameters have been filled in beforehand, so you can figure out how to do them via alternative way, like **curl**.

#### AUTHENTICATION > REQUEST DENIED
When click the "Send" button, you will see response:
```json
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
```
This works as intended because the user does not have access token.

#### AUTHENTICATION > GET TOKEN
When click the "Send" button, you will see response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTU1ODYxNDQsImlhdCI6MTU1NTU4NTg0NCwibmJmIjoxNTU1NTg1ODQ0LCJpZGVudGl0eSI6MTIzfQ.Oqsc1yRb9UCGGPtbKyZvCaQoNrGoLGRQXM9huFOY0JQ"
}
```
Now we have the access token, and should be able to perform the previous request.

#### AUTHENTICATION > REQUEST AUTHENTICATED
Copy the access token to header, we now can retrieve information from the database.
```json
{
    "msg": "OK",
    "result": [
        {
            "dob": "1809-02-12",
            "id": 1,
            "name": "Abraham Lincoln",
            "updated_at": "2019-04-18 18:58:29 +0800"
        },
    ......
    ],
    "status_code": 200
}
```

>> **NOTE**: An access token expires after a period of time, so if you receive `status_code` 401, you need to get another token before querying. 

#### CUSTOMERS_QUERY > QUERY THE YOUNGEST CUSTOMER

User can freely perform complex retrieveal query (GET) on "http://localhost:5000/api/v1/customers_query" endpoint. Send the request will receive a respond of the 2 youngest customers: "Queen Elizabeth II" and "Mr. Anonymous".


## Deployment (80% completed)

In this section, I will show how to deploy a "Hello World!" application on AWS Lightsail's Ubuntu server. However, I haven't configured the intended app to work just yet.

Here are what you need to prepare:
- Sign up for a free [AWS account](https://aws.amazon.com/). Enter your billing information is required, yet you will not be charged.
- Create a `credentials` and `config` file as instructed [here](http://polyglot.ninja/deploying-flask-based-rest-api-aws-lambda-serverless-using-zappa/).
- Prepare AWS IAM User, Role, and Policies for Zappa, following all steps in [here](https://www.codingforentrepreneurs.com/blog/aws-iam-user-role-policies-zappa-serverless-python). Save information of created `ZappaUser`, i.e. `Access key ID` and `Secret access key`.
- Go to AWS Lightsail, create an instance of **Ubuntu 16.04 LTS** with the cheapest plan(first month for free). Once done, connect to it.
- You now need to setup a virtual environment (Python 3.6), install PostgreSQL, and all required package before deploying the service. In the terminal, type in the following lines:
```sh 
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6

cd ~
python3.6 -m venv virtualenv --without-pip
cd virtualenv/
source bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python3
python --version

sudo apt-get install postgresql
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev

pip install psycopg2-binary
pip install psycopg2
pip install flask
pip install flask_restful
pip install flask_jwt
pip install awscli
pip install zappa
```
- Remember `credentials` and `config` files? Now save them to `~/.aws` directory in the server. It is hidden under `ls` command but you can `cd` to it. 
- Enter `Access key ID` and `Secret access key` to the terminal:
```sh
aws configure
AWS Access Key ID [****************GVEA]: <YOUR_AWS_ACCESS_KEY>
AWS Secret Access Key [****************VxPd]: <YOUR_AWS_SECRET_KEY>
Default region name [us-west-2]: 
Default output format [json]: 
```
- In the terminal, move to `sample-python-api/server`. Follow this [instruction](https://www.codingforentrepreneurs.com/blog/serverless-django-with-zappa-on-aws-lambda) to deploy the simple app. 

My "Hello World!" app can be found at "https://p5jf26ld0b.execute-api.us-west-2.amazonaws.com/dev".

The actual app we want to deploy located at `sample-python-api`, however I haven't figured out how to connect to the server yet. Current error is:
```sh
Error while connecting to PostgreSQL FATAL: password authentication failed for user "postgre"
FATAL: password authentication failed for user "postgre"
```

## Built With
- Flask: a micro web framework written in Python

## Author
- Ho Xuan Vinh
## References:
- README template from [Billie Thompson](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2).
- Useful blog series of [Abu Ashraf Masnun](http://polyglot.ninja/rest-apis-concepts-applications/) about Flask and Python.
- Setup PostgreSQL on server: [silviomoreto](https://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi).
- Setup virtual environment with Python3.6 installed: [Casey Labs](https://www.caseylabs.com/how-to-create-a-python-3-6-virtual-environment-on-ubuntu-16-04/).
- Prepare AWS IAM User, Role, and Policies for Zappa and deploy: [Justin Mitchell](https://www.codingforentrepreneurs.com/blog/serverless-django-with-zappa-on-aws-lambda).