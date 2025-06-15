package io.campushub.auth_service.service;

import io.campushub.auth_service.config.JwtService;
import io.campushub.auth_service.config.WebClientFactory;
import io.campushub.auth_service.dto.requests.ProfileServiceRequestDto;
import io.campushub.auth_service.dto.requests.ProfileServiceUpdateDto;
import io.campushub.auth_service.dto.requests.SignInRequestDto;
import io.campushub.auth_service.dto.requests.SignUpRequestDto;
import io.campushub.auth_service.dto.responses.ResponseHandler;
import io.campushub.auth_service.entity.AuthUser;
import io.campushub.auth_service.enums.AuthStatus;
import io.campushub.auth_service.exceptions.AlreadyExistsException;
import io.campushub.auth_service.exceptions.NotFoundException;
import io.campushub.auth_service.exceptions.SchoolAccountException;
import io.campushub.auth_service.repository.AuthRepository;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.sql.Timestamp;
import java.util.Optional;
import java.util.UUID;


@Service
public class AuthService {
    private final AuthRepository authRepository;
    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;
    private final PasswordEncoder passwordEncoder;
    private  WebClient webClient;
    private final WebClientFactory webClientFactory;

    @Value("${campushub.services.user-profile-service}")
    private String profileServiceUrl;

    public AuthService(
            AuthRepository authRepository,
            AuthenticationManager authenticationManager,
            JwtService jwtService,
            PasswordEncoder passwordEncoder,
            WebClientFactory webClientFactory
    ) {
        this.authRepository = authRepository;
        this.authenticationManager = authenticationManager;
        this.jwtService = jwtService;
        this.passwordEncoder = passwordEncoder;
        this.webClientFactory = webClientFactory;
    }

    @PostConstruct
    public void init(){
        this.webClient = webClientFactory.createClient(profileServiceUrl);
    }

    public ResponseEntity<ResponseHandler<String>> signUp(SignUpRequestDto signUpRequestDto) throws Exception {
        String jwt;
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
                    .authStatus(AuthStatus.ACTIVE)
                    .created_at(new Timestamp(System.currentTimeMillis()))
                    .updated_at(new Timestamp(System.currentTimeMillis()))
                    .last_login(new Timestamp(System.currentTimeMillis()))
                    .build();
            authRepository.save(authUser);

            ProfileServiceRequestDto profileServiceRequestDto = new ProfileServiceRequestDto();
            profileServiceRequestDto.setUser_id(authUser.getAuth_id());
            profileServiceRequestDto.setEmail(signUpRequestDto.getEmail());
            profileServiceRequestDto.setFirst_name(signUpRequestDto.getFirstName());
            profileServiceRequestDto.setLast_name(signUpRequestDto.getLastName());

            addUserDetailsToProfileService(profileServiceRequestDto);

            Authentication auth = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            signUpRequestDto.getEmail(),
                            signUpRequestDto.getPassword()
                    )
            );
            SecurityContextHolder.getContext().setAuthentication(auth);
            UserDetails userDetails = (UserDetails) auth.getPrincipal();
            jwt = jwtService.generateToken(userDetails);

        }
        else{
            throw new SchoolAccountException("Email must be a school account");
        }

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(
                        ResponseHandler.<String>builder()
                                .statusCode(201)
                                .status(HttpStatus.CREATED)
                                .message(jwt)
                        .build()
                );
    }

    public ResponseEntity<ResponseHandler<String>> signIn(SignInRequestDto signInRequestDto) throws Exception {
        String jwt;
        Optional<AuthUser> emailExists = authRepository.findByEmail(signInRequestDto.getEmail());
        if (emailExists.isPresent()) {
            AuthUser authUser = emailExists.get();

            Authentication auth = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            signInRequestDto.getEmail(),
                            signInRequestDto.getPassword()
                    )
            );
            SecurityContextHolder.getContext().setAuthentication(auth);
            UserDetails userDetails = (UserDetails) auth.getPrincipal();
            jwt = jwtService.generateToken(userDetails);

            authUser.setLast_login(new Timestamp(System.currentTimeMillis()));
            authUser.setAuthStatus(AuthStatus.ACTIVE);
            authRepository.save(authUser);


        } else {
            throw new NotFoundException("Email does not exists");
        }

        return ResponseEntity
                .status(HttpStatus.OK)
                .body(
                        ResponseHandler
                                .<String>builder()
                                .status(HttpStatus.OK)
                                .statusCode(HttpStatus.OK.value())
                                .message(
                                        jwt
                                )
                                .build()
                );

    }

    public ResponseEntity<ResponseHandler<String>> signOut(UUID auth_id) throws Exception {
        Optional<AuthUser> authUser = authRepository.findById(auth_id);
        if (authUser.isPresent()) {
            authUser.get().setAuthStatus(AuthStatus.INACTIVE);
        } else {
            throw new NotFoundException("User does not Exist");
        }

        return ResponseEntity.status(HttpStatus.OK)
                .body(ResponseHandler
                        .<String>builder()
                        .status(HttpStatus.OK)
                        .statusCode(HttpStatus.OK.value())
                        .message("successful")
                        .build()
                );

    }

    public ResponseEntity<ResponseHandler<String>> updateUserDetails(UUID auth_id, ProfileServiceUpdateDto profileServiceUpdateDto) throws Exception {
        Optional<AuthUser> authUser = authRepository.findById(auth_id);
        if (authUser.isPresent()) {
            AuthUser user = authUser.get();
            user.setFirstName(profileServiceUpdateDto.getFirst_name());
            user.setLastName(profileServiceUpdateDto.getLast_name());
            user.setEmail(profileServiceUpdateDto.getEmail());

            authRepository.save(user);
        } else {
            throw new NotFoundException("User does not Exist");
        }

        return ResponseEntity.status(HttpStatus.OK)
                .body(ResponseHandler
                        .<String>builder()
                        .status(HttpStatus.OK)
                        .statusCode(HttpStatus.OK.value())
                        .message("successful")
                        .build()
                );
    }


    public ResponseEntity<ResponseHandler<String>> deleteUserDetails(UUID auth_id) throws Exception {
        Optional<AuthUser> authUser = authRepository.findById(auth_id);
        if (authUser.isPresent()) {
            AuthUser user = authUser.get();
            authRepository.delete(user);
        } else {
            throw new NotFoundException("User does not Exist");
        }

        return ResponseEntity.status(HttpStatus.OK)
                .body(ResponseHandler
                        .<String>builder()
                        .status(HttpStatus.OK)
                        .statusCode(HttpStatus.OK.value())
                        .message("deleted successfully")
                        .build()
                );
    }

    public boolean validateEmail(String email) {
        return email.endsWith(".edu");
    }

    public void addUserDetailsToProfileService(ProfileServiceRequestDto profileServiceRequestDto) {
        webClient
                .post()
                .uri("/api/v1/users/profile/")
                .bodyValue(profileServiceRequestDto)
                .retrieve()
                .toBodilessEntity()
                .doOnError(error -> {
                    System.err.println("Error calling profile service: " + error.getMessage());
                })
                .block();
    }
}
