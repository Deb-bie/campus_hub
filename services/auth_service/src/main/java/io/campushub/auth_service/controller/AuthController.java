package io.campushub.auth_service.controller;

import io.campushub.auth_service.dto.requests.SignInRequestDto;
import io.campushub.auth_service.dto.requests.SignUpRequestDto;
import io.campushub.auth_service.dto.responses.ResponseHandler;
import io.campushub.auth_service.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.UUID;

@RestController
@RequestMapping("api/auth")
public class AuthController {
    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @Operation(summary = "sign up")
    @ApiResponse(responseCode = "201", description = "successful")
    @PostMapping("/signup")
    public ResponseEntity<ResponseHandler<String>> signUp(@RequestBody SignUpRequestDto signUpRequestDto) throws Exception {
        return this.authService.signUp(signUpRequestDto);
    }

    @Operation(summary = "sign in")
    @ApiResponse(responseCode = "200", description = "successful")
    @PostMapping("/signin")
    public ResponseEntity<ResponseHandler<String>> signIn(@RequestBody SignInRequestDto signInRequestDto) throws Exception {
        return this.authService.signIn(signInRequestDto);
    }

    @Operation(summary = "sign out")
    @ApiResponse(responseCode = "200", description = "successful")
    @PostMapping("/signout")
    public ResponseEntity<ResponseHandler<String>> signOut(@RequestBody UUID auth_id) throws Exception {
        return this.authService.signOut(auth_id);
    }

}
