package com.bastion.transferencias.domain.model;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.Objects;
import java.util.UUID;

public class Transferencia {

    private final UUID id;
    private final UUID cuentaOrigenId;
    private final UUID cuentaDestinoId;
    private final BigDecimal importe;
    private final Currency moneda;

    private EstadoTransferencia estado;
    private String motivoRechazo;

    public Transferencia(
            UUID id,
            UUID cuentaOrigenId,
            UUID cuentaDestinoId,
            BigDecimal importe,
            Currency moneda
    ) {
        this.id = Objects.requireNonNull(id, "id no puede ser null");
        this.cuentaOrigenId = Objects.requireNonNull(
                cuentaOrigenId,
                "cuentaOrigenId no puede ser null"
        );
        this.cuentaDestinoId = Objects.requireNonNull(
                cuentaDestinoId,
                "cuentaDestinoId no puede ser null"
        );
        this.importe = Objects.requireNonNull(importe, "importe no puede ser null");
        this.moneda = Objects.requireNonNull(moneda, "moneda no puede ser null");

        if (cuentaOrigenId.equals(cuentaDestinoId)) {
            throw new IllegalArgumentException(
                    "La cuenta de origen y la cuenta de destino deben ser distintas"
            );
        }

        if (importe.signum() <= 0) {
            throw new IllegalArgumentException("importe debe ser mayor que cero");
        }

        this.estado = EstadoTransferencia.SOLICITADA;
    }

    public static Transferencia rehidratar(
            UUID id,
            UUID cuentaOrigenId,
            UUID cuentaDestinoId,
            BigDecimal importe,
            Currency moneda,
            EstadoTransferencia estado,
            String motivoRechazo
    ) {
        Transferencia transferencia = new Transferencia(
                id,
                cuentaOrigenId,
                cuentaDestinoId,
                importe,
                moneda
        );
        transferencia.estado = Objects.requireNonNull(
                estado,
                "estado no puede ser null"
        );
        transferencia.motivoRechazo = motivoRechazo;
        return transferencia;
    }

    public void iniciarEvaluacionAntifraude() {
        cambiarEstado(
                EstadoTransferencia.SOLICITADA,
                EstadoTransferencia.PENDIENTE_ANTIFRAUDE
        );
    }

    public void aprobarAntifraude() {
        cambiarEstado(
                EstadoTransferencia.PENDIENTE_ANTIFRAUDE,
                EstadoTransferencia.PENDIENTE_DEBITO
        );
    }

    public void rechazarAntifraude(String motivo) {
        validarMotivo(motivo);
        cambiarEstado(
                EstadoTransferencia.PENDIENTE_ANTIFRAUDE,
                EstadoTransferencia.RECHAZADA
        );
        motivoRechazo = motivo.trim();
    }

    public void registrarDebitoRealizado() {
        cambiarEstado(
                EstadoTransferencia.PENDIENTE_DEBITO,
                EstadoTransferencia.PENDIENTE_CREDITO
        );
    }

    public void registrarDebitoRechazado(String motivo) {
        validarMotivo(motivo);
        cambiarEstado(
                EstadoTransferencia.PENDIENTE_DEBITO,
                EstadoTransferencia.RECHAZADA
        );
        motivoRechazo = motivo.trim();
    }

    public void registrarCreditoRealizado() {
        cambiarEstado(
                EstadoTransferencia.PENDIENTE_CREDITO,
                EstadoTransferencia.COMPLETADA
        );
    }

    public void registrarCreditoRechazado(String motivo) {
        validarMotivo(motivo);
        cambiarEstado(
                EstadoTransferencia.PENDIENTE_CREDITO,
                EstadoTransferencia.PENDIENTE_COMPENSACION
        );
        motivoRechazo = motivo.trim();
    }

    public void registrarCompensacionRealizada() {
        cambiarEstado(
                EstadoTransferencia.PENDIENTE_COMPENSACION,
                EstadoTransferencia.COMPENSADA
        );
    }

    public void registrarCompensacionRechazada(String motivo) {
        validarMotivo(motivo);
        cambiarEstado(
                EstadoTransferencia.PENDIENTE_COMPENSACION,
                EstadoTransferencia.ERROR_COMPENSACION
        );
        motivoRechazo = motivo.trim();
    }

    public UUID id() {
        return id;
    }

    public UUID cuentaOrigenId() {
        return cuentaOrigenId;
    }

    public UUID cuentaDestinoId() {
        return cuentaDestinoId;
    }

    public BigDecimal importe() {
        return importe;
    }

    public Currency moneda() {
        return moneda;
    }

    public EstadoTransferencia estado() {
        return estado;
    }

    public String motivoRechazo() {
        return motivoRechazo;
    }

    private void cambiarEstado(
            EstadoTransferencia estadoEsperado,
            EstadoTransferencia nuevoEstado
    ) {
        if (estado != estadoEsperado) {
            throw new IllegalStateException(
                    "No se puede cambiar el estado de "
                            + estado
                            + " a "
                            + nuevoEstado
            );
        }

        estado = nuevoEstado;
    }

    private static void validarMotivo(String motivo) {
        Objects.requireNonNull(motivo, "motivo no puede ser null");

        if (motivo.isBlank()) {
            throw new IllegalArgumentException("motivo no puede estar vacío");
        }
    }
}