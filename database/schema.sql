-- Create base tables
CREATE TABLE episodes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    air_date DATE NOT NULL,
    broadcast_month INTEGER CHECK (broadcast_month BETWEEN 1 AND 12),
    season INTEGER NOT NULL,
    episode_number INTEGER NOT NULL,
    UNIQUE(season, episode_number)
);

CREATE TABLE colors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(50)
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Create junction tables
CREATE TABLE episode_colors (
    episode_id INTEGER REFERENCES episodes(id) ON DELETE CASCADE,
    color_id INTEGER REFERENCES colors(id) ON DELETE CASCADE,
    PRIMARY KEY (episode_id, color_id)
);

CREATE TABLE episode_subjects (
    episode_id INTEGER REFERENCES episodes(id) ON DELETE CASCADE,
    subject_id INTEGER REFERENCES subjects(id) ON DELETE CASCADE,
    PRIMARY KEY (episode_id, subject_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_episodes_broadcast_month ON episodes(broadcast_month);
CREATE INDEX idx_episode_colors_color_id ON episode_colors(color_id);
CREATE INDEX idx_episode_subjects_subject_id ON episode_subjects(subject_id);