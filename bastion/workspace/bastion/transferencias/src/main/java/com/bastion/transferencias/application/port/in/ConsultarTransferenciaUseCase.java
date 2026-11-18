package com.bastion.transferencias.application.port.in;

import java.util.UUID;

import com.bastion.transferencias.domain.model.Transferencia;

public interface ConsultarTransferenciaUseCase {

    Transferencia ejecutar(UUID transferenciaId);
}