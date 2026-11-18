package com.bastion.transferencias.infrastructure.adapter.out.persistence;

import java.util.Optional;
import java.util.UUID;

import org.springframework.stereotype.Repository;

import com.bastion.transferencias.domain.model.Transferencia;
import com.bastion.transferencias.application.port.out.TransferenciaRepository;
import com.bastion.transferencias.infrastructure.persistence.entity.TransferenciaJpaEntity;
import com.bastion.transferencias.infrastructure.persistence.repository.TransferenciaSpringDataRepository;

@Repository
public class TransferenciaPersistenceAdapter implements TransferenciaRepository {

    private final TransferenciaSpringDataRepository springDataRepository;

    public TransferenciaPersistenceAdapter(
            TransferenciaSpringDataRepository springDataRepository) {
        this.springDataRepository = springDataRepository;
    }

    @Override
    public Transferencia guardar(Transferencia transferencia) {
        TransferenciaJpaEntity entidad = springDataRepository
                .findById(transferencia.id())
                .orElseGet(() -> TransferenciaJpaEntity.desdeDominio(transferencia));

        entidad.actualizarDesdeDominio(transferencia);

        return springDataRepository.save(entidad).aDominio();
    }

    @Override
    public Optional<Transferencia> buscarPorId(UUID id) {
        return springDataRepository.findById(id)
                .map(TransferenciaJpaEntity::aDominio);
    }
}