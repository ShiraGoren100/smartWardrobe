package com.example.smartwardrobe.ui.register

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import android.util.Patterns
import androidx.lifecycle.viewModelScope
import com.example.smartwardrobe.data.Result

import com.example.smartwardrobe.R
import com.example.smartwardrobe.data.RegisterRepository
import com.example.smartwardrobe.ui.login.LoggedInUserView
import com.example.smartwardrobe.ui.login.LoginResult
import kotlinx.coroutines.launch

class RegisterViewModel(private val registerRepository: RegisterRepository) : ViewModel() {

    private val _registerForm = MutableLiveData<RegisterFormState>()
    val registerFormState: LiveData<RegisterFormState> = _registerForm

    private val _registerResult = MutableLiveData<LoginResult>()
    val registerResult: LiveData<LoginResult> = _registerResult

     fun register(username: String, mail: String, password: String) {
        // can be launched in a separate asynchronous job


         viewModelScope.launch {
             val result = registerRepository.register(username, mail, password)

             if (result is Result.Success) {
                 _registerResult.value = LoginResult(success = result.data?.let { LoggedInUserView(displayName = it.displayName, id = result.data.userId, interval = it.interval) })
             } else {
                 _registerResult.value = LoginResult(error = R.string.login_failed)
             }
         }
    }

    fun registerDataChanged(username: String, mail: String, password: String) {
        if (!isUserNameValid(username)) {
            _registerForm.value = RegisterFormState(usernameError = R.string.invalid_username)
        } else if (!isMailValid(mail)) {
            _registerForm.value = RegisterFormState(mailError = R.string.invalid_mail)
        } else if (!isPasswordValid(password)) {
            _registerForm.value = RegisterFormState(passwordError = R.string.invalid_password)
        } else {
            _registerForm.value = RegisterFormState(isDataValid = true)
        }
    }

    // A placeholder username validation check
    private fun isMailValid(mail: String): Boolean {
        return if (mail.contains('@')) {
            Patterns.EMAIL_ADDRESS.matcher(mail).matches()
        } else {
            mail.isNotBlank()
        }
    }

    // A placeholder password validation check
    private fun isPasswordValid(password: String): Boolean {
        return password.length > 5
    }

    private fun isUserNameValid(username: String): Boolean {
        return username.length > 5
    }
}