package com.example.smartwardrobe

import com.example.smartwardrobe.data.model.LoggedInUser
import com.example.smartwardrobe.data.model.User
import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface APIService {

    //    @POST("/register")
//    fun registerUser(@Body cunnectedUser:User ): Response<ResponseBody>
    @GET("/register")
    fun registerUser(@Body connectedUser: User): Call<LoggedInUser>

    @GET("/api/users")
    fun getUsers(): Call<List<LoggedInUser>>

  @POST("/addItem")
  fun addItem(@Body json: RequestBody): Call<ResponseBody>

}