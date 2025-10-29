# PostgreSQL Architecture - Technical Deep Dive

---
date: 2024-01-15
tags: [postgres, architecture, technical, database]
author: john-smith
status: approved
---

## Executive Summary

This document describes our PostgreSQL database architecture for the SaaS application. Key decisions:
- **Version**: PostgreSQL 15 (latest stable)
- **Deployment**: Docker Compose (dev), Amazon RDS (production)
- **High Availability**: Multi-AZ with read replicas
- **Backup Strategy**: Automated daily backups, 30-day retention

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                  Application Layer                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Web API │  │ Background│  │  Cron    │          │
│  │  (Flask) │  │ Jobs (RQ) │  │  Tasks   │          │
│  └────┬─────┘  └────┬──────┘  └────┬─────┘          │
│       │             │              │                 │
└───────┼─────────────┼──────────────┼─────────────────┘
        │             │              │
        └──────┬──────┴──────────────┘
               │
        ┌──────▼──────────────────────────────┐
        │   PgBouncer (Connection Pooling)    │
        └──────┬──────────────────────────────┘
               │
        ┌──────▼──────────────────────────────┐
        │   PostgreSQL 15 (Primary)           │
        │   - Multi-AZ for HA                 │
        │   - 4 vCPU, 16GB RAM                │
        └──────┬──────────────────────────────┘
               │
        ┌──────▼──────────────────────────────┐
        │   Read Replicas (2x)                │
        │   - Analytics queries               │
        │   - Reporting                       │
        └─────────────────────────────────────┘
```

## Schema Design

### Core Tables

#### users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB  -- Flexible storage for user preferences
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);
```

#### organizations
```sql
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    settings JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orgs_slug ON organizations(slug);
```

#### documents (Full-Text Search Example)
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id),
    org_id INTEGER REFERENCES organizations(id),
    tags TEXT[],
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', title || ' ' || content)
    ) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full-text search index
CREATE INDEX idx_documents_search ON documents USING GIN(search_vector);

-- Array search index for tags
CREATE INDEX idx_documents_tags ON documents USING GIN(tags);

-- Example full-text search query:
-- SELECT title, ts_rank(search_vector, query) AS rank
-- FROM documents, to_tsquery('english', 'database & postgres') query
-- WHERE search_vector @@ query
-- ORDER BY rank DESC;
```

## Performance Optimizations

### 1. Connection Pooling (PgBouncer)

**Why**: PostgreSQL creates a new process per connection. With 100+ concurrent users, this becomes expensive.

**Configuration**:
```ini
[databases]
app_db = host=postgres port=5432 dbname=production

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
reserve_pool_size = 5
```

**Impact**: Reduces database connections from 1000 to ~30, improves response time by 40%.

### 2. Read Replicas for Analytics

**Why**: Heavy analytical queries (reports, dashboards) slow down transactional queries.

**Strategy**:
- **Primary**: Handle writes + transactional reads
- **Replica 1**: Analytics queries (daily reports)
- **Replica 2**: Real-time dashboards

**Implementation**:
```python
# Application code example
from sqlalchemy import create_engine

# Write connection
engine_primary = create_engine('postgresql://primary:5432/db')

# Read connection (round-robin across replicas)
engine_replica = create_engine('postgresql://replica:5432/db')

# Usage
with engine_primary.connect() as conn:
    conn.execute("INSERT INTO ...")  # Writes go to primary

with engine_replica.connect() as conn:
    results = conn.execute("SELECT ... for analytics")  # Reads from replica
```

### 3. JSONB Indexing

**Why**: We use JSONB for flexible user metadata and organization settings.

**Example**:
```sql
-- Query: Find users with specific preference
SELECT * FROM users
WHERE metadata @> '{"notifications": {"email": true}}';

