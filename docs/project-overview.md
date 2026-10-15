# CloudTask — Project Overview

## 1. Project Introduction

CloudTask is a practical Azure cloud project that demonstrates how to deploy a Python backend application to Microsoft Azure and integrate it with cloud services for data storage, file management, security, monitoring, and resource governance.

The application is built using Python and Flask and is hosted on Azure App Service. It exposes REST API endpoints that allow clients to interact with task-management data stored in an Azure SQL Database.

The project also integrates Azure Blob Storage for file attachments, Azure Queue Storage for task-related messages, and Azure Key Vault for securely retrieving secrets using Managed Identity.

In addition to application hosting and data integration, CloudTask demonstrates Azure administration concepts such as Role-Based Access Control (RBAC), Azure Policy, resource locks, cost monitoring, Application Insights, and Azure Monitor alerts.

The primary goal is to gain hands-on experience with Azure services and understand how application development connects with cloud infrastructure and administration.

## 2. What Does CloudTask Do?

CloudTask provides backend API functionality for a task-management application.

The application includes four main database tables:

- **Users:** Stores user-related information.
- **Projects:** Stores project-related information.
- **Tasks:** Stores task-related information.
- **Comments:** Stores comments associated with application records.

The Flask application exposes REST API endpoints through which clients can send HTTP requests and receive responses.

The implemented API functionality includes:

- Retrieving user information and creating users.
- Retrieving project information and creating projects.
- Retrieving tasks and creating new tasks.
- Updating existing tasks and deleting tasks.
- Uploading files as task attachments.
- Sending task-related messages to Azure Queue Storage.
- Checking application health through dedicated health endpoints.
- Testing Key Vault secret retrieval through a dedicated endpoint.

The API communicates with Azure SQL Database to execute the application's database queries. Uploaded attachments are stored in Azure Blob Storage, while task-related messages are sent to Azure Queue Storage.

**Important:** CloudTask is a backend REST API project, not a complete frontend task-management application. The documented functionality reflects the implemented API endpoints and integrations; it does not imply that every database table has a complete set of CRUD endpoints.

## 3. High-Level Architecture

The application follows a simple cloud-based architecture in which the Python backend is hosted on Azure App Service and connects to other Azure services as required.

### Application Flow

1. A client sends an HTTP request to the CloudTask REST API.
2. Azure App Service hosts and runs the Python Flask application.
3. The application processes the request and interacts with Azure SQL Database when database operations are required.
4. When a task attachment is uploaded, the application sends the file to Azure Blob Storage.
5. When task-related processing messages are required, the application sends messages to Azure Queue Storage.
6. The application retrieves the required secret from Azure Key Vault using Managed Identity and the configured access permissions.
7. Application Insights and Azure Monitor support application monitoring, troubleshooting, and alerting.
8. Azure governance and management features help control access, enforce resource configuration requirements, protect resources, and monitor costs.

These steps describe the overall design. The specific services involved depend on the API endpoint being called.

### Main Azure Components

**Azure App Service**

Hosts the Python Flask REST API without requiring the project to manage the underlying virtual machines.

**Azure SQL Database**

Provides managed relational database storage for the Users, Projects, Tasks, and Comments tables.

**Azure Blob Storage**

Stores task attachment files uploaded through the API.

**Azure Queue Storage**

Stores task-related messages for asynchronous processing.

**Azure Key Vault**

Stores secrets that the application needs to retrieve securely.

**Managed Identity**

Provides an Azure-managed identity that the application can use to authenticate to supported Azure services without embedding credentials in application code.

**Application Insights**

Collects application telemetry to help investigate failures and understand application behaviour.

**Azure Monitor**

Supports monitoring and alert rules, including the configured HTTP 5xx error alert.

**Azure RBAC and Azure Policy**

RBAC controls access to Azure resources, while Azure Policy evaluates resource configurations against assigned governance requirements.

**Resource Locks and Cost Management**

Resource locks help protect resources against accidental deletion. Cost Management helps review Azure spending and configured budget information.

## 4. Azure Concepts Demonstrated

