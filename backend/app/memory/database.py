import os

import psycopg

from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    if not DATABASE_URL:

        raise RuntimeError(
            "DATABASE_URL is not configured."
        )

    return psycopg.connect(
        DATABASE_URL
    )


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables():

    with get_connection() as connection:

        with connection.cursor() as cursor:

            # ------------------------------------------------
            # CONVERSATIONS TABLE
            # ------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (

                    id SERIAL PRIMARY KEY,

                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP
                );
                """
            )


            # ------------------------------------------------
            # MESSAGES TABLE
            # ------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (

                    id SERIAL PRIMARY KEY,

                    conversation_id INTEGER
                        REFERENCES conversations(id)
                        ON DELETE CASCADE,

                    role VARCHAR(50) NOT NULL,

                    content TEXT NOT NULL,

                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

        connection.commit()


# ============================================================
# CREATE NEW CONVERSATION
# ============================================================

def create_conversation():

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO conversations
                DEFAULT VALUES
                RETURNING id;
                """
            )

            conversation_id = (
                cursor.fetchone()[0]
            )

        connection.commit()

    return conversation_id


# ============================================================
# SAVE MESSAGE
# ============================================================

def save_message(
    conversation_id: int,
    role: str,
    content: str
):

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO messages (
                    conversation_id,
                    role,
                    content
                )

                VALUES (%s, %s, %s);
                """,
                (
                    conversation_id,
                    role,
                    content
                )
            )

        connection.commit()


# ============================================================
# GET CONVERSATION MESSAGES
# ============================================================

def get_conversation_messages(
    conversation_id: int
):

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    role,
                    content

                FROM messages

                WHERE conversation_id = %s

                ORDER BY id ASC;
                """,
                (
                    conversation_id,
                )
            )

            rows = cursor.fetchall()


    return [
        {
            "role": role,
            "content": content
        }

        for role, content in rows
    ]


# ============================================================
# GET ALL CONVERSATIONS
# ============================================================

def get_conversations():

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    c.id,
                    c.created_at,

                    (
                        SELECT m.content

                        FROM messages m

                        WHERE
                            m.conversation_id = c.id

                            AND m.role = 'user'

                        ORDER BY m.id ASC

                        LIMIT 1

                    ) AS title

                FROM conversations c

                ORDER BY c.id DESC;
                """
            )

            rows = cursor.fetchall()


    conversations = []


    for row in rows:

        conversation_id = row[0]

        created_at = row[1]

        title = row[2]


        # ----------------------------------------------------
        # Clean conversation title
        # ----------------------------------------------------

        if title:

            title = title.strip()

            # Keep sidebar titles short

            if len(title) > 60:

                title = (
                    title[:60].rstrip()
                    + "..."
                )

        else:

            title = "New Conversation"


        conversations.append(
            {
                "id": conversation_id,

                "created_at": created_at,

                "title": title
            }
        )


    return conversations