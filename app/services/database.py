import asyncpg

async def init_db(db_url):
    conn = await asyncpg.connect(db_url)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            role VARCHAR(50) NOT NULL,
            vehicle_details TEXT,
            client_type VARCHAR(50),
            id_photo TEXT,
            status VARCHAR(50) DEFAULT 'pending'
        )
    ''')
    await conn.close()

async def save_registration(user_id, role, vehicle_details=None, client_type=None, id_photo=None, db_url=None):
    conn = await asyncpg.connect(db_url)
    await conn.execute('''
        INSERT INTO users (user_id, role, vehicle_details, client_type, id_photo)
        VALUES ($1, $2, $3, $4, $5)
    ''', user_id, role, vehicle_details, client_type, id_photo)
    await conn.close()

async def update_registration_status(user_id, status, db_url=None):
    conn = await asyncpg.connect(db_url)
    await conn.execute('''
        UPDATE users SET status = $1 WHERE user_id = $2
    ''', status, user_id)
    await conn.close()

async def get_registration(user_id, db_url=None):
    conn = await asyncpg.connect(db_url)
    result = await conn.fetchrow('''
        SELECT * FROM users WHERE user_id = $1
    ''', user_id)
    await conn.close()
    return result