| Azure service or concept | Purpose in CloudTask |
|---|---|
| Azure App Service | Hosting the Python Flask REST API |
| Azure SQL Database | Storing relational application data |
| Azure Blob Storage | Storing uploaded task attachments |
| Azure Queue Storage | Storing task-related processing messages |
| Azure Key Vault | Secure storage and retrieval of secrets |
| Managed Identity | Identity-based authentication to supported Azure services |
| Azure RBAC | Managing resource access permissions |
| Azure Policy | Evaluating resource compliance with governance requirements |
| Application Insights | Collecting application telemetry and investigating failures |
| Azure Monitor | Monitoring application behaviour and configuring alerts |
| Resource Locks | Protecting Azure resources against accidental deletion |
| Cost Management | Reviewing and managing cloud expenditure |
| Azure Advisor | Reviewing recommendations for Azure resources |

## 5. Security and Governance

Security and governance are important parts of the CloudTask implementation.

The project uses Azure Key Vault to manage secrets and Managed Identity to support secure authentication. Azure RBAC assignments control permissions for accessing Azure resources, including the required Key Vault access.

Azure Policy is used to evaluate resource compliance with the project's governance requirements, including tag-related requirements.

A resource lock is configured to help protect the project resources from accidental deletion. Azure Monitor alerting and Application Insights support the identification and investigation of application errors.

Cost Management and Azure Advisor are used to explore cloud cost information and resource recommendations.

These features demonstrate how an Azure-hosted application can be managed beyond simply deploying its application code.

## 6. Monitoring and Troubleshooting

CloudTask integrates Application Insights and Azure Monitor to demonstrate application monitoring.

The monitoring setup includes application telemetry, failure investigation, metrics, a health-check web test, and an HTTP 5xx alert rule.

HTTP 5xx responses indicate server-side HTTP errors. The configured alert rule helps identify matching failures so that they can be investigated.

Monitoring results and alert notifications provide evidence of the configured monitoring capabilities. They do not necessarily indicate that the application is continuously experiencing errors.

## 7. Azure Function — Development Scope

An Azure Functions component was developed locally to explore serverless application development.

However, the Function was not deployed to Azure as part of this project.

Therefore, Azure Functions is included only as a local development component and is not part of the deployed Azure architecture.

## 8. Project Scope

CloudTask focuses on the following areas:

- Developing a Python Flask REST API.
- Deploying a backend application to Azure App Service.
- Connecting the application to Azure SQL Database.
- Integrating Blob Storage and Queue Storage.
- Managing secrets through Azure Key Vault.
- Configuring Managed Identity and Azure RBAC.
- Exploring Azure Policy and resource compliance.
- Configuring application monitoring and Azure Monitor alerts.
- Applying resource protection and reviewing cloud costs.
- Documenting the deployed architecture and implementation evidence.

The project does not include a deployed Azure Functions application or a separately deployed virtual machine.

## 9. Learning Outcomes

By completing CloudTask, the project demonstrates practical experience in three areas.

### Software Development

- Building a REST API using Python and Flask.
- Working with HTTP methods, request handling, and JSON responses.
- Connecting application code to a relational database.
- Integrating file uploads and queue messaging.

### Azure Cloud Engineering

- Deploying an application to Azure App Service.
- Connecting a backend application to managed Azure services.
- Using identity-based access to retrieve secrets.
- Understanding how application components interact in a cloud environment.

### Azure Administration

- Configuring access permissions using RBAC.
- Evaluating governance requirements using Azure Policy.
- Monitoring application health and failures.
- Creating and reviewing alert rules.
- Protecting resources with locks.
- Reviewing costs and Azure Advisor recommendations.

## 10. Project Summary

CloudTask is a hands-on Azure learning project that connects backend software development with cloud engineering and administration.

It demonstrates how a Python REST API can be hosted on Azure App Service and integrated with managed database, storage, security, and monitoring services.

The project also provides practical exposure to identity management, access control, governance, resource protection, and cost awareness.

Together, these components provide a foundation for understanding how to deploy, secure, monitor, and manage a backend application in Microsoft Azure.