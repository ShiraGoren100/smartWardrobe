package com.example.smartwardrobe.data.model

import android.content.ContentValues
import android.util.Log
import com.example.smartwardrobe.RetrofitClient
import com.example.smartwardrobe.data.Result
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.io.IOException
import java.lang.NullPointerException
import kotlin.coroutines.resume
import kotlin.coroutines.suspendCoroutine

class RegisterDataSource {
    suspend fun register(username: String, mail: String, password: String): Result<LoggedInUser> {
        val user = User(username, mail, password)
        val retrofit = RetrofitClient.myApi
        return withContext(Dispatchers.IO) {
            try {
                val response = retrofit.registerUser(user).execute()
                if (response.isSuccessful) {
                    val userRes = response.body()
                    if (userRes != null) {
                        Result.Success(LoggedInUser(userRes.userId, userRes.displayName))
                    } else {
                        Result.Error(NullPointerException())
                    }
                } else {
                    Result.Error(IOException("Error registering user: ${response.code()}"))
                }
            } catch (e: IOException) {
                Result.Error(e)
            }
        }
    }

    fun logout() {
        // TODO: revoke authentication
    }
}
