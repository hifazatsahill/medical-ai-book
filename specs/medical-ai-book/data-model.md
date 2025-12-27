# Data Model: AI in Medical Laboratory Diagnostics – Interactive Book Development

## Core Entities

### User
**Description**: Represents a registered user of the interactive book system
**Fields**:
- `id`: UUID (Primary Key)
- `email`: String (Unique, Required)
- `name`: String (Required)
- `hashed_password`: String (Required)
- `created_at`: DateTime (Default: now)
- `updated_at`: DateTime (Default: now, Auto-update)
- `is_active`: Boolean (Default: true)

**Validation Rules**:
- Email must be valid email format
- Password must meet security requirements (min 8 chars, complexity)
- Email uniqueness enforced at database level

### UserProfile
**Description**: Stores user background information for personalization
**Fields**:
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key to User)
- `profession`: String (e.g., "pathologist", "lab technician", "student", "software engineer")
- `experience_level`: String (e.g., "beginner", "intermediate", "advanced")
- `technical_background`: String (e.g., "medical", "software", "mixed")
- `preferences`: JSON (Personalization settings)
- `created_at`: DateTime (Default: now)
- `updated_at`: DateTime (Default: now, Auto-update)

**Validation Rules**:
- User_id must reference existing user
- Profession must be from predefined list
- Experience_level must be from predefined list

### BookChapter
**Description**: Represents a chapter in the medical AI book
**Fields**:
- `id`: UUID (Primary Key)
- `title`: String (Required)
- `slug`: String (Unique, URL-friendly, Required)
- `content`: Text (Markdown format, Required)
- `content_urdu`: Text (Translated content in Urdu, Optional)
- `chapter_number`: Integer (Required)
- `word_count`: Integer (Auto-calculated)
- `reading_time`: Integer (Estimated minutes, Auto-calculated)
- `metadata`: JSON (Additional chapter metadata)
- `created_at`: DateTime (Default: now)
- `updated_at`: DateTime (Default: now, Auto-update)

**Validation Rules**:
- Title and slug must be unique
- Chapter_number must be positive
- Content must be valid Markdown

### UserProgress
**Description**: Tracks user progress through the book
**Fields**:
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key to User)
- `chapter_id`: UUID (Foreign Key to BookChapter)
- `progress_percentage`: Integer (0-100)
- `time_spent`: Integer (Seconds)
- `notes`: Text (Optional user notes)
- `bookmarks`: JSON (List of bookmarked positions)
- `last_accessed`: DateTime
- `completed`: Boolean (Default: false)
- `created_at`: DateTime (Default: now)
- `updated_at`: DateTime (Default: now, Auto-update)

**Validation Rules**:
- User_id and chapter_id combination must be unique
- Progress_percentage must be between 0-100

### ChatSession
**Description**: Represents a conversation session between user and RAG chatbot
**Fields**:
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key to User, Optional for anonymous sessions)
- `session_token`: String (For anonymous users)
- `created_at`: DateTime (Default: now)
- `updated_at`: DateTime (Default: now, Auto-update)
- `is_active`: Boolean (Default: true)

**Validation Rules**:
- Either user_id or session_token must be provided

### ChatMessage
**Description**: Individual message in a chat session
**Fields**:
- `id`: UUID (Primary Key)
- `session_id`: UUID (Foreign Key to ChatSession)
- `role`: String (Either "user" or "assistant")
- `content`: Text (Message content)
- `context_type`: String (Either "full_book" or "selected_text")
- `selected_text`: Text (If context_type is "selected_text", Optional)
- `timestamp`: DateTime (Default: now)
- `sources`: JSON (List of source references for RAG responses)

**Validation Rules**:
- Role must be either "user" or "assistant"
- Context_type must be valid enum value

### TranslationCache
**Description**: Caches translated content to improve performance and reduce API costs
**Fields**:
- `id`: UUID (Primary Key)
- `content_hash`: String (Hash of original content, Unique)
- `original_content`: Text (Original English content)
- `translated_content`: Text (Translated content)
- `source_language`: String (Default: "en")
- `target_language`: String (Default: "ur")
- `created_at`: DateTime (Default: now)
- `last_accessed`: DateTime

**Validation Rules**:
- Content_hash must be unique
- Source and target languages must be from supported list

## Relationships

- User → UserProfile (One-to-One)
- User → UserProgress (One-to-Many)
- BookChapter → UserProgress (One-to-Many)
- ChatSession → ChatMessage (One-to-Many)
- User → ChatSession (One-to-Many, Optional)

## State Transitions

### UserProgress
- Initial state: progress_percentage = 0, completed = false
- Active reading: progress_percentage updates based on reading position
- Completed: progress_percentage = 100, completed = true
- Reset: progress_percentage = 0, completed = false

### ChatSession
- Active: is_active = true
- Ended: is_active = false (session timeout or user action)