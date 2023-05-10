package com.example.smartwardrobe

import com.google.android.material.snackbar.Snackbar
import okhttp3.MediaType
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class AddRepository(private val callback: RepositoryCallback) {

    fun addItem(userid:String,json: String) {

        var retrofit = RetrofitClient.myApi
        val requestBody = RequestBody.create("application/json".toMediaTypeOrNull(), json)

        val call = retrofit.addItem(userid,requestBody)
        call.enqueue(object : Callback<ResponseBody> {
            override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                // handle successful response
                callback.onSuccess()
            }

            override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                // handle error
                callback.onError("Error message")
            }
        })
    }
}