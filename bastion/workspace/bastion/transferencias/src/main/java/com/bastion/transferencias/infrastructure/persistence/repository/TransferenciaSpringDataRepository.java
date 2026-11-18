package com.bastion.transferencias.infrastructure.persistence.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.bastion.transferencias.infrastructure.persistence.entity.TransferenciaJpaEntity;

public interface TransferenciaSpringDataRepository
        extends JpaRepository<TransferenciaJpaEntity, UUID> {
}