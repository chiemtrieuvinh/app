Alembic tool overview

**initialize new**
alembic init <folder_name>

**create a new revision**
alembic revision -r <message>

**run upgrade migration**
alembic upgrade <revision\_#>

**run downgrade migration**
alembic downgrade <revision\_#>

**alembic.ini**
Configuration for alembic
Alembic will look for it when invoked

**alembic directory**
Contains all revisions
Place we call migration to updated/downgrade

**flow create new alembic tables**

- update schemas files
- alembic revision --autogenerate -m "<message>" to update alembic revision for migrating data to postgresql db
- "alembic upgrade head" to update revisions to db

**To generate secret key**

- "openssl rand -hex 32"

create user table
op.bulk_insert(user_table, [
{
"id": uuid4(),
"email": "examples@gmail.com",
"username": "fa_admin",
"password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
"first_name": "fast_api",
"last_name": "Admin",
"is_active": True,
"is_admin": True,
"created_at": datetime.utcnow(),
"updated_at": datetime.utcnow()
}
])

use this user to access auth so that we can get access_token

{
"email": "test@gmail.com",
"username": "root",
"first_name": "Vinh",
"last_name": "Chiem",
"password": "abc@123",
"is_admin": true
}
