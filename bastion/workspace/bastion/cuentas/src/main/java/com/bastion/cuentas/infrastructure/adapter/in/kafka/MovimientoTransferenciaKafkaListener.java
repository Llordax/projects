package com.bastion.cuentas.infrastructure.adapter.in.kafka;

import java.util.Objects;
import java.util.Currency;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.application.port.in.AcreditarCuentaUseCase;
import com.bastion.cuentas.application.port.in.CompensarCuentaUseCase;
import com.bastion.cuentas.application.port.in.DebitarCuentaUseCase;
import com.bastion.cuentas.domain.model.ReglaCuentaException;
import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.cuentas.CompensacionSolicitadaData;
import com.bastion.eventos.contrato.cuentas.CreditoSolicitadoData;
import com.bastion.eventos.contrato.cuentas.DebitoSolicitadoData;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class MovimientoTransferenciaKafkaListener {

    private static final TypeReference<Evento<JsonNode>> TIPO_EVENTO =
            new TypeReference<>() {
            };

    private final ObjectMapper objectMapper;
    private final DebitarCuentaUseCase debitarCuentaUseCase;
    private final AcreditarCuentaUseCase acreditarCuentaUseCase;
    private final CompensarCuentaUseCase compensarCuentaUseCase;

    public MovimientoTransferenciaKafkaListener(
            ObjectMapper objectMapper,
            DebitarCuentaUseCase debitarCuentaUseCase,
            AcreditarCuentaUseCase acreditarCuentaUseCase,
            CompensarCuentaUseCase compensarCuentaUseCase) {
        this.objectMapper = Objects.requireNonNull(
                objectMapper,
                "objectMapper no puede ser null"
        );
        this.debitarCuentaUseCase = Objects.requireNonNull(
                debitarCuentaUseCase,
                "debitarCuentaUseCase no puede ser null"
        );
        this.acreditarCuentaUseCase = Objects.requireNonNull(
                acreditarCuentaUseCase,
                "acreditarCuentaUseCase no puede ser null"
        );
        this.compensarCuentaUseCase = Objects.requireNonNull(
                compensarCuentaUseCase,
                "compensarCuentaUseCase no puede ser null"
        );
    }

    @KafkaListener(
            topics = "bastion.transferencia.v1",
            groupId = "${spring.kafka.consumer.group-id}"
    )
    public void consumir(String mensaje) throws JsonProcessingException {
        Evento<JsonNode> evento = leerEvento(mensaje);

        switch (evento.eventType()) {
            case TiposEvento.DEBITO_SOLICITADO -> procesarDebito(evento.data());
            case TiposEvento.CREDITO_SOLICITADO -> procesarCredito(evento.data());
            case TiposEvento.COMPENSACION_SOLICITADA ->
                    procesarCompensacion(evento.data());
            default -> {
                // El tópico contiene otros eventos de la saga.
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

    private void procesarDebito(JsonNode data) throws JsonProcessingException {
        DebitoSolicitadoData datos =
                objectMapper.treeToValue(data, DebitoSolicitadoData.class);

        try {
            debitarCuentaUseCase.ejecutar(
                    datos.cuentaId(),
                    datos.transferenciaId(),
                    datos.importe(),
                    Currency.getInstance(datos.moneda())
            );
        } catch (ReglaCuentaException | CuentaNoEncontradaException excepcion) {
            // DebitarCuentaService ya registró debito.rechazado en el Outbox.
        }
    }

    private void procesarCredito(JsonNode data) throws JsonProcessingException {
        CreditoSolicitadoData datos =
                objectMapper.treeToValue(data, CreditoSolicitadoData.class);

        try {
            acreditarCuentaUseCase.ejecutar(
                    datos.cuentaId(),
                    datos.transferenciaId(),
                    datos.importe(),
                    Currency.getInstance(datos.moneda())
            );
        } catch (CuentaNoEncontradaException | ReglaCuentaException excepcion) {
            // AcreditarCuentaService ya registró credito.rechazado en el Outbox.
        }
    }

    private void procesarCompensacion(JsonNode data) throws JsonProcessingException {
        CompensacionSolicitadaData datos =
                objectMapper.treeToValue(data, CompensacionSolicitadaData.class);

        try {
            compensarCuentaUseCase.ejecutar(
                    datos.cuentaId(),
                    datos.transferenciaId(),
                    datos.importe(),
                    Currency.getInstance(datos.moneda())
            );
        } catch (CuentaNoEncontradaException | ReglaCuentaException excepcion) {
            // El servicio ya registró compensacion.rechazada en el Outbox.
        }
    }
}
