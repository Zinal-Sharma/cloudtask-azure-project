# CloudTask — Azure Cloud Architecture & Web API

A practical Azure cloud deployment demonstrating multi-tier application hosting, managed relational data, secrets retrieval via Managed Identity, asynchronous queue messaging, monitoring with alert rules, and resource governance.

---

## 1. Project Overview

CloudTask bridges backend software engineering and cloud operations. The project deploys a Python Flask REST API to **Azure App Service**, connects to **Azure SQL Database**, manages files and message queues via an **Azure Storage Account**, retrieves configuration secrets from **Azure Key Vault** using a **Managed Identity**, and enforces enterprise governance in the **CloudTask-RG** resource group.

---

## 2. Architecture & Request Flow


<img width="900" height="550" alt="architecture" src="https://github.com/user-attachments/assets/d27120a5-0ddc-47fb-a90a-5808e0800bce" />



1. **Client Ingress:** Web clients communicate over HTTPS (Port 443).
2. **Compute Layer:** **Azure App Service (`cloudtask-api`)** runs the Python Flask REST API.
3. **Identity & Secrets:** App Service queries **Azure Key Vault** using system-assigned **Managed Identity** to retrieve connection secrets.
4. **Data Layer:**
   * **Azure SQL Database (`CloudTaskDB`):** Manages relational application state over a secure SQL connection.
   * **Azure Storage Account:**
     * **Private Blob Storage (`task-attachments`):** Stores file attachments via blob storage operations.
     * **Storage Queue (`task-processing`):** Decouples asynchronous operations via queue messaging.
5. **Monitoring & Operations:** Telemetry and execution logs stream directly to **Azure Monitor / Application Insights**.
6. **Background Worker Scope:** Background queue processing was developed and validated locally; Azure deployment of Azure Functions is planned for a future phase.

---

## 3. Technology Stack & Azure Services

| Service / Technology | Resource / Component Name | Role in Solution |
| :--- | :--- | :--- |
| **Compute** | Azure App Service (`cloudtask-api`) | Hosts the live Python Flask REST API runtime. |
| **Relational Database** | Azure SQL Database (`CloudTaskDB`) | Stores relational task records via managed SQL connection. |
| **Object Storage** | Private Blob Storage (`task-attachments`) | Stores task file attachments securely. |
| **Message Queue** | Storage Queue (`task-processing`) | Decouples task messaging workflows. |
| **Secrets Management** | Azure Key Vault | Centralizes connection strings and runtime credentials. |
| **Identity & Access** | Azure Managed Identity & Azure RBAC | Enforces zero-credential authentication and least-privilege roles. |
| **Monitoring** | Azure Monitor & Application Insights | Live telemetry tracking and active operational alerts. |
| **Governance** | Azure Policy, Resource Locks, Resource Tags | Enforces tag compliance and accidental deletion locks. |
| **Cost & Advisory** | Azure Cost Management, Budgets, Azure Advisor | Budget threshold alerting and operational recommendations. |

---

## 4. Application Endpoints

| Category | Method | Endpoint | Description | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| Health | `GET` | `/` | Confirms that the CloudTask API is running. | Verified |
| Health | `GET` | `/api/health` | Returns the API health status and application information. | Verified |
| Users | `GET` | `/api/users` | Retrieves all users from Azure SQL Database. | Verified |
| Users | `GET` | `/api/users/{user_id}` | Retrieves a specific user by ID. | Verified |
| Users | `POST` | `/api/users` | Creates a new user using the provided name and email. | Verified |
| Projects | `GET` | `/api/projects` | Retrieves all projects from Azure SQL Database. | Verified |
| Projects | `POST` | `/api/projects` | Creates a new project with a name and optional description. | Verified |
| Tasks | `GET` | `/api/tasks` | Retrieves all tasks and their details. | Verified |
| Tasks | `GET` | `/api/tasks/{task_id}` | Retrieves a specific task by ID. | Verified |
| Tasks | `POST` | `/api/tasks` | Creates a task associated with a project. | Verified |
| Tasks | `PUT` | `/api/tasks/{task_id}` | Updates a task's title, description, status, assignee, and due date. | Verified |
| Tasks | `DELETE` | `/api/tasks/{task_id}` | Deletes a task by ID. | Verified |
| Comments | `GET` | `/api/tasks/{task_id}/comments` | Retrieves comments associated with a specific task. | Verified |
| Comments | `POST` | `/api/tasks/{task_id}/comments` | Adds a comment to a task for a specified user. | Verified |
| Attachments & Azure Storage | `POST` | `/api/tasks/{task_id}/attachments` | Uploads a task attachment to Azure Blob Storage and sends a processing message to Azure Queue Storage. | Verified |
| Azure Key Vault | `GET` | `/api/keyvault-test` | Checks Key Vault secret access and returns the secret's length without exposing its value. | Verified |

