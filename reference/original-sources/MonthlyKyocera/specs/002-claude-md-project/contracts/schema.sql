-- Kyocera Meter Reading Management System
-- DuckDB Database Schema
-- Version: 1.0.0
-- Date: 2025-09-11

-- Enable UUID extension for generating unique IDs
-- INSTALL uuid;
-- LOAD uuid;

-- ============================================
-- Schema Version Tracking
-- ============================================
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255)
);

INSERT INTO schema_version (version, description) 
VALUES (1, 'Initial schema creation');

-- ============================================
-- Devices Table
-- ============================================
CREATE TABLE IF NOT EXISTS devices (
    -- Composite primary key for model + serial combination
    model VARCHAR(100) NOT NULL,
    serial_number VARCHAR(100) NOT NULL,
    
    -- Device information
    location VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'active' 
        CHECK (status IN ('active', 'inactive', 'retired')),
    
    -- Tracking fields
    last_reading_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    PRIMARY KEY (model, serial_number)
);

-- Indexes for devices
CREATE INDEX idx_device_serial ON devices(serial_number);
CREATE INDEX idx_device_status ON devices(status);
CREATE INDEX idx_device_location ON devices(location);

-- Comments
COMMENT ON TABLE devices IS 'Kyocera office devices (printers, copiers, MFPs)';
COMMENT ON COLUMN devices.model IS 'Device model number (e.g., TASKalfa 3253ci)';
COMMENT ON COLUMN devices.serial_number IS 'Unique device serial number';
COMMENT ON COLUMN devices.status IS 'Device lifecycle status: active, inactive, or retired';
COMMENT ON COLUMN devices.last_reading_date IS 'Timestamp of most recent meter reading';

