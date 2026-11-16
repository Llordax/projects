package com.bastion.cuentas.application.port.in;

import java.util.UUID;

public interface DesbloquearCuentaUseCase {

    boolean ejecutar(UUID cuentaId);
}