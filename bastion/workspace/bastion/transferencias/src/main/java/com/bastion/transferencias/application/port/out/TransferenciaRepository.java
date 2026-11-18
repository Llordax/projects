package com.bastion.transferencias.application.port.out;

import java.util.Optional;
import java.util.UUID;

import com.bastion.transferencias.domain.model.Transferencia;

public interface TransferenciaRepository {

    Transferencia guardar(Transferencia transferencia);

    Optional<Transferencia> buscarPorId(UUID transferenciaId);
}