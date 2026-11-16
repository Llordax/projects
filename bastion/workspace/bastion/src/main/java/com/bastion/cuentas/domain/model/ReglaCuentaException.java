package com.bastion.cuentas.domain.model;

import java.util.Objects;

public class ReglaCuentaException extends RuntimeException {

    private final Codigo codigo;

    public ReglaCuentaException(Codigo codigo, String mensaje) {
        super(mensaje);
        this.codigo = Objects.requireNonNull(codigo, "codigo no puede ser null");
    }

    public Codigo codigo() {
        return codigo;
    }

    public enum Codigo {
        CUENTA_BLOQUEADA,
        SALDO_INSUFICIENTE
    }
}