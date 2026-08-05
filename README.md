# GitLab CI/CD Pipeline – Automated Docker Deployment to AWS EC2

An end-to-end GitLab CI/CD pipeline that builds, tests, containerizes, and deploys a Flask
web application to an AWS EC2 instance, with images stored in AWS ECR and health
monitored via CloudWatch.

## Architecture

```
Git Push (main) → GitLab CI/CD
  → build (install deps)
  → test (pytest)
  → dockerize (build image, push to ECR)
  → deploy (SSH into EC2, pull latest image, restart container)
```

## Tech Stack

- **App**: Python 3.11, Flask
- **CI/CD**: GitLab CI/CD (`.gitlab-ci.yml`)
- **Container Registry**: AWS ECR
- **Compute**: AWS EC2 (Ubuntu, Docker installed)
- **Monitoring**: AWS CloudWatch (CPU/memory/health alarms) + SNS email alerts

## Pipeline Stages

| Stage | What it does |
|---|---|
| `build` | Installs Python dependencies |
| `test` | Runs `pytest` unit tests against the Flask app |
| `dockerize` | Builds the Docker image and pushes it to AWS ECR (tagged with commit SHA + `latest`) |
| `deploy` | SSHes into the EC2 instance, pulls the new image from ECR, stops the old container, and starts the new one |

## Local Development

```bash
pip install -r requirements.txt
python app.py
# visit http://localhost:5000
```

## Run with Docker

```bash
docker build -t flask-devops-app .
docker run -p 5000:5000 flask-devops-app
```

## Run Tests

```bash
pytest test_app.py -v
```

## Required GitLab CI/CD Variables

Set these under **Project → Settings → CI/CD → Variables**:

| Variable | Description |
|---|---|
| `AWS_ACCOUNT_ID` | Your 12-digit AWS account ID |
| `AWS_REGION` | e.g. `ap-south-1` |
| `ECR_REPOSITORY_NAME` | Name of the ECR repo (e.g. `flask-devops-app`) |
| `AWS_ACCESS_KEY_ID` | IAM user access key (scoped to ECR push only) |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `EC2_HOST` | Public IP or DNS of the EC2 instance |
| `EC2_USER` | e.g. `ubuntu` |
| `EC2_SSH_PRIVATE_KEY` | Private key (PEM) to SSH into EC2, marked "Protected" + "Masked" (if possible) |

## Monitoring

CloudWatch alarms are configured for:
- EC2 CPU Utilization > 80%
- Memory usage (via CloudWatch agent)
- Container/app health check failures

Alarms notify via an SNS topic subscribed to email.

## Author

Narendra Deshmukh
AWS & Devops Enginner