package com.bastion.cuentas.application.port.in;

import java.util.Currency;
import java.util.UUID;

import com.bastion.cuentas.domain.model.Cuenta;

public interface CrearCuentaUseCase {
	Cuenta ejecutar(UUID titularId, Currency moneda);
}
