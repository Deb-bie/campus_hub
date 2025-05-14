package io.campushub.auth_service.service;

import io.campushub.auth_service.config.JwtService;
import io.campushub.auth_service.dto.requests.SignInRequestDto;
import io.campushub.auth_service.dto.requests.SignUpRequestDto;
import io.campushub.auth_service.dto.responses.ResponseHandler;
import io.campushub.auth_service.entity.AuthUser;
import io.campushub.auth_service.exceptions.AlreadyExistsException;
import io.campushub.auth_service.exceptions.NotFoundException;
import io.campushub.auth_service.exceptions.SchoolAccountException;
import io.campushub.auth_service.repository.AuthRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

// TODO: when I log in or sign up, i have to set the last loggined in
// TODO: chane the type of the body message for the response handler

@Service
public class AuthService {
    private final AuthRepository authRepository;
    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;
    private final PasswordEncoder passwordEncoder;

    public AuthService(
            AuthRepository authRepository,
            AuthenticationManager authenticationManager,
            JwtService jwtService,
            PasswordEncoder passwordEncoder
    ) {
        this.authRepository = authRepository;
        this.authenticationManager = authenticationManager;
        this.jwtService = jwtService;
        this.passwordEncoder = passwordEncoder;
    }

    public ResponseEntity<ResponseHandler> signUp(SignUpRequestDto signUpRequestDto) throws Exception {
        Optional<AuthUser> emailExists = authRepository.findByEmail(signUpRequestDto.getEmail());

        if (emailExists.isPresent()) {
            throw new AlreadyExistsException("This email address is already in use");
        }

        if (validateEmail(signUpRequestDto.getEmail())) {
            String encodedPassword = passwordEncoder.encode(signUpRequestDto.getPassword());
            AuthUser authUser = AuthUser.builder()
                    .firstName(signUpRequestDto.getFirstName())
                    .lastName(signUpRequestDto.getLastName())
                    .email(signUpRequestDto.getEmail())
                    .password(encodedPassword)
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

    public ResponseEntity<ResponseHandler> signIn(SignInRequestDto signInRequestDto) throws Exception {
        String jwt = "";
        Optional<AuthUser> emailExists = authRepository.findByEmail(signInRequestDto.getEmail());
        if (emailExists.isPresent()) {

            Authentication auth = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            signInRequestDto.getEmail(),
                            signInRequestDto.getPassword()
                    )
            );
            SecurityContextHolder.getContext().setAuthentication(auth);
            UserDetails userDetails = (UserDetails) auth.getPrincipal();
            jwt = jwtService.generateToken(userDetails);

        } else {
            throw new NotFoundException("Email does not exists");
        }

        return ResponseEntity
                .status(HttpStatus.OK)
                .body(
                        ResponseHandler
                                .builder()
                                .status(HttpStatus.OK)
                                .statusCode(HttpStatus.OK.value())
                                .message(
                                        jwt
                                )
                                .build()
                );

    }



    public boolean validateEmail(String email) {
        return email.endsWith(".edu");
    }
}
