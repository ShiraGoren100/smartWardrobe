package com.example.smartwardrobe

import com.example.smartwardrobe.data.ClothingItem
import com.example.smartwardrobe.data.model.LoggedInUser
import com.example.smartwardrobe.data.model.User
import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Response
import retrofit2.http.*

interface APIService {

    //    @POST("/register")
//    fun registerUser(@Body connectedUser:User ): Response<ResponseBody>
    @POST("/login")
    fun loginUser(@Body connectedUser: User): Call<LoggedInUser>

    @POST("/register")
    fun registerUser(@Body connectedUser: User): Call<LoggedInUser>

    @GET("/api/users")
    fun getUsers(): Call<List<LoggedInUser>>

    @GET("/closet")
    fun getCloset(@QueryMap params: Map<String, String>): Call<List<ClothingItem>>

    @GET("/outfit")
    fun getOutfit(@QueryMap params: Map<String, String>): Call<ArrayList<ClothingItem>>

    @POST("/addItem")
    fun addItem(@Query("id") userid: String, @Body json: RequestBody): Call<ResponseBody>


}