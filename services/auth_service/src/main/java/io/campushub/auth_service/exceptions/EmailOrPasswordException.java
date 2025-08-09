package io.campushub.auth_service.exceptions;

public class EmailOrPasswordException extends Exception{
    public EmailOrPasswordException(String message) {
        super(message);
    }
}
