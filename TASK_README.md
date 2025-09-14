# Task Management System Documentation

This project now includes a comprehensive task management system with user assignment, cadence tracking, and completion tracking.

## Task Model

The Task model includes the following fields:

- **id**: Primary key (auto-generated)
- **title**: Task title (required, max 255 characters)
- **description**: Task description (optional, max 1000 characters)
- **cadence**: Task frequency (required, max 100 characters)
  - Examples: "daily", "weekly", "monthly", "custom", "every 2 days"
- **last_completed**: Last completion timestamp (optional)
- **assigned_to**: Foreign key to User table (required)
- **created_at**: Creation timestamp (auto-generated)
- **updated_at**: Last update timestamp (auto-generated)

## API Endpoints

### Task Management Endpoints

All task endpoints require authentication (Bearer token).

#### Create Task
- **POST** `/api/tasks`
- **Body**: `TaskCreate` schema
- **Response**: `TaskRead` schema
- **Description**: Create a new task assigned to a user

#### Get All Tasks
- **GET** `/api/tasks`
- **Query Parameters**: 
  - `skip`: Number of tasks to skip (default: 0)
  - `limit`: Maximum number of tasks to return (default: 100)
- **Response**: List of `TaskRead` schemas
- **Description**: Get all tasks (paginated)

#### Get My Tasks
- **GET** `/api/tasks/my`
- **Response**: List of `TaskRead` schemas
- **Description**: Get tasks assigned to the current authenticated user

#### Get Task by ID
- **GET** `/api/tasks/{task_id}`
- **Response**: `TaskRead` schema
- **Description**: Get a specific task by ID

#### Update Task
- **PUT** `/api/tasks/{task_id}`
- **Body**: `TaskUpdate` schema
- **Response**: `TaskRead` schema
- **Description**: Update an existing task

#### Complete Task
- **PATCH** `/api/tasks/{task_id}/complete`
- **Body**: `TaskComplete` schema
- **Response**: `TaskRead` schema
- **Description**: Mark a task as completed (only by assigned user)

#### Delete Task
- **DELETE** `/api/tasks/{task_id}`
- **Response**: Success message
- **Description**: Delete a task

## Usage Examples

### 1. Create a Task

```bash
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Daily Standup",
    "description": "Attend daily team standup meeting",
    "cadence": "daily",
    "assigned_to": 1
  }'
```

### 2. Get My Tasks

```bash
curl -X GET "http://localhost:8000/api/tasks/my" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. Complete a Task

```bash
curl -X PATCH "http://localhost:8000/api/tasks/1/complete" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "completed_at": "2025-01-14T10:30:00Z"
  }'
```

### 4. Update a Task

```bash
curl -X PUT "http://localhost:8000/api/tasks/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Daily Standup",
    "description": "Updated description",
    "cadence": "weekdays"
  }'
```

## Database Schema

### Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    cadence VARCHAR(100) NOT NULL,
    last_completed DATETIME,
    assigned_to INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);

CREATE INDEX ix_tasks_title ON tasks(title);
```

## Cadence Examples

The `cadence` field supports various formats:

- **"daily"** - Every day
- **"weekly"** - Every week
- **"monthly"** - Every month
- **"weekdays"** - Monday through Friday
- **"every 2 days"** - Every 2 days
- **"every 3 weeks"** - Every 3 weeks
- **"custom"** - Custom schedule (handled by application logic)

## Security Features

1. **Authentication Required**: All task endpoints require valid JWT tokens
2. **User Assignment Validation**: Tasks can only be assigned to existing users
3. **Completion Authorization**: Only the assigned user can mark a task as completed
4. **Data Validation**: All input data is validated using Pydantic schemas

## Error Handling

The API returns appropriate HTTP status codes:

- **200**: Success
- **201**: Created
- **400**: Bad Request (validation errors, user not found)
- **401**: Unauthorized (invalid or missing token)
- **403**: Forbidden (trying to complete someone else's task)
- **404**: Not Found (task or user not found)

## Migration

To apply the task table migration:

```bash
alembic upgrade head
```

This will create the tasks table with proper foreign key relationships to the users table.

## Integration with Authentication

The task system integrates seamlessly with the existing authentication system:

1. All task operations require authentication
2. Tasks are linked to users via foreign key relationships
3. Users can only complete tasks assigned to them
4. The system tracks who created and last modified each task

## Future Enhancements

Potential future features:

1. **Task Categories**: Add category/tag system
2. **Due Dates**: Add due date tracking
3. **Recurring Tasks**: Automatic task regeneration based on cadence
4. **Task Dependencies**: Link tasks that depend on others
5. **Notifications**: Email/SMS reminders for overdue tasks
6. **Task Templates**: Predefined task templates for common activities
7. **Bulk Operations**: Bulk create, update, or delete tasks
8. **Task Analytics**: Completion rates, productivity metrics
