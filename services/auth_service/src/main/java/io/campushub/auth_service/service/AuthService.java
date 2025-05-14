package io.campushub.auth_service.service;

import io.campushub.auth_service.dto.requests.SignUpRequestDto;
import io.campushub.auth_service.dto.responses.ResponseHandler;
import io.campushub.auth_service.entity.AuthUser;
import io.campushub.auth_service.exceptions.AlreadyExistsException;
import io.campushub.auth_service.exceptions.SchoolAccountException;
import io.campushub.auth_service.repository.AuthRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class AuthService {
    private final AuthRepository authRepository;

    public AuthService(AuthRepository authRepository) {
        this.authRepository = authRepository;
    }

    public ResponseEntity<ResponseHandler> signUp(SignUpRequestDto signUpRequestDto) throws Exception {
        Optional<AuthUser> emailExists = authRepository.findByEmail(signUpRequestDto.getEmail());

        if (emailExists.isPresent()) {
            throw new AlreadyExistsException("This email address is already in use");
        }

        if (validateEmail(signUpRequestDto.getEmail())) {
            AuthUser authUser = AuthUser.builder()
                    .firstName(signUpRequestDto.getFirstName())
                    .lastName(signUpRequestDto.getLastName())
                    .email(signUpRequestDto.getEmail())
                    .password(signUpRequestDto.getPassword())
                    .build();
            authRepository.save(authUser);
        }
        else{
            throw new SchoolAccountException("Email must be a school account");
        }

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(
                        ResponseHandler.builder()
                                .statusCode(201)
                                .status(HttpStatus.CREATED)
                                .message("successful")
                        .build()
                );
    }

    public boolean validateEmail(String email) {
        return email.endsWith(".edu");
    }
}
