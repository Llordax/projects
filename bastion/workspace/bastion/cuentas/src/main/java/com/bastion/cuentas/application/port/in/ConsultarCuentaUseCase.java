package com.bastion.cuentas.application.port.in;

import java.util.Optional;
import java.util.UUID;

import com.bastion.cuentas.domain.model.Cuenta;

public interface ConsultarCuentaUseCase {
	Optional<Cuenta> ejecutar(UUID cuentaId);
}
