package com.example.smartwardrobe.data

import com.example.smartwardrobe.APIService
import com.example.smartwardrobe.RetrofitClient
import com.example.smartwardrobe.data.model.LoggedInUser
import java.io.IOException

/**
 * Class that handles authentication w/ login credentials and retrieves user information.
 */
class LoginDataSource {

      fun login(username: String, password: String): Result<LoggedInUser> {
       /* var retrofit = RetrofitClient.getInstance()
        var apiInterface = retrofit.create(APIService::class.java)*/
        try {
            // TODO: handle loggedInUser authentication
            val fakeUser = LoggedInUser(java.util.UUID.randomUUID().toString(), "Jane Doe")
//            val registrationData = LoggedInUser(username, password)
//            val response = apiInterface.registerUser(registrationData)
            return Result.Success(fakeUser)
//            if (response.isSuccessful){
//                registrationData.userId= response.body().toString()
//                return Result.Success(registrationData)
//            }
//            return Result.Success(registrationData)
        } catch (e: Throwable) {
            return Result.Error(IOException("Error logging in", e))
        }
    }

    fun logout() {
        // TODO: revoke authentication
    }
}