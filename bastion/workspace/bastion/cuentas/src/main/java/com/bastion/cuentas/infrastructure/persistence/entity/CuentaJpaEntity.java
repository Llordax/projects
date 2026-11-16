package com.bastion.cuentas.infrastructure.persistence.entity;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.UUID;

import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.model.EstadoCuenta;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Version;

@Entity
@Table(name = "cuentas")
public class CuentaJpaEntity {

    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;

    @Column(name = "titular_id", nullable = false)
    private UUID titularId;

    @Column(name = "moneda", nullable = false, length = 3)
    private String moneda;

    @Column(name = "saldo", nullable = false, precision = 19, scale = 4)
    private BigDecimal saldo;

    @Enumerated(EnumType.STRING)
    @Column(name = "estado", nullable = false, length = 20)
    private EstadoCuenta estado;

    @Version
    @Column(name = "version", nullable = false)
    private Long version;

    protected CuentaJpaEntity() {
        // Constructor requerido por JPA.
    }

    public static CuentaJpaEntity desdeDominio(Cuenta cuenta) {
        CuentaJpaEntity entidad = new CuentaJpaEntity();
        entidad.id = cuenta.id();
        entidad.actualizarDesdeDominio(cuenta);
        return entidad;
    }

    public Cuenta aDominio() {
        return Cuenta.rehidratar(
                id,
                titularId,
                Currency.getInstance(moneda),
                saldo,
                estado
        );
    }

    public void actualizarDesdeDominio(Cuenta cuenta) {
        titularId = cuenta.titularId();
        moneda = cuenta.moneda().getCurrencyCode();
        saldo = cuenta.saldo();
        estado = cuenta.estado();
    }

    public UUID getId() {
        return id;
    }
}