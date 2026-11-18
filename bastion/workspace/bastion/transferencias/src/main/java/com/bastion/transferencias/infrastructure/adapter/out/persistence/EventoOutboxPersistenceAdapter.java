package com.bastion.transferencias.infrastructure.adapter.out.persistence;

import java.util.Objects;

import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.eventos.contrato.Evento;
import com.bastion.transferencias.application.port.out.EventoOutboxPort;
import com.bastion.transferencias.infrastructure.persistence.entity.OutboxJpaEntity;
import com.bastion.transferencias.infrastructure.persistence.repository.OutboxSpringDataRepository;
import com.fasterxml.jackson.databind.ObjectMapper;

@Repository
public class EventoOutboxPersistenceAdapter implements EventoOutboxPort {

    private final OutboxSpringDataRepository springDataRepository;
    private final ObjectMapper objectMapper;

    public EventoOutboxPersistenceAdapter(
            OutboxSpringDataRepository springDataRepository,
            ObjectMapper objectMapper) {
        this.springDataRepository = Objects.requireNonNull(
                springDataRepository,
                "springDataRepository no puede ser null"
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
                "transferencia",
                evento.aggregateId(),
                evento.eventType(),
                payload
        );

        springDataRepository.save(entidad);
    }
}