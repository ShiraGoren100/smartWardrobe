package com.example.smartwardrobe.data.model

/**
 * Data class that captures user information for logged in users retrieved from LoginRepository
 */
data class LoggedInUser(
    var userId: String,
    val displayName: String
)