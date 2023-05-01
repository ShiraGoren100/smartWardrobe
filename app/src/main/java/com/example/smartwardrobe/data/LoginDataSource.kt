package com.example.smartwardrobe.data

import android.content.ContentValues
import android.util.Log
import com.example.smartwardrobe.RetrofitClient
import com.example.smartwardrobe.data.model.LoggedInUser
import com.example.smartwardrobe.data.model.User
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.io.IOException
import java.lang.NullPointerException

/**
 * Class that handles authentication w/ login credentials and retrieves user information.
 */
class LoginDataSource {

    fun login(mail: String, password: String): Result<LoggedInUser> {
        val user = User(email = mail, password = password)
        try {
            // TODO: handle loggedInUser authentication
            var retrofit = RetrofitClient.myApi
            val call = retrofit.loginUser(user)
            var pname: String? = null
            var uid: String? = null

            call.enqueue(object : Callback<LoggedInUser> {
                override fun onResponse(call: Call<LoggedInUser>, response: Response<LoggedInUser>) {
                    val userRes = response.body()
                    if (userRes == null) {

                    }
                    Log.i(ContentValues.TAG, "onResponse: " + userRes)
                    pname = userRes.displayName
                    uid = userRes.userId
                }

                override fun onFailure(call: Call<LoggedInUser>?, t: Throwable) {
                    // handle network error here
                    Log.e(ContentValues.TAG, "Error: " + t.message)
                }

            })
            if (uid == null || pname == null) {
                return Result.Error(NullPointerException())
            } else {
                val fakeUser = LoggedInUser(uid!!, pname!!)
                return Result.Success(fakeUser)
            }
        } catch (e: Throwable) {
            return Result.Error(IOException("Error logging in", e))
        }
    }

    fun register(username: String, mail: String, password: String): Result<LoggedInUser> {
        val user = User(username, mail, password)
        try {
            var retrofit = RetrofitClient.myApi
            val call = retrofit.registerUser(user)
            var pname: String? = null
            var uid: String? = null

            call.enqueue(object : Callback<LoggedInUser> {
                override fun onResponse(call: Call<LoggedInUser>, response: Response<LoggedInUser>) {
                    val userRes = response.body()
                    if (userRes == null) {

                    }
                    Log.i(ContentValues.TAG, "onResponse: " + userRes)
                    pname = userRes.displayName
                    uid = userRes.userId
                }

                override fun onFailure(call: Call<LoggedInUser>?, t: Throwable) {
                    // handle network error here
                    Log.e(ContentValues.TAG, "Error: " + t.message)
                }

            })
            if (uid == null || pname == null) {
                return Result.Error(NullPointerException())
            } else {
                val fakeUser = LoggedInUser(uid!!, pname!!)
                return Result.Success(fakeUser)
            }
        } catch (e: Throwable) {
            return Result.Error(IOException("Error logging in", e))
        }
    }

    fun logout() {
        // TODO: revoke authentication
    }
}