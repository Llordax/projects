package com.bastion.antifraude.infrastructure.adapter.out.persistence;

import java.util.Objects;

import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.antifraude.application.port.out.EventoOutboxPort;
import com.bastion.antifraude.infrastructure.persistence.entity.OutboxJpaEntity;
import com.bastion.antifraude.infrastructure.persistence.repository.OutboxSpringDataRepository;
import com.bastion.eventos.contrato.Evento;
import com.fasterxml.jackson.databind.ObjectMapper;

@Repository
public class EventoOutboxPersistenceAdapter implements EventoOutboxPort {

    private final OutboxSpringDataRepository outboxSpringDataRepository;
    private final ObjectMapper objectMapper;

    public EventoOutboxPersistenceAdapter(
            OutboxSpringDataRepository outboxSpringDataRepository,
            ObjectMapper objectMapper) {
        this.outboxSpringDataRepository = Objects.requireNonNull(
                outboxSpringDataRepository,
                "outboxSpringDataRepository no puede ser null"
        );
        this.objectMapper = Objects.requireNonNull(
                objectMapper,
                "objectMapper no puede ser null"
        );
    }

    @Override
    @Transactional
    public void registrar(Evento<?> evento) {
        Objects.requireNonNull(evento, "evento no puede ser null");

        var payload = objectMapper.valueToTree(evento);

        OutboxJpaEntity entidad = new OutboxJpaEntity(
                evento.eventId(),
                "antifraude",
                evento.aggregateId(),
                evento.eventType(),
                payload
        );

        outboxSpringDataRepository.save(entidad);
    }
}