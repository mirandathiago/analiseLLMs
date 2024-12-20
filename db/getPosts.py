from db.connection import connect_database

def fetch_posts(post_ids):

    query = """
    SELECT 
        id, title, body, score, creationdate, viewcount, tags, answercount, favoritecount
    FROM posts
    WHERE id = ANY(%s) ORDER BY id;
    """
    posts = []
    try:
        with connect_database() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (post_ids,))
                rows = cur.fetchall()
                for row in rows:
                    posts.append({
                        "id": row[0],
                        "title": row[1],
                        "body": row[2],
                        "score": row[3],
                        "creationdate": row[4].isoformat(),
                        "viewcount": row[5],
                        "tags": row[6],
                        "answercount": row[7],
                        "favoritecount": row[8],
                    })
    except Exception as e:
        print(f"Erro ao consultar o banco de dados: {e}")
    return posts