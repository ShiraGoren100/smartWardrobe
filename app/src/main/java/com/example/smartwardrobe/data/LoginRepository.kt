package com.example.smartwardrobe.data

import android.content.ContentValues.TAG
import android.content.Context
import android.util.Log
import android.widget.Toast
import com.example.smartwardrobe.RetrofitClient
import com.example.smartwardrobe.data.model.LoggedInUser
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


/**
 * Class that requests authentication and user information from the remote data source and
 * maintains an in-memory cache of login status and user credentials information.
 */

class LoginRepository(val dataSource: LoginDataSource) {

    // in-memory cache of the loggedInUser object
    var user: LoggedInUser? = null
        private set

    val isLoggedIn: Boolean
        get() = user != null

    init {
        // If user credentials will be cached in local storage, it is recommended it be encrypted
        // @see https://developer.android.com/training/articles/keystore
        user = null
    }

    fun logout() {
        user = null
        dataSource.logout()
    }

    fun login(username: String, password: String): Result<LoggedInUser> {
        var retrofit = RetrofitClient.myApi
        val call = retrofit.getUsers()

        call.enqueue(object : Callback<List<LoggedInUser>> {
            override fun onResponse(call: Call<List<LoggedInUser>>, response: Response<List<LoggedInUser>>) {
                val users = response.body()
                // Do something with the list of users
                Log.i(TAG, "onResponse: " + users)
            }

            override fun onFailure(call: Call<List<LoggedInUser>>?, t: Throwable) {
                // handle network error here
                Log.e(TAG, "Error: " + t.message)
            }


        })
        /*bla bla*/
        // handle login
        val result = dataSource.login(username, password)
        if (result is Result.Success) {
            setLoggedInUser(result.data)
//            val sharedPreference = getSharedPreferences("PREFERENCE_NAME", Context.MODE_PRIVATE)
//            var editor = sharedPreference.edit()
//            editor.putString("userid",loggedInUser.userId)
//            editor.commit()

        }

        return result
    }

    private fun setLoggedInUser(loggedInUser: LoggedInUser) {
        this.user = loggedInUser

        // If user credentials will be cached in local storage, it is recommended it be encrypted
        // @see https://developer.android.com/training/articles/keystore
    }
}