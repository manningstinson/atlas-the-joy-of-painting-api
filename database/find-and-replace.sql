-- find-and-replace.sql

-- First create backups
CREATE TABLE IF NOT EXISTS episodes_backup AS SELECT * FROM episodes;
CREATE TABLE IF NOT EXISTS colors_backup AS SELECT * FROM colors;
CREATE TABLE IF NOT EXISTS subjects_backup AS SELECT * FROM subjects;

-- Find duplicates in Episodes
SELECT 'EPISODES DUPLICATES:' as table_check;
SELECT title, season, episode_number, COUNT(*) as duplicate_count,
       array_agg(id) as duplicate_ids
FROM episodes
GROUP BY title, season, episode_number
HAVING COUNT(*) > 1;

-- Find duplicates in Colors
SELECT 'COLORS DUPLICATES:' as table_check;
SELECT name, code, COUNT(*) as duplicate_count,
       array_agg(id) as duplicate_ids
FROM colors
GROUP BY name, code
HAVING COUNT(*) > 1;

-- Find duplicates in Subjects
SELECT 'SUBJECTS DUPLICATES:' as table_check;
SELECT name, COUNT(*) as duplicate_count,
       array_agg(id) as duplicate_ids
FROM subjects
GROUP BY name
HAVING COUNT(*) > 1;

-- Remove duplicates from Episodes
DELETE FROM episodes
WHERE id IN (
    SELECT id
    FROM (
        SELECT id,
               ROW_NUMBER() OVER (
                   PARTITION BY title, season, episode_number
                   ORDER BY id
               ) as row_num
        FROM episodes
    ) duplicates
    WHERE row_num > 1
);

-- Remove duplicates from Colors
DELETE FROM colors
WHERE id IN (
    SELECT id
    FROM (
        SELECT id,
               ROW_NUMBER() OVER (
                   PARTITION BY name, code
                   ORDER BY id
               ) as row_num
        FROM colors
    ) duplicates
    WHERE row_num > 1
);

-- Remove duplicates from Subjects
DELETE FROM subjects
WHERE id IN (
    SELECT id
    FROM (
        SELECT id,
               ROW_NUMBER() OVER (
                   PARTITION BY name
                   ORDER BY id
               ) as row_num
        FROM subjects
    ) duplicates
    WHERE row_num > 1
);

-- Verify duplicates are removed
SELECT 'VERIFICATION - Checking for remaining duplicates:' as verification_check;

-- Check Episodes
SELECT 'EPISODES CHECK:' as table_check;
SELECT title, season, episode_number, COUNT(*)
FROM episodes
GROUP BY title, season, episode_number
HAVING COUNT(*) > 1;

-- Check Colors
SELECT 'COLORS CHECK:' as table_check;
SELECT name, code, COUNT(*)
FROM colors
GROUP BY name, code
HAVING COUNT(*) > 1;

-- Check Subjects
SELECT 'SUBJECTS CHECK:' as table_check;
SELECT name, COUNT(*)
FROM subjects
GROUP BY name
HAVING COUNT(*) > 1;