package com.example.smartwardrobe.data.model

import android.content.ContentValues
import android.util.Log
import com.example.smartwardrobe.RetrofitClient
import com.example.smartwardrobe.data.Result
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
        return suspendCoroutine { continuation ->
            retrofit.registerUser(user).enqueue(object : Callback<LoggedInUser> {
                override fun onResponse(call: Call<LoggedInUser>, response: Response<LoggedInUser>) {
                    val userRes = response.body()
                    if (userRes != null) {
                        val fakeUser = LoggedInUser(userRes.userId, userRes.displayName)
                        continuation.resume(Result.Success(fakeUser))
                    } else {
                        continuation.resume(Result.Error(NullPointerException()))
                    }
                }

                override fun onFailure(call: Call<LoggedInUser>, t: Throwable) {
                    continuation.resume(Result.Error(IOException("Error logging in", t)))
                }
            })
        }
    }

    fun logout() {
        // TODO: revoke authentication
    }
}
