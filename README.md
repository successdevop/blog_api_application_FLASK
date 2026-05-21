# blog_api_application_FLASK
A RESTful blog API built with Flask, featuring user authentication, post management, and comment functionality.

## Tech Stack

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Migrate** - Database migrations
- **Marshmallow-SQLAlchemy** - Object serialization/deserialization
- **Werkzeug** - Password hashing

## Features

### Authentication
- User registration with email validation
- Secure password hashing (min 8 chars, 1 uppercase, 1 number)
- JWT-based login system
- Password reset functionality

### Posts
- Create, read, update, delete posts
- Pagination support (20 items per page, max 100)
- Title (max 200 chars) and body (min 10 chars) validation
- Author-only edit/delete permissions

### Comments
- Add comments to posts
- Edit/delete own comments
- Paginated comment listing
- Cascade delete when post is removed

## Database Schema

### Users Table
| Column | Type | Constraints |
|--------|------|-------------|
| user_id | String(20) | Primary Key, Auto-generated |
| user_name | String(64) | Unique, Indexed |
| email | String(120) | Unique, Indexed |
| password | String(225) | Hashed |

### Posts Table
| Column | Type | Constraints |
|--------|------|-------------|
| post_id | String(20) | Primary Key |
| title | String(200) | Required |
| body | Text | Required |
| created_at | DateTime | Auto timestamp |
| author_id | String(20) | Foreign Key → users.user_id |

### Comments Table
| Column | Type | Constraints |
|--------|------|-------------|
| comment_id | String(20) | Primary Key |
| body | String(255) | Required |
| timestamp | DateTime | Auto timestamp |
| author_id | String(20) | Foreign Key → users.user_id |
| post_id | String(20) | Foreign Key → posts.post_id |

## API Endpoints

### Authentication (`/register`, `/login`, `/auth`)

#### POST `/register`

#### POST `/login`

#### POST `/auth`

### Posts

- Posts (/posts)
- Method	Endpoint	Auth Required	Description
- POST	/posts	Yes	Create new post
- GET	/posts	No	List all posts (paginated)
- GET	/posts/{post_id}	No	Get single post
- PATCH	/posts/{post_id}	Yes (author)	Update post
- DELETE	/posts/{post_id}	Yes (author)	Delete post


### src/
- ├── model/           # Database models (User, Post, Comments)
- ├── schema/          # Marshmallow schemas
- ├── controllers/     # Route blueprints
- ├── services/        # Business logic (PostService, Auth)
- ├── repo/           # Database configuration
- ├── utils/          # Helper functions
- └── config.py       # Configuration settings

### Security Features
- Passwords hashed using Werkzeug's generate_password_hash

- JWT tokens with user identity claims

- Input validation and sanitization

- SQL injection protection via SQLAlchemy ORM

- Email format validation

- Password strength requirements

flask create_db    # Create all database tables
flask drop_db      # Drop all database tables
flask db migrate   # Create migration
flask db upgrade   # Apply migrations