-- Index to make this fast:
CREATE INDEX idx_users_metadata_gin ON users USING GIN(metadata jsonb_path_ops);
```

**Performance**: Query time reduced from 800ms to 12ms with index.

## Backup and Recovery

### Automated Backups

**Strategy**: Point-in-Time Recovery (PITR)
- **Full backups**: Daily at 2 AM UTC
- **WAL archiving**: Continuous (every 60 seconds)
- **Retention**: 30 days

**RTO (Recovery Time Objective)**: 4 hours
**RPO (Recovery Point Objective)**: 1 minute (via WAL)

### Disaster Recovery Procedure

1. **Identify failure** (monitoring alerts)
2. **Assess damage** (data corruption vs. infrastructure failure)
3. **Initiate recovery**:
   ```bash
   # Restore from latest backup
   aws rds restore-db-instance-to-point-in-time \
     --source-db-instance prod-postgres \
     --target-db-instance prod-postgres-recovery \
     --restore-time 2024-01-15T10:00:00Z
   ```
4. **Verify integrity** (checksums, query tests)
5. **Switch DNS** to recovery instance
6. **Post-mortem** documentation

## Monitoring

### Key Metrics

| Metric | Threshold | Alert |
|--------|-----------|-------|
| CPU Utilization | > 80% for 5 min | Warning |
| Connection Count | > 900 | Critical |
| Replication Lag | > 60 seconds | Warning |
| Disk Space | < 20% free | Critical |
| Query Duration (p95) | > 500ms | Warning |

### Monitoring Stack

- **Prometheus**: Metric collection (postgres_exporter)
- **Grafana**: Dashboards and visualization
- **PagerDuty**: On-call alerting

**Dashboard Panels**:
1. Active connections over time
2. Query duration percentiles (p50, p95, p99)
3. Cache hit ratio (target: > 99%)
4. Replication lag (target: < 10 seconds)
5. Table bloat percentage

## Security

### Authentication
- **Application**: Connection pooling via PgBouncer (user/password)
- **Admins**: IAM authentication (AWS RDS)
- **Backups**: Encryption at rest (AES-256)

### Authorization
```sql
-- Principle of least privilege
CREATE ROLE app_read;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_read;

CREATE ROLE app_write;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_write;

-- Application uses app_write, analytics tools use app_read
```

### Network Security
- **VPC**: PostgreSQL in private subnet (no public internet access)
- **Security Groups**: Only application tier can connect (port 5432)
- **SSL/TLS**: Required for all connections

## Compliance (SOC2)

### Audit Requirements Met

1. **Access Logging**: All queries logged via pgAudit extension
2. **Encryption**: At rest (AES-256) and in transit (TLS 1.2+)
3. **Backup Verification**: Monthly restore tests
4. **Access Control**: Role-based access, least privilege
5. **Change Management**: All schema changes via migration scripts (tracked in Git)

**Audit Trail Example**:
```sql
-- Enable pgAudit
CREATE EXTENSION pgaudit;

-- Log all DDL and user management
ALTER SYSTEM SET pgaudit.log = 'ddl, role';

-- Query audit logs
SELECT * FROM pgaudit.log
WHERE command = 'ALTER' AND timestamp > NOW() - INTERVAL '7 days';
```

## Migration Plan

### Timeline: 6 Weeks

**Week 1-2**: Schema design and review
**Week 3**: Test migration scripts
**Week 4**: Dry-run migration with production data dump
**Week 5**: Performance testing and optimization
**Week 6**: Production migration (scheduled downtime: 2 hours)

### Migration Scripts

All migrations tracked in `migrations/` directory:
```
migrations/
├── 001_initial_schema.sql
├── 002_add_users_metadata.sql
├── 003_create_documents_table.sql
└── 004_add_fulltext_search.sql
```

**Rollback Strategy**: Each migration includes DOWN script.

## Related Documents

- Database Selection Decision: `sample-decision.md`
- Meeting Notes: `sample-meeting-notes.md`
- Production Runbook: (TBD)
- Incident Response Plan: (TBD)

## Authors and Reviewers

- **Author**: John Smith (@john), Engineering Lead
- **Reviewers**: Mike Chen (@mike), Sarah Johnson (@sarah)
- **Approved**: 2024-01-15
