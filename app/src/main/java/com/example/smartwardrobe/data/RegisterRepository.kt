package com.example.smartwardrobe.data

import com.example.smartwardrobe.data.model.LoggedInUser
import com.example.smartwardrobe.data.model.RegisterDataSource


class RegisterRepository(val dataSource: RegisterDataSource) {

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

     suspend fun register(username: String, mail:String, password: String): Result<LoggedInUser> {

        /*bla bla*/
        // handle login
        val result = dataSource.register(username,mail, password)
        if (result is Result.Success) {
            setLoggedInUser(result.data)
//            val sharedPreference = getSharedPreferences("PREFERENCE_NAME", Context.MODE_PRIVATE)
//            var editor = sharedPreference.edit()
//            editor.putString("userid",loggedInUser.userId)
//            editor.commit()

        }

        return result
    }

    private fun setLoggedInUser(loggedInUser: LoggedInUser?) {
        this.user = loggedInUser

        // If user credentials will be cached in local storage, it is recommended it be encrypted
        // @see https://developer.android.com/training/articles/keystore
    }
}
