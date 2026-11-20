package com.bastion.antifraude.infrastructure.persistence.entity;

import java.util.Objects;
import java.util.UUID;

import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import com.fasterxml.jackson.databind.JsonNode;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "outbox_event")
public class OutboxJpaEntity {

    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;

    @Column(name = "aggregatetype", nullable = false, length = 100)
    private String aggregateType;

    @Column(name = "aggregateid", nullable = false, length = 255)
    private String aggregateId;

    @Column(name = "type", nullable = false, length = 100)
    private String type;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "payload", nullable = false, columnDefinition = "jsonb")
    private JsonNode payload;

    protected OutboxJpaEntity() {
        // Constructor requerido por JPA.
    }

    public OutboxJpaEntity(
            UUID id,
            String aggregateType,
            String aggregateId,
            String type,
            JsonNode payload
    ) {
        this.id = Objects.requireNonNull(id, "id no puede ser null");
        this.aggregateType = Objects.requireNonNull(
                aggregateType,
                "aggregateType no puede ser null"
        );
        this.aggregateId = Objects.requireNonNull(
                aggregateId,
                "aggregateId no puede ser null"
        );
        this.type = Objects.requireNonNull(type, "type no puede ser null");
        this.payload = Objects.requireNonNull(payload, "payload no puede ser null");
    }
}