package com.evernym.verity.sdk.exceptions;

public class WalletException extends Exception {
    public WalletException(String message, Throwable cause) {
        super(message, cause);
    }

    public WalletException(String message) {
        super(message);
    }
}
