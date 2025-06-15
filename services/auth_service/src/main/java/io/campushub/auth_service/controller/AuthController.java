package io.campushub.auth_service.controller;

import io.campushub.auth_service.dto.requests.ProfileServiceUpdateDto;
import io.campushub.auth_service.dto.requests.SignInRequestDto;
import io.campushub.auth_service.dto.requests.SignUpRequestDto;
import io.campushub.auth_service.dto.responses.ResponseHandler;
import io.campushub.auth_service.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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

    @Operation(summary = "update user details")
    @ApiResponse(responseCode = "200", description = "successful")
    @PutMapping("/update/{auth_id}")
    public ResponseEntity<ResponseHandler<String>> updateUserDetails(
            @PathVariable("auth_id") UUID auth_id,
            @RequestBody ProfileServiceUpdateDto profileServiceUpdateDto
    ) throws Exception {
        return this.authService.updateUserDetails(auth_id, profileServiceUpdateDto);
    }

}
