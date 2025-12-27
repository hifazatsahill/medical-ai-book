# Data Model: Integrated RAG Chatbot for Interactive Book

## Key Entities

### 1. Book Content
**Description**: Represents the text content of the book, divided into searchable segments with metadata.

**Fields**:
- `id` (UUID): Unique identifier for the book
- `title` (String): Title of the book
- `author` (String): Author of the book
- `content` (Text): Full text content of the book
- `metadata` (JSON): Additional book metadata (language, publication date, etc.)
- `created_at` (DateTime): Timestamp when the book was added to the system
- `updated_at` (DateTime): Timestamp when the book was last updated
- `chunks` (Array<BookChunk>): List of content chunks for the book

**Relationships**:
- One-to-many with BookChunk
- One-to-many with SessionData (via book_id)

**Validation Rules**:
- Title and author must not be empty
- Content must be properly formatted text
- Metadata must be valid JSON

### 2. Book Chunk
**Description**: Represents a segment of the book content that has been processed for vector search.

**Fields**:
- `id` (UUID): Unique identifier for the chunk
- `book_id` (UUID): Reference to the parent book
- `content` (Text): The text content of the chunk
- `token_count` (Integer): Number of tokens in the chunk
- `chunk_index` (Integer): Position of the chunk in the book
- `vector_id` (String): ID in the vector database for this chunk
- `metadata` (JSON): Additional metadata for the chunk (page number, section, etc.)
- `created_at` (DateTime): Timestamp when the chunk was created

**Relationships**:
- Many-to-one with BookContent (via book_id)

**Validation Rules**:
- Content must be between 512-1024 tokens as per spec
- token_count must match actual tokenization
- vector_id must be unique

### 3. User Query
**Description**: Represents a question or request from the reader, including context about selected text.

**Fields**:
- `id` (UUID): Unique identifier for the query
- `session_id` (UUID): Reference to the user session
- `query_text` (Text): The actual question asked by the user
- `selected_text` (Text, optional): Specific text selected by the user (if applicable)
- `query_type` (Enum): Type of query ('full_book' or 'selected_text')
- `timestamp` (DateTime): When the query was made
- `metadata` (JSON): Additional query metadata

**Relationships**:
- Many-to-one with SessionData (via session_id)
- Many-to-many with RetrievedSegment (via query_segment table)

**Validation Rules**:
- query_text must not be empty
- query_type must be one of the allowed values
- selected_text must be provided if query_type is 'selected_text'

### 4. Retrieved Segments
**Description**: Represents relevant text segments from the book retrieved based on the user query.

**Fields**:
- `id` (UUID): Unique identifier for the retrieved segment
- `query_id` (UUID): Reference to the original query
- `chunk_id` (UUID): Reference to the original book chunk
- `relevance_score` (Float): Score indicating how relevant this segment is to the query
- `content` (Text): The retrieved content segment
- `metadata` (JSON): Additional metadata for the segment
- `retrieved_at` (DateTime): Timestamp when the segment was retrieved

**Relationships**:
- Many-to-one with UserQuery (via query_id)
- Many-to-one with BookChunk (via chunk_id)

**Validation Rules**:
- relevance_score must be between 0 and 1
- content must match the original chunk content
- chunk_id must reference an existing chunk

### 5. Session Data
**Description**: Represents temporary user session information, including conversation history.

**Fields**:
- `id` (UUID): Unique identifier for the session
- `book_id` (UUID): Reference to the book being queried
- `session_token` (String): Unique token to identify the session
- `created_at` (DateTime): When the session was created
- `last_accessed` (DateTime): When the session was last used
- `expires_at` (DateTime): When the session expires
- `metadata` (JSON): Additional session metadata
- `conversation_history` (JSON): History of queries and responses in this session

**Relationships**:
- Many-to-one with BookContent (via book_id)
- One-to-many with UserQuery (via session_id)

**Validation Rules**:
- session_token must be unique
- expires_at must be in the future
- conversation_history must be valid JSON

### 6. Embed Configuration
**Description**: Represents parameters for embedding the chatbot in different book formats.

**Fields**:
- `id` (UUID): Unique identifier for the embed configuration
- `book_id` (UUID): Reference to the book
- `embed_type` (Enum): Type of embedding ('js_widget' or 'iframe')
- `configuration` (JSON): Configuration parameters for the embed
- `created_at` (DateTime): When the configuration was created
- `updated_at` (DateTime): When the configuration was last updated

**Relationships**:
- Many-to-one with BookContent (via book_id)

**Validation Rules**:
- embed_type must be one of the allowed values
- configuration must be valid JSON
- book_id must reference an existing book