-- ============================================
-- Email Threads Table
-- ============================================
CREATE TABLE IF NOT EXISTS email_threads (
    thread_id VARCHAR(100) PRIMARY KEY,
    root_message_id VARCHAR(255) NOT NULL,
    subject VARCHAR(500),
    participant_count INTEGER NOT NULL DEFAULT 1,
    message_count INTEGER NOT NULL DEFAULT 1,
    first_message_date TIMESTAMP NOT NULL,
    last_activity TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for email_threads
CREATE INDEX idx_thread_activity ON email_threads(last_activity DESC);
CREATE INDEX idx_thread_root ON email_threads(root_message_id);

-- Comments
COMMENT ON TABLE email_threads IS 'Email conversation threads for tracking related messages';
COMMENT ON COLUMN email_threads.thread_id IS 'Hash of root message ID';
COMMENT ON COLUMN email_threads.root_message_id IS 'Original Message-ID that started the thread';

-- ============================================
-- Email Messages Table
-- ============================================
CREATE TABLE IF NOT EXISTS email_messages (
    -- Use hash of email headers as ID
    id VARCHAR(100) PRIMARY KEY,
    
    -- Email headers for threading
    message_id VARCHAR(255) NOT NULL UNIQUE,
    in_reply_to VARCHAR(255),
    references TEXT,
    thread_id VARCHAR(100),
    
    -- Email metadata
    received_date TIMESTAMP NOT NULL,
    sender VARCHAR(255) NOT NULL,
    subject VARCHAR(500),
    body_text TEXT,
    
    -- Processing information
    attachments JSON,  -- List of attachment metadata
    processing_status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (processing_status IN ('pending', 'processed', 'failed', 'quarantined')),
    quarantine_reason VARCHAR(500),
    processed_at TIMESTAMP,
    
    -- Tracking
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key to thread
    FOREIGN KEY (thread_id) REFERENCES email_threads(thread_id)
);

-- Indexes for email_messages
CREATE INDEX idx_email_status ON email_messages(processing_status);
CREATE INDEX idx_email_date ON email_messages(received_date DESC);
CREATE INDEX idx_email_sender ON email_messages(sender);
CREATE INDEX idx_email_message_id ON email_messages(message_id);
CREATE INDEX idx_email_thread ON email_messages(thread_id);

-- Comments
COMMENT ON TABLE email_messages IS 'Original emails containing meter reading data (no file size limits)';
COMMENT ON COLUMN email_messages.id IS 'Hash of Message-ID + Date headers';
COMMENT ON COLUMN email_messages.message_id IS 'RFC 822 Message-ID header for threading';
COMMENT ON COLUMN email_messages.in_reply_to IS 'In-Reply-To header for thread relationships';
COMMENT ON COLUMN email_messages.references IS 'References header chain for complete thread context';
COMMENT ON COLUMN email_messages.thread_id IS 'Foreign key to email_threads table';
COMMENT ON COLUMN email_messages.attachments IS 'JSON array of attachment metadata';
COMMENT ON COLUMN email_messages.processing_status IS 'Current processing state of email';

-- ============================================
-- Meter Readings Table
-- ============================================
CREATE SEQUENCE meter_reading_id_seq START 1;

CREATE TABLE IF NOT EXISTS meter_readings (
    id INTEGER PRIMARY KEY DEFAULT nextval('meter_reading_id_seq'),
    
    -- Device reference (foreign key)
    device_model VARCHAR(100) NOT NULL,
    device_serial VARCHAR(100) NOT NULL,
    
    -- Reading data
    reading_date DATE NOT NULL,
    total_counter INTEGER NOT NULL DEFAULT 0 CHECK (total_counter >= 0),
    black_counter INTEGER DEFAULT 0 CHECK (black_counter >= 0),
    color_counter INTEGER DEFAULT 0 CHECK (color_counter >= 0),
    scan_counter INTEGER DEFAULT 0 CHECK (scan_counter >= 0),
    fax_counter INTEGER DEFAULT 0 CHECK (fax_counter >= 0),
    
    -- Source tracking
    source_email_id VARCHAR(100) NOT NULL,
    file_paths JSON NOT NULL,  -- {"pdf": "path", "txt": "path", "md": "path", "yaml": "path"}
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (device_model, device_serial) 
        REFERENCES devices(model, serial_number)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (source_email_id) 
        REFERENCES email_messages(id)
        ON DELETE RESTRICT,
    
    -- Prevent exact duplicates (same device, date, and creation time)
    UNIQUE (device_model, device_serial, reading_date, created_at)
);

-- Indexes for meter_readings
CREATE INDEX idx_reading_date ON meter_readings(reading_date DESC);
CREATE INDEX idx_device_reading ON meter_readings(device_model, device_serial, reading_date DESC);
CREATE INDEX idx_reading_email ON meter_readings(source_email_id);

-- Comments
COMMENT ON TABLE meter_readings IS 'Individual meter readings from devices';
COMMENT ON COLUMN meter_readings.total_counter IS 'Total page count across all functions';
COMMENT ON COLUMN meter_readings.file_paths IS 'JSON object with paths to generated files';

-- ============================================
-- Reports Table
-- ============================================
CREATE SEQUENCE report_id_seq START 1;

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY DEFAULT nextval('report_id_seq'),
    
    -- Report metadata
    report_type VARCHAR(50) NOT NULL 
        CHECK (report_type IN ('monthly', 'yearly', 'device', 'department')),
    
    -- Optional device reference
    device_model VARCHAR(100),
    device_serial VARCHAR(100),
    
    -- Report parameters
    start_date DATE NOT NULL,
    end_date DATE NOT NULL CHECK (end_date >= start_date),
    format VARCHAR(20) NOT NULL 
        CHECK (format IN ('pdf', 'excel', 'csv', 'json')),
    
    -- Report content
    content TEXT,  -- For text-based formats
    file_path VARCHAR(500),  -- Path to generated file
    
    -- Metadata
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    FOREIGN KEY (device_model, device_serial) 
        REFERENCES devices(model, serial_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Indexes for reports
CREATE INDEX idx_report_type ON reports(report_type);
CREATE INDEX idx_report_dates ON reports(start_date, end_date);
CREATE INDEX idx_report_device ON reports(device_model, device_serial);

-- Comments
COMMENT ON TABLE reports IS 'Generated reports for devices or time periods';
COMMENT ON COLUMN reports.report_type IS 'Type of report: monthly, yearly, device, or department';

-- ============================================
-- Processing Logs Table
-- ============================================
CREATE SEQUENCE processing_log_id_seq START 1;

CREATE TABLE IF NOT EXISTS processing_logs (
    id INTEGER PRIMARY KEY DEFAULT nextval('processing_log_id_seq'),
    
    -- Log entry data
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    action VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL 
        CHECK (status IN ('success', 'failure', 'warning')),
    
    -- Entity reference
    entity_type VARCHAR(50),  -- 'email', 'device', 'reading', etc.
    entity_id VARCHAR(100),   -- ID of affected entity
    
    -- Additional information
    details JSON,              -- Structured metadata
    error_message TEXT,        -- Error details if failed
    file_path VARCHAR(500),    -- Related file path
    
    -- Index for time-based queries
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for processing_logs
CREATE INDEX idx_log_timestamp ON processing_logs(timestamp DESC);
CREATE INDEX idx_log_status ON processing_logs(status);
CREATE INDEX idx_log_entity ON processing_logs(entity_type, entity_id);
CREATE INDEX idx_log_action ON processing_logs(action);

-- Comments
COMMENT ON TABLE processing_logs IS 'Audit trail of all system operations';
COMMENT ON COLUMN processing_logs.details IS 'JSON object with structured metadata';
COMMENT ON COLUMN processing_logs.error_message IS 'Detailed error message for failures';

-- ============================================
-- Compressed Emails Table
-- ============================================
CREATE TABLE IF NOT EXISTS compressed_emails (
    id VARCHAR(100) PRIMARY KEY,
    original_message_id VARCHAR(255) NOT NULL UNIQUE,
    compression_method VARCHAR(20) NOT NULL 
        CHECK (compression_method IN ('zstd', 'gzip', 'none')),
    compressed_data BLOB NOT NULL,
    original_size INTEGER NOT NULL,
    compressed_size INTEGER NOT NULL CHECK (compressed_size <= original_size),
    metadata_json JSON NOT NULL,  -- All headers and structure for reconstruction
    compressed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key to original email
    FOREIGN KEY (original_message_id) REFERENCES email_messages(message_id)
);

-- Indexes for compressed_emails
CREATE INDEX idx_compressed_message ON compressed_emails(original_message_id);
CREATE INDEX idx_compressed_date ON compressed_emails(compressed_at DESC);

-- Comments
COMMENT ON TABLE compressed_emails IS 'Compressed email storage for long-term archive';
COMMENT ON COLUMN compressed_emails.compression_method IS 'Compression algorithm used (zstd preferred)';
COMMENT ON COLUMN compressed_emails.compressed_data IS 'Compressed email content (target <10MB)';
COMMENT ON COLUMN compressed_emails.metadata_json IS 'Complete headers and MIME structure for full reconstruction';

-- ============================================
-- Archive Tables (for data older than 24 months)
-- ============================================
CREATE TABLE IF NOT EXISTS meter_readings_archive (
    LIKE meter_readings INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS processing_logs_archive (
    LIKE processing_logs INCLUDING ALL
);

CREATE TABLE IF NOT EXISTS email_messages_archive (
    LIKE email_messages INCLUDING ALL
);

-- ============================================
-- Views for Common Queries
-- ============================================

-- Latest reading per device
CREATE OR REPLACE VIEW latest_device_readings AS
SELECT 
    d.model,
    d.serial_number,
    d.location,
    d.status,
    mr.reading_date,
    mr.total_counter,
    mr.black_counter,
    mr.color_counter,
    mr.created_at
FROM devices d
LEFT JOIN LATERAL (
    SELECT *
    FROM meter_readings mr
    WHERE mr.device_model = d.model 
      AND mr.device_serial = d.serial_number
    ORDER BY mr.reading_date DESC, mr.created_at DESC
    LIMIT 1
) mr ON true;

-- Monthly usage summary
CREATE OR REPLACE VIEW monthly_usage_summary AS
SELECT 
    DATE_TRUNC('month', reading_date) as month,
    device_model,
    device_serial,
    COUNT(*) as reading_count,
    MAX(total_counter) - MIN(total_counter) as pages_printed,
    MAX(black_counter) - MIN(black_counter) as black_pages,
    MAX(color_counter) - MIN(color_counter) as color_pages
FROM meter_readings
GROUP BY DATE_TRUNC('month', reading_date), device_model, device_serial;

-- Processing queue status
CREATE OR REPLACE VIEW processing_queue_status AS
SELECT 
    processing_status,
    COUNT(*) as email_count,
    MIN(received_date) as oldest_email,
    MAX(received_date) as newest_email
FROM email_messages
WHERE processing_status != 'processed'
GROUP BY processing_status;

-- Email thread view
CREATE OR REPLACE VIEW email_thread_view AS
SELECT 
    et.thread_id,
    et.subject,
    et.message_count,
    et.participant_count,
    et.first_message_date,
    et.last_activity,
    COUNT(em.id) as unprocessed_count
FROM email_threads et
LEFT JOIN email_messages em ON et.thread_id = em.thread_id 
    AND em.processing_status != 'processed'
GROUP BY et.thread_id, et.subject, et.message_count, 
    et.participant_count, et.first_message_date, et.last_activity;

-- Compression statistics view
CREATE OR REPLACE VIEW compression_stats AS
SELECT 
    compression_method,
    COUNT(*) as email_count,
    AVG(original_size) as avg_original_size,
    AVG(compressed_size) as avg_compressed_size,
    AVG(1.0 - (compressed_size::FLOAT / original_size)) * 100 as avg_compression_ratio,
    SUM(original_size - compressed_size) as total_bytes_saved
FROM compressed_emails
GROUP BY compression_method;

-- Device activity summary
CREATE OR REPLACE VIEW device_activity_summary AS
SELECT 
    d.model,
    d.serial_number,
    d.status,
    COUNT(mr.id) as total_readings,
    MAX(mr.reading_date) as last_reading,
    AVG(mr.total_counter) as avg_counter,
    DATEDIFF('day', MIN(mr.reading_date), MAX(mr.reading_date)) as days_monitored
FROM devices d
LEFT JOIN meter_readings mr ON d.model = mr.device_model 
    AND d.serial_number = mr.device_serial
GROUP BY d.model, d.serial_number, d.status;

-- ============================================
-- Sample Queries for Common Operations
-- ============================================

-- Find devices without recent readings (> 30 days)
/*
SELECT model, serial_number, location, last_reading_date
FROM devices
WHERE status = 'active'
  AND (last_reading_date IS NULL 
       OR last_reading_date < CURRENT_DATE - INTERVAL 30 DAY)
ORDER BY last_reading_date;
*/

-- Get usage trend for a specific device
/*
SELECT 
    DATE_TRUNC('month', reading_date) as month,
    MAX(total_counter) - MIN(total_counter) as monthly_usage
FROM meter_readings
WHERE device_serial = 'ABC1234567'
  AND reading_date >= CURRENT_DATE - INTERVAL 12 MONTH
GROUP BY DATE_TRUNC('month', reading_date)
ORDER BY month;
*/

-- Identify high-usage devices
/*
WITH monthly_usage AS (
    SELECT 
        device_model,
        device_serial,
        DATE_TRUNC('month', reading_date) as month,
        MAX(total_counter) - MIN(total_counter) as pages
    FROM meter_readings
    WHERE reading_date >= CURRENT_DATE - INTERVAL 3 MONTH
    GROUP BY device_model, device_serial, DATE_TRUNC('month', reading_date)
)
SELECT 
    device_model,
    device_serial,
    AVG(pages) as avg_monthly_pages
FROM monthly_usage
GROUP BY device_model, device_serial
HAVING AVG(pages) > 10000
ORDER BY avg_monthly_pages DESC;
*/

-- Processing error investigation
/*
SELECT 
    timestamp,
    action,
    entity_type,
    entity_id,
    error_message,
    details
FROM processing_logs
WHERE status = 'failure'
  AND timestamp >= CURRENT_DATE - INTERVAL 7 DAY
ORDER BY timestamp DESC
LIMIT 50;
*/

-- ============================================
-- Maintenance Procedures
-- ============================================

-- Archive old meter readings (> 24 months)
/*
INSERT INTO meter_readings_archive
SELECT * FROM meter_readings
WHERE reading_date < CURRENT_DATE - INTERVAL 24 MONTH;

DELETE FROM meter_readings
WHERE reading_date < CURRENT_DATE - INTERVAL 24 MONTH;
*/

-- Compress old emails for archive
/*
-- This would be done via application logic, not SQL
-- Example process:
-- 1. Select emails older than 90 days
-- 2. Compress using zstd
-- 3. Store in compressed_emails table
-- 4. Update original email status
*/

-- Clean up old processing logs
/*
INSERT INTO processing_logs_archive
SELECT * FROM processing_logs
WHERE timestamp < CURRENT_DATE - INTERVAL 90 DAY
  AND status = 'success';

DELETE FROM processing_logs
WHERE timestamp < CURRENT_DATE - INTERVAL 90 DAY
  AND status = 'success';
*/

-- Update device last_reading_date
/*
UPDATE devices d
SET last_reading_date = (
    SELECT MAX(reading_date)
    FROM meter_readings mr
    WHERE mr.device_model = d.model 
      AND mr.device_serial = d.serial_number
),
updated_at = CURRENT_TIMESTAMP;
*/

-- Update email thread counts
/*
UPDATE email_threads et
SET message_count = (
    SELECT COUNT(*)
    FROM email_messages em
    WHERE em.thread_id = et.thread_id
),
last_activity = (
    SELECT MAX(received_date)
    FROM email_messages em
    WHERE em.thread_id = et.thread_id
);
*/

-- Reconstruct email from compressed storage (application logic)
/*
-- This would be done in Python:
-- 1. Retrieve compressed_data and metadata_json
-- 2. Decompress using specified method
-- 3. Reconstruct .eml file from metadata and content
-- 4. Return complete email with all headers and attachments
*/