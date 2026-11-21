package com.bastion.antifraude.infrastructure.adapter.in.kafka;

import java.time.Instant;
import java.util.Currency;
import java.util.Objects;
import java.util.UUID;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import com.bastion.antifraude.application.port.in.EvaluarTransferenciaUseCase;
import com.bastion.antifraude.application.port.out.EventoOutboxPort;
import com.bastion.antifraude.domain.model.DecisionAntifraude;
import com.bastion.antifraude.domain.model.ResultadoEvaluacionAntifraude;
import com.bastion.antifraude.domain.model.SolicitudAntifraude;
import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.transferencias.TransferenciaAprobadaData;
import com.bastion.eventos.contrato.transferencias.TransferenciaRechazadaData;
import com.bastion.eventos.contrato.transferencias.TransferenciaSolicitadaData;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class TransferenciaSolicitadaKafkaListener {

    private static final TypeReference<Evento<JsonNode>> TIPO_EVENTO =
            new TypeReference<>() {
            };

    private final ObjectMapper objectMapper;
    private final EvaluarTransferenciaUseCase evaluarTransferenciaUseCase;
    private final EventoOutboxPort eventoOutboxPort;

    public TransferenciaSolicitadaKafkaListener(
            ObjectMapper objectMapper,
            EvaluarTransferenciaUseCase evaluarTransferenciaUseCase,
            EventoOutboxPort eventoOutboxPort) {
        this.objectMapper = Objects.requireNonNull(
                objectMapper,
                "objectMapper no puede ser null"
        );
        this.evaluarTransferenciaUseCase = Objects.requireNonNull(
                evaluarTransferenciaUseCase,
                "evaluarTransferenciaUseCase no puede ser null"
        );
        this.eventoOutboxPort = Objects.requireNonNull(
                eventoOutboxPort,
                "eventoOutboxPort no puede ser null"
        );
    }

    @KafkaListener(
            topics = "bastion.transferencia.v1",
            groupId = "${spring.kafka.consumer.group-id}"
    )
    public void consumir(String mensaje) throws JsonProcessingException {
        Evento<JsonNode> evento = leerEvento(mensaje);

        if (!TiposEvento.TRANSFERENCIA_SOLICITADA.equals(evento.eventType())) 
            return;

        TransferenciaSolicitadaData datos = objectMapper.treeToValue(
                evento.data(),
                TransferenciaSolicitadaData.class
        );

        SolicitudAntifraude solicitud = new SolicitudAntifraude(
                datos.transferenciaId(),
                datos.cuentaOrigenId(),
                datos.cuentaDestinoId(),
                datos.importe(),
                Currency.getInstance(datos.moneda())
        );

        ResultadoEvaluacionAntifraude resultado =
                evaluarTransferenciaUseCase.ejecutar(solicitud);

        UUID eventId = UUID.randomUUID();
        Evento<?> eventoResultado;

        if (resultado.decision() == DecisionAntifraude.APROBADA) 
            eventoResultado = new Evento<>(
                    eventId,
                    TiposEvento.TRANSFERENCIA_APROBADA,
                    1,
                    Instant.now(),
                    datos.transferenciaId().toString(),
                    evento.correlationId(),
                    new TransferenciaAprobadaData(
                            datos.transferenciaId(),
                            resultado.reglasAplicadas()
                    )
            );
        else 
            eventoResultado = new Evento<>(
                    eventId,
                    TiposEvento.TRANSFERENCIA_RECHAZADA,
                    1,
                    Instant.now(),
                    datos.transferenciaId().toString(),
                    evento.correlationId(),
                    new TransferenciaRechazadaData(
                            datos.transferenciaId(),
                            resultado.motivoRechazo()
                    )
            );

        eventoOutboxPort.registrar(eventoResultado);
    }

    private Evento<JsonNode> leerEvento(String mensaje) throws JsonProcessingException {
        JsonNode contenido = objectMapper.readTree(mensaje);
        if (contenido != null && contenido.isTextual()) {
            contenido = objectMapper.readTree(contenido.textValue());
        }
        return objectMapper.readValue(contenido.traverse(objectMapper), TIPO_EVENTO);
    }
}
