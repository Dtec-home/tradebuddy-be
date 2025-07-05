-- Add OAuth columns to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS oauth_provider VARCHAR,
ADD COLUMN IF NOT EXISTS oauth_provider_id VARCHAR,
ADD COLUMN IF NOT EXISTS avatar_url VARCHAR;

-- Also make hashed_password nullable for OAuth users
ALTER TABLE users 
ALTER COLUMN hashed_password DROP NOT NULL;