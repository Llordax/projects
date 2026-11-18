package com.bastion.cuentas.domain.port.out;

import java.util.Optional;
import java.util.UUID;

import com.bastion.cuentas.domain.model.Cuenta;

public interface CuentaRepository {
	Cuenta guardar(Cuenta cuenta);
	Optional<Cuenta> buscarPorId(UUID id);
}
