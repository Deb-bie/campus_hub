package io.campushub.auth_service.exceptions;

public class AlreadyExistsException extends Exception{
    public AlreadyExistsException (String message) {
        super((message));
    }
}
