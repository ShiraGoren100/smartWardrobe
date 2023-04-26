package com.example.smartwardrobe

interface RepositoryCallback {
    fun onSuccess()
    fun onError(message: String)
}
