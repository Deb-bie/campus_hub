package io.campushub.auth_service.exceptions;

import io.campushub.auth_service.dto.responses.ResponseHandler;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
public class ExceptionController {

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ResponseHandler> notFoundExceptionHandler (NotFoundException notFoundException) {
        return ResponseEntity
                .status(HttpStatus.NOT_FOUND)
                .body(ResponseHandler.builder()
                        .status(HttpStatus.NOT_FOUND)
                        .statusCode(HttpStatus.NOT_FOUND.value())
                        .message(notFoundException.getMessage())
                        .build()
                );
    }

    @ExceptionHandler(AlreadyExistsException.class)
    public ResponseEntity<ResponseHandler> alreadyExistsExceptionHandler (AlreadyExistsException alreadyExistsException) {
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(ResponseHandler.builder()
                        .status(HttpStatus.BAD_REQUEST)
                        .statusCode(HttpStatus.BAD_REQUEST.value())
                        .message(alreadyExistsException.getMessage())
                        .build());

    }

    @ExceptionHandler(SchoolAccountException.class)
    public ResponseEntity<ResponseHandler> schoolAccountExceptionHandler (SchoolAccountException schoolAccountException) {
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(ResponseHandler.builder()
                        .status(HttpStatus.BAD_REQUEST)
                        .statusCode(HttpStatus.BAD_REQUEST.value())
                        .message(schoolAccountException.getMessage())
                .build());
    }

    @ExceptionHandler(EmailOrPasswordException.class)
    public ResponseEntity<ResponseHandler> emailOrPasswordExceptionHandler (EmailOrPasswordException emailOrPasswordException) {
        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(ResponseHandler.builder()
                        .status(HttpStatus.BAD_REQUEST)
                        .statusCode(HttpStatus.BAD_REQUEST.value())
                        .message(emailOrPasswordException.getMessage())
                        .build());
    }
}
