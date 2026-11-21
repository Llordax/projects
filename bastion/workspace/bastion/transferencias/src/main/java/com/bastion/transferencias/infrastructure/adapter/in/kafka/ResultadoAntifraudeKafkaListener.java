package com.bastion.transferencias.infrastructure.adapter.in.kafka;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.transferencias.TransferenciaAprobadaData;
import com.bastion.eventos.contrato.transferencias.TransferenciaRechazadaData;
import com.bastion.transferencias.application.port.in.ProcesarTransferenciaAprobadaUseCase;
import com.bastion.transferencias.application.port.in.ProcesarTransferenciaRechazadaUseCase;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Objects;

@Component
public class ResultadoAntifraudeKafkaListener {

    private static final TypeReference<Evento<JsonNode>> TIPO_EVENTO =
            new TypeReference<>() {
            };

    private final ObjectMapper objectMapper;
    private final ProcesarTransferenciaAprobadaUseCase procesarAprobadaUseCase;
    private final ProcesarTransferenciaRechazadaUseCase procesarRechazadaUseCase;

    public ResultadoAntifraudeKafkaListener(
            ObjectMapper objectMapper,
            ProcesarTransferenciaAprobadaUseCase procesarAprobadaUseCase,
            ProcesarTransferenciaRechazadaUseCase procesarRechazadaUseCase) {
        this.objectMapper = Objects.requireNonNull(
                objectMapper,
                "objectMapper no puede ser null"
        );
        this.procesarAprobadaUseCase = Objects.requireNonNull(
                procesarAprobadaUseCase,
                "procesarAprobadaUseCase no puede ser null"
        );
        this.procesarRechazadaUseCase = Objects.requireNonNull(
                procesarRechazadaUseCase,
                "procesarRechazadaUseCase no puede ser null"
        );
    }

    @KafkaListener(
            topics = "bastion.antifraude.v1",
            groupId = "${spring.kafka.consumer.group-id}"
    )
    public void consumir(String mensaje) throws JsonProcessingException {
        Evento<JsonNode> evento = leerEvento(mensaje);

        switch (evento.eventType()) {
            case TiposEvento.TRANSFERENCIA_APROBADA -> {
                TransferenciaAprobadaData datos = objectMapper.treeToValue(
                        evento.data(),
                        TransferenciaAprobadaData.class
                );

                procesarAprobadaUseCase.ejecutar(
                        datos.transferenciaId(),
                        evento.correlationId()
                );
            }
            case TiposEvento.TRANSFERENCIA_RECHAZADA -> {
                TransferenciaRechazadaData datos = objectMapper.treeToValue(
                        evento.data(),
                        TransferenciaRechazadaData.class
                );

                procesarRechazadaUseCase.ejecutar(
                        datos.transferenciaId(),
                        datos.motivo()
                );
            }
            default -> throw new IllegalArgumentException(
                    "Tipo de evento antifraude no soportado: " + evento.eventType()
            );
        }
    }

    private Evento<JsonNode> leerEvento(String mensaje) throws JsonProcessingException {
        JsonNode contenido = objectMapper.readTree(mensaje);
        if (contenido != null && contenido.isTextual()) {
            contenido = objectMapper.readTree(contenido.textValue());
        }
        return objectMapper.readValue(contenido.traverse(objectMapper), TIPO_EVENTO);
    }
}
