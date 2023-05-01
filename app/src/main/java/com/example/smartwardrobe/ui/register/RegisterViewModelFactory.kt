package com.example.smartwardrobe.ui.register

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider

import com.example.smartwardrobe.data.model.RegisterDataSource
import com.example.smartwardrobe.data.RegisterRepository

class RegisterViewModelFactory : ViewModelProvider.Factory {

    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(RegisterViewModel::class.java)) {
            return RegisterViewModel(
                registerRepository = RegisterRepository(
                    dataSource = RegisterDataSource()
                )
            ) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}