package com.bastion.transferencias.infrastructure.adapter.in.kafka;

import java.util.Objects;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.cuentas.CompensacionRealizadaData;
import com.bastion.eventos.contrato.cuentas.CompensacionRechazadaData;
import com.bastion.eventos.contrato.cuentas.CreditoRealizadoData;
import com.bastion.eventos.contrato.cuentas.CreditoRechazadoData;
import com.bastion.eventos.contrato.cuentas.DebitoRealizadoData;
import com.bastion.eventos.contrato.cuentas.DebitoRechazadoData;
import com.bastion.transferencias.application.port.in.ProcesarCompensacionRealizadaUseCase;
import com.bastion.transferencias.application.port.in.ProcesarCompensacionRechazadaUseCase;
import com.bastion.transferencias.application.port.in.ProcesarCreditoRealizadoUseCase;
import com.bastion.transferencias.application.port.in.ProcesarCreditoRechazadoUseCase;
import com.bastion.transferencias.application.port.in.ProcesarDebitoRealizadoUseCase;
import com.bastion.transferencias.application.port.in.ProcesarDebitoRechazadoUseCase;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class ResultadoMovimientoCuentaKafkaListener {

    private static final TypeReference<Evento<JsonNode>> TIPO_EVENTO =
            new TypeReference<>() {
            };

    private final ObjectMapper objectMapper;
    private final ProcesarDebitoRealizadoUseCase procesarDebitoRealizadoUseCase;
    private final ProcesarDebitoRechazadoUseCase procesarDebitoRechazadoUseCase;
    private final ProcesarCreditoRealizadoUseCase procesarCreditoRealizadoUseCase;
    private final ProcesarCreditoRechazadoUseCase procesarCreditoRechazadoUseCase;
    private final ProcesarCompensacionRealizadaUseCase procesarCompensacionRealizadaUseCase;
    private final ProcesarCompensacionRechazadaUseCase procesarCompensacionRechazadaUseCase;

    public ResultadoMovimientoCuentaKafkaListener(
            ObjectMapper objectMapper,
            ProcesarDebitoRealizadoUseCase procesarDebitoRealizadoUseCase,
            ProcesarDebitoRechazadoUseCase procesarDebitoRechazadoUseCase,
            ProcesarCreditoRealizadoUseCase procesarCreditoRealizadoUseCase,
            ProcesarCreditoRechazadoUseCase procesarCreditoRechazadoUseCase,
            ProcesarCompensacionRealizadaUseCase procesarCompensacionRealizadaUseCase,
            ProcesarCompensacionRechazadaUseCase procesarCompensacionRechazadaUseCase) {
        this.objectMapper = Objects.requireNonNull(objectMapper, "objectMapper no puede ser null");
        this.procesarDebitoRealizadoUseCase = Objects.requireNonNull(
                procesarDebitoRealizadoUseCase,
                "procesarDebitoRealizadoUseCase no puede ser null"
        );
        this.procesarDebitoRechazadoUseCase = Objects.requireNonNull(
                procesarDebitoRechazadoUseCase,
                "procesarDebitoRechazadoUseCase no puede ser null"
        );
        this.procesarCreditoRealizadoUseCase = Objects.requireNonNull(
                procesarCreditoRealizadoUseCase,
                "procesarCreditoRealizadoUseCase no puede ser null"
        );
        this.procesarCreditoRechazadoUseCase = Objects.requireNonNull(
                procesarCreditoRechazadoUseCase,
                "procesarCreditoRechazadoUseCase no puede ser null"
        );
        this.procesarCompensacionRealizadaUseCase = Objects.requireNonNull(
                procesarCompensacionRealizadaUseCase,
                "procesarCompensacionRealizadaUseCase no puede ser null"
        );
        this.procesarCompensacionRechazadaUseCase = Objects.requireNonNull(
                procesarCompensacionRechazadaUseCase,
                "procesarCompensacionRechazadaUseCase no puede ser null"
        );
    }

    @KafkaListener(
            topics = {"bastion.cuenta", "bastion.cuenta.v1"},
            groupId = "${spring.kafka.consumer.group-id}"
    )
    public void consumir(String mensaje) throws JsonProcessingException {
        Evento<JsonNode> evento = leerEvento(mensaje);

        switch (evento.eventType()) {
            case TiposEvento.DEBITO_REALIZADO -> {
                DebitoRealizadoData datos = objectMapper.treeToValue(
                        evento.data(),
                        DebitoRealizadoData.class
                );
                procesarDebitoRealizadoUseCase.ejecutar(
                        datos.transferenciaId(),
                        evento.correlationId()
                );
            }
            case TiposEvento.DEBITO_RECHAZADO -> {
                DebitoRechazadoData datos = objectMapper.treeToValue(
                        evento.data(),
                        DebitoRechazadoData.class
                );
                procesarDebitoRechazadoUseCase.ejecutar(
                        datos.transferenciaId(),
                        datos.motivo()
                );
            }
            case TiposEvento.CREDITO_REALIZADO -> {
                CreditoRealizadoData datos = objectMapper.treeToValue(
                        evento.data(),
                        CreditoRealizadoData.class
                );
                procesarCreditoRealizadoUseCase.ejecutar(
                        datos.transferenciaId(),
                        evento.correlationId()
                );
            }
            case TiposEvento.CREDITO_RECHAZADO -> {
                CreditoRechazadoData datos = objectMapper.treeToValue(
                        evento.data(),
                        CreditoRechazadoData.class
                );
                procesarCreditoRechazadoUseCase.ejecutar(
                        datos.transferenciaId(),
                        datos.motivo(),
                        evento.correlationId()
                );
            }
            case TiposEvento.COMPENSACION_REALIZADA -> {
                CompensacionRealizadaData datos = objectMapper.treeToValue(
                        evento.data(),
                        CompensacionRealizadaData.class
                );
                procesarCompensacionRealizadaUseCase.ejecutar(
                        datos.transferenciaId(),
                        evento.correlationId()
                );
            }
            case TiposEvento.COMPENSACION_RECHAZADA -> {
                CompensacionRechazadaData datos = objectMapper.treeToValue(
                        evento.data(),
                        CompensacionRechazadaData.class
                );
                procesarCompensacionRechazadaUseCase.ejecutar(
                        datos.transferenciaId(),
                        datos.motivo()
                );
            }
            default -> {
                // El tópico de cuentas también contiene eventos ajenos a esta saga.
            }
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
