-- Connect investory.users (profile) to Supabase Auth (auth.users)
-- Apply once after 001. Assumes investory.users is empty / Auth-compatible.
-- Does not delete data.

-- 1. Stop auto-generating random UUIDs — id must be the Auth user's id
ALTER TABLE investory.users
    ALTER COLUMN id DROP DEFAULT;

-- 2. Enforce the link: every profile row belongs to an Auth identity
--    ON DELETE CASCADE: deleting Auth user removes profile (+ watchlist via 001 FKs)
ALTER TABLE investory.users
    ADD CONSTRAINT users_auth_id_fkey
    FOREIGN KEY (id) REFERENCES auth.users (id) ON DELETE CASCADE;

-- 3. When Auth inserts a new user, also insert investory.users with the same id
--    SECURITY DEFINER: runs with function owner privileges (needed to write profile)
--    search_path='': safer for privileged functions; we fully qualify investory.users
CREATE OR REPLACE FUNCTION investory.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
    -- NEW = the row just inserted into auth.users
    INSERT INTO investory.users (id, email, display_name)
    VALUES (
        NEW.id,
        NEW.email,
        NEW.raw_user_meta_data ->> 'display_name'  -- optional metadata from signup
    );
    RETURN NEW;
END;
$$;

-- 4. Attach the function to Auth's user table
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION investory.handle_new_user();