---

## 5. Security, Monitoring & Governance

* **Zero-Secret Codebase:** App Service retrieves secrets via a system-assigned Managed Identity from Azure Key Vault, preventing credentials in version control.
* **Access Control:** Azure Role-Based Access Control (RBAC) scopes permissions strictly at the resource group level.
* **Resource Immutability:** A `CanNotDelete` Resource Lock on `CloudTask-RG` prevents accidental resource deletion during maintenance.
* **Resource Tagging & Policies:** Standardized tags (`Project: CloudTask`, `Environment: Dev`) are enforced across resources.
* **Operational Alert Rules:** Azure Monitor Application Insights tracks reliability through configured rules:
  * `CloudTask-HTTP5xx-Alert` (triggers on HTTP 5xx server errors).
  * `cloudtask-health-test-cloudtask-api-insights` (tracks health endpoint synthetic probe failures).
* **Cost Governance:** Budget notifications configured (`Budget - cost exceeded threshold`) to track consumption against spending limits.

---

## 6. Verification Evidence
Screenshots validating the CloudTask Azure deployment, application functionality, monitoring, security, governance, and cost management are cataloged in screenshots/:

* **01-resource-group.png** — Shows the CloudTask-RG resource group and its deployed Azure resources.

* **02-app-service.png** — Documents the deployed CloudTask API hosted on Azure App Service.

* **03-health-endpoint.png** — Verifies the API health endpoint and confirms that the application responds successfully.

* **04-database-connectivity.png** — Demonstrates connectivity between the CloudTask API and Azure SQL Database.

* **05-storage-blob.png** — Shows the Azure Blob Storage configuration used for task attachments.

* **storage-blob-samplefile.png** — Provides evidence of a sample file uploaded to Blob Storage.

* **06-storage-queue.png** — Shows the Azure Queue Storage configuration for task-processing messages.

* **07-key-vault.png** — Documents the Azure Key Vault configuration for securely storing application secrets.

* **08-managed-identity.png** — Demonstrates the App Service managed identity configuration for Azure resource access.

* **09-RG-rbac.png** — Documents role-based access control (RBAC) assignments at the resource group level.

* **10-KV-rbac.png** — Shows Key Vault role assignments controlling access to secrets.

* **11-policy-compliance.png** — Provides evidence of Azure Policy assignment and policy compliance status.

* **12-policy-tag-compliance.png** — Documents compliance checks for the required resource tagging policy.

* **13-application-insights-overview.png** — Shows the Application Insights overview for monitoring application telemetry.

* **14-application-insights-failures.png** — Documents application failure monitoring and troubleshooting information.

* **15-azure-monitor-metrics.png** — Shows Azure Monitor metrics used to observe application and resource performance.

* **16-azure-monitor-alert-rule.png** — Documents the Azure Monitor alert rule configuration.

* **monitor-HTTP5xx-alert.png** — Provides evidence of the HTTP 5xx alert notification or triggered alert.

* **17-resource-lock.png** — Shows the resource lock configuration used to help prevent accidental resource deletion.

* **18-cost-management-analysis_charts.png** — Documents Azure Cost Management analysis charts used to review resource spending.

* **cost-alert.png** — Provides evidence of cost alert configuration for monitoring Azure spending.

* **19-azure-advisor.png** — Shows Azure Advisor recommendations for cost optimization, security, reliability, performance, and operational excellence.

* **The screenshots/sampledataapplication/** folder contains screenshots of JSON responses returned by the deployed CloudTask REST API for Users, Projects, Tasks, and Comments. These examples demonstrate how the API retrieves and returns application data stored in Azure SQL Database, including user details, project information, task descriptions, statuses, assignments, due dates, and task-related comments.

The screenshots provide evidence of the API's data retrieval functionality and illustrate the response structure returned by the implemented endpoints.

* **Repository Structure**

The repository is organized to separate the backend application, Azure Functions prototype, database scripts, documentation, and sample API responses.

* **app/** — Contains the Python Flask REST API, including application routes, database connectivity, Azure Key Vault integration, Blob Storage uploads, Queue Storage messaging, and the required dependencies.

* **docs/** — Contains the Azure architecture diagram (architecture.png) illustrating the application's cloud architecture.

* **functions/** — Contains the Azure Functions-related Python code and dependencies. The Functions code was developed locally and was not deployed to Azure.

* **sql/** — Contains schema.sql for the database schema and sample-data.sql for sample database records.

