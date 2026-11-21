package com.bastion.cuentas.application.port.in;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.UUID;

import com.bastion.cuentas.domain.model.Cuenta;

public interface AcreditarCuentaUseCase {

    Cuenta ejecutar(UUID cuentaId, UUID transferenciaId, BigDecimal importe, Currency moneda);

    default Cuenta ejecutar(UUID cuentaId, UUID transferenciaId, BigDecimal importe) {
        return ejecutar(cuentaId, transferenciaId, importe, null);
    }
}
