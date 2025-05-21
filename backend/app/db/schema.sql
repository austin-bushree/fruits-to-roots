-- NGSS Schema for SQLite
DROP TABLE IF EXISTS expectations;
DROP TABLE IF EXISTS seps;
DROP TABLE IF EXISTS cccs;
DROP TABLE IF EXISTS dcis;
DROP TABLE IF EXISTS expectations_seps;
DROP TABLE IF EXISTS expectations_cccs;
DROP TABLE IF EXISTS expectations_dcis;

-- Table: Performance Expectations
CREATE TABLE expectations (
    id TEXT PRIMARY KEY,                 -- e.g. HS-PS3-1
    grade_level TEXT NOT NULL,          -- e.g. HS, MS
    topic TEXT NOT NULL,                -- e.g. Energy, Structure and Function
    dci_group TEXT NOT NULL,            -- e.g. PS3
    description TEXT NOT NULL,          -- Full PE statement
    performance_features TEXT  -- JSON-encoded outline of evidence statement features
);

-- Table: seps (Science and Engineering Practices)
CREATE TABLE seps (
    id INTEGER PRIMARY KEY,          -- 1 to 8
    sep_name TEXT NOT NULL,
    description TEXT
);

-- Table: cccs (Crosscutting Concepts)
CREATE TABLE cccs (
    id INTEGER PRIMARY KEY,          -- 1 to 7
    ccc_name TEXT NOT NULL,
    description TEXT
);

-- Table: dcis (Disciplinary Core Ideas)
-- CREATE TABLE dcis (
--     id TEXT PRIMARY KEY,           -- e.g. PS3.B
--     dci_name TEXT NOT NULL,          -- e.g. Conservation of Energy
--     domain TEXT NOT NULL,            -- PS, LS, etc.
--     topic TEXT NOT NULL,             -- topic names
--     description TEXT
-- );

CREATE TABLE dcis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,                         -- 1
    domain TEXT NOT NULL,              -- PS
    topic TEXT NOT NULL,               -- Energy
    group_code TEXT NOT NULL,          -- PS3.A
    group_name TEXT NOT NULL,          -- PS3.A: Definitions of Energy
    heading TEXT NOT NULL,             -- "Energy is" (first 3 words of full idea, from bullet point)
    full_idea TEXT,                     -- "Energy is a quantitative property of a system that ... " (full bullet point)
    UNIQUE(full_idea)
);

-- Relationship table: standards ↔ seps
CREATE TABLE expectations_seps (
    expectation_id TEXT NOT NULL,
    sep_id INTEGER NOT NULL,
    PRIMARY KEY (expectation_id, sep_id),
    FOREIGN KEY (expectation_id) REFERENCES expectations(id),
    FOREIGN KEY (sep_id) REFERENCES seps(id)
);

-- Relationship table: standards ↔ cccs
CREATE TABLE expectations_cccs (
    expectation_id TEXT NOT NULL,
    ccc_id INTEGER NOT NULL,
    PRIMARY KEY (expectation_id, ccc_id),
    FOREIGN KEY (expectation_id) REFERENCES expectations(id),
    FOREIGN KEY (ccc_id) REFERENCES cccs(id)
);

-- Relationship table: standards ↔ dcis
CREATE TABLE expectations_dcis (
    expectation_id TEXT NOT NULL,
    dci_id INTEGER NOT NULL,
    PRIMARY KEY (expectation_id, dci_id),
    FOREIGN KEY (expectation_id) REFERENCES expectations(id),
    FOREIGN KEY (dci_id) REFERENCES dcis(id)
);

CREATE TABLE IF NOT EXISTS observable_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pe_id TEXT NOT NULL,
    section_label TEXT NOT NULL,
    level INTEGER NOT NULL,
    text TEXT NOT NULL,
    parent_label TEXT
);
--
--
-- -- Sample inserts to validate the schema
--
-- -- Insert a sample performance expectation
-- INSERT INTO expectations (id, grade_level, topic, dci_group, description, performance_hierarchy)
-- VALUES (
--     'HS-PS3-1',
--     'HS',
--     'Energy',
--     'PS3',
--     'Create a computational model to calculate the change in energy...',
--     '{"1": {"a": ["Identify components", "Quantify initial/final energy"]}, "2": {"a": ["Use energy flow equations"]}}'
-- );
--
-- -- Insert sample SEPs
-- INSERT INTO seps (id, sep_name, description)
-- VALUES
--     (1, 'Asking Questions and Defining Problems', 'Science begins with questions...'),
--     (2, 'Developing and Using Models', 'Modeling in 3–12 builds on K–2 experiences...');
--
-- -- Insert sample CCCs
-- INSERT INTO cccs (id, ccc_name, description)
-- VALUES
--     (1, 'Patterns', 'Observed patterns can guide organization and classification.'),
--     (2, 'Cause and Effect', 'Events have causes, sometimes multifaceted.');
--
-- -- Insert sample DCIs
-- INSERT INTO dcis (id, dci_name, domain, description)
-- VALUES
--     ('PS3.B', 'Conservation of Energy', 'PS', 'Energy cannot be created or destroyed...');
--
-- -- Link the performance expectation to SEPs
-- INSERT INTO expectations_seps (expectation_id, sep_id)
-- VALUES
--     ('HS-PS3-1', 2);
--
-- -- Link the performance expectation to CCCs
-- INSERT INTO expectations_cccs (expectation_id, ccc_id)
-- VALUES
--     ('HS-PS3-1', 1);
--
-- -- Link the performance expectation to DCIs
-- INSERT INTO expectations_dcis (expectation_id, dci_id)
-- VALUES
--     ('HS-PS3-1', 'PS3.B');
--
-- -- Test query: Join expectation with its related SEPs, CCCs, and DCIs
-- SELECT
--     e.id AS expectation_id,
--     e.description,
--     s.sep_name,
--     c.ccc_name,
--     d.dci_name
-- FROM expectations e
-- LEFT JOIN expectations_seps es ON e.id = es.expectation_id
-- LEFT JOIN seps s ON es.sep_id = s.id
-- LEFT JOIN expectations_cccs ec ON e.id = ec.expectation_id
-- LEFT JOIN cccs c ON ec.ccc_id = c.id
-- LEFT JOIN expectations_dcis ed ON e.id = ed.expectation_id
-- LEFT JOIN dcis d ON ed.dci_id = d.id
-- WHERE e.id = 'HS-PS3-1';