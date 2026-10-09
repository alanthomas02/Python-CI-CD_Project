# Python CI/CD Pipeline on AWS EC2

A hands-on CI/CD project that automates testing and deployment of a Python web application to an AWS EC2 instance using GitHub Actions and AWS Systems Manager (SSM).

## Project Overview

This project demonstrates how to build a basic CI/CD pipeline that tests application code and automatically deploys changes to an EC2 instance when code is pushed to the `main` branch.

The deployment uses GitHub Actions with OpenID Connect (OIDC) to authenticate with AWS without storing long-lived AWS access keys in GitHub.

## Architecture

```text
Developer pushes code to GitHub
              |
              v
       GitHub Actions
              |
              v
      Python CI checks
      - Syntax validation
      - Unit tests
              |
              v
      AWS authentication
       through OIDC
              |
              v
      AWS Systems Manager
          Run Command
              |
              v
          AWS EC2
      - Pull latest code
      - Restart systemd service
      - Run health check
```

## Technologies Used

* **Python** — simple HTTP application and unit tests
* **Git and GitHub** — source code management
* **GitHub Actions** — continuous integration and deployment workflow
* **AWS EC2** — application hosting
* **AWS Systems Manager (SSM)** — remote deployment without SSH
* **AWS IAM and OIDC** — secure GitHub Actions authentication
* **Linux and systemd** — application service management
* **Bash** — deployment automation

## Application Features

* Serves a homepage with a text response.
* Provides a `/health` endpoint that returns a JSON health status.
* Includes automated unit tests for the health endpoint.
* Runs as a systemd service on the EC2 instance.
* Automatically deploys changes pushed to the `main` branch.

## CI/CD Workflow

### Continuous Integration

On pushes and pull requests targeting `main`, GitHub Actions:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Validates Python syntax.
4. Runs the unit tests.

### Continuous Deployment

After successful tests, pushes to `main` trigger the deployment job:

1. Authenticates to AWS using GitHub OIDC.
2. Sends a deployment command through AWS Systems Manager.
3. Pulls the latest code from GitHub on EC2.
4. Restarts the `python-cicd` systemd service.
5. Checks the service status and application health endpoint.

Deployment is configured to run only for pushes to `main`, not pull requests.

## Application Endpoints

| Endpoint  | Purpose                            |
| --------- | ---------------------------------- |
| `/`       | Returns the application homepage   |
| `/health` | Returns application health as JSON |

Example health response:

```json
{
  "status": "healthy",
  "application": "python-cicd-ec2"
}
```

The application listens on port `8000`. Browser access depends on the EC2 security group and network configuration.

## AWS Configuration

The deployment requires:

* An EC2 instance with the application repository cloned.
* A systemd service named `python-cicd`.
* An EC2 IAM role configured for Systems Manager.
* An AWS IAM role that trusts the GitHub repository's OIDC identity.
* A GitHub repository variable named `AWS_ROLE_ARN`.
* A GitHub repository variable named `EC2_INSTANCE_ID`.

The EC2 instance must be managed by Systems Manager and have access to retrieve the repository from GitHub.

## Security Considerations

* Uses OIDC instead of long-lived AWS access keys for GitHub Actions.
* Restricts the AWS role trust policy to the intended GitHub repository and branch.
* Uses IAM permissions for the deployment operations.
* Uses Systems Manager instead of requiring SSH access for automated deployments.
* Restricts direct application-port access through the EC2 security group during testing.

## What I Learned

* Building CI workflows with GitHub Actions.
* Automating deployments to Linux servers.
* Configuring AWS IAM roles and GitHub OIDC authentication.
* Deploying through AWS Systems Manager.
* Managing Python applications with systemd.
* Troubleshooting Git permissions, IAM trust policies, and deployment failures.
* Verifying deployments with HTTP health checks.

## Future Improvements

* Add test coverage reporting and linting.
* Build and deploy a Docker image.
* Configure Nginx as a reverse proxy.
* Enable HTTPS using a domain and TLS certificate.
* Add application logging and monitoring.
* Introduce deployment rollback and versioning.

## Author

**Alan Thomas**

[GitHub Profile](https://github.com/alanthomas02)
