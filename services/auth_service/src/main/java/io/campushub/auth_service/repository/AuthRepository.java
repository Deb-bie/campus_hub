package io.campushub.auth_service.repository;

import io.campushub.auth_service.entity.AuthUser;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface AuthRepository extends CrudRepository<AuthUser, UUID> {
    Optional<AuthUser> findByEmail(String email);
}
