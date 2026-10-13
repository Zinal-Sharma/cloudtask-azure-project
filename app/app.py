#Flask REST API

import os

from azure.monitor.opentelemetry import configure_azure_monitor

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor()

from flask import Flask, request, jsonify
from database import get_connection
from storage import upload_file
from azure_queue import send_task_message
from keyvault import get_secret

app = Flask(__name__)


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.route("/")
def home():
    return "CloudTask API is running!"


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "application": "CloudTask",
        "service": "REST API"
    })


# ---------------------------------------------------------
# USERS
# ---------------------------------------------------------

@app.route("/api/users", methods=["GET"])
def get_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Id, Name, Email, CreatedDate
        FROM Users
        ORDER BY Id
    """)

    rows = cursor.fetchall()

    users = []

    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "createdDate": row[3].isoformat()
        })

    conn.close()

    return jsonify(users)


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Id, Name, Email, CreatedDate
        FROM Users
        WHERE Id = ?
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "createdDate": row[3].isoformat()
    })


@app.route("/api/users", methods=["POST"])
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "error": "name and email are required"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Users (Name, Email)
        OUTPUT INSERTED.Id
        VALUES (?, ?)
    """, (name, email))

    new_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({
        "id": new_id,
        "name": name,
        "email": email
    }), 201


# ---------------------------------------------------------
# PROJECTS
# ---------------------------------------------------------

@app.route("/api/projects", methods=["GET"])
def get_projects():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Id, Name, Description, CreatedDate
        FROM Projects
        ORDER BY Id
    """)

    rows = cursor.fetchall()

    projects = []

    for row in rows:
        projects.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "createdDate": row[3].isoformat()
        })

    conn.close()

    return jsonify(projects)


@app.route("/api/projects", methods=["POST"])
def create_project():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({
            "error": "name is required"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Projects (Name, Description)
        OUTPUT INSERTED.Id
        VALUES (?, ?)
    """, (name, description))

    new_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({
        "id": new_id,
        "name": name,
        "description": description
    }), 201


# ---------------------------------------------------------
# TASKS
# ---------------------------------------------------------

@app.route("/api/tasks", methods=["GET"])
def get_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Id,
            ProjectId,
            Title,
            Description,
            Status,
            AssignedTo,
            CreatedDate,
            DueDate
        FROM Tasks
        ORDER BY Id
    """)

    rows = cursor.fetchall()

    tasks = []

    for row in rows:

        task = {
            "id": row[0],
            "projectId": row[1],
            "title": row[2],
            "description": row[3],
            "status": row[4],
            "assignedTo": row[5],
            "createdDate": row[6].isoformat(),
            "dueDate": row[7].isoformat() if row[7] else None
        }

        tasks.append(task)

    conn.close()

    return jsonify(tasks)


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Id,
            ProjectId,
            Title,
            Description,
            Status,
            AssignedTo,
            CreatedDate,
            DueDate
        FROM Tasks
        WHERE Id = ?
    """, (task_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "id": row[0],
        "projectId": row[1],
        "title": row[2],
        "description": row[3],
        "status": row[4],
        "assignedTo": row[5],
        "createdDate": row[6].isoformat(),
        "dueDate": row[7].isoformat() if row[7] else None
    })


@app.route("/api/tasks", methods=["POST"])
def create_task():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    project_id = data.get("projectId")
    title = data.get("title")
    description = data.get("description")
    status = data.get("status", "Todo")
    assigned_to = data.get("assignedTo")
    due_date = data.get("dueDate")

    if not project_id or not title:
        return jsonify({
            "error": "projectId and title are required"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Tasks
        (
            ProjectId,
            Title,
            Description,
            Status,
            AssignedTo,
            DueDate
        )
        OUTPUT INSERTED.Id
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        project_id,
        title,
        description,
        status,
        assigned_to,
        due_date
    ))

    new_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({
        "id": new_id,
        "projectId": project_id,
        "title": title,
        "description": description,
        "status": status,
        "assignedTo": assigned_to,
        "dueDate": due_date
    }), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    assigned_to = data.get("assignedTo")
    due_date = data.get("dueDate")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Tasks
        SET
            Title = ?,
            Description = ?,
            Status = ?,
            AssignedTo = ?,
            DueDate = ?
        WHERE Id = ?
    """, (
        title,
        description,
        status,
        assigned_to,
        due_date,
        task_id
    ))

    if cursor.rowcount == 0:
        conn.close()

        return jsonify({
            "error": "Task not found"
        }), 404

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task updated successfully",
        "id": task_id
    })


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM Tasks
        WHERE Id = ?
    """, (task_id,))

    if cursor.rowcount == 0:
        conn.close()

        return jsonify({
            "error": "Task not found"
        }), 404

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Task deleted successfully",
        "id": task_id
    })


# ---------------------------------------------------------
# COMMENTS
# ---------------------------------------------------------

@app.route("/api/tasks/<int:task_id>/comments", methods=["GET"])
def get_comments(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.Id,
            c.TaskId,
            c.UserId,
            u.Name,
            c.CommentText,
            c.CreatedDate
        FROM Comments c
        INNER JOIN Users u
            ON c.UserId = u.Id
        WHERE c.TaskId = ?
        ORDER BY c.Id
    """, (task_id,))

    rows = cursor.fetchall()

    comments = []

    for row in rows:

        comments.append({
            "id": row[0],
            "taskId": row[1],
            "userId": row[2],
            "userName": row[3],
            "comment": row[4],
            "createdDate": row[5].isoformat()
        })

    conn.close()

    return jsonify(comments)


@app.route("/api/tasks/<int:task_id>/comments", methods=["POST"])
def create_comment(task_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    user_id = data.get("userId")
    comment_text = data.get("comment")

    if not user_id or not comment_text:
        return jsonify({
            "error": "userId and comment are required"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Comments
        (
            TaskId,
            UserId,
            CommentText
        )
        OUTPUT INSERTED.Id
        VALUES (?, ?, ?)
    """, (
        task_id,
        user_id,
        comment_text
    ))

    new_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({
        "id": new_id,
        "taskId": task_id,
        "userId": user_id,
        "comment": comment_text
    }), 201

#attachment/upload endpoint

@app.route("/api/tasks/<int:task_id>/attachments", methods=["POST"])
def upload_attachment(task_id):

    if "file" not in request.files:
        return jsonify({
            "error": "No file provided"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    try:
        # 1. Upload file to Blob Storage
        blob_name = upload_file(file)

        # 2. Put processing message into Azure Queue
        queue_result = send_task_message(
            task_id,
            blob_name
        )

        return jsonify({
            "message": "File uploaded and processing queued",
            "taskId": task_id,
            "fileName": blob_name,
            "queue": "task-processing",
            "queueMessageId": queue_result["message_id"]
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

#Keyvault endpoint 
@app.route("/api/keyvault-test", methods=["GET"])
def keyvault_test():
    try:
        secret = get_secret("CloudTaskTest1Secret")

        return jsonify({
            "status": "success",
            "message": "Key Vault access is working",
            "secretLength": len(secret)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500
    
# ---------------------------------------------------------
# APPLICATION START
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)