Docker Multi-Tier Application (Frontend + Backend + AWS RDS)

This project is a 3-tier web application deployed on AWS EC2 using Docker Compose.

Frontend: Nginx
Backend: Flask (Python REST API)
Database: AWS RDS MySQL


Architecture:

User Browser
   |
   |  HTTP :80
   v
Nginx (Frontend Container)
   |
   |  /api/* -> proxy
   v
Flask API (Backend Container)
   |
   |  MySQL :3306
   v
AWS RDS MySQL


Features:

- View students from database
- Add new student
- Update student name
- Delete student
- Backend connects to AWS RDS using environment variables
- Fully containerized using Docker Compose


Tech Stack:

- AWS EC2
- AWS RDS (MySQL)
- Docker
- Docker Compose
- Nginx
- Flask (Python)


How to Run:

1) Clone the repository

git clone https://github.com/Tanu-25995/docker-multitier-rds-app.git
cd docker-multitier-rds-app


2) Configure database in docker-compose.yml

Open the file docker-compose.yml and update these values:

DB_HOST
DB_USER
DB_PASSWORD
DB_NAME


3) Start the application

docker compose up -d --build


4) Open in browser

http://<EC2_PUBLIC_IP>/


Database Setup (First Time Only):

If you get this error: Unknown database appdb

Run:

sudo apt update -y
sudo apt install -y mysql-client
mysql -h <RDS_ENDPOINT> -u <DB_USER> -p

Then inside MySQL run:

CREATE DATABASE appdb;
EXIT;


Notes:

- Frontend and backend run in Docker containers.
- Database is hosted on AWS RDS.
- Docker Compose is used to run all services together.
