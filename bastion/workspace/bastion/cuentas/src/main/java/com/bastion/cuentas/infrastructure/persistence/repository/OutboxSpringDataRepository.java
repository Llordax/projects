package com.bastion.cuentas.infrastructure.persistence.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.bastion.cuentas.infrastructure.persistence.entity.OutboxJpaEntity;

public interface OutboxSpringDataRepository extends JpaRepository<OutboxJpaEntity, UUID> {
}