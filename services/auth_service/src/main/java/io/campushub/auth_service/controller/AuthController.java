package io.campushub.auth_service.controller;

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
    public ResponseEntity<ResponseHandler> signUp(@RequestBody SignUpRequestDto signUpRequestDto) throws Exception {
        return this.authService.signUp(signUpRequestDto);
    }

}
