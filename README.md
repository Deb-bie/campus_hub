
# Campus Hub 🎓

A web application that helps college students discover, manage, and attend campus events. The platform displays upcoming events, allows students to track attendance, and provides event organizers with tools to promote and monitor event engagement.



## ✨ Features

- Authentication & Authorization
- Event Listings – Browse upcoming campus events with event details.
- Attendance Tracking – View the number of attendees per event.
- Notifications – Real-time updates for event reminders and changes.
- User Profiles – Manage personal profiles and track attended events.
- Event Organizer Dashboard – Create, edit, and monitor events.
- Search & Filters – Easily find events by category, date, or location.


## 🛠️ Tech Stack

**Frontend:** Angular, TailwindCSS

**Backend:**  Springboot, Flask, FastAPI, Node, Express


## 🏗️ Architecture

### 📂 Microservices
- API Gateway: Central entry point with routing and authentication

- Auth Service: Handles user registration, log in, authentication and authorization.

- Event Service: Event CRUD operations and management

- User Profile Service: Manages user profiles and personal data.

- Notification Service: Manages real-time and email notifications.

- Search Service: Indexes and searches events using Elasticsearch.


### 📊 Data Layer
- PostgresQL: Primary relational database for structured data

- MongoDB: Document store for notifications and logs

- Redis: Caching layer for performance optimization

- Elasticsearch: Full-text search and event indexing

- Object Storage: Media files and user uploads
## Installation & Setup

**Prerequisites**
- Node.js 24+
- Python 3.12
- Java 21
- PostgreSQL
- Redis
- Kafka & Zookeeper
- Elasticsearch 
- Docker & Docker Compose

## Run Locally

Clone the project

```bash
  git clone https://github.com/Deb-bie/campus_hub.git
```

Go to the project directory

```bash
  cd campus_hub
```

Setup Environment Variables

- Duplicate ``` .env.example ``` files in each service and fill in the required values.

Start services with Docker Compose

```bash
docker-compose up --build
```

## 🧑‍💻 Project Structure

```
campus_hub/
├── services/
│   ├── api-gateway/          # API Gateway service
│   ├── auth-service/         # Authentication service
│   ├── event-service/        # Event management service
│   ├── user-service/         # User profile service
│   ├── notification-service/ # Notification service
│   └── search-service/       # Search service
├── .github/                  # Github actions
│       └── workflows
├── .env
└── docker-compose.yml        # Docker compose

```
## 📝 Key Functionalities I Built

- Built microservices and ensured clean inter-service communication via **REST APIs** and **Kafka Events**.

- Integrated **Elasticsearch** for efficient event search functionality.

- Implemented **Kafka event-driven workflows** to trigger notifications and sync services.

- Containerized the entire application stack using **Docker Compose** for easy deployment.


## 🔗 Connect With Me

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/deborah-asamoah/)
