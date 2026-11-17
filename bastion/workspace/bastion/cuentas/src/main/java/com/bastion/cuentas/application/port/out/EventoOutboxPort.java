package com.bastion.cuentas.application.port.out;

import com.bastion.eventos.contrato.Evento;

public interface EventoOutboxPort {

    void registrar(Evento<?> evento);

    void registrarRechazo(Evento<?> evento);
}