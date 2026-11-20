package com.bastion.antifraude.application.port.out;

import com.bastion.eventos.contrato.Evento;

public interface EventoOutboxPort {

    void registrar(Evento<?> evento);
}