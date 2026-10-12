# CloudTask — Azure Cloud Architecture & Web API

A practical Azure cloud deployment demonstrating multi-tier application hosting, managed relational data, secrets retrieval via Managed Identity, asynchronous queue messaging, monitoring with alert rules, and resource governance. Designed as a portfolio implementation aligned with Microsoft Azure Fundamentals (AZ-900).

---

## 1. Project Overview

CloudTask bridges backend software engineering and cloud operations. The project deploys a Python Flask REST API to **Azure App Service**, connects to **Azure SQL Database**, manages files and message queues via an **Azure Storage Account**, retrieves configuration secrets from **Azure Key Vault** using a **Managed Identity**, and enforces enterprise governance in the **CloudTask-RG** resource group.

---

## 2. Architecture & Request Flow

![CloudTask Azure Architecture](docs/architecture.png)[cite: 1]

1. **Client Ingress:** Web clients communicate over HTTPS (Port 443).
2. **Compute Layer:** **Azure App Service (`cloudtask-api`)** runs the Python Flask REST API.
3. **Identity & Secrets:** App Service queries **Azure Key Vault** using system-assigned **Managed Identity** to retrieve connection secrets.
4. **Data Layer:**
   * **Azure SQL Database (`CloudTaskDB`):** Manages relational application state over a secure SQL connection.
   * **Azure Storage Account:**
     * **Private Blob Storage (`task-attachments`):** Stores file attachments via blob storage operations[cite: 1].
     * **Storage Queue (`task-processing`):** Decouples asynchronous operations via queue messaging[cite: 1].
5. **Observability:** Telemetry and execution logs stream directly to **Azure Monitor / Application Insights**[cite: 1].
6. **Background Worker Scope:** Background queue processing was developed and validated locally; Azure deployment of Azure Functions is planned for a future phase[cite: 1].

---

## 3. Technology Stack & Azure Services

| Service / Technology | Resource / Component Name | Role in Solution |
| :--- | :--- | :--- |
| **Compute** | Azure App Service (`cloudtask-api`)[cite: 1] | Hosts the live Python Flask REST API runtime[cite: 1]. |
| **Relational Database** | Azure SQL Database (`CloudTaskDB`)[cite: 1] | Stores relational task records via managed SQL connection[cite: 1]. |
| **Object Storage** | Private Blob Storage (`task-attachments`)[cite: 1] | Stores task file attachments securely[cite: 1]. |
| **Message Queue** | Storage Queue (`task-processing`)[cite: 1] | Decouples task messaging workflows[cite: 1]. |
| **Secrets Management** | Azure Key Vault[cite: 1] | Centralizes connection strings and runtime credentials[cite: 1]. |
| **Identity & Access** | Azure Managed Identity & Azure RBAC[cite: 1] | Enforces zero-credential authentication and least-privilege roles[cite: 1]. |
| **Monitoring** | Azure Monitor & Application Insights[cite: 1] | Live telemetry tracking and active operational alerts[cite: 1]. |
| **Governance** | Azure Policy, Resource Locks, Resource Tags[cite: 1] | Enforces tag compliance and accidental deletion locks[cite: 1]. |
| **Cost & Advisory** | Azure Cost Management, Budgets, Azure Advisor[cite: 1] | Budget threshold alerting and operational recommendations[cite: 1]. |

---

## 4. Application Endpoints

| Method | Endpoint | Description | Verification Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/`[cite: 1] | Base index returning application health and runtime status[cite: 1]. | Verified[cite: 1] |
| `GET` | `/api/health`[cite: 1] | Liveness probe verifying application process availability[cite: 1]. | Verified[cite: 1] |
| `GET` | `/api/keyvault-test`[cite: 1] | Validates Managed Identity authentication and Key Vault secret access[cite: 1]. | Verified[cite: 1] |
| `GET` | `/tasks` | Retrieves active task records from Azure SQL Database. | Roadmap / CRUD |
| `POST` | `/tasks` | Creates task and posts a payload to `task-processing` queue[cite: 1]. | Roadmap / CRUD |

---

## 5. Security, Monitoring & Governance

* **Zero-Secret Codebase:** App Service retrieves secrets via a system-assigned Managed Identity from Azure Key Vault, preventing credentials in version control[cite: 1].
* **Access Control:** Azure Role-Based Access Control (RBAC) scopes permissions strictly at the resource group level[cite: 1].
* **Resource Immutability:** A `CanNotDelete` Resource Lock on `CloudTask-RG` prevents accidental resource deletion during maintenance[cite: 1].
* **Resource Tagging & Policies:** Standardized tags (`Project: CloudTask`, `Environment: Dev`) are enforced across resources[cite: 1].
* **Operational Alert Rules:** Azure Monitor Application Insights tracks reliability through configured rules[cite: 1]:
  * `CloudTask-HTTP5xx-Alert` (triggers on HTTP 5xx server errors)[cite: 1]
  * `cloudtask-health-test-cloudtask-api-insights` (tracks health endpoint synthetic probe failures)[cite: 1]
* **Cost Governance:** Budget notifications configured (`Budget - cost exceeded threshold`) to track consumption against spending limits[cite: 1].

---

## 6. Verification Evidence
Artifacts and logs validating the live deployment are cataloged in screenshots/:

01-resource-group-overview.png — Deployed services inside CloudTask-RG showing tag definitions.

02-api-health-keyvault-response.png — Verified HTTP 200 responses for /api/health and /api/keyvault-test.

03-sql-database-connection.png — Active CloudTaskDB deployment and SQL query metrics.

04-storage-blob-queue.png — Created task-attachments blob container and task-processing queue.

05-alerts-insights.png — Configured alert rules (CloudTask-HTTP5xx-Alert and health test probes).

06-governance-budget.png — Resource locks, policy compliance checks, and budget threshold configuration.

