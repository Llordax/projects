CREATE ROLE bastion_cuentas
    WITH LOGIN REPLICATION
    PASSWORD 'bastion_cuentas_local';

CREATE DATABASE bastion_cuentas
    OWNER bastion_cuentas;

CREATE ROLE bastion_transferencias
    WITH LOGIN REPLICATION
    PASSWORD 'bastion_transferencias_local';

CREATE DATABASE bastion_transferencias
    OWNER bastion_transferencias;

CREATE ROLE bastion_antifraude
    WITH LOGIN REPLICATION
    PASSWORD 'bastion_antifraude_local';

CREATE DATABASE bastion_antifraude
    OWNER bastion_antifraude;

CREATE ROLE bastion_auditoria
    WITH LOGIN REPLICATION
    PASSWORD 'bastion_auditoria_local';

CREATE DATABASE bastion_auditoria
    OWNER bastion_auditoria;