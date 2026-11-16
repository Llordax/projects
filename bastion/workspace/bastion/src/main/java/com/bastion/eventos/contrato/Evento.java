package com.bastion.eventos.contrato;

import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

public record Evento<T>(
		UUID eventId,
        String eventType,
        int schemaVersion,
        Instant occurredAt,
        String aggregateId,
        UUID correlationId,
        T data
) {
	
	public Evento {
		Objects.requireNonNull(eventId, "eventId no puede ser null");

        eventType = Objects.requireNonNull(eventType, "eventType no puede ser null").trim();
        if (eventType.isBlank()) 
            throw new IllegalArgumentException("eventType no puede estar vacío");

        if (schemaVersion < 1) 
            throw new IllegalArgumentException("schemaVersion debe ser mayor o igual que 1");

        Objects.requireNonNull(occurredAt, "occurredAt no puede ser null");

        aggregateId = Objects.requireNonNull(aggregateId, "aggregateId no puede ser null").trim();
        if (aggregateId.isBlank()) 
            throw new IllegalArgumentException("aggregateId no puede estar vacío");

        Objects.requireNonNull(correlationId, "correlationId no puede ser null");
        Objects.requireNonNull(data, "data no puede ser null");
	}

}
