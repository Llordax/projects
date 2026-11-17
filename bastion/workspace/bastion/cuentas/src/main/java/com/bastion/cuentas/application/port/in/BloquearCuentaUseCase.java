package com.bastion.cuentas.application.port.in;

import java.util.UUID;

public interface BloquearCuentaUseCase {

    boolean ejecutar(UUID cuentaId, String motivo);
}