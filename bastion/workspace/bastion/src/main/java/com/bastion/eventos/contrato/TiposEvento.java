package com.bastion.eventos.contrato;

public final class TiposEvento {

    public static final String CUENTA_CREADA = "cuenta.creada";
    public static final String CUENTA_BLOQUEADA = "cuenta.bloqueada";
    public static final String CUENTA_DESBLOQUEADA = "cuenta.desbloqueada";

    public static final String TRANSFERENCIA_SOLICITADA = "transferencia.solicitada";
    public static final String TRANSFERENCIA_APROBADA = "transferencia.aprobada";
    public static final String TRANSFERENCIA_RECHAZADA = "transferencia.rechazada";
    public static final String TRANSFERENCIA_COMPLETADA = "transferencia.completada";
    public static final String TRANSFERENCIA_COMPENSADA = "transferencia.compensada";

    public static final String DEBITO_SOLICITADO = "debito.solicitado";
    public static final String DEBITO_REALIZADO = "debito.realizado";
    public static final String DEBITO_RECHAZADO = "debito.rechazado";

    public static final String CREDITO_SOLICITADO = "credito.solicitado";
    public static final String CREDITO_REALIZADO = "credito.realizado";
    public static final String CREDITO_RECHAZADO = "credito.rechazado";

    public static final String COMPENSACION_SOLICITADA = "compensacion.solicitada";
    public static final String COMPENSACION_REALIZADA = "compensacion.realizada";
    public static final String COMPENSACION_RECHAZADA = "compensacion.rechazada";

    private TiposEvento() {
        throw new AssertionError("No se debe instanciar esta clase");
    }
}