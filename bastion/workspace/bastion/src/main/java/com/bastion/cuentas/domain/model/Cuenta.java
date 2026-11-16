package com.bastion.cuentas.domain.model;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.Objects;
import java.util.UUID;

public class Cuenta {

    private final UUID id;
    private final UUID titularId;
    private final Currency moneda;

    private BigDecimal saldo;
    private EstadoCuenta estado;

    public Cuenta(UUID id, UUID titularId, Currency moneda) {
        this(id, titularId, moneda, BigDecimal.ZERO, EstadoCuenta.ACTIVA);
    }

    private Cuenta(
            UUID id,
            UUID titularId,
            Currency moneda,
            BigDecimal saldo,
            EstadoCuenta estado
    ) {
        this.id = Objects.requireNonNull(id, "id no puede ser null");
        this.titularId = Objects.requireNonNull(titularId, "titularId no puede ser null");
        this.moneda = Objects.requireNonNull(moneda, "moneda no puede ser null");
        this.saldo = Objects.requireNonNull(saldo, "saldo no puede ser null");
        this.estado = Objects.requireNonNull(estado, "estado no puede ser null");

        if (saldo.signum() < 0) 
            throw new IllegalArgumentException("saldo no puede ser negativo");
    }

    public static Cuenta rehidratar(
            UUID id,
            UUID titularId,
            Currency moneda,
            BigDecimal saldo,
            EstadoCuenta estado
    ) {
        return new Cuenta(id, titularId, moneda, saldo, estado);
    }

    public void debitar(BigDecimal importe) {
        validarImportePositivo(importe);

        if (estado == EstadoCuenta.BLOQUEADA) 
            throw new ReglaCuentaException(ReglaCuentaException.Codigo.CUENTA_BLOQUEADA, "No se puede debitar de una cuenta bloqueada");
        
        if (saldo.compareTo(importe) < 0) 
            throw new ReglaCuentaException(ReglaCuentaException.Codigo.SALDO_INSUFICIENTE, "El saldo disponible es insuficiente");

        saldo = saldo.subtract(importe);
    }

    public void acreditar(BigDecimal importe) {
        validarImportePositivo(importe);
        saldo = saldo.add(importe);
    }

    public boolean bloquear() {
        if (estado == EstadoCuenta.BLOQUEADA) 
            return false;

        estado = EstadoCuenta.BLOQUEADA;
        return true;
    }

    public boolean desbloquear() {
        if (estado == EstadoCuenta.ACTIVA) 
            return false;

        estado = EstadoCuenta.ACTIVA;
        return true;
    }

    public UUID id() {
        return id;
    }

    public UUID titularId() {
        return titularId;
    }

    public Currency moneda() {
        return moneda;
    }

    public BigDecimal saldo() {
        return saldo;
    }

    public EstadoCuenta estado() {
        return estado;
    }

    private static void validarImportePositivo(BigDecimal importe) {
        Objects.requireNonNull(importe, "importe no puede ser null");

        if (importe.signum() <= 0) 
            throw new IllegalArgumentException("importe debe ser mayor que cero");
    }
}