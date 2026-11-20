CREATE TABLE outbox_event (
    id UUID PRIMARY KEY,
    aggregatetype VARCHAR(100) NOT NULL,
    aggregateid VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL
);

CREATE INDEX idx_outbox_event_aggregateid
    ON outbox_event (aggregateid);