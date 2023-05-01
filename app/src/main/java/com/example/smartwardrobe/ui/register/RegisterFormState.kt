package com.example.smartwardrobe.ui.register

data class RegisterFormState(
    val usernameError: Int? = null,
    val mailError: Int? = null,
    val passwordError: Int? = null,
    val isDataValid: Boolean = false
)